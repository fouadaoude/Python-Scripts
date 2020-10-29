import http.server
import socketserver
import threading
import os
import time
import sys
import mysql.connector
from prettytable import PrettyTable
import stdiomask

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler
server = socketserver.TCPServer(("", PORT), Handler)

class XContact:

    def __init__(self):
        self.userInfo = {}
        self.cleanedUserInfo = ""        
        self.contacts = {}


    def connect_db_animation(self, load_str=None, load_speed=None, clear=True, stop=False):   
        if clear:
            self.clear_input() 
        
        if load_str == None:
            load_str = 'Connecting'
        
        if load_speed == None:
            load_speed = 0.07

        while True:
            dots = '...'
            
            for letter in load_str:
                sys.stdout.write(letter)
                sys.stdout.flush()
                #sys.stdout.write('\b')
                time.sleep(load_speed)
            
            for dot in dots:
                sys.stdout.write(dot)
                sys.stdout.flush()
                time.sleep(load_speed)
            
            if clear == True:
                self.clear_input()    
            break

    def connect_mysql(self, prnt=True, load_str=None):
        self.clear_input()
        
        while True:

            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="contact_book"
                )
                
                if load_str:
                    self.connect_db_animation(load_str, 0.06)            
                
                if prnt:
                    self.connect_db_animation(load_str)            
                    print('Connected To Database...')
                return db 

            except mysql.connector.Error as err:
                print("Something went wrong {}".format(err))
                print('Re-attempting to connect. Make sure to turn on MySQL Database.')
                self.connect_db_animation(False)
                self.clear_input()
                continue

    def start_server(self):
        print("Starting server port: ",PORT)
        os.system()
        thread = threading.Thread(target=server.serve_forever())
        thread.daemon = True
        thread.start()    

    def stop_server(self):
        server.shutdown()

    def select_all_query(self, username=None, password=None):
        if username != None and password != None:

            try:
                stmt = ("SELECT * FROM users WHERE username='{}' and password='{}'".format(username, password))                
                db = self.connect_mysql(False)
                cursor = db.cursor()
                cursor.execute(stmt)
                result = cursor.fetchall()
                
                if result:
                    self.connect_db_animation(load_str = "Gathering users info")
                    return result

            except mysql.connector.Error as err:
                print("Either username or password is incorrect. {}".format(err))
    
    def xContact(self):        
        
        logged_in = False            

        while True:
            
            if logged_in:                        
                self.user_interface()
            
            option = self.greet()                        
            
            if int(option) == 3:
                exit(0)

            elif int(option) == 1:
                try:
                    user = self.login()  

                    if user:
                        logged_in = True                                     

                        for value in user:                    
                            self.userInfo = {'userID': value[0], 'username': value[1], 'password': value[2], 'email': value[3]}                    

                except mysql.connector.Error as err:
                    print("Cannot login {}".format(err))                
                        

            elif int(option) == 2:
                logged_in = self.register()   
                if logged_in:
                    logged_in = True
                continue         
    

    def user_interface(self):
            while True:

                self.clear_input()

                try:
                    print("[1] View Contacts\n[2] Add New Contact\n[3] Log Out\n")
                    option = input("")                                
                except ValueError:
                    print("Invalid option")
                
                if int(option) == 1:
                    try:                    
                        self.get_contacts()                    
                        print("\n[1] Update")
                        print("\n[0] Back") 
                        option = input("")  

                        if int(option) == 1:
                            #update or delete row
                            id = input("Please Enter the ID of the contact you would like to change: ")
                            contact = self.get_contact_by_id(id)
                            self.update_contact(contact, id)                              

                        elif int(option) == 0:
                            continue

                    except ValueError:
                        print("No Contacts You Loser")                                                

                elif int(option) == 2:
                    self.add_contact()

                elif int(option) == 3:
                    self.xContact()                      

    def get_contact_by_id(self, id=None):
        if id:
            lst = []
            
            try:
                db = self.connect_mysql(False)
                cursor = db.cursor()
                stmt = ("SELECT firstname, lastname, phone, email, address, birthday FROM contacts WHERE ID = {}".format(id))
                cursor.execute(stmt)
                contact = cursor.fetchall()
                
                for value in contact:
                    lst.append(value)
                return lst

            except mysql.connector.Error as err:
                print("Something went wrong getting contact by id {}".format(err))

    def get_contacts(self):
        if self.userInfo:
            try:
                stmt = ("SELECT * FROM contacts WHERE userID = {}".format(self.userInfo['userID']))
                load_str = "Collecting All Contacts"
                db = self.connect_mysql(False, load_str)
                cursor = db.cursor()
                cursor.execute(stmt)
                result = cursor.fetchall()                
                
                self.clean_contacts(result)            

                table = PrettyTable(["ID", "Name", "Phone", "Email", "Address", "Birthday"], align="l")                            
                for key, inside_key in self.contacts.items():          
                    values = list(inside_key.values())                    
                    table.add_row([key, values[0], values[1], values[2], values[3], values[4]])                                    
                print(table)                

            except mysql.connector.Error as err:
                print("Something went wrong collecting contacts {}".format(err))

    def update_contact(self, update_contact, id):        
        dict = self.add_contact(update_contact)
        
        values = []

        if dict:            
            
            for value in dict.values():
                values.append(str(value))
        
        if values:
            try:
                db = self.connect_mysql(False)
                cursor = db.cursor()
                stmt = ("UPDATE contacts SET firstname = %s, lastname = %s, phone = %s, email = %s, address = %s, birthday = %s WHERE ID = %s")
                val = (values[0], values[1], values[2], values[3], values[4], values[5], id)
                cursor.execute(stmt, val)
                db.commit()
            except mysql.connector.Error as err:
                print("Something went wrong updating the contact {}".format(err))
                time.sleep(8)

    def add_contact(self, update_contact=None):
        self.clear_input()
        done = False
        entered_input = False
        new_contact = {}                        

        if update_contact:
            firstname_input = ["[1] First Name", ' [' + str(update_contact[0][0]) + ']']        
            lastname_input = ["[2] Last Name", ' [' + str(update_contact[0][1]) + ']']        
            phone_input = ["[3] Phone Number", ' [' + update_contact[0][2] + ']']
            email_input = ["[4] Email", ' [' + update_contact[0][3] + ']']        
            address_input = ["[5] Address", ' [' + update_contact[0][4] + ']']
            birthday_input = ["[6] Birthday", ' [' + update_contact[0][5] + ']']
            new_contact['firstname'] = update_contact[0][0].title()
            new_contact['lastname'] = update_contact[0][1].title()
            new_contact['phone'] = update_contact[0][2].title()
            new_contact['email'] = update_contact[0][3].title()
            new_contact['address'] = update_contact[0][4].title()
            new_contact['birthday'] = update_contact[0][5].title()
        else:
            firstname_input = ["[1] First Name"]        
            lastname_input = ["[2] Last Name"]        
            phone_input = ["[3] Phone Number"]
            email_input = ["[4] Email"]        
            address_input = ["[5] Address"]
            birthday_input = ["[6] Birthday"]                

        while done == False:
            try:
                self.clear_input()
                print(''.join(firstname_input))
                print(''.join(lastname_input))
                print(''.join(phone_input))
                print(''.join(email_input))
                print(''.join(address_input))
                print(''.join(birthday_input))
                option = input("")

                '''
                Needs work to update every 
                '''

                if entered_input:
                    print("[0] Save Changes")                          

                if option == "1":                                          
                    firstname = input("Enter First Name: ")
                    new_contact['firstname'] = firstname.upper()   
                    if len(firstname_input) > 1:
                        firstname_input.pop(1)                                                                           
                    firstname_input.append( ' [' + firstname.upper() + ']')                      

                elif option == "2":
                    lastname = input("Enter Last Name: ")
                    new_contact['lastname'] = lastname.upper()                    
                    if len(lastname_input) > 1:
                        lastname_input.pop(1) 
                    lastname_input.append( ' [' + lastname.upper() + ']')
                elif option == "3":
                    phone = input("Enter Phone Number: ")
                    new_contact['phone'] = phone                    
                    if len(phone_input) > 1:
                        phone_input.pop(1) 
                    phone_input.append( ' [' + phone + ']')
                elif option == "4":
                    email = input("Enter Email: ")
                    new_contact['email'] = email
                    if len(email_input) > 1:
                        email_input.pop(1) 
                    email_input.append( ' [' + email + ']')
                elif option == "5":
                    address = input("Enter Address: ")
                    new_contact['address'] = address                                 
                    if len(address_input) > 1:
                        address_input.pop(1) 
                    address_input.append( ' [' + address + ']')                           
                elif option == "6":
                    birthday = input("Enter Birthday: ")
                    new_contact['birthday'] = birthday  
                    if len(birthday_input) > 1:
                        birthday_input.pop(1) 
                    birthday_input.append( ' [' + birthday + ']')                                          
                elif option == "0":
                    reset = input("Would you like to change any options? [y/n] ")
                    if reset == "y" or reset == "Y":                        
                        continue              
                    elif reset.lower() == "n":
                        if update_contact:
                            return new_contact   
                        else:                     
                            self.insert_into_db(new_contact)                    
                    break
                else:
                    print("Invalid option")
            except ValueError:
                print("IDK")        
                        
    def insert_into_db(self, dict=None, new_user=None):
        if dict:

            values = []    
            for value in dict.values():
                values.append(str(value))                       

        if dict and new_user:
            try:
                db = self.connect_mysql(False, load_str="Saving user into database")
                cursor = db.cursor()
                stmt = ("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)")
                val = [values[0], values[1], values[2]]
                cursor.execute(stmt, val)
                db.commit()
                return True
            except mysql.connector.Error as err:
                print("Something went wrong in registration. Please try again. {}".format(err))

        elif dict:                    
            if len(values) != 6:                
                
                for i in range(0, 6):
                    values.append("")
                    if len(values) == 6:
                        break                                
                
            userID = self.userInfo['userID']            

            try:
                db = self.connect_mysql(False, load_str="Adding contact into database")
                cursor = db.cursor()
                stmt = ("INSERT INTO contacts (userID, firstname, lastname, phone, email, address, birthday) VALUES (%s, %s, %s, %s, %s, %s, %s)")
                val = [userID, values[0], values[1], values[2], values[3], values[4], values[5]]
                cursor.execute(stmt, val)
                db.commit()                
            except mysql.connector.Error as err:
                print("Error inputting values into database {}".format(err))        
                
    def log_out(self):
        pass

    def clean_contacts(self, contacts):
        self.usersDBheadings = []
        for heading in self.userInfo.keys():
            self.usersDBheadings.append(heading)

        count = 0         
        for contact in contacts:                        
            name = str(contact[2]).title() + ' ' + str(contact[3]).title()             
            
            count += 1            
            self.contacts[count] = {'Name': name, 
                                    'Phone': contact[4],
                                    'Email': contact[5],
                                    'Address': contact[6],
                                    'Birthday': contact[7]}                                                                                                                                                                                                                              

    def login(self):
        self.clear_input()
        
        while True:
            
            try:                            
                username = input('Enter Username: ')                
                password = stdiomask.getpass(prompt='Password: ', mask='*')
                userInfo = self.select_all_query(username, password)                
                
                if userInfo:
                    return userInfo
                else:
                    self.clear_input()
                    print("Either username or password is incorrect\n")                    
                    continue

            except mysql.connector.Error as err:
                print("Either username or password is incorrect. Error: {}".format(err))
                continue

    def register(self):                
        user_info = {}

        while True:
            self.clear_input() 

            try:                
                username = input("Enter a username: ")
                email = input("Enter your email: ")
                password = stdiomask.getpass(prompt='Enter a password: ', mask='*')
                repeat_password = stdiomask.getpass(prompt='Re-enter password: ', mask='*')
                user_info['username'] = username
                user_info['password'] = password
                user_info['email'] = email                

                if password == repeat_password and username and email:                    
                    logged_in = self.insert_into_db(user_info, new_user=True)
                    return logged_in                    
                else:
                    continue

            except ValueError:
                print("Something went wrong. Please try again.")    

    def greet(self):
        self.clear_input()
        option = input("Welcome to X Contact!\n[1] Login\n[2] Register\n[3] Exit\n")
        return int(option)

    def clear_input(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

user = XContact()
user.xContact()