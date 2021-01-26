from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import datetime as dt
import data_management as timetable_data
import TimeTemplateClass as timetable_template
import numpy as np
from win10toast import ToastNotifier
import time

cur_dir = os.getcwd()
separator = '\\'
main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
icon_dir = main_dir + separator + 'Timetable_no_bg.png'
saveicon_dir = main_dir + separator + 'save_Icon.png'
tasks_dir = main_dir + separator + "tasks"

root = Tk()
root.title("TIMETABLE MANAGEMENT")
root.iconphoto(False, PhotoImage(file=icon_dir))
screen_size_x = 20
screen_size_y = 20

seperator_arrow = " > "
seperator_dot = "."


# root.geometry(str(screen_size_x)+"x"+str(screen_size_y))

def import_all_tasks():
    global tasks_database
    tasks_database = timetable_data.TimetableDataManagement().Task('task')
    return tasks_database.query_task()


def import_templates():
    global templates_database
    templates_database = timetable_data.TimetableDataManagement.Template('Default')
    return templates_database.query_template()


def Tasks(current_frame=None):
    if current_frame is not None:
        current_frame.destroy()

    def init():
        pad = 20
        Frame_init = LabelFrame(root, padx=pad, pady=pad)
        Frame_init.pack()
        Categories(Frame_init, import_categories())
        Frame1 = LabelFrame(Frame_init, text="Available Tasks", padx=pad, pady=pad)
        Frame2 = LabelFrame(Frame_init, text="Task", padx=pad, pady=pad)
        Frame1.grid(row=1, column=0, sticky=N + S, padx=pad, pady=pad)
        Frame2.grid(row=1, column=1, sticky=N + S, columnspan=2, padx=pad, pady=pad)
        return Frame_init, Frame1, Frame2

    def import_categories():
        category_items = []
        for i in np.array(tasks_database.query_task())[:, 1]:
            if len(category_items) > 0:
                if category_items.count(i) == 0:
                    category_items.append(i)
            else:
                category_items.append(i)
        return category_items

    def tasks_for_each_category(category):
        list_items = []
        for item in tasks_database.query_task():
            if item[1] == category:
                list_items.append(item)
        return list_items

    def Categories(Frame_init, categories=None):
        global items
        global selected_category
        Label(Frame_init, text="Choose Your Category ->").grid(row=0, column=0, sticky=E)
        # DropBox for existing title
        items = categories
        selected_category = StringVar()
        selected_category.set(items[0])
        drop = OptionMenu(Frame_init, selected_category, *items, command=new_task_mode)
        drop.grid(row=0, column=1, padx=10, sticky=W + E)
        Button(Frame_init, text="+/- Category", command=edit_category).grid(row=0, column=2, sticky=W + E)

    def edit_category(change=None):
        # create a global variable for thing that you want to put on the screen for second window
        # is very important. If not, it would not work
        global top
        global my_img
        # use TopLevel() to create new window
        top = Toplevel()
        top.title("Edit Categories")

        var = StringVar()
        row = 0
        temp_items = []
        if change is not None:
            for i in change:
                temp_items.append(i)
        else:
            for i in items:
                temp_items.append(i)

        for i in temp_items:
            Radiobutton(top, text=i, variable=var, value=i, padx=100, anchor=W).grid(row=row, column=0, sticky=W)
            row += 1

        def delete_category():
            response = messagebox.askyesno('Confirmation', 'Are you sure you want to delete ' + str(var.get()) + "?")
            if response == 1:
                temp_items.remove(var.get())
                top.destroy()
                edit_category(temp_items)

        def add_new_category():
            if new_item.get() != "":
                temp_items.append(new_item.get())
                top.destroy()
                edit_category(temp_items)

        def Save_all_category():
            items = temp_items
            top.destroy()
            Categories(Frame_init, items)

        def Cancel():
            top.destroy()
            Categories(Frame_init, items)

        new_item = Entry(top)
        new_item.grid(row=row, column=0)
        row += 1
        Button(top, text="Add new Category", command=add_new_category).grid(row=row, column=0, sticky=W + E)
        row += 1
        Button(top, text='Delete', command=delete_category).grid(row=row, column=0, sticky=W + E)
        row += 1
        Button(top, text='Save', command=Save_all_category).grid(row=row, column=0, sticky=W + E)
        row += 1
        btn2 = Button(top, text='Cancel', command=Cancel).grid(row=row, column=0, sticky=W + E)
        row += 1

    def new_task_mode(category):
        available_tasks_frame(category)
        creating_task_frame()

    # Available tasks Frame
    def available_tasks_frame(category):
        global available_tasks
        available_tasks = tasks_for_each_category(category)
        clear_all_widget(Frame1)

        # if the category is new than show this
        if len(available_tasks) == 0:
            Label(Frame1, text="EMPTY Tasks").grid(row=0, column=0)
            Button(Frame1, text="Create new task", command=lambda: del_task(available_tasks[val.get()])) \
                .grid(row=len(available_tasks), column=0, sticky=W + E)

        else:
            global val
            # variable for the selected task from the selected category
            val = IntVar()
            # Add all new radio button for each task
            for id in available_tasks:
                text_separator = " "
                Radiobutton(Frame1, text=text_separator.join(i for i in id[2:4]), variable=val,
                            value=available_tasks.index(id), command=lambda *args: creating_task_frame(val.get())) \
                    .grid(row=available_tasks.index(id), column=0, sticky=W)
            val.set(None)
            # Creating Create new task button
            Button(Frame1, text="Create new task", command=creating_task_frame) \
                .grid(row=len(available_tasks), column=0, sticky=W + E)
            # Creating Delete selected task button
            Button(Frame1, text="Delete selected task", command=lambda: del_task(available_tasks[val.get()]),
                   state=DISABLED) \
                .grid(row=len(available_tasks) + 1, column=0, sticky=W + E)

    def del_task(task_id):
        response = messagebox.askyesno('Confirmation',
                                       'Are you sure you want to delete ' + task_id[2] + "/" + task_id[3] + "?")
        if response == 1:
            oid = task_id[0]
            tasks_database.delete_task(oid)
            available_tasks_frame(selected_category.get())
            creating_task_frame()

    # Creating task frame
    def creating_task_frame(task_data_id=None):
        global title
        global task
        global deadline
        # Label for each input box
        Task_title_label = Label(Frame2, text="Title")
        Task_title_label.grid(row=0, column=0)
        Task_name_label = Label(Frame2, text="Task")
        Task_name_label.grid(row=1, column=0)
        Task_deadline_label = Label(Frame2, text="Deadline")
        Task_deadline_label.grid(row=2, column=0)

        # User input box
        Task_title_input = Entry(Frame2)
        Task_title_input.grid(row=0, column=1, columnspan=2)
        Task_name_input = Entry(Frame2)
        Task_name_input.grid(row=1, column=1, columnspan=2)
        Task_deadline_input = Entry(Frame2)
        Task_deadline_input.grid(row=2, column=1, columnspan=2)

        def save_task():
            title = Task_title_input.get()
            task = Task_name_input.get()
            deadline = Task_deadline_input.get().split(".")
            if task_data_id is None:
                tasks_database.submit_new_task(selected_category.get(),
                                               title,
                                               task,
                                               deadline[0],
                                               deadline[1],
                                               deadline[2]
                                               )
            else:

                oid = available_tasks[val.get()][0]
                tasks_database.update_task(oid,
                                           selected_category.get(),
                                           title,
                                           task,
                                           int(deadline[0]),
                                           int(deadline[1]),
                                           int(deadline[2])
                                           )
            available_tasks_frame(selected_category.get())
            clear_input()

        def clear_input():
            Task_title_input.delete(0, END)
            Task_name_input.delete(0, END)
            Task_deadline_input.delete(0, END)

        def show_edit_input(data_id):
            # Clear all the existing input
            clear_input()
            # Collect the specific data from the database
            data = np.array(available_tasks[data_id])
            # show the data on the UI
            Task_title_input.insert(0, data[2])
            Task_name_input.insert(0, data[3])
            seperator = "."
            Task_deadline_input.insert(0, seperator.join(data[4:7]))

        if task_data_id is not None:
            # if user click a created task to edit
            show_edit_input(task_data_id)

        if task_data_id is None:
            val.set(None)
            # Save task btn
            Save_task_btn = Button(Frame2, text="Save", command=save_task)
            Save_task_btn.grid(row=3, column=1, sticky=W + E)
            # Disable delete button if the user has not click a task

            Button(Frame1, text="Delete selected task", command=lambda: del_task(available_tasks[val.get()]),
                   state=DISABLED) \
                .grid(row=len(available_tasks) + 1, column=0, sticky=W + E)
        else:
            # Save edit button
            Save_task_btn = Button(Frame2, text="Save Edit", command=save_task)
            Save_task_btn.grid(row=3, column=1, sticky=W + E)
            # Allow user to delete task if they clicked it
            Button(Frame1, text="Delete selected task", command=lambda: del_task(available_tasks[val.get()])) \
                .grid(row=len(available_tasks) + 1, column=0, sticky=W + E)
        # Clear task btn
        Clear_task_btn = Button(Frame2, text="Clear", command=clear_input)
        Clear_task_btn.grid(row=3, column=2, sticky=W + E)

    def back_mainmenu():
        Back_MainPage = Button(Frame_init, text="MainPage", command=lambda: MainPage(Frame_init))
        Back_MainPage.grid(row=2, column=0, columnspan=3, sticky=W + E)

    def clear_all_widget(frame):
        # Destory all the existing widget in the Frame1
        for i in frame.winfo_children():
            i.destroy()

    Frame_init, Frame1, Frame2 = init()
    available_tasks_frame(selected_category.get())
    creating_task_frame()
    back_mainmenu()


