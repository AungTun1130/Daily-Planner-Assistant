import numpy as np
import datetime as dt
from plyer import notification

class TimeTableTemplateClass:
    def __init__(self, start_time=None, short_break=None, long_break=None, sleep_hour=None, work_hour=None, lunch_hour=None,
                 dinner_hour=None, self_care=None,
                 self_development_hour=None,social_hour=None, planned_date=None):
        SelectTask =  np.array(["Sleep", "Work",
                               "Lunch", "Dinner",
                               "Self-care", "Self-development",
                               "Social", "Short break", "Long break"])
        self.DutyCategory = np.array(["Work", "Lunch", "Dinner", "Self-care", "Self-development", "Relax","Short break", "Long break","Custom"])
        self.Category = np.array(["Work", "Self-care", "Self-development", "Relax"])
        if start_time is not None:
            self.PlannedDate = planned_date
            print(start_time)
            self.StartTime = dt.datetime.combine(planned_date, start_time)
            self.shortBreak = dt.timedelta(minutes=short_break)
            self.longBreak = dt.timedelta(minutes=long_break)
            self.TotalSleepHour = dt.timedelta(hours=sleep_hour + 1, minutes=30)
            self.TotalWorkHour = dt.timedelta(hours=work_hour)
            self.LunchHour = dt.timedelta(hours=lunch_hour)
            self.DinnerHour = dt.timedelta(hours=dinner_hour)
            self.SelfCare = dt.timedelta(hours=self_care)
            self.TotalSelfDevelopmentHour = dt.timedelta(hours=self_development_hour)
            self.SocialHour = dt.timedelta(hours = social_hour)
            self.WorkAssignments = np.array([])
            self.SelfDevelopmentAssignment = np.array([])
            self.TimeTable = []

            self.LunchTime = dt.datetime.combine(self.PlannedDate, dt.time(hour=12, minute=45))
            self.DinnerTime = dt.datetime.combine(self.PlannedDate, dt.time(hour=17, minute=45))

            self.StartingTime = None
            self.EndingTime = None
            self.WorkedHour = dt.timedelta(minutes=0)
            self.SleepTime = self.StartTime + dt.timedelta(days=1) - self.TotalSleepHour
        info_dict_text = ["start_time", "short_break", "long_break", "sleep_hour", "work_hour", "lunch_hour",
                 "dinner_hour", "self_care",
                 "self_development_hour","social_hour", "planned_date"]
        info = [start_time, short_break, long_break, sleep_hour, work_hour, lunch_hour,
                             dinner_hour, self_care,
                             self_development_hour, social_hour, planned_date]
        self.AllInputInfo={}
        for i in info_dict_text:
            self.AllInputInfo[i] = info[info_dict_text.index(i)]




    def show_created_template(self):
        print("")
        print("############    Template    ############")
        if len(self.TimeTable) > 0:
            for i in self.TimeTable:
                print(i)
        print("########################################")
        print(self.get_all_input())
        return  self.TimeTable
    def choose_template(self):
        show_text = "Would like to create a new template or choose a default?"
        print(show_text)
        while True:
            template = input("Choose 0 for default / 1 to create new")
            if template.isnumeric():
                if int(template) == 0:
                    self.create_default_template()
                if int(template) == 1:
                    self.create_custom_template()
                break

    def create_default_template(self):

        self.work_time()
        self.lunch_time()
        self.work_time()
        self.dinner_time()
        self.add_short_break()
        self.self_care_time()
        self.add_long_break()
        self.self_development_time()

        self.show_created_template()
        return self.TimeTable

    def create_custom_template(self,CMD = None):


        for i in CMD:
            if i.isnumeric():
                i = int(i)

            if i ==0 or i == self.DutyCategory[0]:
                self.work_time()
            elif i == 1or i == self.DutyCategory[1]:
                self.lunch_time()
            elif i == 2 or i ==  self.DutyCategory[2]:
                self.dinner_time()
            elif i == 3 or i == self.DutyCategory[3]:
                self.self_care_time()
            elif i == 4 or i == self.DutyCategory[4]:
                self.self_development_time()
            elif i == 5 or i == self.DutyCategory[5]:
                self.social_time()
            elif i == 6 or i == self.DutyCategory[6]:
                self.add_short_break()
            elif i == 7 or i == self.DutyCategory[7]:
                self.add_long_break()
        self.show_created_template()
        return self.TimeTable

    def work_time(self):
        self.start_time_init()
        # morning work
        if self.WorkedHour.seconds == 0:
            self.EndingTime = self.LunchTime
        # Afternoon work before dinner
        elif (self.TotalWorkHour - self.WorkedHour).seconds > 0 and self.StartingTime < self.DinnerTime:
            self.StartingTime = self.EndingTime
            self.EndingTime = self.StartingTime + self.TotalWorkHour - self.WorkedHour

            # If the work will not be finished by dinner, stop at dinner and continue after dinner
            if (self.TotalWorkHour - self.WorkedHour).seconds > (self.DinnerTime - self.StartingTime).seconds:
                self.EndingTime = self.DinnerTime

        # Work after dinner
        elif (
                self.TotalWorkHour - self.WorkedHour).seconds > 0 and self.EndingTime >= self.DinnerTime + self.DinnerHour:
            self.StartingTime = self.EndingTime
            self.EndingTime = self.StartingTime + self.TotalWorkHour - self.WorkedHour
            print(self.StartingTime, self.EndingTime)

        if self.TotalWorkHour != self.WorkedHour:
            WorkedHour = self.EndingTime - self.StartingTime
            self.WorkedHour = dt.timedelta(seconds=self.WorkedHour.seconds + WorkedHour.seconds)

            timeDif = dt.timedelta(seconds=WorkedHour.seconds / 2)

            StartBreakTime = self.StartingTime + timeDif
            EndBreakTime = self.StartingTime + timeDif + self.shortBreak

            self.TimeTable.append([self.StartingTime.time().strftime("%H:%M"), StartBreakTime.strftime("%H:%M"), "Work"])
            self.TimeTable.append([StartBreakTime.strftime("%H:%M"), EndBreakTime.strftime("%H:%M"), "Break"])
            self.TimeTable.append([EndBreakTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "Work"])

            # If work hour finished before dinner, then this time slot will be free
            if (
                    self.DinnerTime - self.EndingTime).seconds / 60 > 0 and self.LunchTime < self.StartingTime < self.DinnerTime:
                self.TimeTable.append([self.EndingTime.strftime("%H:%M"), self.DinnerTime.strftime("%H:%M"), "Free slot"])

    def start_time_init(self):
        if self.StartingTime is None:
            self.StartingTime = self.StartTime

    def dinner_time(self):
        self.StartingTime = self.DinnerTime
        self.EndingTime = self.DinnerTime + self.DinnerHour
        self.TimeTable.append([self.DinnerTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "Dinner"])
        if (self.TotalWorkHour - self.WorkedHour).seconds > 0:
            self.work_time()

    def lunch_time(self):
        self.StartingTime = self.LunchTime
        self.EndingTime = self.LunchTime + self.LunchHour
        self.TimeTable.append([self.LunchTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "Lunch"])

    def self_care_time(self):
        self.start_time_init()
        self.StartingTime = self.EndingTime
        self.EndingTime = self.StartingTime + self.SelfCare
        self.TimeTable.append([self.StartingTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "Exercise"])

    def self_development_time(self):
        self.start_time_init()
        self.StartingTime = self.EndingTime
        self.EndingTime = self.StartingTime + self.SelfCare
        self.TimeTable.append(
            [self.StartingTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "self_development"])

    def social_time(self):
        self.start_time_init()
        self.StartingTime = self.EndingTime
        self.EndingTime = self.StartingTime + self.SocialHour
        self.TimeTable.append(
            [self.StartingTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "Social time"])

    def add_short_break(self):
        self.StartingTime = self.EndingTime
        self.EndingTime = self.StartingTime + self.shortBreak
        self.TimeTable.append(
            [self.StartingTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "Short break"])

    def add_long_break(self):
        self.StartingTime = self.EndingTime
        self.EndingTime = self.StartingTime + self.longBreak
        self.TimeTable.append(
            [self.StartingTime.strftime("%H:%M"), self.EndingTime.strftime("%H:%M"), "Long break"])

    def get_DutyCategory(self):
        return self.DutyCategory

    def get_all_input(self):
        data = []
        for i,info in self.AllInputInfo.items():
            data.append(i+":"+str(info))
        return data

    def get_CMD_to_stringlist(self,CMD):
        CMD = str(CMD)
        result_list = []
        for i in CMD:
            result_list.append(self.DutyCategory[int(i)])
        return result_list

    def get_stringlist_to_CMD(self,list):
        list = np.array(list)
        temp_CMD= np.zeros(len(list))
        for index in range(len(self.DutyCategory)):
            temp_CMD += (list == self.DutyCategory[index])*index
        return temp_CMD

    def StartTheDay(self):
        print("Starting the day")
        print(dt.datetime.now().strftime("%H:%M"))
        currentTime = dt.datetime.now().strftime("%H:%M")
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

        startTime = dt.time(hour=hour_value, minute=minute_value)
        print("Starting day time :", startTime)

        notification.notify(
            app_name="Daily planner",
            title="Daily planner",
            message="Start doing work",
            timeout=10
        )

if __name__ == '__main__':
    # Default config Amount of total hour for each task
    SleepingHour = 8  # hour
    WorkingHour = 9  # hour
    ExerciseHour = 1  # hour
    FriendsHour = 1  # hour
    SelfDevelopmentHour = 1  # hour
    LunchHour = 1
    DinnerHour = 2

    # Time
    PlannedDate = dt.datetime(2020, 11, 23)
    StartTime = dt.time(8, 45)
    shortBreak = 5
    longBreak = 30
    x = TimeTableTemplateClass(PlannedDate, StartTime, shortBreak, longBreak, SleepingHour, WorkingHour, LunchHour,
                          DinnerHour,
                          ExerciseHour,
                          SelfDevelopmentHour,
                          FriendsHour)
    #x.create_default_template()
    x.create_custom_template()
