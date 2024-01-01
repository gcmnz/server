import socket
import threading
import json
import sys


class Server:
    def __init__(self, host='127.0.0.1', port=12345):
        self.HOST = host
        self.PORT = port
        self.__starting = False
        self.user, self.addr = None, None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

    def start(self):
        print('Server started')
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        self.__starting = True
        self.on_connect_listener()

    def stop(self):
        self.__starting = False
        self.server.close()

    def on_connect_listener(self):
        while self.__starting:
            self.user, self.addr = self.server.accept()
            thread = threading.Thread(target=self.user_messaging)
            thread.start()

    def user_messaging(self):
        print(f'{self.addr} Successfully connected!')
        while True:
            msg = self.user.recv(1024).decode('utf-8')
            if len(msg) == 0:
                print(f'{self.addr} Disconnected!')
                break
            type_, login, password = msg.split('\t')
            if type_ == 'LOGIN':
                result = self.check_login(login=login, password=password)
            elif type_ == 'REGISTER':
                result = self.check_authorization(login=login, password=password)
            else:
                result = 0
            self.send_message(result)

    def send_message(self, message):
        self.user.send(message.encode('utf-8'))

    @staticmethod
    def check_login(login, password) -> str:
        with open('base.json', 'r') as f:
            authorized_users = json.load(f)
            if login in authorized_users:
                if password == authorized_users[login]:
                    return 'Success'
                else:
                    return 'Invalid password'
            else:
                return 'Invalid login'

    @staticmethod
    def check_authorization(login, password) -> str:
        with open('base.json', 'r') as f:
            authorized_users = json.load(f)
        if login in authorized_users:
            return 'Login already signed up'
        else:
            with open('base.json', 'w') as f:
                authorized_users[login] = password
                json.dump(authorized_users, f, indent=2)
            return 'Success'



if __name__ == '__main__':
    server = Server('127.0.0.1', 12345)
    server.start()
