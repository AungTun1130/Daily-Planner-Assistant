import os
import sqlite3
import glob


class TimetableDataManagement:
    def __init__(self):
        cur_dir = os.getcwd()
        separator = '\\'
        self.main_dir = separator.join(i for i in cur_dir.split("\\")[:-1])
        self.icon_dir = self.main_dir + separator + 'planner-icon.jpg'
        self.saveicon_dir = self.main_dir + separator + 'save_Icon.png'

    class Task:
        def __init__(self, name):
            self.task_dir = TimetableDataManagement().main_dir + "\\tasks\\" + name + ".db"
            self.create_task_database_init()

        def create_task_database_init(self):
            new = not os.path.isfile(self.task_dir)

            # connect a database
            conn = sqlite3.connect(self.task_dir)
            c = conn.cursor()

            if new:
                c.execute("""CREATE TABLE Task(
                    category text,
                    title text,
                    task text,
                    deadline_day integer,
                    deadline_month integer,
                    deadline_year integer,
                    active integer,
                    complete integer
                    )""")
                print("##CREATED NEW DATABASE FOR TASK##")
            # commit changes
            conn.commit()
            # Close connection
            conn.close()

        def submit_new_task(self, category=None, title=None, task=None,
                            deadline_day=None, deadline_month=None, deadline_year=None, active=False, complete=False):
            # Create a database or connect to one
            conn = sqlite3.connect(self.task_dir)
            # Create cursor
            c = conn.cursor()

            c.execute(
                "INSERT INTO Task VALUES(:category, :title, :task, "
                ":deadline_day, :deadline_month, :deadline_year,:active, :complete)",
                {
                    "category": category,
                    "title": title,
                    "task": task,
                    "deadline_day": deadline_day,
                    "deadline_month": deadline_month,
                    "deadline_year": deadline_year,
                    "active": active,
                    "complete": complete
                })
            # commit changes
            conn.commit()

            # Close connection
            conn.close()

        def query_task(self):
            conn = sqlite3.connect(self.task_dir)
            # Create cursor
            c = conn.cursor()

            # Query database
            c.execute("SELECT oid,* FROM Task")
            data = c.fetchall()

            # commit changes
            conn.commit()

            # Close connection
            conn.close()
            return data

        # Editing the specific task
        def update_task(self, oid=None, category=None, title=None, task=None,
                        deadline_day=None, deadline_month=None, deadline_year=None, active=False, complete=False):
            # Connect to database
            conn = sqlite3.connect(self.task_dir)
            # Create cursor
            c = conn.cursor()
            # Update the task into the database
            c.execute("""UPDATE Task SET
                category        = :category,
                title           = :title,
                task            = :task,
                deadline_day    = :deadline_day,
                deadline_month  = :deadline_month,
                deadline_year   = :deadline_year,
                active          = :active,
                complete        = :complete
                
                WHERE oid = :oid""",
                      {
                          'category': category,
                          'title': title,
                          'task': task,
                          'deadline_day': deadline_day,
                          'deadline_month': deadline_month,
                          'deadline_year': deadline_year,
                          'active': active,
                          'complete': complete,

                          'oid': oid
                      })
            # commit changes
            conn.commit()

            # Close connection
            conn.close()

        def delete_task(self, oid):
            # Connect to database
            conn = sqlite3.connect(self.task_dir)
            # Create cursor
            c = conn.cursor()
            # Delete a record
            # oid is the ID of the data usually 1,2,3,4,5...
            c.execute("DELETE from Task WHERE oid = " + str(oid))

            # commit changes
            conn.commit()

            # Close connection
            conn.close()

    class Template:
        def __init__(self, name):
            self.template_dir = TimetableDataManagement().main_dir + "\\templates\\" + name + ".db"
            self.create_template_database_init()

        def create_template_database_init(self):
            new = not os.path.isfile(self.template_dir)

            # connect a database
            conn = sqlite3.connect(self.template_dir)
            c = conn.cursor()

            if new:
                c.execute("""CREATE TABLE Template(
                    Name text,
                    CMD text,
                    planned_date blob,
                    start_time blob,
                    short_break integer,
                    long_break integer,
                    sleep_duration real,
                    work_duration real,
                    lunch_duration real,
                    dinner_duration real,
                    self_care real,
                    self_development real,
                    social_duration real
                    )""")
                print("##CREATED NEW DATABASE FOR TEMPLATE##")
            # commit changes
            conn.commit()
            # Close connection
            conn.close()

        def submit_new_template(self, Name=None, CMD=None, planned_date=None, start_time=None,
                                short_break=None, long_break=None, sleep_duration=None,
                                work_duration=None, lunch_duration=None, dinner_duration=None,
                                self_care=None, self_development=None, social_duration=None):
            # Create a database or connect to one
            conn = sqlite3.connect(self.template_dir)
            # Create cursor
            c = conn.cursor()

            c.execute(
                "INSERT INTO Template VALUES(:Name,:CMD, :planned_date, :start_time, :short_break, :long_break, "
                ":sleep_duration,:work_duration,:lunch_duration,:dinner_duration,"
                ":self_care,:self_development,:social_duration)",
                {
                    "Name": Name,
                    "CMD": CMD,
                    "planned_date": planned_date,
                    "start_time": start_time,
                    "short_break": short_break,
                    "long_break": long_break,
                    "sleep_duration": sleep_duration,
                    "work_duration": work_duration,
                    "lunch_duration": lunch_duration,
                    "dinner_duration": dinner_duration,
                    "self_care": self_care,
                    "self_development": self_development,
                    "social_duration": social_duration
                })
            # commit changes
            conn.commit()

            # Close connection
            conn.close()

        def query_template(self):
            conn = sqlite3.connect(self.template_dir)
            # Create cursor
            c = conn.cursor()

            # Query database
            c.execute("SELECT oid,* FROM Template")
            data = c.fetchall()

            # commit changes
            conn.commit()

            # Close connection
            conn.close()
            return data

        # Editing the specific task
        def update_template(self, oid=None, Name=None, CMD=None, planned_date=None, start_time=None,
                            short_break=None, long_break=None, sleep_duration=None,
                            work_duration=None, lunch_duration=None, dinner_duration=None,
                            self_care=None, self_development=None, social_duration=None):
            # Connect to database
            conn = sqlite3.connect(self.template_dir)
            # Create cursor
            c = conn.cursor()
            # Update the task into the database
            c.execute("""UPDATE addresses SET
                Name = :Name,
                CMD = :CMD,
                planned_date=:planned_date,
                start_time=:start_time,
                short_break=:short_break,
                long_break=:long_break,
                sleep_duration=:sleep_duration,
                work_duration=:work_duration,
                lunch_duration=:lunch_duration,
                dinner_duration=:dinner_duration,
                self_care=:self_care,
                self_development=:self_development,
                social_duration=:social_duration

                WHERE oid = :oid""",
                      {
                          "Name": Name,
                          "CMD": CMD,
                          "planned_date": planned_date,
                          "start_time": start_time,
                          "short_break": short_break,
                          "long_break": long_break,
                          "sleep_duration": sleep_duration,
                          "work_duration": work_duration,
                          "lunch_duration": lunch_duration,
                          "dinner_duration": dinner_duration,
                          "self_care": self_care,
                          "self_development": self_development,
                          "social_duration": social_duration,

                          'oid': oid
                      })
            # commit changes
            conn.commit()

            # Close connection
            conn.close()

    class TemplateV2:
        def __init__(self, name=None):

            if name is not None:
                self.template_dir = TimetableDataManagement().main_dir + "\\templatesV2\\" + name + ".db"
                self.create_template_database_init()

            self.template_folder_dir = TimetableDataManagement().main_dir + "\\templatesV2"
            if not os.path.exists(self.template_folder_dir):
                os.mkdir(self.template_folder_dir)

        def available_templates(self):
            current_dir = os.getcwd()
            os.chdir(self.template_folder_dir)
            list = glob.glob("*.db")
            os.chdir(current_dir)
            return list

        def create_template_database_init(self):

            new = not os.path.isfile(self.template_dir)

            # connect a database
            conn = sqlite3.connect(self.template_dir)
            c = conn.cursor()

            if new:
                c.execute("""CREATE TABLE Template(
                    StartTime blob,
                    EndTime blob,
                    item text
                    )""")
                print("##CREATED NEW DATABASE FOR TEMPLATE##")
            # commit changes
            conn.commit()
            # Close connection
            conn.close()

        def submit_data(self, StartTime=None, EndTime=None, item=None):
            # Create a database or connect to one
            conn = sqlite3.connect(self.template_dir)
            # Create cursor
            c = conn.cursor()

            c.execute(
                "INSERT INTO Template VALUES(:StartTime,:EndTime, :item)",
                {
                    "StartTime": StartTime,
                    "EndTime": EndTime,
                    "item": item
                })
            # commit changes
            conn.commit()

            # Close connection
            conn.close()

        def query_template(self,filepath = None):
            if filepath is not None:
                conn = sqlite3.connect(filepath)
            else:
                conn = sqlite3.connect(self.template_dir)
            # Create cursor
            c = conn.cursor()

            # Query database
            c.execute("SELECT * FROM Template")
            data = c.fetchall()

            # commit changes
            conn.commit()

            # Close connection
            conn.close()
            return data

        # Editing the specific task
        def update_template(self, oid=None, StartTime=None, EndTime=None, item=None):
            # Connect to database
            conn = sqlite3.connect(self.template_dir)
            # Create cursor
            c = conn.cursor()
            # Update the task into the database
            c.execute("""UPDATE Template SET
                StartTime = :StartTime,
                EndTime = :EndTime,
                item=:item

                WHERE oid = :oid""",
                      {
                          "StartTime": StartTime,
                          "EndTime": EndTime,
                          "item": item,
                          'oid': oid
                      })
            # commit changes
            conn.commit()

            # Close connection
            conn.close()