def Templates(current_frame=None):
    if current_frame is not None:
        current_frame.destroy()

    def init():
        global timetable_category_items

        timetable_category_items = timetable_template.TimeTableTemplateClass().DutyCategory[:-1]
        Frame_init = LabelFrame(root, padx=10, pady=10)
        Frame_init.pack()
        Frame0 = LabelFrame(Frame_init, text="Items")
        Frame1 = LabelFrame(Frame_init, text="TimeTable", padx=40, pady=10)
        Frame2 = LabelFrame(Frame_init, text="Creating Template", padx=10, pady=10)
        Frame0.grid(row=1, column=0, sticky=N + S)
        Frame1.grid(row=1, column=1, sticky=N + S)
        Frame2.grid(row=1, column=2, columnspan=2, sticky=N + S)
        return Frame_init, Frame0, Frame1, Frame2

    def available_template():
        Label(Frame_init, text="Choose Mode First -->").grid(row=0, column=0, sticky=E)
        global items
        global selected_template

        Button(Frame_init, text="+ Add template", command=lambda: add_template_mode()).grid(row=0, column=1,
                                                                                            sticky=W + E)
        Button(Frame_init, text="Edit template", command=lambda: edit_template_mode()).grid(row=0, column=2,
                                                                                            columnspan=2, sticky=W + E)

    def add_template_mode():
        global list_of_item_in_timetable
        global selected_template_database
        global CMD

        # selected_template.set(None)
        list_of_item_in_timetable = []
        CMD = ""
        timetable_frame()
        creating_timetable_frame()
        template_items(active=True)

    def edit_template_mode():
        global edit_panel
        global final_timetable

        def selected_edit_template_file(name):
            file_path = template_dir + separator + name
            final_timetable = []
            print(file_path)
            data = timetable_data.TimetableDataManagement.TemplateV2().query_template(file_path)

            for i in data:
                final_timetable.append([i[0], i[1], i[2]])
            print(final_timetable)
            editing_final_timetable(name[:-3], final_timetable, True)
            edit_panel.destroy()

        def delete_template_file(name):
            file_path = template_dir + separator + name
            os.remove(file_path)
            edit_panel.destroy()
            edit_template_mode()

        edit_panel = Toplevel()

        # DropBox for existing title
        template_dir = timetable_data.TimetableDataManagement.TemplateV2().template_folder_dir
        items = np.array(timetable_data.TimetableDataManagement.TemplateV2().available_templates())
        print(items)
        print(template_dir + separator + items[0])

        if len(items) > 0:
            selected_template = IntVar()
            selected_template.set(None)
            Label(edit_panel, text="Available Templates").grid(row=0, column=0, columnspan=2, padx=50, pady=10,
                                                               sticky=W + E)
            temp_row = 1
            for i in range(len(items)):
                item = items[i]
                Radiobutton(edit_panel, text=item[:-3], variable=selected_template, val=i) \
                    .grid(row=temp_row, column=0, columnspan=2, sticky=W + E)
                temp_row += 1
            Button(edit_panel, text="Delete", command=lambda: delete_template_file(items[selected_template.get()])) \
                .grid(row=temp_row, column=1, sticky=W + E)

            Button(edit_panel, text="Select", command=lambda: selected_edit_template_file(
                items[selected_template.get()]
            )).grid(row=temp_row, column=0, sticky=W + E)

    def template_items(active=False):
        global template_task_item
        template_task_item = StringVar()

        def print_item(value):
            timetable_frame(item=value)
            # print(value, len(Frame1.winfo_children()))

        if active:
            active = ACTIVE
        else:
            active = DISABLED
        Button(Frame0, text=timetable_category_items[0], state=active,
               command=lambda: print_item(timetable_category_items[0])).grid(row=0, column=0, sticky=W + E)
        Button(Frame0, text=timetable_category_items[1], state=active,
               command=lambda: print_item(timetable_category_items[1])).grid(row=1, column=0, sticky=W + E)
        Button(Frame0, text=timetable_category_items[2], state=active,
               command=lambda: print_item(timetable_category_items[2])).grid(row=2, column=0, sticky=W + E)
        Button(Frame0, text=timetable_category_items[3], state=active,
               command=lambda: print_item(timetable_category_items[3])).grid(row=3, column=0, sticky=W + E)
        Button(Frame0, text=timetable_category_items[4], state=active,
               command=lambda: print_item(timetable_category_items[4])).grid(row=4, column=0, sticky=W + E)
        Button(Frame0, text=timetable_category_items[5], state=active,
               command=lambda: print_item(timetable_category_items[5])).grid(row=5, column=0, sticky=W + E)
        Button(Frame0, text=timetable_category_items[6], state=active,
               command=lambda: print_item(timetable_category_items[6])).grid(row=6, column=0, sticky=W + E)
        Button(Frame0, text=timetable_category_items[7], state=active,
               command=lambda: print_item(timetable_category_items[7])).grid(row=7, column=0, sticky=W + E)

    def timetable_frame(edit_template=None, item=None):
        global timetable_selected_item
        timetable_selected_item = IntVar()

        def delete(item):
            list_of_item_in_timetable.remove(list_of_item_in_timetable[item])
            update_timetable_UI()

        def move_up(item):
            if item > 0:
                lists = list_of_item_in_timetable
                lists[item - 1], lists[item] = lists[item], lists[item - 1]
                update_timetable_UI()

        def move_down(item):
            if item < len(list_of_item_in_timetable) - 1:
                lists = list_of_item_in_timetable
                lists[item + 1], lists[item] = lists[item], lists[item + 1]
                update_timetable_UI()

        def update_timetable_UI():
            row = len(list_of_item_in_timetable)
            for i in Frame1.winfo_children():
                i.destroy()
            for i in range(len(list_of_item_in_timetable)):
                Radiobutton(Frame1, text=list_of_item_in_timetable[i], variable=timetable_selected_item, val=i).grid(
                    row=i, column=0, columnspan=3)

            timetable_selected_item.set(None)
            Button(Frame1, text="UP", command=lambda: move_up(timetable_selected_item.get())).grid(row=row + 1,
                                                                                                   column=0,
                                                                                                   sticky=W + E)

            Button(Frame1, text="DOWN", command=lambda: move_down(timetable_selected_item.get())).grid(row=row + 1,
                                                                                                       column=1,
                                                                                                       sticky=W + E)
            Button(Frame1, text="DEL", command=lambda: delete(timetable_selected_item.get())).grid(row=row + 1,
                                                                                                   column=2,
                                                                                                   sticky=W + E)

        # Clear all the existing widget in the Frame1
        for i in Frame1.winfo_children():
            i.destroy()

        # Case of creating New template
        if item is None and edit_template is None:
            for widget in Frame2.winfo_children():
                widget.destroy()
            Label(Frame1,
                  text="Click the items on the right side \n in the order of the tasks you want to do first").grid(
                row=0, column=0)

        # Cases when user want to edit the template
        else:
            update_timetable_UI()

        # Cases when user adding item into timetable
        if edit_template is None and item is not None:
            list_of_item_in_timetable.append(item)
            update_timetable_UI()

    def creating_timetable_frame(edit_template=None):

        for widget in Frame2.winfo_children():
            widget.destroy()
        list = ["Name",
                "Start Time",
                "Work Duration",
                "Lunch Duration",
                "Dinner Duration",
                "Self-Care",
                "Self-Development",
                "Relax",
                "Short Break Duration",
                "Long Break Duration"]

        def Label_and_Entry_input_UI(lists):
            global input_list
            row = 0
            input_list = []
            for item in lists:
                Label(Frame2, text=item).grid(row=row, column=0, sticky=W)
                if item != "Short Break Duration" and item != "Long Break Duration":
                    input_list.append(Entry(Frame2))
                    input_list[row].grid(row=row, column=1)
                    if item != "Name" and item != "Start Time":
                        Label(Frame2, text="Hours").grid(row=row, column=2)
                else:

                    input_list.append(IntVar())
                    if item == "Short Break Duration":
                        shortbreaktime = [5, 10, 15, 20]
                        OptionMenu(Frame2, input_list[row], *shortbreaktime).grid(row=row, column=1, sticky=W + E)
                        Label(Frame2, text="Minutes").grid(row=row, column=2)
                        input_list[row].set(shortbreaktime[0])
                    elif item == "Long Break Duration":
                        longbreaktime = [30, 45, 60]
                        OptionMenu(Frame2, input_list[row], *longbreaktime).grid(row=row, column=1, sticky=W + E)
                        Label(Frame2, text="Minutes").grid(row=row, column=2)
                        input_list[row].set(longbreaktime[0])
                row += 1
            Label(Frame2, text="_" * 50).grid(row=row, column=0, columnspan=3, sticky=W + E)
            row += 1
            Button(Frame2, text="Generate the final timetable", command=generating_timetable).grid(row=row,
                                                                                                   column=0,
                                                                                                   columnspan=3,
                                                                                                   sticky=W + E)
            return input_list

        if edit_template is None:
            input_list = Label_and_Entry_input_UI(list)

        else:
            # Label(Frame2, text="Edit Template: " + edit_template).grid(row=0, column=0)
            input_list = Label_and_Entry_input_UI(list)
            data = selected_template_database
            for i in range(len(input_list)):
                if i == 0:
                    input_list[i].insert(0, data[1])
                elif i == 1:
                    input_list[i].insert(0, data[4])
                elif i in range(2, 8):
                    input_list[i].insert(0, data[i + 6])
                elif i == 8:
                    input_list[i].set(data[5])
                elif i == 9:
                    input_list[i].set(data[6])

    def collect_all_input():
        global CMD
        # Double checking all the input if they exist
        check_out_CMD = False
        check_out_input = True
        # check if the items are selected
        if len(list_of_item_in_timetable) == 0:
            messagebox.showerror("Missing", message="Missing items")
        else:
            check_out_CMD = True
        print("CMD :", list_of_item_in_timetable)
        CMD = list_of_item_in_timetable
        # check if the user fill in the hours
        for i in input_list:
            check_out_input *= i.get() != ""
        print(check_out_input)

        # If all the input are fills. return True
        return check_out_input * check_out_CMD

    def generating_timetable():
        global final_timetable
        if collect_all_input():
            # Default config Amount of total hour for each task
            SleepingHour = 7  # hour
            WorkingHour = float(input_list[2].get())  # hour
            ExerciseHour = float(input_list[5].get())  # hour
            FriendsHour = float(input_list[7].get())  # hour
            SelfDevelopmentHour = float(input_list[6].get())  # hour
            LunchHour = float(input_list[3].get())
            DinnerHour = float(input_list[4].get())
            shortBreak = float(input_list[8].get())
            longBreak = float(input_list[9].get())
            # Time
            PlannedDate = dt.datetime(dt.datetime.today().year, dt.datetime.today().month, dt.datetime.today().day)

            if input_list[1].get().count(":") > 0:
                StartTime = dt.time(int(input_list[1].get().split(":")[0]), int(input_list[1].get().split(":")[1]))
            elif input_list[1].get().count(".") > 0:
                StartTime = dt.time(int(input_list[1].get().split(".")[0]), int(input_list[1].get().split(".")[1]))
            x = timetable_template.TimeTableTemplateClass(StartTime, shortBreak, longBreak, SleepingHour, WorkingHour,
                                                          LunchHour,
                                                          DinnerHour,
                                                          ExerciseHour,
                                                          SelfDevelopmentHour,
                                                          FriendsHour,
                                                          PlannedDate)
            final_timetable = x.create_custom_template(CMD=CMD)

            editing_final_timetable(input_list[0].get(), final_timetable)

    def editing_final_timetable(name, final_timetable_edit, Update=False):
        global selected_item_final_tb
        global Top_temp

        print("Read all timetable..")
        for i in range(len(final_timetable_edit)):
            final_timetable_edit[i][0] = StringVar(Frame1, value=final_timetable_edit[i][0])
            final_timetable_edit[i][1] = StringVar(Frame1, value=final_timetable_edit[i][1])
            final_timetable_edit[i][2] = StringVar(Frame1, value=final_timetable_edit[i][2])
        try:
            Top_temp.destroy()
        except:
            print("Only one editing panel exist")
        Top_temp = Toplevel()
        Top_temp.title("Final Timetable")
        Label(Top_temp, text=name).grid(row=0, column=0, columnspan=2, sticky=W + E)
        FrameTimetable_Temp = LabelFrame(Top_temp, text="TimeTable", padx=40, pady=10)
        FrameTimetable_Temp.grid(row=1, column=1, sticky=N + S)
        FrameTool_Temp = LabelFrame(Top_temp, text="Tools", padx=40, pady=10)
        FrameTool_Temp.grid(row=1, column=0, sticky=N + S)

        def delete(item):
            if item != 0 and item != len(final_timetable_edit) - 1:
                final_timetable_edit[item + 1][0] = final_timetable_edit[item - 1][1]
            final_timetable_edit.remove(final_timetable_edit[item])
            update_final_timetable_UI()

        def move_up(item):
            if item > 0:
                lists = final_timetable_edit
                lists[item - 1][2], lists[item][2] = lists[item][2], lists[item - 1][2]
                update_final_timetable_UI()

        def move_down(item):
            if item < len(final_timetable_edit) - 1:
                lists = final_timetable_edit
                lists[item + 1][2], lists[item][2] = lists[item][2], lists[item + 1][2]
                update_final_timetable_UI()

        def update_final_timetable_UI():
            for i in FrameTimetable_Temp.winfo_children():
                i.destroy()
            Label(FrameTimetable_Temp, text="Item").grid(row=0, column=0)
            Label(FrameTimetable_Temp, text="Start Time").grid(row=0, column=1)
            Label(FrameTimetable_Temp, text="End Time").grid(row=0, column=2)
            row_temp = 1

            for index in range(len(final_timetable_edit)):
                item = final_timetable_edit[index]

                # DropBox for existing title
                drop = OptionMenu(FrameTimetable_Temp, item[2], *timetable_category_items)
                Radio = Radiobutton(FrameTimetable_Temp, text=">", variable=selected_item_final_tb, val=index)
                start_input = Entry(FrameTimetable_Temp, textvariable=item[0])
                end_input = Entry(FrameTimetable_Temp, textvariable=item[1])

                Radio.grid(row=row_temp, column=0)
                drop.grid(row=row_temp, column=1, padx=10, sticky=W + E)
                start_input.grid(row=row_temp, column=2)
                end_input.grid(row=row_temp, column=3)

                row_temp += 1

        Button(FrameTool_Temp, text="").grid(row=1, column=0, sticky=W + E)
        Button(FrameTool_Temp, text="Move Up", command=lambda: move_up(selected_item_final_tb.get())).grid(row=2,
                                                                                                           column=0,
                                                                                                           sticky=W + E)
        Button(FrameTool_Temp, text="Move Down", command=lambda: move_down(selected_item_final_tb.get())).grid(row=3,
                                                                                                               column=0,
                                                                                                               sticky=W + E)
        Button(FrameTool_Temp, text="Delete", command=lambda: delete(selected_item_final_tb.get())).grid(row=4,
                                                                                                         column=0,
                                                                                                         sticky=W + E)

        selected_item_final_tb = IntVar()
        update_final_timetable_UI()

        Button(Top_temp, text="Save The Template", command=lambda: save_template(name, final_timetable_edit, Update)).grid(
            row=2, column=0, columnspan=2)

    def save_template(name, final_template_list, Update=False):
        response = messagebox.askyesno('Confirmation',
                                       'You have finished the final templete ?')
        if response == 1:
            for i in final_template_list:
                print(i[0].get(), i[1].get(), i[2].get())
            timetable_temp = timetable_data.TimetableDataManagement.TemplateV2(name)
            if not Update:
                for i in final_template_list:
                    timetable_temp.submit_data(StartTime=i[0].get(),
                                               EndTime=i[1].get(),
                                               item=i[2].get())
            else:
                for i in final_template_list:
                    timetable_temp.update_template(final_template_list.index(i) + 1,
                                                   StartTime=i[0].get(),
                                                   EndTime=i[1].get(),
                                                   item=i[2].get())
            Top_temp.destroy()

    def back_MainPage():
        Back_MainPage = Button(Frame_init, text="MainPage", command=lambda: MainPage(Frame_init))
        Back_MainPage.grid(row=2, column=0, columnspan=4, sticky=W + E)

    Frame_init, Frame0, Frame1, Frame2 = init()
    template_items()
    available_template()
    timetable_frame()
    creating_timetable_frame()
    back_MainPage()
    return


