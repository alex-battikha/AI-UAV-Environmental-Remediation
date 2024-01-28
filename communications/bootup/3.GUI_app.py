from tkinter import *

root = Tk()
root.title(' Hello World ')
root.geometry('700x500')

myLabel = Label(root, text='APP',fg ='red',bg = 'black',font =('Helvtica',32))


myLabel.pack()

myLabe2 = Label(root, text='Hello world',relief ='groove')

myLabe2.pack()


root.mainloop()
