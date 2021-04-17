import socket
import time

def socket_connect_tcp(IP, PORT):
    print("INFO: connecting")
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((IP, PORT))
            if not sock._closed:
                break
        except:
            pass
    print("INFO: connected")
    return sock

def recieve_data(sock):
    recieve = ""
    t0 = time.time()
    print("INFO: receiving")
    while True:
        try:
            data = sock.recv(1024)
            recieve += data.decode()
            if data:
                break
        except:
            pass
    print("INFO: recieved")
    print("OUT: ", recieve)
    return recieve

def send_data(sock, data):
    print("INFO: sending")
    sock.sendall(data.encode('ascii'))
    print("INFO: sent")

def binary2ascii(raw):
    filtered = raw.split(" ")
    out = ""
    for word in filtered:
        try:
            out += chr(int(word, 2))
        except:
            pass
    print("OUT: ", out)
    return out

def dec2ascii(raw):
    filtered = raw.split(" ")
    out = ""
    for word in filtered:
        try:
            out += chr(int(word, 8))
        except:
            pass
    print("OUT: ", out)
    return out

def decode_hex(raw):
    filtered = raw.split(" ")
    out = ""
    for word in filtered:
        try:
            out += bytes.fromhex(word).decode('ascii')
        except:
            pass
    print("OUT: ", out)
    return out

if __name__ == "__main__":
    IP = "jupiter.challenges.picoctf.org"
    PORT = 15130
    s = socket_connect_tcp(IP, PORT)
    raw = recieve_data(s)
    out = binary2ascii(raw)
    send_data(s,out)
    send_data(s,"\n")

    raw = recieve_data(s)
    out = dec2ascii(raw)
    send_data(s,out)
    send_data(s,"\n")

    raw = recieve_data(s)
    out = decode_hex(raw)
    send_data(s,out)
    send_data(s,"\n")

    raw = recieve_data(s)

    s.close()
