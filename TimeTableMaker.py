import os
class TimeTableMaker:
    def __init__(self):
        self.taskFolder = "tasks"
        self.templateFolder = "templates"
        self.timetableFolder = "Timetable"
        self.check_create_dir()
    def check_create_dir(self):
        dir = os.getcwd()
        tasksDir = dir+"\\" + self.taskFolder
        templatesDir = dir+"\\" +self.templateFolder
        timetableDir = dir+"\\" +self.timetableFolder
        if not os.path.exists(tasksDir):
            os.makedirs(tasksDir)
        if not os.path.exists(templatesDir):
            os.makedirs(templatesDir)
        if not os.path.exists(timetableDir):
            os.makedirs(timetableDir)
    def createNewTimeTableTemplate(self,TempName, dir, timetable, cmd=None):

        # input:
        #       TimeTable
        #       directory
        #       Name of the template
        #       Command number for the creating custom timetable

        # output
        #       Timetable txt file
        Filedir = dir +"\\"+self.templateFolder
        FileName = Filedir + "\\" + TempName + ".txt"
        i = 0
        while os.path.exists(FileName):
            FileName = Filedir + "\\" + TempName +"("+str(i)+")" + ".txt"
            i+=1
        print("")
        timetable_list = timetable.show_created_template()
        timetable_input_info = timetable.get_all_input()

        if not timetable_list:
            timetable.create_custom_template(cmd)
            timetable_list = timetable.show_created_template()

        with open(FileName,"w") as File:
            File.write("TimeTable Template Info" + "\n")
            File.write("CMD:" + cmd + "\n")
            separator = ","
            for i in timetable_input_info:
                File.write(str(i) + "\n")
            File.write("Schedule"+"\n")
            for i in timetable_list:
                File.write(separator.join(i) + "\n")


            File.close()
    #def CreateTimeTable(self,timetable,tasks):

class TimeTableReader:
    def ReadTimeTable(self,path):
        data = []
        with open(path,'r') as File:
            cmd = File.readline()
            lines = File.readlines()
            for line in lines:
                print(line.split(","))

