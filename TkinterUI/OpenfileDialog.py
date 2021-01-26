from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import os

cur_dir = os.getcwd()
separator = '\\'
main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
icon_dir = main_dir + separator + 'planner-icon.jpg'
saveicon_dir = main_dir + separator + 'save_Icon.png'
root = Tk()
root.title('Open file dialog')


filetype = (
    ("Png files","*.png"),
    ("Jpg files","*.jpg"),
    ("All files files","*.*")
)
def open():
    global  my_img
    root.filename = filedialog.askopenfilename(initialdir = main_dir,title = 'Select A file',filetypes = filetype)
    my_label = Label(root,text = root.filename).pack()
    my_img = ImageTk.PhotoImage(Image.open(root.filename))
    lbl = Label(image = my_img).pack()

Button(root,text = 'import img',command = open).pack()
mainloop()
