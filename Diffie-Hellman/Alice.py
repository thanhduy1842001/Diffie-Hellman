import socket
import numpy as np
import random
die = random.SystemRandom()
bits = 128

def connect():
    HOST = '192.168.1.13' # thiet lap ipv4 cua may tai day
    PORT = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Waiting to connect...')
    client, addr = s.accept()
    return client

def recv(client):
    data = client.recv(1024)
    data = data.decode('utf8')
    return int(data)

def send(client,x):
    client.sendall(bytes(x, "utf8"))

def single_test(n, a):
    exp = n - 1
    while not exp & 1:
        exp >>= 1
        
    if pow(a, exp, mod=n) == 1:
        return True
        
    while exp < n - 1:
        if pow(a, exp, mod=n) == n - 1:
            return True
            
        exp <<= 1
        
    return False
    
def millerRabin(n,k=40):
    for i in range(k):
        a = die.randrange(2, n - 1)
        if not single_test(n, a):
            return False
            
    return True

def genPrime():
    while True:
        a = (die.randrange(1 << bits - 1, 1 << bits) << 1) + 1
        if millerRabin(a):
            return a

def primRoot(p):
    for i in range (2,p):
        if pow(i,p-1,mod=p) == 1:
            return i

def keyExchange():
    client = connect()
    a = np.random.randint(bits)
    p = genPrime()
    g = primRoot(p)
    tmp = pow(g,a,mod=p)
    m = str(g) + ' ' + str(p) + ' ' + str(tmp)
    send(client,m)
    b = recv(client)
    return pow(b,a,mod=p)

key = keyExchange()
print(f'key = {key}')
print('Press enter to exit...')
i = input()