def Planner(current_frame=None):
    if current_frame is not None:
        current_frame.destroy()
    template_files = timetable_data.TimetableDataManagement.TemplateV2().available_templates()

    def init():
        Frame_init = LabelFrame(root, padx=10, pady=10)
        Frame_init.pack()

        Frame1 = LabelFrame(Frame_init, text="Available Task Categories", padx=10, pady=10)
        Frame2 = LabelFrame(Frame_init, text="Available Tasks", padx=10, pady=10)
        Frame3 = LabelFrame(Frame_init, text="Available Templates", padx=10, pady=10)
        Frame1.grid(row=0, column=0, sticky=N + S)
        Frame2.grid(row=0, column=1, sticky=N + S)
        Frame3.grid(row=0, column=2, sticky=N + S)
        return Frame_init, Frame1, Frame2, Frame3

    def task_category_buttons():
        global final_task_category_id
        global selected_category_tasks
        selected_category_tasks = []
        categories = []
        for i in np.array(tasks_database.query_task())[:, 1]:
            selected_category_tasks.append(IntVar())
            if categories.count(i) == 0:
                categories.append(i)
        last = ''
        index = 0
        final_task_category_id = StringVar()
        for item in categories:

            if last != item:
                radio = Radiobutton(Frame1, text=item, variable=final_task_category_id, value=item,
                                    command=lambda: available_task_selected_category(final_task_category_id.get()))
                radio.grid(row=index, column=0, sticky=W, padx=10)
                last = item
                index += 1
        final_task_category_id.set("None")

    def available_task_selected_category(category=None):

        index = 0
        for widget in Frame2.winfo_children():
            widget.destroy()
        if category is None:
            Label(Frame2, text="Select a category first").grid(row=index, column=0, sticky=W + E)
            index += 1
        else:
            data = tasks_database.query_task()
            for task in data:
                if task[1] == category:
                    deadline = str(task[4]) + seperator_dot + str(task[5]) + seperator_dot + str(task[6])
                    c = Checkbutton(Frame2, text=seperator_arrow.join(task[2:4]) + " " + deadline,
                                    variable=selected_category_tasks[data.index(task)])
                    c.grid(row=index, column=0, sticky=W + E)
                    index += 1

    def print_val():
        text = ''
        lists = tasks_database.query_task()
        for i in range(len(selected_category_tasks)):
            if selected_category_tasks[i].get() != 0:
                text += str(">".join(lists[i][2:4])) + "\n"
        print("SELECTED TASKS")
        print(text)

        print("SELECTED TEMPLATE \n", template_files[final_selected_template.get()])

    def notify_function():
        path = timetable_data.TimetableDataManagement.TemplateV2().template_folder_dir + "\\" + template_files[
            final_selected_template.get()]
        timetable = np.array(timetable_data.TimetableDataManagement.TemplateV2().query_template(path))
        print(timetable)
        start_time_list = convert_string_to_time(timetable[:, 0])
        end_time_list = convert_string_to_time(timetable[:, 1])
        task_category_name_list = timetable[:, 2]
        active_notification = False
        notify = ToastNotifier()
        while True:
            current_time = dt.datetime.now().strftime("%H:%M:%S")

            check = start_time_list == current_time
            if sum(check):
                if not active_notification:
                    index = list(check).index(True)
                    catagory_item = task_category_name_list[index]
                    text = ''
                    tasks = np.array(tasks_database.query_task())
                    for i in range(len(selected_category_tasks)):
                        if selected_category_tasks[i].get() != 0:
                            if tasks[i][1] == catagory_item:
                                text += str(" > ".join(tasks[i][2:4])) + "\n"

                    notify.show_toast("Daily Planner notification: " + catagory_item,
                                      text,
                                      icon_path="../icon.ico",
                                      duration=20,
                                      threaded=True)
                    active_notification = True
            else:
                active_notification = False
            print(current_time)
            time.sleep(1)

    def start():
        # Debugging
        # Check if all the selected tasks and template are correct
        root.withdraw()
        print_val()
        notify_function()

        # Change the active status for all the selected task
        # for i in range(len(selected_category_tasks)):
        #     if selected_category_tasks[i].get() != 0:
        #         task = tasks_database.query_task()[i]
        #         tasks_database.update_task(oid=task[0],
        #                                    category=task[1],
        #                                    title=task[2],
        #                                    task=task[3],
        #                                    deadline_day=task[4],
        #                                    deadline_month=task[5],
        #                                    deadline_year=task[6],
        #                                    active=True)

    def convert_string_to_time(lists):
        temp = []
        for i in lists:
            k = dt.datetime.strptime(i, "%H:%M")
            temp.append(k.strftime("%H:%M:%S"))
        temp = np.array(temp)
        return temp

    def available_template_button():
        global final_selected_template
        final_selected_template = IntVar()
        temp_row = 0
        for index in range(len(template_files)):
            template_name = template_files[index]
            radio = Radiobutton(Frame3, text=template_name, variable=final_selected_template, value=index)
            radio.grid(row=temp_row, column=0, sticky=W + E)
            temp_row += 1

    Frame_init, Frame1, Frame2, Frame3 = init()
    task_category_buttons()
    available_task_selected_category()
    available_template_button()

    Start_btn = Button(Frame_init, text="Start", command=start)
    Start_btn.grid(row=1, column=0, columnspan=3, sticky=W + E)
    Back_MainPage = Button(Frame_init, text="MainPage", command=lambda: MainPage(Frame_init))
    Back_MainPage.grid(row=2, column=0, columnspan=3, sticky=W + E)

    return


