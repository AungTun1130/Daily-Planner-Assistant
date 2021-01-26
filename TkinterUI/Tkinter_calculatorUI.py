from tkinter import *

root =Tk()
root.title("Simple Calculator")

number = Entry(root,width =35)
number.grid(row= 0,column =0,columnspan=3,padx = 10,pady=10)

math_func_type = ['add','subtract','multiply','divide']
def button_click(num):
    #number.delete(0,END)
    current = number.get()
    number.delete(0,END)
    number.insert(0,str(current) + str(num))

def button_clear():
    number.delete(0,END)

def add():
    first_number = float(number.get())
    global f_num
    global math_func
    math_func= math_func_type[0]
    f_num = first_number
    number.delete(0,END)

def subtract():
    first_number = float(number.get())
    global f_num
    global math_func
    math_func= math_func_type[1]
    f_num = first_number
    number.delete(0,END)

def multiply():
    first_number = float(number.get())
    global f_num
    global math_func
    math_func= math_func_type[2]
    f_num = first_number
    number.delete(0,END)

def divide():
    first_number = float(number.get())
    global f_num
    global math_func
    math_func= math_func_type[3]
    f_num = first_number
    number.delete(0,END)


def button_equal():
    second_number = number.get()
    number.delete(0, END)
    if math_func == math_func_type[0]:
        number.insert(0,f_num+float(second_number))
    elif math_func == math_func_type[1]:
        number.insert(0,f_num-float(second_number))
    elif math_func == math_func_type[2]:
        number.insert(0,f_num*float(second_number))
    elif math_func == math_func_type[3]:
        number.insert(0,f_num/float(second_number))
button_size_x=40
button_size_y=20

button_1 = Button(root,text ="1",padx=button_size_x,pady=button_size_y,command = lambda: button_click(1))
button_2 = Button(root,text ="2",padx=button_size_x,pady=button_size_y,command = lambda: button_click(2))
button_3 = Button(root,text ="3",padx=button_size_x,pady=button_size_y,command = lambda: button_click(3))
button_4 = Button(root,text ="4",padx=button_size_x,pady=button_size_y,command = lambda: button_click(4))
button_5 = Button(root,text ="5",padx=button_size_x,pady=button_size_y,command = lambda: button_click(5))
button_6 = Button(root,text ="6",padx=button_size_x,pady=button_size_y,command = lambda: button_click(6))
button_7 = Button(root,text ="7",padx=button_size_x,pady=button_size_y,command = lambda: button_click(7))
button_8 = Button(root,text ="8",padx=button_size_x,pady=button_size_y,command = lambda: button_click(8))
button_9 = Button(root,text ="9",padx=button_size_x,pady=button_size_y,command = lambda: button_click(9))
button_0 = Button(root,text ="0",padx=button_size_x,pady=button_size_y,command = lambda: button_click(0))
button_add = Button(root,text ="+",padx=button_size_x-1,pady=button_size_y,command = add)
button_subtract = Button(root,text ="-",padx=button_size_x,pady=button_size_y,command = subtract)
button_multiply = Button(root,text ="x",padx=button_size_x,pady=button_size_y,command = multiply)
button_divide = Button(root,text ="/",padx=button_size_x,pady=button_size_y,command = divide)
button_equal = Button(root,text ="=",padx=button_size_x+49,pady=button_size_y,command = button_equal)
button_clear = Button(root,text ="Clear",padx=button_size_x+39,pady=button_size_y,command = button_clear)

button_1.grid(row=3,column=0)
button_2.grid(row=3,column=1)
button_3.grid(row=3,column=2)

button_4.grid(row=2,column=0)
button_5.grid(row=2,column=1)
button_6.grid(row=2,column=2)

button_7.grid(row=1,column=0)
button_8.grid(row=1,column=1)
button_9.grid(row=1,column=2)

button_0.grid(row=4,column =0)
button_clear.grid(row=4,column =1,columnspan =2)

button_add.grid(row=5,column =0)
button_equal.grid(row=5,column =1,columnspan =2)

button_subtract.grid(row=6,column =0)
button_multiply.grid(row=6,column =1)
button_divide.grid(row=6,column =2)

root.mainloop()