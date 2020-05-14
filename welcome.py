from tkinter import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time

msg = ''
room = []
#Connect to the server
def connect_server():
    name = userName.get()
    client_socket.send(bytes(name, "utf8"))
    main_menu()
    return

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            if msg[:6] == '{room}':
                tmp = msg[6:-1] #cutting {room} + the last ','
                rm = tmp.split(',') #split rooms by , and by using split, it stores strings into a list by default
                for x in rm:
                    if not x in room: #without this, it duplicates rooms
                        room.append(x)
        except OSError:  # Possibly client has left the chat.
            break


def make_room():
    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    lablel2 = Label(newWindow, text="MAKE A ROOM")
    fm = Frame(newWindow)

    back_main = Button(fm, text="Main menu", command=main_menu).pack(side=TOP)
    fm.pack(fill=BOTH)

#join rooms function
def join_room():
    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    fm = Frame(newWindow)

    client_socket.send(bytes("{room}", "utf8")) #request the server to send the client the list of rooms
    time.sleep(2) #wait for 2 seconds to receive the info
    count = 0
    for x in room:
        count += 1
        Label(fm, text=str(count) + ": " + x).pack()
        print(x) #for debugging
    
    entry = Entry(fm, textvariable=roomName).pack()
    join = Button(fm, text="JOIN", command=connect_room).pack(side=TOP)
    fm.pack()


def connect_room():
    name = roomName.get() #get rooms name
    return


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
window.title("CS494_PROJECT")
window.geometry("300x200")
fm = Frame(window)

userName = StringVar() #User variable
roomName = StringVar() #specific room name
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

receive_thread = Thread(target=receive)
receive_thread.start()


window.mainloop();




