from tkinter import *


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
    label2 = Label(fm,text="Hi," + str(userName.get())).pack()
    makeRoom = Button(fm,text='MAKE A ROOM', command=make_room).pack(side=TOP, expand=YES)
    makeRoom = Button(fm,text='JOIN A ROOM', command=join_room).pack(side=TOP,expand=YES)
    makeRoom = Button(fm,text='LEAVE', command=quit).pack(side=TOP,expand=YES)
    fm.pack(fill=BOTH)


window = Tk()
window.title("Welcome to the ChatAPP")
window.geometry("300x200")
fm = Frame(window)
userName = StringVar() #User variable
label = Label(fm,text="Hello! Enter your name!").pack(side=TOP)
entry = Entry(fm, textvariable=userName).pack()
main = Button(fm, text="go to main", command=main_menu).pack(side=TOP)
fm.pack()


window.mainloop();




