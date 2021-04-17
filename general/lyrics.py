"""
output from web interpreter
"""
#rock = "114 114 114 111 99 107 110 114 110 48 49 49 51 114"
rock = "66 79 78 74 79 86 73"
out = ''

for i in rock.split():
    out += chr(int(i))

print(out)
