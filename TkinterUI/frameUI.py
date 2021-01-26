from tkinter import *
from PIL import  ImageTk,Image
import os

cur_dir = os.getcwd()
separator = '\\'
main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
icon_dir = main_dir + separator + 'planner-icon.jpg'

root = Tk()
root.title("Frame UI")

frame = LabelFrame(root,text = " The Frame ", padx= 20,pady=15)
frame1 = LabelFrame(root,text = " The Frame ", padx= 20,pady=15)
frame.grid(row = 0 ,column =0,padx=10,pady=10)
frame1.grid(row = 1 ,column =0,padx=10,pady=10)

b=Button(frame,text = " Hi ")
b1=Button(frame,text = " Hi ")
b.grid(row =0 ,column = 0)
b1.grid(row =1 ,column = 1)

b=Button(frame1,text = " Hi ")
b1=Button(frame1,text = " Hi ")
b.grid(row =0 ,column = 0)
b1.grid(row =1 ,column = 1)


root.mainloop()