from tkinter import *

window = Tk()
window.title("Welcome to the ChatAPP")
window.geometry("300x200")
fm = Frame(window)

label = Label(fm, text="***** MENU *****").pack(side=TOP)
makeRoom = Button(fm, text='MAKE A ROOM').pack(side=TOP, expand=YES)
makeRoom = Button(fm, text='JOIN A ROOM').pack(side=TOP,expand=YES)
makeRoom = Button(fm, text='LEAVE', command=quit).pack(side=TOP,expand=YES)
fm.pack(fill=BOTH)

window.mainloop()



