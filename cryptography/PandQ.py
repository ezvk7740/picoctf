from Crypto.Util.number import inverse
from Crypto.Util.number import long_to_bytes

def read_values(filename):
    out = []
    with open(filename, 'r') as f:
        for line in f.readlines()[1:]:
            out.append(int(line.split(" ")[1]))
        return out

if __name__ == '__main__':
#    c = 8533139361076999596208540806559574687666062896040360148742851107661304651861689
#    n = 769457290801263793712740792519696786147248001937382943813345728685422050738403253
#    e = 65537
    c, n, e = read_values('values')
    p = 1617549722683965197900599011412144490161
    q = 475693130177488446807040098678772442581573
    d = inverse(e, (p-1)*(q-1))
    m = pow(c, d, n)
    print('m: ', m)
    print('d: ', d)
    print(long_to_bytes(m))

