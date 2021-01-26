from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox

root = Tk()
root.title('message box')

#all the function for message box
#showinfo,showwarning,showerror,askquestion,askokcancel,askyesno
def popup():
    ###################(name of the tab, message in the box)
    response = messagebox.askyesno('This is my Popup','Hello world!')
    Label(root,text = response).pack()
Button(root,text = "popup",command = popup).pack()

root.mainloop()