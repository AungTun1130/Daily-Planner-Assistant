import numpy as np
import os
from datetime import datetime, time, timedelta
from plyer import notification
import TimeTemplateClass as timetable

list = np.array(["Work", "Exercise", "Friends", "Self-development"])

leftHour = None
# Default config Amount of total hour for each task
SleepingHour = 8  # hour
WorkingHour = 9  # hour
ExerciseHour = 1  # hour
FriendsHour = 1  # hour
SelfDevelopmentHour = 1  # hour
EatingHour = 1

# Time
PlannedDate = datetime(2020, 11, 23)
StartTime = time(8, 45)
shortBreak = 5
longBreak = 30


def initUserName(Filedir):
    Name = input("Your name :")
    filename = Filedir + "\\" + Name + ".txt"
    if not os.path.isfile(filename):
        Email = input("Email :")
        file = open(filename, "w")
        file.write(Name + "\n")
        file.close()
    return Name


# Hour of day left
def inputLeftHour(value):
    print(leftHour)


def timetable_maker():
    TotalHour = 24 - SleepingHour  # hour


def createNewTimeTableTemplate(TempName, dir,timetable,cmd=None):

    # input:
    #       TimeTable
    #       directory
    #       Name of the template
    #       Command number for the creating custom timetable

    # output
    #       Timetable txt file
    Filedir = dir + "\Template"
    FileName = Filedir + "\\" + TempName + ".txt"

    # print("Input how much hour you would like to spend for these")
    # SleepingHour = float(input("Total Sleeping Hour :"))  # hour
    # WorkingHour = float(input("Total Working Hour :"))  # hour
    # ExerciseHour = float(input("Exercise Hour :"))  # hour
    # # FriendsHour = int(input("Social Hour :"))  # hour
    # SelfDevelopmentHour = float(input("Self-development Hour :"))  # hour
    # LunchHour = float(input("Lunch :"))   # hour
    # DinnerHour = float(input("Dinner :"))    # hour
    #
    # # Time
    # print("What time do you want to start? [example : 08:45 , 17:45]")
    # StartHourTime = int(input("Hour [integer]:"))
    # StartMinuteTime = int(input("Minute [integer]:"))
    # PlannedDate = datetime(2020, 11, 23)
    #
    # StartTime = time(StartHourTime, StartMinuteTime)
    # shortBreak = int(input("Short break in Minutes [integer]:"))
    # longBreak = int(input("Long break in Minutes [integer]:"))
    #
    # socialHour = float(input("Social Hour :"))

    # x = timetable.TimeTableTemplate( StartTime, shortBreak, longBreak, SleepingHour, WorkingHour, LunchHour,
    #                       DinnerHour,
    #                       ExerciseHour,
    #                       SelfDevelopmentHour,socialHour,PlannedDate)
    print("")
    timetable_list = timetable.show_created_template()
    if timetable_list == []:
        timetable.create_custom_template(cmd)
        timetable_list = timetable.show_created_template()

    with open(FileName) as File:
        File.write("CMD:" + cmd + "\n")
        separator = ","
        for i in timetable:
            File.write(separator.join(i)+"\n")
        File.close()





def createNewTimetableFile(UserName, dir):
    print("Plane for today or tomorrow?")
    PlanDate = input("Select 0 for today and 1 for tomorrow: ")
    TodayDate = datetime.today()
    if PlanDate == "1":
        TodayDate = TodayDate.now() + timedelta(days=1)

    Template = input("Please Select the template :")
    Filedir = dir + "\data"
    FileName = Filedir + "\\" + str(TodayDate) + UserName + ".txt"

    data = [str(TodayDate), UserName]
    # writingFile(Filedir,FileName,data)


def StartTheDay():
    print("Starting the day")
    print(datetime.now().strftime("%H:%M"))
    currentTime = datetime.now().strftime("%H:%M")
    hour_value = int(currentTime.split(":")[0])
    minute_value = int(currentTime.split(":")[1])
    if minute_value in range(30, 46):
        minute_value = 45
    if minute_value in range(15, 31):
        minute_value = 30
    if minute_value in range(0, 16):
        minute_value = 15
    if minute_value in range(46, 60):
        minute_value = 0
        hour_value += 1

    startTime = time(hour=hour_value, minute=minute_value)
    print("Starting day time :", startTime)

    notification.notify(
        app_name="Daily planner",
        title="Daily planner",
        message="Start doing work",
        timeout=10
    )


def writingFile(filedir, filename, dataList):
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    if os.path.isfile(filename):
        rewirteFile = input("File has already existed, Would you like to rewirte it? (y,n)")
        if rewirteFile.lower() == "n":
            filename = filedir + "\\" + filename.split("\\")[-1][:-4] + "(1)" + ".txt"
        # print(filename)

    file = open(filename, "w")
    for i in dataList:
        file.write(str(i) + "\n")
    file.close()

    print("Finish writing file")


def readingFile():
    print("Finish reading file")


if __name__ == '__main__':
    dir = os.getcwd()
    print("Welcome to the daily planner")
    userName = input("Username :")
    print("##### MAIN MENU #######")
    Menu = np.array(
        ["0:Creating Timetable template", "1:Create timetable", "2:Start the day schedule", "3:Evaluation of the day"])
    for item in Menu:
        print(item)
    while True:
        while True:
            TaskInput = input("Please choose the item [0,1,2,3] :")
            Confirm = input("Please confirm the selected item [Y,N] :")
            if Confirm.lower() == "y":
                print("")
                break

        if TaskInput.isnumeric() and int(TaskInput) in range(0, 4):
            command = int(TaskInput)
            if command ==0:
                print("Start Creating timetable template")
                TempName = input("Name of the template :")
                createNewTimeTableTemplate(TempName,dir)
            if (command == 1):
                # do this
                print("Start Creating timetable")
                createNewTimetableFile(userName, dir)

            elif (command == 2):
                # do this
                StartTheDay()
            elif (command == 3):
                # do this
                print("Start Evaluating the timetable")

            break
    # UserName = initUserName(dir)
    # createNewTimetableFile(UserName,dir)
    # while True:
    #      leftHour = input("Enter value: ")
    #      if leftHour.isnumeric():
    #          float(leftHour)
    #          break
