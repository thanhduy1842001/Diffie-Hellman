import socket
import numpy as np
bits = 16

def connect():
    HOST = '192.168.1.13' # thiet lap ipv4 tuong ung cua may
    PORT = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    s.connect(server_address)
    return s

def send(s,y):
    s.sendall(bytes(y, "utf8"))
    
def recv(s):
    data = s.recv(1024)
    data = data.decode('utf8')
    data = data.split(' ')
    g = int(data[0])
    p = int(data[1])
    a = int(data[2])
    return g,p,a

def keyExchange():
    s = connect()
    b = np.random.randint(bits)
    g,p,a = recv(s)
    tmp = pow(g,b,mod=p)
    send(s,str(tmp))
    return pow(a,b,mod=p)

key = keyExchange()
print(f'key = {key}')
print("Press enter to exit...")
i = input()

