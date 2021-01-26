from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Slide")

vertical = Scale(root, from_=0, to=200)
vertical.pack()

horizontal = Scale(root, from_=0, to=400, orient=HORIZONTAL)
horizontal.pack()


def click():
    my_label = Label(root, text=str(horizontal.get()) + "," + str(vertical.get())).pack()
    root.geometry(str(horizontal.get()) + "x200")


btn = Button(root, text='value', command=click).pack()
mainloop()
