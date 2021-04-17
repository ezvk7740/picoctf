with open('ascii.txt', 'r') as f:
    out = ''
    for  line in f.readlines():
        out += chr(int(line))
    print(out)
