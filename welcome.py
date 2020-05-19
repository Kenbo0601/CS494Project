from tkinter import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time

msg = ''
room = []
msg_list = None
client_socket = socket(AF_INET, SOCK_STREAM)
BUFSIZ = 1024

#Connect to the server
def connect_server():
    name = userName.get()
    client_socket.send(bytes(name, "utf8"))
    main_menu()
    return

def receive():
    """Handles receiving of messages."""
    while True:
        #try:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        print(msg)
        if msg[:6] == '{room}':
            tmp = msg[6:-1] #cutting {room} + the last ','
            rm = tmp.split(',') #split rooms by , and by using split, it stores strings into a list by default
            for x in rm:
                if not x in room: #without this, it duplicates rooms
                    if len(x) > 0:
                        room.append(x)
        elif msg[:6] == '{exit}':
            client_socket.close()
            window.quit()
            break
        else:
            msg_list.insert(END,msg)
        #except OSError:  # Possibly client has left the chat.
            #break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    return

def make_room():
    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    lablel = Label(newWindow, text="MAKE A ROOM")
    fm = Frame(newWindow)
    fm.pack(fill=BOTH)
    return

#join rooms function
def join_room():

    '''inner function'''
    def connect_room():
        name = roomName.get() #get rooms name
        client_socket.send(bytes("{join}"+name, "utf8"))
        chat_screen() #call chat_screen 
        newWindow.destroy() #close the current window
        return

    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    fm = Frame(newWindow)

    client_socket.send(bytes("{room}", "utf8")) #request the server to send the client the list of rooms
    time.sleep(2) #wait for 2 seconds to receive the info
    count = 0
    for x in room:
        count += 1
        Label(fm, text=str(count) + ": " + x, fg="blue", font=(None, 20)).pack()
    
    entry = Entry(fm, textvariable=roomName).pack()
    join = Button(fm, text="JOIN", command=connect_room).pack(side=TOP) #connect_room gets called when client clicked the button
    fm.pack()

    return

def chat_screen():
    #now the chat screen is visible 
    msg_list.delete(0,END)  #clear all the messages 
    top.deiconify() 
    return

#leave the current room
def leave_room():
   client_socket.send(bytes("{quit}","utf8"))
   msg_list.delete(0,END)  #clear all the messages 
   top.withdraw()
   return

def quit_chatApp():
    client_socket.send(bytes("{exit}","utf8"))
    return

def main_menu():
    newWindow = Toplevel(window)
    newWindow.geometry("300x200")
    fm = Frame(newWindow)
    label = Label(fm,text="***** MENU *****").pack(side=TOP)
    label2 = Label(fm,text="Hi," + str(userName.get()) + ". What would you like to do?").pack()
    makeRoom = Button(fm,text='MAKE A ROOM', command=make_room).pack(side=TOP, expand=YES)
    makeRoom = Button(fm,text='JOIN A ROOM', command=join_room).pack(side=TOP,expand=YES)
    makeRoom = Button(fm,text='EXIT', command=quit_chatApp).pack(side=TOP,expand=YES)
    fm.pack(fill=BOTH)
    return


''' --------------------Main loop starts here ----------------------'''
window = Tk()
window.title("CS494_PROJECT")
window.geometry("400x300")
fm = Frame(window)

userName = StringVar() #User variable
roomName = StringVar() #specific room name
HOST = StringVar() #IP ADDRESS
PORT = IntVar() #PORT
PORT.set("")

'''--------------- fuction to connect to the server -------------------'''
def begin(HOST,PORT):

    port = PORT.get()
    host = HOST.get()
    ADDR = (host, port)

    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()
    nameEntry()
    return

'''--------- this screen appears after connecting to the server---------'''
def nameEntry():
    welcome = Label(fm, text="Connection successful! Enter your name", fg="red").pack()
    label1 = Label(fm,text="NAME").pack(side=TOP)
    entry1 = Entry(fm, textvariable=userName).pack()
    main = Button(fm, text="LogIn", command=connect_server).pack(side=TOP)
    return

'''---------------host,port screen----------------------'''
label2 = Label(fm,text="HOST").pack(side=TOP)
entry2 = Entry(fm, textvariable=HOST).pack()
label3 = Label(fm,text="PORT").pack(side=TOP)
entry3 = Entry(fm, textvariable=PORT).pack()
connect = Button(fm, text="CONNECT", highlightthickness=0, command=lambda : begin(HOST,PORT)).pack()
fm.pack()

'''--------------- Main chat screen ---------------------'''
top = Toplevel(window)
top.title("Chatter")
my_msg = StringVar() 
messages_frame = Frame(top)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(top, text="Send", command=send)
quit_button = Button(top, text="Leave", command=leave_room)
send_button.pack()
quit_button.pack()
#top.protocol("WM_DELETE_WINDOW", on_closing)
top.withdraw() #hide the chat screen

window.mainloop()




