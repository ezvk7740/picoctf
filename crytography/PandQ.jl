using Test

function dixon_factor(n::Union{Int8, Int16, Int32, Int64, BigInt}, debug::Bool = false)
    base::Array{Int,1} = [2, 3, 5, 7]
    start::BigInt = trunc(BigInt, (n)^(1/2))
    pairs = Array{Array{BigInt,1}, 1}()
    for i = start:n
        for j = 1:length(base)
            lhs = i^2 % n
            rhs = base[j]^2 % n
            if (lhs == rhs)
                push!(pairs, [i, base[j]])
            end
        end
    end
    new = Array{BigInt, 1}()
    for i = 1:length(pairs)
        factor = gcd(pairs[i][1] - pairs[i][2], n)
        if (factor != 1)
            push!(new, factor)
        end
    end
    if debug
        println("pairs", pairs)
        println("new", new)
    end
    return unique(new)
end

function calculate_private_key(p::BigInt, q::BigInt, e::BigInt)
    phi = (p-1)*(q-1)
    function mod_inverse(i, m)
        m0 = m
        y = 0
        x = 1
        if (m == 1)
            return 0
        end
        while (i > 1)
            q = i ÷ m
            t = m
            m = i % m
            i = t
            t = y
            y = x - q * y
            x = t
        end
        if (x<0)
            x = x + m0
        end
    end
    d = mod_inverse(e,phi)
    return d
end

function parse_file(file::String)
    open(file) do f
        out = read(f, String)
        println(out)
        out = split(out, "\n")
        c::BigInt = parse(BigInt, split(out[2], " ")[2])
        n::BigInt = parse(BigInt, split(out[3], " ")[2])
        e::BigInt = parse(BigInt, split(out[4], " ")[2])
        return c,n,e
    end
end

#### julia forum
function to_bytes(n::Integer; bigendian=true, len=sizeof(n))
    bytes = Array{UInt8}(undef, len)
    for byte in (bigendian ? (1:len) : reverse(1:len))
        bytes[byte] = n & 0xff
        n >>= 8
    end
    return bytes
end

##### from BitsConvert.jl
function bigint2bytes(n::BigInt)
    nbytes_z = n.size * sizeof(Sys.WORD_SIZE)
    uint8_ptr = convert(Ptr{UInt8}, n.d)
    nbytes = 1
    if ENDIAN_BOM == 0x04030201
        for i in nbytes_z:-1:1
            if unsafe_load(uint8_ptr, i) != 0x00
                nbytes = i
                break
            end
        end
        result = Array{UInt8}(undef, nbytes)
        for i in 1:nbytes
            @inbounds result[nbytes + 1 - i] = unsafe_load(uint8_ptr, i)
        end
    else
        for i in 1:nbytes_z
            if unsafe_load(uint8_ptr, i) != 0x00
                nbytes = i
                break
            end
        end
        result = Array{UInt8}(undef, nbytes)
        for i in 1:nbytes
            @inbounds result[i] = unsafe_load(uint8_ptr,i)
        end
    end
    return result
end

###### my implementation
function int2bytes(n::Integer)
    # reverse endian
    # pkcs#1 => 256
    return binary = reverse!(digits(UInt8, n, base=256))
end

function decodeRSA(file::String, debug::Bool = false)
    """
    m^e % n = c
    c^d % n = m
    """
    c, n, e = parse_file(file)
    if debug
        @test dixon_factor(6557) == BigInt[79, 83]
        @test dixon_factor(23449) == BigInt[131, 179]
        p::BigInt = 475693130177488446807040098678772442581573
        q::BigInt = 1617549722683965197900599011412144490161
        d::BigInt = 582402748221564772374696843202153883711652351188297188998024166320268538694734273
        @test calculate_private_key(p, q, e) == d
        m::BigInt = powermod(c,d,n)
        println("d: ", d)
        println("m: ", m)

        binary = int2bytes(m)
        binary2 = to_bytes(m, len=256, bigendian=false)
        binary3 = bigint2bytes(m)

        println(String(binary))
        println(String(binary2))
        println(String(binary3))
    else
        out = dixon_factor(n)
        d = calculate_private_key(out[0], out[1], e)
        m = powermod(c,d,n)
        println(out)
        println("d: ", d)
        println("m: ", m)
        binary = int2bytes(m)
        println(String(binary))
    end
end

@time decodeRSA("values", true)
