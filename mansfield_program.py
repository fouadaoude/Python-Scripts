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
        
    except mysql.connector.Error as e:
        print("Something went wrong {}".format(e))

    return db

def get_weekday():
        today = date.today()
        return calendar.day_name[today.weekday()]

def get_date():
    return date.today()


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
                    selected_user = employee_info[option-1]                    
                    print("[1] Current time")
                    print("[2] Custom time")
                    print('[0] Update checkin for today')
                    time = input("Select: ")
                    if int(time) == 0:                        
                        self.update_check_in(selected_user, time=self.get_current_datetime())
                        break
                    elif int(time) == 1:   
                        is_inserted, attendanceID = self.check_if_already_inserted(selected_user)
                        if is_inserted and attendanceID:
                            self.update_check_in(selected_user)
                            break
                        input_time = self.get_current_datetime()
                        self.insert_check_in(input_time, selected_user)
                        break
                    elif int(time) == 2:                        
                        is_inserted, attendanceID = self.check_if_already_inserted(selected_user)       
                        if is_inserted and attendanceID:
                            self.update_check_in(selected_user)
                            break
                        self.insert_check_in(input_time, selected_user)
                        break
                    else:
                        print("Invalid option. Try again\n")

                    print(input_time)                                                            
                    break                
        except ValueError:
            print("Something went wrong checking in employee")    

    def get_attendance(self, selected_user):
        if selected_user:
            userID = selected_user[0]
            try:
                db = connect()
                cursor = db.cursor()
                stmt = ("SELECT * FROM attendance WHERE userID = '{userID}'".format(userID=userID))
                cursor.execute(stmt)
                attendance = cursor.fetchall()
                return attendance
            except mysql.connector.Error as e:  
                print("Something went wrong getting attendance from database ERROR: {}".format(e))
            
    def check_if_already_inserted(self, selected_user):
        attendance = self.get_attendance(selected_user)
        #get attendance and check if todays date has already been inserted
        if attendance:
            todays_date = get_date()
            for today in attendance:            
                if today[4] in today:
                    print("inhere", today[4])
                    return True, today[0]
                else:
                    return False
                
                     
    def format_time(self, time=None):
        if time:
            return str(get_weekday()) + ' ' + time + ' ' + str(get_date())
        else:
            return str(get_weekday()) + ' ' + str(self.get_current_datetime())


    def update_check_in(self, selected_user, time=None):        
        if selected_user:
            is_inserted, attendanceID = self.check_if_already_inserted(selected_user)                
            if is_inserted and attendanceID:
                print("Would you like to update checkin time for today?")
                option = input("Y/N\n")
                if option.lower() in ['y','yes']: 
                    while True:
                        clear()
                        print("[1] Current time")
                        print("[2] Custom time")
                        option = input("")                        
                        if int(option) == 2:
                            print("Enter custom time for {employee}".format(employee=selected_user[1]))
                            time = input("")                    
                            formatted_time = self.format_time(time)
                            print("Change todays check in for {employee} to {format_time}?".format(employee=selected_user[1], format_time=formatted_time))
                            option = input("")
                            if option.lower() in ['y', 'yes']:
                                break
                            else:
                                self.manager_view()                                        
                        elif int(option) == 1:         
                            time = self.get_current_datetime()        
                            formatted_time = self.format_time()
                            print(formatted_time)
                            break     
        else:
            self.manager_view()                                   

        if not self.check_if_already_inserted(selected_user):                
            userID = selected_user[0] if selected_user[0] else 0
            firstname = selected_user[1] if len(selected_user[1]) > 0 else "Empty"
            lastname = selected_user[2] if len(selected_user[2]) > 0 else "Empty"
            checkin = formatted_time
            checkout = "Pending"                   
                    
            try:
                db = connect()
                cursor = db.cursor()
                stmt = ("UPDATE attendance SET checkin = '{time}' WHERE userID='{userID}' AND attendanceID='{attendanceID}';".format(time=checkin, userID=userID,attendanceID=attendanceID))                                        
                cursor.execute(stmt)
                db.commit()
                clear()
                return print("Updated Successfully")

            except mysql.connector.Error as e:
                return print("Error updating checkin field {}".format(e))

    def insert_check_in(self, time, selected_user):
        is_inserted = self.check_if_already_inserted
        if is_inserted:            
            self.update_check_in(selected_user, time)        
        if selected_user and is_inserted == False:
            #check if there is a userid if there isnt set it to 0 and do not carry on the insertion into db
            userID = selected_user[0] if selected_user[0] else 0

            if userID != 0:
                firstname = selected_user[1] if len(selected_user[1]) > 0 else "Empty"
                lastname = selected_user[2] if len(selected_user[2]) > 0 else "Empty"
                checkin = get_weekday() + ' ' + time
                checkout = "Pending"
                try:
                    print(checkin)
                    db = connect()
                    cursor = db.cursor()
                    stmt = ("INSERT INTO attendance (userID, firstname, lastname, checkin, checkout) VALUES (%s, %s, %s, %s, %s)")
                    val = [userID, firstname, lastname, checkin, checkout]
                    cursor.execute(stmt, val)
                    db.commit()
                    return "Inserted check in time successfully"
                except mysql.connector.Error as e:                    
                    clear()
                    print("Error {}".format(e))                
            else:
                print("Missing userID please try again.")
                return
            clear()

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

