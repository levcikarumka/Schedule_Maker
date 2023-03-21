import socket
import threading
import time
import os
import sqlite3
import shutil
#from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime

class Server:
    IP = "0.0.0.0"
    PORT = 5050
    ADDR = (IP, PORT)
    SERVER = ()
    SIZE = 4096
    FORMAT = "utf-8"
    
    CLIENTS = []
    FINISH = False

    def main(self):
        db_conn = sqlite3.connect('Server.db')
        self.create_db(db_conn)
        db_conn.execute(f'UPDATE Users SET clientId = NULL')
        db_conn.commit()
        db_conn.close()

        print("\nStarting server...")   

        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.bind(self.ADDR)
        self.SERVER.listen()
        

        print(f"Listening: {self.IP}:{self.PORT}")
        create_thread(self.new_client_thread)

        while not self.FINISH:
            time.sleep(10)
        
        print("Server closed.")

    def new_client_thread(self):
        while True:
            conn, addr = self.SERVER.accept()
            ip = addr[0]
            client = Client(ip, conn)
            self.CLIENTS.append(client)
            client_id = self.CLIENTS.index(client)

            print(f"\n{client_id}. New msgs connection: {addr} connected.")
            create_thread(self.handle_msgs_thread, (client_id,))

    def handle_msgs_thread(self, client_id):
        client = self.CLIENTS[client_id]
        conn = client.conn_msgs
        exit = False
        while not exit:
            msg = conn.recv(self.SIZE).decode(self.FORMAT, errors= 'ignore')
            print(msg)
            db_conn = sqlite3.connect('Server.db')
            msg_list = msg.split("|")
            for msg in msg_list:
                if msg:
                    if msg == "exit": # when the app is closed
                        exit = True
                        break
                    
                    elif msg[:3] == "reg": # when client registers a new account
                        msg = msg[4:]
                        username = msg.split()[0]
                        password = msg.split()[1]
                        password_rep = msg.split()[2]
                        temp = db_conn.execute(f'SELECT `password` FROM `Users` WHERE `username` = "{username}"').fetchone() 
                        if password != password_rep:
                            self.send(conn, "Passwords do not match.")
                        elif temp:
                            self.send(conn, "This username has already been used.")
                        else:
                            db_conn.execute(f'INSERT INTO `Users` (`username`, `password`) VALUES("{username}", "{password}")')
                            db_conn.commit()
                            client = self.CLIENTS[client_id]
                            self.send(conn, "online")
                            print(f"{client_id}. Successefuly registered: username - {username}, password - {password}.")

                    elif msg[:5] == "login": # when user login
                        msg = msg[6:]
                        username = msg.split()[0]
                        password = msg.split()[1]
                       # hashed_password = db_conn.execute(f'SELECT password FROM Users WHERE username = "{username}"').fetchone()
                        passwordd = db_conn.execute(f'SELECT `password` FROM `Users` WHERE `username` = "{username}"').fetchone() 
                        if not passwordd:
                            self.send(conn, "There is no user with such login and password.")
                            print(f"{client_id}. There is no user with login - {username}.")
                        elif str(passwordd[0]) != str(password):
                            self.send(conn, "There is no user with such login and password.")
                            print(f"{client_id}. The password - {password} for user with login - {username} is wrong.")
                        else: 
                            self.send(conn, "online")
                            print(f'{client_id}. Logged in.')

                    elif msg[:6] == "create": # when client registers a new account
                        msg = msg[7:]
                        title = msg.split()[0]
                        password = msg.split()[1]
                        password_rep = msg.split()[2]
                        temp = db_conn.execute(f'SELECT `password` FROM `Schedules` WHERE `title` = "{title}"').fetchone() 
                        if password != password_rep:
                            self.send(conn, "Passwords do not match.")
                        elif temp:
                            self.send(conn, "This title has already been used.")
                        else:
                            db_conn.execute(f'INSERT INTO `Schedules` (`title`, `password`) VALUES("{title}", "{password}")')
                            db_conn.execute(f'INSERT INTO `Permissions` (`guestUsername`, `scheduleTitle`) VALUES("{username}", "{title}")')
                            db_conn.commit()
                            client = self.CLIENTS[client_id]
                            self.send(conn, "online")
                            print(f"{client_id}. Successefuly registered: title - {title}, password - {password}.")
                    
                    elif msg[:9] == "sch_login": # when user login
                        msg = msg[10:]
                        title = msg.split()[0]
                        password = msg.split()[1]
                       # hashed_password = db_conn.execute(f'SELECT password FROM Users WHERE username = "{username}"').fetchone()
                        passwordd = db_conn.execute(f'SELECT `password` FROM `Schedules` WHERE `title` = "{title}"').fetchone() 
                        if not passwordd:
                            self.send(conn, "There is no schedule with such title and password.")
                            print(f"{client_id}. There is no schedule with title - {title}.")
                        elif str(passwordd[0]) != str(password):
                            self.send(conn, "There is no schedule with such title and password.")
                            print(f"{client_id}. The password - {password} for schedule with title - {title} is wrong.")
                        else: 
                            if username not in str(db_conn.execute(f'SELECT `guestUsername` FROM `Permissions` WHERE `scheduleTitle` = "{title}"').fetchall()):
                                db_conn.execute(f'INSERT INTO `Permissions` (`guestUsername`, `scheduleTitle`) VALUES("{username}", "{title}")')
                                db_conn.commit()
                            self.send(conn, "online")
                            print(f'{client_id}. Logged in.')
                            print(db_conn.execute(f'SELECT `guestUsername` FROM `Permissions` WHERE `scheduleTitle` = "{title}"').fetchall() )

#str(db_conn.execute(f'SELECT `title` FROM `Schedules` WHERE `password` = "{f}"').fetchall())
                       
#достать из бд хэш пароль. Использоывть Асобенный функиця. сравнить. 

   
    def send(self, conn, msg):
        conn.send(msg.encode(self.FORMAT, errors= 'ignore'))

    def create_db(self, db_conn):
        db_conn.execute('''CREATE TABLE IF NOT EXISTS Users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT ,
            username STRING NOT NULL ,
            password STRING NOT NULL ,
            clientId INTEGER)''')
        db_conn.execute('''CREATE TABLE IF NOT EXISTS Schedules (
            scheduleId INTEGER PRIMARY KEY AUTOINCREMENT ,
            title STRING NOT NULL ,
            password STRING NOT NULL)''')
        db_conn.execute('''CREATE TABLE IF NOT EXISTS Permissions (
            PermissionsId INTEGER PRIMARY KEY AUTOINCREMENT ,
            guestUsername STRING NOT NULL,
            scheduleTitle STRING NOT NULL)''')

def create_thread(thread_function, args=(), daemon_state='True', name_extra='', start='True'):
    new_thread = threading.Thread(target=thread_function, args=args)
    new_thread.daemon = daemon_state
    if not name_extra:
        new_thread.name = thread_function.__name__
    else:
        new_thread.name = thread_function.__name__ + " " + name_extra
    if start:
        new_thread.start()
    return new_thread



class Client:
    def __init__(self, ip, conn_msgs, online=False):
        self.ip = ip
        self.conn_msgs = conn_msgs
        self.online = online

    def info(self):
        print(f"ip: {self.ip}")
        print(f"conn_msgs: {self.conn_msgs}") 

        print(f"online: {self.online}") 

if __name__ == "__main__":
    Server().main()