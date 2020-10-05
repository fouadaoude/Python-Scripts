from datetime import datetime, timedelta
from email.mime.text import MIMEText
import csv
import pandas as pd
import smtplib
import schedule
import time

class Stack:
    def __init__(self, name):
        self.size = 0
        self.top_item = None
        self.limit = 1000
        self.name = name

    def push(self, value):
        pass

    def pop(self):
        if self.size > 0:
            item_to_remove = self.top_item
            self.top_item = item_to_remove.get_next_node()
            self.size -= 1
            return item_to_remove.get_value() 
        print("This stack is totally empty.")

    def peek(self):
        if self.size > 0:
            return self.top_item.get_value()
        print("Nothing to see here")
    
    def has_space(self):
        return self.limit > self.size
    
    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

class Email:
    def __init__(self):
        self.day_of_week = None
        self.col_lst = ["Time", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "WeekOf"]
        self.schedule_data = {}
        self.schedule_data_string = ""
        self.schedule_data_time_string = ""
        self.schedule_items_string = ""

    def send_email(self, schedule):
        title = 'Get To Work!'
        msg_content = """
            <html>
                <head></head>
                    <body>
                        <h2>{title}</h2>
                        <h3>{day}</h3>                        
                        <p>                        
                            {schedule}
                        </p>                        

                    </body
            </html>                                            
                      """.format(title=title, day=self.day_of_week, schedule=self.schedule_data_string)
        msg = MIMEText(msg_content, 'html')

        msg['From'] = 'Sender Name <email>'
        msg['To'] = 'Receiver Name <email>'
        msg['Subject'] = 'Get To Work'

        msg_full = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login('username', 'password')
        server.sendmail('sender', 'receiver', msg_full)
        server.quit()
    
    def send_email_daily(self):
        schedule.every().day.at("07:00").do(self.send_email, self.schedule_data)

        while True:
            schedule.run_pending()
            time.sleep(1)
        

    def get_to_do_schedule(self):
        try:
            df = pd.read_csv("weekly_schedule.csv", usecols=self.col_lst)
            day = self.get_weekday()       
            time = df['Time']
            schedule = df[day]

            all_times = []
            all_schedule = []            

            for item in time:
                all_times.append(item) 
                self.schedule_data_time_string += str(item)                                                
            for item in schedule:
                all_schedule.append(item)   
            for i in range(len(all_times)):
                self.schedule_data[all_times[i]] = all_schedule[i]                
            for key, value in self.schedule_data.items():
                self.schedule_data_string += str(key) + ' ' + str(value) + '<br><hr style="float:left;width:20%"><br>'
            print(self.schedule_data_string)
        except KeyError:
            print("Error")

    def append_data_to_csv(self, data):
        try:
            df = pd.read_csv('weekly_schedule.csv')
            new_col = pd.DataFrame([self.get_date_for_first_day_of_week()])
            df = df.merge(new_col, left_index=True, right_index=True)
            df.to_csv('weekly_schedule.csv', index=False)
        except KeyError:
            print("Ran into an oopsie")
    
    def get_date_for_first_day_of_week(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        return str(start_of_week)

    def get_whole_week_schedule(self):
        df = pd.read_csv("weekly_schedule.csv", usecols=self.col_lst)
        df.to_csv("weekly_schedule.csv", index=False)
        for weekday in self.col_lst:
            print(df[weekday])   
        

    def get_time_of_schedule(self):
        pass
        #df = pd.read_csv("weekly_schedule.csv", usecols=self.col_lst)
        #print(df)

    def get_weekday(self):
        self.day_of_week = str(datetime.today().strftime('%A')) 
        return str(datetime.today().strftime('%A'))
        
email = Email()
email.get_to_do_schedule()
email.send_email(email.schedule_data)
#email.get_whole_week_schedule()
email.send_email_daily()