#using FileIO
using SharedArrays
using Distributed

function dixon_factor(n::BigInt)
#    base::Array{Int,1} = [2, 3, 5, 7, 11, 13, 17, 19, 23]
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
    println(pairs)
    new = Array{BigInt, 1}()
    for i = 1:length(pairs)
        factor = gcd(pairs[i][1] - pairs[i][2], n)
        if (factor != 1)
            push!(new, factor)
        end
    end
    println(new)
    return unique(new)
end

function dixon_factor(n::BigInt, parallel::Bool)
    base::Array{Int,1} = [2, 3, 5, 7]
    start::BigInt = trunc(BigInt, (n)^(1/2))
    pairs = Array{Union{Int,Nothing}, 1}()
    function reducer(i, j::Int)
        push!(pairs, j)
    end
    @distributed for i = start:n
        @distributed reducer for j = 1:length(base)
            lhs = i^2 % n
            rhs = base[j]^2 % n
            if (lhs == rhs)
                push!(pairs, base[j])
            end
        end
        println(pairs)
    end
    filter!(x->x!=nothing, pairs)
    println(pairs)
    new = Array{BigInt, 1}()
    for i = 1:length(pairs)
        factor = gcd(pairs[i][1] - pairs[i][2], n)
        if (factor != 1)
            push!(new, factor)
        end
        println(new)
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
    

function decodeRSA(file::String)
    open(file) do f
        out = read(f, String)
        println(out)
        out = split(out, "\n")
        println(length(split(out[3], " ")[2]))
        c = parse(BigInt, split(out[2], " ")[2])
        n = parse(BigInt, split(out[3], " ")[2])
        e = parse(BigInt, split(out[4], " ")[2])
        println("c: ", c)
        println("n: ", n)
        println("e: ", e)
        # m^e % n = c
        # c^d % n = m
#        println(dixon_factor(n))
#        test::BigInt = 23449
#        test::BigInt = 6557
#        @time println(dixon_factor(test))

        p::BigInt = 475693130177488446807040098678772442581573
        q::BigInt = 1617549722683965197900599011412144490161
        d = calculate_private_key(p,q,e)
        println("d: ", d)
        m = (c^d) % n
        println(m)
    end
end

decodeRSA("values")
