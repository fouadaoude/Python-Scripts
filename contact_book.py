import http.server
import socketserver
import threading
import os

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler
server = socketserver.TCPServer(("", PORT), Handler)

def start_server():
    print("Starting server port: ",PORT)
    thread = threading.Thread(target=server.serve_forever())
    thread.daemon = True
    thread.start()    

def stop_server():
    server.shutdown()

def xContact():
    pass

def login():
    pass

def register():
    pass

def greet():
    clearInput()
    account = input("Welcome to X Contact!\n[1] Login\n[2] Register\n")

def clearInput():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

start_server()