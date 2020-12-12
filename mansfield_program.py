from datetime import date
import time
import calendar
import mysql.connector
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mansfield"
        )
        print("connected successfully")
    except mysql.connector.Error as e:
        print("Something went wrong {}".format(e))

    return db


class Employee:    
    def manager_view(self):
        while True:
            try:
                print("[1] Add new employee")
                print("[2] Check in employee")
                print("[3] Check out employee")
                print("[4] Log job done")
                print("[5] Log parts for job")
                print("[6] Employee withdraw money")
                option = int(input("\nSelect: "))
                if option >= 1 and option <= 6:
                    if option == 1:
                        self.add_employee_view()  
                    elif option == 2:
                        self.check_in_view()                    
            except ValueError:
                print("Incorrect selection")

    def add_employee_view(self):        
        employee_array = []
        while True:
            try:
                employee_array.append(input("Enter employee first name: "))
                employee_array.append(input("Enter employee last name: "))
                employee_array.append(input("Enter employee phone number: "))
                employee_array.append(input("Enter employee email: "))
                employee_array.append(input("Enter employee job description: "))
                print(employee_array)
                if len(employee_array) > 2:
                    result = self.add_employee(employee_array) 
                    clear()                   
                    print(result)                    
                    break
            except ValueError:
                print("Something went wrong please try again")

    def check_in_view(self):
        employee_info = self.get_all_employees_info()
        clear()
        try:
            while True:
                for employee in employee_info:
                    print('[{id}] {employee}'.format(id=employee[0], employee=employee[1] + ' ' + employee[2]))
                option = int(input("Select: "))
                if isinstance(option, int):
                    print("[1] Current time")
                    print("[2] Custom time")
                    time = input("Select: ")
                    if time == "1":
                        time = self.get_current_datetime()
                    else:
                        time = input("Enter check in time for {employee}: ".format(employee=employee_info[option-1][1]))                        
                    print(time)
                    self.insert_check_in(time, userID)
                
        except ValueError:
            print("Something went wrong")

    def insert_check_in(self, time, employee_info):
        if (employee_info):
            userID = employee_info[option-1][0]
            try:
                db = connect()
                cursor = db.cursor()
                stmt = ("INSERT INTO attendance (userID, firstname, lastname, checkin, checkout) VALUES (%s, %s, %s, %s, %s)")
                val = (userID, )
            except ValueError:
                print('Something went wrong inserting into database')

    def get_current_datetime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def get_all_employees_info(self):
        try:
            db = connect()
            cursor = db.cursor()
            stmt = ("SELECT * FROM employees")
            cursor.execute(stmt)
            all_employees = cursor.fetchall()            
        except ValueError:
            print("Something went wrong getting users information")

        return all_employees if len(all_employees) > 1 else "Empty"

    def check_in(self, time):
        pass

    def get_today(self):
        today = date.today()
        return calendar.day_name[today.weekday()]

    def add_employee(self, employee_array):
        firstname = employee_array[0].title() if employee_array else "Empty"
        lastname = employee_array[1].title() if employee_array else "Empty"
        phone = employee_array[2] if employee_array else "Empty"
        email = employee_array[3] if employee_array else "Empty"
        job_description = employee_array[4] if employee_array else "Empty"

        try:
            db = connect()
            cursor = db.cursor()
            stmt = ("INSERT INTO employees (firstname, lastname, phone, email, job_description) VALUES (%s, %s, %s, %s, %s)")
            val = [firstname, lastname, phone, email, job_description]
            cursor.execute(stmt, val)
            db.commit()
            return "Added new employee successfully"
        except mysql.connector.Error as e:
            print("Something went wrong {}".format(e))

fouad = Employee()

fouad.manager_view()

