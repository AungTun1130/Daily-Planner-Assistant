from tkinter import *
from PIL import ImageTk,Image
import numpy as np
root = Tk()
root.title("Check box")
root.geometry("400x400")

var = StringVar()
val = np.array([IntVar()]*10)

def check():
    myLabel = Label(root, text=var.get()).pack()
    for i in f:
        print(i.get())
def print_val(val):
    print(val)
f=[]
for i in range(10):
    f.append(StringVar())
    c = Checkbutton(root, text="check the box " + str(i+1), variable=f[i],onvalue = str(i+1))
    c.deselect()
    c.pack()
c= Checkbutton(root,text = "check the box",variable = var,onvalue = "On",offvalue = "Off")
c.select()
c.pack()

myLabel = Label(root,text = var.get()).pack()
Button(root,text = " check val ", command = check).pack()


root.mainloop()