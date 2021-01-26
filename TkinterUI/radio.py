from tkinter import *
from PIL import  ImageTk,Image
import os

cur_dir = os.getcwd()
separator = '\\'
main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
icon_dir = main_dir + separator + 'planner-icon.jpg'

root = Tk()
root.title(" Radio ")

r= IntVar()
# pre-set
r.set(2)
pizza = IntVar()
pizza.set(0)

def clicked(value):
    label = Label(root,text = value)
    label.grid(row =12,column = 0)

MODES = [
    ("Pepperoni", 0),
    ("Cheese", 1),
    ("Mushroom", 2),
    ("Onion", 3),
         ]
for i in range(10):
    Radiobutton(root,text = "Option "+str(i),variable = r,value =i,command = lambda : clicked(r.get())).grid(row=i,column=0)
for mode,val in MODES:
    Radiobutton(root,text = mode,variable = pizza,value =val,command = lambda : clicked(r.get())).grid(row=val,column=1,sticky = W)


label = Label(root,text = r.get())
label.grid(row =10,column = 0)

b1= Button(root,text = "click me",command = lambda : clicked(r.get()) )
b1.grid(row =11,column = 0)

root.mainloop()