if __name__ == '__main__':
    import numpy as np

    x = TimetableDataManagement().Task('task')
    y = TimetableDataManagement().Template('Default')
    x.submit_new_task("Work", "IDT", "Meeting", 7, 6, 2021)
    x.submit_new_task("Work", "Research", "Drone control system", 7, 6, 2021)
    x.submit_new_task("Self-care", "Cooking", "Learn new thai recipe", 7, 6, 2021)
    x.submit_new_task("Self-care", "Exercise", "Push UP", 7, 6, 2021)
    x.submit_new_task("Self-development", "Coding course", "Java tutorial", 7, 6, 2021)
    x.submit_new_task("Self-development", "Drawing", "Ipad drawing tutorial", 7, 6, 2021)
    x.submit_new_task("Self-development", "Coding course", "C++ tutorial", 7, 6, 2021)
    Name0 = "Default2"
    CMD0 = "010327478"
    planned_date0 = "2020 - 12 - 14"
    start_time0 = "08:45:00"
    short_break0 = 6.0
    long_break0 = 12.0
    sleep_hour0 = 8.0
    work_hour0 = 7.0
    lunch_hour0 = 1.0
    dinner_hour0 = 2.0
    self_care0 = 1.0
    self_development_hour0 = 2.0
    social_hour0 = 0.0

    # y.submit_new_template(Name0,CMD0, planned_date0, start_time0, short_break0, long_break0, sleep_hour0,
    #                       work_hour0, lunch_hour0, dinner_hour0,
    #                       self_care0, self_development_hour0, social_hour0)

    # NOTE!!!
    # if the data is put into the numpy it convert all the data into string
    print(type(x.query_task()[0][-1]))
    print(np.array(x.query_task()))
    print(y.query_template())
    # os.remove(x.task_dir)
    # os.remove(y.template_dir)