def Evaluation(current_frame=None):
    messagebox.showerror("Evaluation", message="Under development")
    # Workflow
    # Collect all the task that are active
    # Create 1 Frame with 2 column grid
    # first column show all the category that are active with Label
    # second column show all the tasks that are active with checkbox
    # Create a save/update button for save all data after user finish evaluating
    # If a selected task is complete, inactive the task and update complete status on the data
    # Else just inactive the task
    return


def MainPage(current_frame=None):
    if current_frame is not None:
        current_frame.destroy()

    Frame_MainPage = LabelFrame(root, text="MAIN PAGE", padx=10, pady=10)
    Frame_MainPage.configure(labelanchor=N, bd=3)
    Frame_MainPage.pack()

    Tasks_btn = Button(Frame_MainPage, text="Tasks", font="Arial 15", padx=screen_size_x, pady=screen_size_y,
                       command=lambda: Tasks(Frame_MainPage))
    Tasks_btn.grid(row=0, column=0, sticky=W + E)

    Templates_btn = Button(Frame_MainPage, text="Templates", font="Arial 15", padx=screen_size_x, pady=screen_size_y,
                           command=lambda: Templates(Frame_MainPage))
    Templates_btn.grid(row=1, column=0, sticky=W + E)

    Planner_btn = Button(Frame_MainPage, text="Planner", font="Arial 15", padx=screen_size_x, pady=screen_size_y,
                         command=lambda: Planner(Frame_MainPage))
    Planner_btn.grid(row=2, column=0, sticky=W + E)

    Evaluation_btn = Button(Frame_MainPage, text="Evaluation", font="Arial 15", padx=screen_size_x, pady=screen_size_y,
                            command=lambda: Evaluation(Frame_MainPage))
    Evaluation_btn.grid(row=3, column=0, sticky=W + E)

    timetable_img = ImageTk.PhotoImage(Image.open(icon_dir))

    label = Label(Frame_MainPage, image=timetable_img)
    label.image = timetable_img
    label.grid(row=0, column=1, rowspan=4)


import_all_tasks()
import_templates()
MainPage()

root.mainloop()
