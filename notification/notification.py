from plyer import notification
import datetime as dt
import time
import numpy as np
from win10toast import ToastNotifier
import os
from PIL import ImageTk, Image
cur_dir = os.getcwd()
separator = '\\'
main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
icon_dir = main_dir + separator + 'Timetable_no_bg.png'
icon_ico = Image.open(icon_dir)
icon_ico.save('icon.ico')

now = dt.datetime.now()
string = now.strftime("%d/%m/%Y")

dt_string = np.array(['23:30','22:59','23:00'])
name = ["k","po","er"]
temp =[]
for i in dt_string:
    k = dt.datetime.strptime(i, "%H:%M")
    temp.append(k.strftime("%H:%M:%S"))
temp = np.array(temp)

active = False
toaster = ToastNotifier()
while True:

    print(dt.datetime.now().strftime("%H:%M:%S"),dt_string, active)
    check = temp == dt.datetime.now().strftime("%H:%M:%S")
    if sum(check):
        if not active:
            print("Show...")
            print(name[list(check).index(True)])
            toaster.show_toast("Demo notification",
                               "Hello world",
                               icon_path="../icon.ico",
                               duration=10)

        active = True
    else:
        active = False
    time.sleep(1)


