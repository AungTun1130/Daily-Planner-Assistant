import pygame
import sys
import os
import pygame_button as button
import math
import numpy as np
import time, datetime
import distutils.util
import TimeTemplateClass
import TimeTableMaker


class Task:
    def __init__(self, name, subTask_name, deadline=None, difficult=None, finish_task=False):
        self.name = name
        self.subTask_name = subTask_name
        self.subTask_deadline = str(deadline)
        self.finish = str(finish_task)
        self.list_subtask = []
        self.difficult = str(difficult)

    def add_subtask(self, task):
        self.list_subtask.append(task)

    def get_subtask(self, index):
        return self.list_subtask[index]

    def get_name(self):
        return self.name

    def get_subtask_name(self):
        return self.subTask_name

    def get_deadline(self):
        return self.subTask_deadline

    def get_finish_task(self):
        return self.finish

    def get_all_parameter(self):
        return self.name + "," + self.subTask_name + "," + self.subTask_deadline + "," + self.difficult + "," + str(
            self.finish)


def check_save_path():
    task_path = os.getcwd() + "\\tasks"
    if not os.path.exists(task_path):
        os.mkdir(task_path)

    template_path = os.getcwd() + "\\templates"
    if not os.path.exists(template_path):
        os.mkdir(template_path)


