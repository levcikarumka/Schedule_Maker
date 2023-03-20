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
    PORT = 8000
    ADDR = (IP, PORT)
    SERVER = ()
    SIZE = 4096
    FORMAT = "utf-8"
    
    CLIENTS = []
    FINISH = False

    def main(self):
        db_conn = sqlite3.connect('Server.db')
        self.create_db(db_conn)
        db_conn.execute(f'UPDATE Users SET clientId = NULL, openedFilePath = NULL')
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
                    elif msg[:5] == "login": # when user login
                        msg = msg[6:]
                        login = msg.split()[0]
                        password = msg.split()[1]
                        self.send(conn, "online")
#Есть ли юзер с этим логом на серве. достать из бд хэш пароль. Использоывть Асобенный функиця. сравнить. 

   
    def send(self, conn, msg):
        conn.send(msg.encode(self.FORMAT, errors= 'ignore'))

    def create_db(self, db_conn):
        db_conn.execute('''CREATE TABLE IF NOT EXISTS Users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT ,
            login STRING NOT NULL ,
            password STRING NOT NULL ,
            clientId INTEGER ,
            openedFilePath STRING ,
            regTime STRING NOT NULL ,
            lastLogInTime STRING )''')
        db_conn.execute('''CREATE TABLE IF NOT EXISTS Schedule (
            creatorId INTEGER NOT NULL ,
            guestId INTEGER NOT NULL ,
            path STRING NOT NULL ,
            FOREIGN KEY (creatorId) REFERENCES Users (userId) ,
            FOREIGN KEY (guestId) REFERENCES Users (userId) )''')

            

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