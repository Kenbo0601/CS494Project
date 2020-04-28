from tkinter import *

window = Tk()
window.title("Welcome to the ChatAPP")
window.geometry("400x300")
fm = Frame(window)

makeRoom = Button(fm, text='MAKE A ROOM').pack(side=TOP, expand=YES)
makeRoom = Button(fm, text='JOIN A ROOM').pack(side=TOP,expand=YES)
makeRoom = Button(fm, text='LEAVE', command=quit).pack(side=TOP,expand=YES)
fm.pack(fill=BOTH,expand=YES)

window.mainloop()



