from datetime import datetime, timedelta
from email.mime.text import MIMEText
import csv
import pandas as pd
import smtplib
import schedule
import time

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

                    </body>
            </html>                                            
                      """.format(title=title, day=self.get_weekday(), schedule=self.get_to_do_schedule())
        msg = MIMEText(msg_content, 'html')

        msg['From'] = 'Sender Name <EMAIL>'
        msg['To'] = 'Receiver Name <EMAIL>'
        msg['Subject'] = 'Get To Work'

        msg_full = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login('EMAIL', 'PASSWORD')
        server.sendmail('SENDER', 'RECEIVER', msg_full)
        server.quit()
    
    def send_email_daily(self):
        schedule.every().day.at("07:00").do(self.send_email, self.schedule_data)
        print("Email set to go out at 7AM")

        while True:
            schedule.run_pending()
            time.sleep(1)
        

    def get_to_do_schedule(self):
        self.schedule_data_string = ""
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
        except KeyError:
            print("Error")
        return self.schedule_data_string

    def append_data_to_csv(self, data):
        try:
            df = pd.read_csv('weekly_schedule.csv')
            new_col = pd.DataFrame([self.get_date_for_first_day_of_week()])
            df = df.merge(new_col, left_index=True, right_index=True)
            df.to_csv('weekly_schedule.csv', index=False)
        except KeyError:
            print("Something fucked up")
    
    def get_date_for_first_day_of_week(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        return str(start_of_week)

    def get_whole_week_schedule(self):
        df = pd.read_csv("weekly_schedule.csv", usecols=self.col_lst)
        df.to_csv("weekly_schedule.csv", index=False)
        for weekday in self.col_lst:
            print(df[weekday])   

    def get_weekday(self):
        self.day_of_week = str(datetime.today().strftime('%A')) 
        return str(datetime.today().strftime('%A'))
        
email = Email()
email.get_to_do_schedule()
email.send_email(email.schedule_data)
email.send_email_daily()