class TimetableUI:
    def __init__(self):
        # initializing the constructor
        pygame.init()

        # screen resolution
        res = (1000, 650)

        # opens up a window
        self.screen = pygame.display.set_mode(res)

        self.tab_height = 40
        self.text_size = 20

        self.refreshIcon = pygame.image.load('refresh_black_192x192.png')
        self.All_button_scene0 = []
        self.All_tasks = []

        self.temp_template_name = ""
        self.temp_Sleephour = ""
        self.temp_Workhour = ""
        self.temp_Lunchhour = ""
        self.temp_Dinnerhour = ""
        self.temp_SelfCarehour = ""
        self.temp_SelfDevhour = ""
        self.temp_Socialhour = ""
        self.temp_Shortbreak = ""
        self.temp_Longbreak = ""
        self.temp_datetime = datetime.datetime.now()

        self.read_task()
        self.refreshAllTasks = False
        self.SelectTask ={}
        SelectTask =  np.array([ "Work",
                               "Lunch", "Dinner",
                               "Self-care", "Self-development",
                               "Social", "Short break", "Long break","Sleep"])
        for i in range(len(SelectTask)):
            self.SelectTask[SelectTask[i]] = i
        print(self.SelectTask)

    def read_task(self):
        path = os.getcwd() + "\\tasks\\task.txt"
        self.All_button_scene0.clear()
        self.All_tasks.clear()
        with open(path, "r") as File:
            data = File.readlines()
            for i in data:
                text = i.split(",")
                btn = button.Button(self.screen,string= text[0],mouse_pos=(0,0),x=0,y=0,width=300,height=self.tab_height-15)
                self.All_button_scene0.append(btn)
                task = Task(text[0],text[1],text[2],text[3],distutils.util.strtobool(text[4].replace("\n","")))
                self.All_tasks.append(task)
            File.close()

    def write_task(self, list):
        path = os.getcwd() + "\\tasks\\task.txt"
        with open(path, "w") as File:
            for t in list:
                text = t.get_all_parameter() + "\n"
                File.write(text)
            File.close()

    def read_template(self):
        path = os.getcwd() + "\\tasks\\template.txt"

    def write_template(self):
        path = os.getcwd() + "\\tasks\\template.txt"

    def create_line_of_text(self, screen, width, height, font, text, show=True):
        # create a text suface object,
        # on which text is drawn on it.
        Header = font.render(text, True, (0, 0, 0))
        if show:
            screen.blit(Header, ((width - Header.get_width()) / 2, height))
        return Header.get_rect()

    # Add task scene
    def add_Info_task_panel(self, screen, font, width, height, mouse_pos):
        Text_rect = self.create_line_of_text(screen, width - 50, 0, font, "Tasks")
        height = height * 0.05 + Text_rect.height

        show_add_Info_task_panel_height = 500
        show_add_Info_task_panel_width = width * 0.55
        pygame.draw.rect(screen, (224, 255, 255), [width * 0.5, height, width * 0.8 * 0.5
            , show_add_Info_task_panel_height])

        offset = 10
        height += offset
        input_rect_list = []
        Titles = np.array(["Title", "Task", "Deadline", "Difficulty Level"])
        Title = "Title"
        for i in Titles:
            Title_text_surface = font.render(i, True, (0, 0, 0))
            screen.blit(Title_text_surface, (show_add_Info_task_panel_width, height))
            height += Title_text_surface.get_height() + offset

            input_rect = pygame.Rect(show_add_Info_task_panel_width, height, 300, 40)
            pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
            input_rect_list.append(input_rect)
            height += input_rect.height + offset

        return input_rect_list

    def add_task_panel_scene(self, screen, font, width, height, mouse_pos):
        Text_rect = self.create_line_of_text(screen, width - 50, 0, font, "Tasks", show=False)
        y = height * 0.05 + Text_rect.height
        x = width * 0.05

        tab_width = width * 0.8 * 0.5
        tab_height = 500
        pygame.draw.rect(screen, (240, 240, 240), [x, y, width * 0.8 * 0.5
            , tab_height])
        return x, y, tab_width, tab_height

    ###############################################################################
    # Create template scene
    ###############################################################################

    def duty_panel_scene(self, screen, font, width, height, mouse_pos):
        Text_rect = self.create_line_of_text(screen, width, 0, font, "Templates", show=False)
        y = height * 0.05 + Text_rect.height
        x = width * 0.05

        tab_width = width * 0.8 * 0.5
        tab_height = 500
        pygame.draw.rect(screen, (240, 240, 240), [x, y, width * 0.8 * 0.5
            , tab_height])
        return x, y, tab_width, tab_height

    def add_Template_Info_panel(self, screen, bigfont, smallfont, width, height, mouse_pos):
        listOfInputBox = []

        Text_rect = self.create_line_of_text(screen, width - 50, 0, bigfont, "Templates")
        height = height * 0.01 + Text_rect.height

        show_add_Info_panel_height = 550
        show_add_Info_panel_width = width * 0.55
        pygame.draw.rect(screen, (224, 255, 255), [width * 0.5, height, width * 0.8 * 0.5
            , show_add_Info_panel_height])

        offset = 10
        height += offset
        Title = "Name of Template"
        Title_text_surface = smallfont.render(Title, True, (0, 0, 0))
        screen.blit(Title_text_surface, (show_add_Info_panel_width, height))
        height += Title_text_surface.get_height() + offset

        input_rect_title = pygame.Rect(show_add_Info_panel_width, height, 300, 30)
        pygame.draw.rect(screen, (0, 0, 0), input_rect_title, 2)
        listOfInputBox.append(input_rect_title)
        height += input_rect_title.height + offset

        Title = "Insert number of hour for each task"
        Title_text_surface = smallfont.render(Title, True, (0, 0, 0))
        screen.blit(Title_text_surface, (show_add_Info_panel_width, height))
        height += Title_text_surface.get_height() + offset

        TaskNames = np.array(["Sleeping Hours :", "Working Hours :",
                              "Lunch Hours :", "Dinner Hours :",
                              "Self-care Hours :", "Self-development Hours :",
                              "Social Hours :", "Short break :", "Long break :"])

        for i in TaskNames:
            Title_text_surface = smallfont.render(i, True, (0, 0, 0))
            screen.blit(Title_text_surface, (show_add_Info_panel_width, height))
            input_rect = pygame.Rect(show_add_Info_panel_width + 230, height, 50, 25)
            pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
            listOfInputBox.append(input_rect)
            height += input_rect.height + offset

        SelectTask = self.SelectTask

        min_limit_width = width * 0.52
        max_limit_width = min_limit_width + width * 0.5 * 0.8
        tab_height = 25
        Task_buttons = []
        for i in SelectTask:
            Title_text_surface = smallfont.render(i, True, (0, 0, 0))
            if min_limit_width < min_limit_width + Title_text_surface.get_width() < max_limit_width:
                x = button.Button(screen, i, (0, 0, 0), (170, 170, 170), (255, 255, 255),
                                  min_limit_width,
                                  height,
                                  width=Title_text_surface.get_width() * 1.2, height=tab_height, mouse_pos=mouse_pos)
                x.text_size(20)
                x.create_rect_btn()
                min_limit_width += x.width + 10
                Task_buttons.append(x)
            else:
                min_limit_width = width * 0.52
                height += tab_height + offset
                x = button.Button(screen, i, (0, 0, 0), (170, 170, 170), (255, 255, 255),
                                  min_limit_width,
                                  height,
                                  width=Title_text_surface.get_width() * 1.2, height=tab_height, mouse_pos=mouse_pos)
                x.text_size(20)
                x.create_rect_btn()
                min_limit_width += x.width + 10
                Task_buttons.append(x)
        return listOfInputBox, Task_buttons

    ###############################################################################
    # Plan the day
    ###############################################################################

    def PTD_right_panel(self, screen, bigfont, smallfont, width, height, mouse_pos):
        Text_rect = self.create_line_of_text(screen, (width -50)/2 , 30, smallfont, "Available tasks")
        self.create_line_of_text(screen, (width -50)*1.45, 30, smallfont, "Choose the task")
        y = height * 0.05 + Text_rect.height +15
        x = width * 0.5
        tab_width = width * 0.8 * 0.5
        tab_height = 500
        show_add_Info_panel_height = 500
        show_add_Info_panel_width = width * 0.55
        pygame.draw.rect(screen, (224, 255, 255), [x, y,tab_width
            , show_add_Info_panel_height])
        pygame.draw.rect(screen, (220, 230, 230), [x, y, tab_width
            , show_add_Info_panel_height/2])
        y1 =y +show_add_Info_panel_height/2
        self.create_line_of_text(screen, (width - 50) * 1.5, y1+10, smallfont, "Choose the template")

        return x, y, tab_width, tab_height

    def PTD_left_panel(self, screen, bigfont, smallfont, width, height, mouse_pos):
        Text_rect = self.create_line_of_text(screen, width, 0, bigfont, "Templates", show=False)
        y = height * 0.05 + Text_rect.height
        x = width * 0.05

        tab_width = width * 0.8 * 0.5
        tab_height = 500
        pygame.draw.rect(screen, (240, 240, 240), [x, y, tab_width
            , tab_height])

        refreshIcon = pygame.transform.scale(self.refreshIcon, (30, 30))
        scene2_height = (height - refreshIcon.get_height()) / 2
        screen.blit(refreshIcon, (tab_width + 1.75 * refreshIcon.get_width(), y))
        refresh_box = pygame.rect.Rect(tab_width + 1.75 * refreshIcon.get_width(), y, refreshIcon.get_width(),
                                       refreshIcon.get_height())

        self.refreshAllTasks = pygame.mouse.get_pressed(5)[0] and refresh_box.collidepoint(pygame.mouse.get_pos())
        return x, y, tab_width, tab_height

    def refreshTasks(self):
        self.read_task()
        self.read_template()
        print("Read file : Done")
        time.sleep(0.1)

    def Run(self):

        screen = self.screen
        # color
        black = (0, 0, 0)
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        light_blue = 135, 206, 250
        # light shade of the button
        color_light = (170, 170, 170)
        # dark shade of the button
        color_dark = (100, 100, 100)

        # stores the width of the
        # screen into a variable
        width = screen.get_width()

        # stores the height of the
        # screen into a variable
        height = screen.get_height()

        # defining a font
        bigfont = pygame.font.SysFont('Corbel', 35)
        smallfont = pygame.font.SysFont('Corbel', 20)
        inputfont = pygame.font.SysFont('Arial', 20)
        default_font = pygame.font.SysFont("Arial", 20)

        # set the pygame window name
        pygame.display.set_caption('Daily Planner')
        programIcon = pygame.image.load('planner-icon.jpg')
        pygame.display.set_icon(programIcon)

        scene1 = False
        scene2 = False
        scene3 = False
        running = True

        All_button_scene1 = self.All_button_scene0
        All_button_scene2 = []
        All_button_scene3_notselected = []
        All_button_scene3_selected = []

        show_task_panel_x, show_task_panel_y, show_task_panel_width, show_task_panel_height = 0, 0, 0, 0

        init_input_rect_scene1 = self.add_Info_task_panel(screen,
                                                          bigfont,
                                                          width,
                                                          0,
                                                          (0, 0))
        input_rect_scene1 = []
        input_rect_scene1_active = np.array([False] * len(init_input_rect_scene1))
        input_TextBox_scene1 = [" "] * len(init_input_rect_scene1)

        # Scene 2 initilize

        init_input_rect_scene2, init_scene2_task_buttons = self.add_Template_Info_panel(screen,
                                                                                        bigfont,
                                                                                        smallfont,
                                                                                        width,
                                                                                        0,
                                                                                        (0, 0))
        scene2_task_buttons = init_scene2_task_buttons
        input_rect_scene2 = init_input_rect_scene2
        input_rect_scene2_active = np.array([False] * len(init_input_rect_scene2))
        input_TextBox_scene2 = [""] * len(init_input_rect_scene2)
        cmd = ""


        input_rect_scene3 = []

        PTD_r_x,PTD_r_y,PTD_r_tab_width,PTD_r_tab_height =0,0,0,0
        PTD_l_x, PTD_l_y, PTD_l_tab_width, PTD_l_tab_height = 0,0,0,0

        while running:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            btn_save_template = None
            btn_clear_template = None



            screen.fill(white)
            self.create_line_of_text(screen, width * 1.8, 10, default_font, str(current_time))
            # create_line_of_text(screen, width*1.8, 10, default_font, str(current_date))
            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()

            tab_width = width / 3
            tab_height = self.tab_height
            text_size = self.text_size

            btn_add_task = button.Button(screen, "Add Tasks", white, color_light, color_dark, 0, height - tab_height,
                                         width=tab_width,
                                         height=tab_height, mouse_pos=mouse)
            btn_create_template = button.Button(screen, "Create Template", white, color_light, color_dark, tab_width,
                                                height - tab_height,
                                                width=tab_width, height=tab_height, mouse_pos=mouse)
            btn_plan_the_day = button.Button(screen, "Plan the day", white, color_light, color_dark, tab_width * 2,
                                             height - tab_height,
                                             width=tab_width, height=tab_height, mouse_pos=mouse)
            add_btn = button.Button(screen, "+", white, light_blue, blue, width * 0.9,
                                    (height - tab_height) * 0.05 + 35,
                                    width=50,
                                    height=50, mouse_pos=mouse)
            add_btn.text_size(30)
            btn_add_task.text_size(text_size)
            btn_create_template.text_size(text_size)
            btn_plan_the_day.text_size(text_size)

            # if mouse is hovered on a button it
            # changes to lighter shade
            btn_add_task.create_rect_btn()
            btn_create_template.create_rect_btn()
            btn_plan_the_day.create_rect_btn()

            if not scene1 and not scene2 and not scene3:
                Text_rect = self.create_line_of_text(screen, width, 10, smallfont, 'Welcome to the daily planner')
                programIcon = pygame.transform.scale(programIcon, (256, 256))
                scene0_height = (height - programIcon.get_height()) / 2 - 100
                screen.blit(programIcon, ((width - programIcon.get_width()) / 2, scene0_height))

                self.create_line_of_text(screen, width, 500, smallfont, "Let start planning")

            elif scene1:

                input_rect_scene1 = self.add_Info_task_panel(screen,
                                                             bigfont,
                                                             width,
                                                             height - tab_height,
                                                             mouse)
                show_task_panel_x, show_task_panel_y, show_task_panel_width, show_task_panel_height = self.add_task_panel_scene(
                    screen,
                    bigfont,
                    width,
                    height - tab_height,
                    mouse)

                add_btn.create_rect_btn()

            elif scene2:
                input_rect_scene2, scene2_task_buttons = self.add_Template_Info_panel(screen,
                                                                                      bigfont,
                                                                                      smallfont,
                                                                                      width,
                                                                                      height - tab_height,
                                                                                      mouse)
                show_task_panel_x, show_task_panel_y, show_task_panel_width, show_task_panel_height = self.duty_panel_scene(
                    screen,
                    bigfont,
                    width,
                    height - tab_height,
                    mouse)
                btn_save_template = button.Button(screen, "Save", white, color_light, color_dark, show_task_panel_x+show_task_panel_width*2+50,
                                             show_task_panel_y,
                                             width=50,
                                             height=tab_height, mouse_pos=mouse)
                btn_save_template.text_size(15)
                btn_save_template.create_rect_btn()
                btn_clear_template = button.Button(screen, "Clear", white, color_light, color_dark,
                                                  show_task_panel_x + show_task_panel_width * 2 + 50,
                                                  show_task_panel_y+tab_height,
                                                  width=50,
                                                  height=tab_height, mouse_pos=mouse)
                btn_clear_template.text_size(15)
                btn_clear_template.create_rect_btn()
            elif scene3:
                # self.plan_the_day_scene(screen, width, height - tab_height, bigfont, mouse)
                PTD_l_x,PTD_l_y,PTD_l_tab_width,PTD_l_tab_height = self.PTD_left_panel(screen, bigfont, smallfont, width, height - tab_height, mouse)
                PTD_r_x,PTD_r_y,PTD_r_tab_width,PTD_r_tab_height =self.PTD_right_panel(screen, bigfont, smallfont, width, height - tab_height, mouse)
                btn_start = button.Button(screen, "Start", white, color_light, color_dark, PTD_r_x+PTD_r_tab_width,
                                             PTD_r_y+250,
                                             width=40,
                                             height=tab_height, mouse_pos=mouse)
                btn_start.text_size(15)
                btn_start.create_rect_btn()

            # updates the frames of the game

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                    # checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN:

                    if btn_add_task.button_click() or btn_create_template.button_click() or btn_plan_the_day.button_click():
                        scene1 = btn_add_task.button_click()
                        scene2 = btn_create_template.button_click()
                        scene3 = btn_plan_the_day.button_click()

                    if scene1:
                        if len(All_button_scene1) > 0:
                            for i in All_button_scene1:
                                i.button_click()

                        if len(input_rect_scene1) > 0:
                            for i in range(len(input_rect_scene1)):
                                input_rect_scene1_active[i] = bool(input_rect_scene1[i].collidepoint(ev.pos))

                        if add_btn.button_click() and input_TextBox_scene1[0] != "":
                            x = button.Button(screen, input_TextBox_scene1[0], white, color_light, color_dark,
                                              show_task_panel_x,
                                              show_task_panel_y,
                                              width=300, height=tab_height - 15, mouse_pos=mouse)
                            x.text_size(20)
                            x.create_rect_btn()
                            All_button_scene1.append(x)

                            temp_task = Task(input_TextBox_scene1[0],
                                             input_TextBox_scene1[1],
                                             input_TextBox_scene1[2],
                                             input_TextBox_scene1[3],
                                             finish_task=False)

                            self.All_tasks.append(temp_task)
                            self.write_task(self.All_tasks)

                    elif scene2:
                        if len(scene2_task_buttons) > 0:
                            for i in scene2_task_buttons:
                                i.button_click()
                                if i.button_click():
                                    x = button.Button(screen, i.text, white, color_light, color_dark,
                                                      show_task_panel_x,
                                                      show_task_panel_y,
                                                      width=300, height=tab_height - 15, mouse_pos=mouse)
                                    x.text_size(20)
                                    x.create_rect_btn()
                                    All_button_scene2.append(x)
                        if len(All_button_scene2) > 0:
                            for i in All_button_scene2:
                                i.button_click()

                        if len(input_rect_scene2) > 0:
                            input_rect_scene2_active = [bool(i.collidepoint(ev.pos)) for i in input_rect_scene2]

                        if btn_save_template is not None:
                            if btn_save_template.button_click():
                                for i in All_button_scene2:
                                    name = i.get_name()
                                    cmd += str(self.SelectTask.get(name))

                                timetable = self.save_template(input_rect_scene2, input_TextBox_scene2, inputfont, screen,cmd)
                                TimeTableMaker.TimeTableMaker().createNewTimeTableTemplate(input_TextBox_scene2[0],os.getcwd(),timetable,cmd)
                                cmd = ""
                        if btn_clear_template is not None:
                            if btn_clear_template.button_click():
                                input_TextBox_scene2,All_button_scene2 =self.clear_scene2(input_TextBox_scene2,All_button_scene2)



                    elif scene3:
                        if len(All_button_scene3_selected) > 0:
                            for i in All_button_scene3_selected:
                                i.button_click()

                        if len(All_button_scene3_notselected) > 0:
                            for i in All_button_scene3_notselected:
                                if i.button_click():
                                    All_button_scene3_selected.append(i)
                                    i.set_selected(False)
                                    self.update_button_pos(All_button_scene3_selected, PTD_r_x, PTD_r_y, tab_width,
                                                           tab_height, mouse)
                                    All_button_scene3_notselected.remove(i)

                if ev.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()

                    if scene1:
                        if len(All_button_scene1) > 0:
                            for i in All_button_scene1:
                                if i.get_selected() and ev.key == pygame.K_DELETE:
                                    self.All_tasks.pop(All_button_scene1.index(i))
                                    All_button_scene1.remove(i)
                                    self.write_task(self.All_tasks)
                        for index in range(len(input_rect_scene1_active)):
                            if input_rect_scene1_active[index]:
                                if ev.key == pygame.K_BACKSPACE:
                                    input_TextBox_scene1[index] = input_TextBox_scene1[index][:-1]
                                elif ev.key == pygame.K_KP_ENTER or ev.key == pygame.K_RETURN or ev.key == pygame.K_ESCAPE:
                                    input_rect_scene1_active = np.array([False] * len(input_rect_scene1))
                                else:
                                    input_TextBox_scene1[index] += str(ev.unicode)
                    elif scene2:
                        # Left panel
                        if len(All_button_scene2) > 0:
                            temp_check_list = [i.get_selected() for i in All_button_scene2]
                            if temp_check_list.__contains__(True):
                                index = temp_check_list.index(True)
                                if key[pygame.K_DELETE]:
                                    All_button_scene2.remove(All_button_scene2[index])
                                elif key[pygame.K_DOWN] and index < len(All_button_scene2) - 1:
                                    temp = All_button_scene2[index]
                                    All_button_scene2[index] = All_button_scene2[index + 1]
                                    All_button_scene2[index + 1] = temp
                                elif ev.key == pygame.K_UP and index > 0:
                                    temp = All_button_scene2[index]
                                    All_button_scene2[index] = All_button_scene2[index - 1]
                                    All_button_scene2[index - 1] = temp
                        # Right panel

                        if input_rect_scene2_active.__contains__(True):
                            index = [i for i in input_rect_scene2_active].index(True)
                            if ev.key == pygame.K_BACKSPACE:
                                input_TextBox_scene2[index] = input_TextBox_scene2[index][:-1]
                            elif ev.key == pygame.K_KP_ENTER or ev.key == pygame.K_RETURN or ev.key == pygame.K_ESCAPE:
                                input_rect_scene2_active = np.array([False] * len(input_rect_scene2))
                            else:
                                if index == 0:
                                    input_TextBox_scene2[index] += str(ev.unicode)
                                elif index > 0 and len(input_TextBox_scene2[index]) < 3 and str(ev.unicode).isnumeric():
                                    input_TextBox_scene2[index] += ev.unicode
                                    if float(input_TextBox_scene2[index]) > 12:
                                        input_TextBox_scene2[index] = "12"
                            if input_TextBox_scene2[0] != "":
                                self.temp_template_name = input_TextBox_scene2[0]
                            if input_TextBox_scene2[1] != "":
                                self.temp_Sleephour = input_TextBox_scene2[1]
                            if input_TextBox_scene2[2] != "":
                                self.temp_Workhour = input_TextBox_scene2[2]
                            if input_TextBox_scene2[3] != "":
                                self.temp_Lunchhour = input_TextBox_scene2[3]
                            if input_TextBox_scene2[4] != "":
                                self.temp_Dinnerhour = input_TextBox_scene2[4]
                            if input_TextBox_scene2[5] != "":
                                self.temp_SelfCarehour = input_TextBox_scene2[5]
                            if input_TextBox_scene2[6] != "":
                                self.temp_SelfDevhour = input_TextBox_scene2[6]
                            if input_TextBox_scene2[7] != "":
                                self.temp_Socialhour = input_TextBox_scene2[7]
                            if input_TextBox_scene2[8] != "":
                                self.temp_Shortbreak = input_TextBox_scene2[8]
                            if input_TextBox_scene2[9] != "":
                                self.temp_Longbreak = input_TextBox_scene2[9]
                    elif scene3:
                        if len(All_button_scene3_selected) > 0:
                            for i in All_button_scene3_selected:
                                if i.button_click():
                                    if key[pygame.K_LEFT] or key[pygame.K_DELETE] or key[pygame.K_KP_MINUS]:

                                        All_button_scene3_notselected.append(i)
                                        self.update_button_pos(All_button_scene3_notselected, show_task_panel_x,
                                                               show_task_panel_y, tab_width, tab_height, mouse)
                                        All_button_scene3_selected.remove(i)

            if scene1:

                for i in range(len(All_button_scene1)):

                    All_button_scene1[i].text_size(20)
                    # All_button_scene1[i].screen = screen
                    if i == 0:
                        All_button_scene1[i].set_pos(show_task_panel_x, show_task_panel_y)
                    else:
                        All_button_scene1[i].set_pos(show_task_panel_x, show_task_panel_y + (tab_height - 15) * i)
                    All_button_scene1[i].mouse_pos_update(mouse)
                    All_button_scene1[i].set_Button_width(show_task_panel_width)
                    All_button_scene1[i].create_rect_btn()

                if len(input_rect_scene1) > 0:
                    for i in range(len(input_rect_scene1)):
                        input_rect_scene1[i] += np.array([10, 10, 0, 0])
                        screen.blit(inputfont.render(input_TextBox_scene1[i], True, (0, 0, 0)), input_rect_scene1[i])

            elif scene2:
                for i in range(len(All_button_scene2)):
                    if i == 0:
                        All_button_scene2[i].set_pos(show_task_panel_x, show_task_panel_y)
                    else:
                        All_button_scene2[i].set_pos(show_task_panel_x, show_task_panel_y + (tab_height - 15) * i)
                    All_button_scene2[i].mouse_pos_update(mouse)
                    All_button_scene2[i].set_Button_width(show_task_panel_width)
                    All_button_scene2[i].create_rect_btn()
                self.save_template(input_rect_scene2, input_TextBox_scene2, inputfont, screen)

            elif scene3:
                if self.refreshAllTasks:
                    All_button_scene3_notselected = self.All_button_scene0
                    self.refreshAllTasks = False

                self.update_button_pos(All_button_scene3_notselected, PTD_l_x, PTD_l_y, PTD_l_tab_width, tab_height, mouse)
                self.update_button_pos(All_button_scene3_selected,PTD_r_x,PTD_r_y,PTD_r_tab_width,tab_height,mouse)

            pygame.display.update()

    def clear_scene2(self,input_TextBox_scene2,All_button_scene2):
        All_button_scene2 = []
        input_TextBox_scene2 = [""] * len(input_TextBox_scene2)
        self.temp_template_name = ""
        self.temp_Sleephour = ""
        self.temp_Workhour = ""
        self.temp_Lunchhour = ""
        self.temp_Dinnerhour = ""
        self.temp_SelfCarehour = ""
        self.temp_SelfDevhour = ""
        self.temp_Socialhour = ""
        self.temp_Shortbreak = ""
        self.temp_Longbreak = ""
        return input_TextBox_scene2,All_button_scene2
    def save_template(self,input_rect_scene2,input_TextBox_scene2,inputfont,screen,cmd=None):
        if len(input_rect_scene2) > 0:
            all_info_collected = 0
            for i in range(len(input_rect_scene2)):
                input_rect_scene2[i] += np.array([4, 0, 0, 0])
                screen.blit(inputfont.render(input_TextBox_scene2[i], True, (0, 0, 0)), input_rect_scene2[i])


                all_info_collected += (
                            input_TextBox_scene2[i]!= "")

            if all_info_collected == len(input_TextBox_scene2) and cmd is not None:
                # Default config Amount of total hour for each task
                SleepingHour = float(self.temp_Sleephour)  # hour
                WorkingHour = float(self.temp_Workhour)  # hour
                ExerciseHour = float(self.temp_SelfCarehour)  # hour
                FriendsHour =float(self.temp_Socialhour)  # hour
                SelfDevelopmentHour = float(self.temp_SelfDevhour)  # hour
                LunchHour = float(self.temp_Lunchhour)
                DinnerHour = float(self.temp_Dinnerhour)

                # Time
                PlannedDate = self.temp_datetime.date()
                StartTime = datetime.time(8, 45)
                shortBreak = float(self.temp_Shortbreak)
                longBreak = float(self.temp_Longbreak)

                x = TimeTemplateClass.TimeTableTemplate(StartTime, shortBreak, longBreak, SleepingHour, WorkingHour,
                                                        LunchHour,
                                                        DinnerHour,
                                                        ExerciseHour,
                                                        SelfDevelopmentHour,
                                                        FriendsHour, PlannedDate)
                print(cmd)
                if cmd is not None:
                    x.create_custom_template(cmd)

                return x

    def update_button_pos(self,list,x,y,tab_width,tab_height,mouse):
        for i in range(len(list)):
            list[i].text_size(20)
            if i == 0:
                list[i].set_pos(x, y)
            else:
                list[i].set_pos(x, y + (tab_height - 15) * i)
            list[i].mouse_pos_update(mouse)
            list[i].set_Button_width(tab_width)
            list[i].create_rect_btn()

if __name__ == '__main__':
    x = TimetableUI()
    check_save_path()
    x.Run()
