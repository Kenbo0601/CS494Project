from tkinter import *
from socket import socket, AF_INET, SOCK_STREAM

#Connect to the server 
def connect_server():
    name = userName.get()
    client_socket.send(bytes(name, "utf8"))
    return

def make_room():
    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    lablel2 = Label(newWindow, text="MAKE A ROOM")
    fm = Frame(newWindow)

    back_main = Button(fm, text="Main menu", command=main_menu).pack(side=TOP)
    fm.pack(fill=BOTH)

def join_room():
    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    lablel2 = Label(newWindow, text="JOIN A ROOM")


def main_menu():
    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    fm = Frame(newWindow)
    label = Label(fm,text="***** MENU *****").pack(side=TOP)
    label2 = Label(fm,text="Hi," + str(userName.get()) + ". What would you like to do?").pack()
    makeRoom = Button(fm,text='MAKE A ROOM', command=make_room).pack(side=TOP, expand=YES)
    makeRoom = Button(fm,text='JOIN A ROOM', command=join_room).pack(side=TOP,expand=YES)
    makeRoom = Button(fm,text='LEAVE', command=quit).pack(side=TOP,expand=YES)
    fm.pack(fill=BOTH)


window = Tk()
window.title("Welcome to the ChatAPP")
window.geometry("300x200")
fm = Frame(window)

userName = StringVar() #User variable
#HOST = StringVar() #IP ADDRESS
#PORT = StringVar() #PORT
#label = Label(fm,text="Hello! Enter your name, IP address, and PORT").pack(side=TOP)
label1 = Label(fm,text="NAME").pack(side=TOP)
entry1 = Entry(fm, textvariable=userName).pack()
#label2 = Label(fm,text="HOST").pack(side=TOP)
#entry2 = Entry(fm, textvariable=HOST).pack()
#label3 = Label(fm,text="PORT").pack(side=TOP)
#entry3 = Entry(fm, textvariable=PORT).pack()
main = Button(fm, text="CONNECT", command=connect_server).pack(side=TOP)
fm.pack()


HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 9009
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

#receive_thread = Thread(target=receive)
#receive_thread.start()


window.mainloop();




