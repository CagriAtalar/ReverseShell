from tkinter import *
import socket
from threading import Thread
import sys
from time import sleep
import configparser
import signal

global sock_list
sock_list = []


class Client():
    def __init__(self,sock,ip):
        self.sock = sock
        self.ip = ip


def getIP(parser):
    parser.read("server.inf")
    return parser['IP']['ip']

def socket_create():
    
    global s
    global PORT
    global HOST
    PORT = 5545
    parser = configparser.ConfigParser()
    HOST = getIP(parser)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST,PORT))
    s.listen(60)
    while True:
        clis , addr = s.accept()
        sock_list.append(Client(clis,addr))
        sr = "Connected : ", addr[0] ,"\n"
        allentry.insert(END,sr)

def listele():
    if sock_list == []:
        allentry.insert(END,"No one has been connected yet :D")
    for i,j in enumerate(sock_list):
        c = "Connected {} : {} \n".format(i,j.ip)
        allentry.insert(END,c)

def sendall():
    global sock_list
    if sock_list == []:
        allentry.insert(END,"No one has been connected yet :D\n")
    else:
        com = sendal_ent.get(1.0,END)
        if com != None:
            if ('reboot' or 'poweroff' or 'init' )in com:
                sock_list = []
            for i in sock_list:
                i.sock.send(com.encode('utf-8'))
                a = i.sock.recv(1024)

def close_all():
    global sock_list
    if sock_list == []:
        allentry.insert(END,"No one has been connected yet :D\n")
    else:     
        for i in sock_list:
            i.sock.close()

def selend(sock,ip,num,com):
    while True:
        if ('reboot' or 'poweroff' or 'init') in com:
            sock.send(data)
            del sock_list[num]
            break 
        try:
            sock.send(com.encode("utf-8"))
            cli_recv = sock.recv(10024).decode('ISO-8859-1')
            f = "{}> {}\n".format(ip[0],cli_recv)
            allentry.insert(END,f)
            break
        except Exception as e:
            print(e)
            allentry.insert(END,"Bağlantı kayboldu..\n")
            del sock_list[num]
            break
   

def ana_menu():
    data = send_ent.get(1.0,END)
    if "quit" in data:
        root.destroy()

    elif  "list" in data:
        listele()

    elif data[:6] == "selend":
        data = data.split('@')     
        target = int(data[1])
        target_sock = sock_list[target].sock
        target_ip = sock_list[target].ip
        selend(target_sock,target_ip,target,data[2])
        
    else:
        allentry.insert(END,"Try something\n")
    

            

##Window conf.
root = Tk()

root.resizable(width=False, height=False)


windowWidth = root.winfo_reqwidth()

windowHeight = root.winfo_reqheight()

positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)

positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)

root.geometry("900x450+{}+{}".format(positionRight, positionDown))

root.title("Class Management Software v0.1")

root.configure(background="black")

t = Thread(target=socket_create,args=())
t.daemon = True
t.start()

##Button
sendall1 = Button(root,text="Sendall",bg="white",fg="red",command=sendall)
sendall1.place(relx=0.65,rely=0.12)


selend1 = Button(root,text="Selend",bg="white",fg="red",command=ana_menu)
selend1.place(relx=0.09,rely=0.66)

##Entry
allentry = Text(root,bg="white",fg="red",width=50, height = 10)
allentry.place(relx=0.09,rely=0.12)

send_ent = Text(root,bg="white",fg="red",width=20,height=0.5)
send_ent.place(relx=0.09,rely=0.73)

sendal_ent= Text(root,bg="white",fg="red",width=20,height=0.5)
sendal_ent.place(relx=0.65,rely=0.22)

root.mainloop()




