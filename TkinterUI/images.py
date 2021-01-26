from tkinter import *
from PIL import ImageTk, Image
import os

cur_dir = os.getcwd()
separator = '\\'
main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
icon_dir = main_dir + separator + 'planner-icon.jpg'

root = Tk()
root.title('Images icon')
root.iconphoto(False, PhotoImage(file=icon_dir))

status_bar = Label(root, text='planner-icon.jpg', bd=1, relief=SUNKEN, anchor=E)

my_img = ImageTk.PhotoImage(Image.open(main_dir + separator + 'save_Icon.png'))
mylabel = Label(image=my_img)
mylabel.grid(row=0, column=0)

# erase the img
# mylabel.grid_forget()

button_quit = Button(root, text="exit", command=root.quit)
button_quit.grid(row=1, column=0, pady=5)
status_bar.grid(row=2, column=0, sticky=W + E)

root.mainloop()
