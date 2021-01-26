from tkinter import *
from PIL import ImageTk,Image
import os

cur_dir = os.getcwd()
separator = '\\'
main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
icon_dir = main_dir + separator + 'planner-icon.jpg'
saveicon_dir = main_dir + separator + 'save_Icon.png'

root= Tk()
root.title("Creating new window")
def close():
    top.destroy()
    main()
def open():
    # create a global variable for thing that you want to put on the screen for second window
    # is very important. If not, it would not work
    global top
    global my_img
    #use TopLevel() to create new window
    top = Toplevel()
    top.title("second window")
    my_img = ImageTk.PhotoImage(Image.open(saveicon_dir))
    my_label = Label(top,image = my_img).pack()
    btn2 = Button(top,text= 'close',command = close).pack()
def main():
    global my_img
    my_img = ImageTk.PhotoImage(Image.open(icon_dir))
    my_label = Label(root, image=my_img).grid(row=0,column = 0)
    btn = Button(root, text='open new window', command=open).grid(row=1,column = 0)

main()

mainloop()