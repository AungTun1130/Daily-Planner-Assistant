from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title("Check box")
root.geometry("400x400")

#Drop Down box
item = ["Monday","Tuesday","Wednesday"]
def show():
    mylabel = Label(root,text = clicked.get()).pack()

clicked = StringVar()
clicked.set(item[0])


drop = OptionMenu(root,clicked,*item)
drop.pack()

Button(root,text= 'show selection',command = show).pack()
root.mainloop()