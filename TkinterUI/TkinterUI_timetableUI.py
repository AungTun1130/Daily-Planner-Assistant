from tkinter import *

root = Tk()
# # Add Text
# mylabel = Label(root, text="TimeTable")
# mylabel2 = Label(root,text = "Made by: Aung")
#
# mylabel.grid(row =0,column = 0 )
# mylabel2.grid(row =1,column = 0 )

def input_box(root):
    e = Entry(root, width=50)
    e.pack()
    e.insert(0,"Enter a value")
    return e
e=input_box(root)
def Click():
    label = Label(root,text = "input :"+ e.get())
    label.pack()

button = Button(root,text= "click me",padx = 50,pady=10,command = Click,fg = "blue",bg = "white")
button.pack()

root.mainloop()