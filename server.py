import socket
import threading
# from datetime import datetime
import json


class Server:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
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
            thread = threading.Thread(target=self.user_connect)
            thread.start()

    def user_connect(self):
        print(f'{self.addr} Successfully connected!')

        self.send_message('Зарегистрироваться[0]\nВойти[1]\n')
        reg_or_login = self.user.recv(512).decode('utf-8')

        if reg_or_login == '0':
            self.register()
        elif reg_or_login == '1':
            self.login()
        else:
            self.send_message('Неверное значение\n')

    def login(self):
        self.send_message('Введите логин -> ')
        login = self.user.recv(64).decode('utf-8')
        self.send_message('Введите пароль -> ')
        password = self.user.recv(64).decode('utf-8')
        with open('authorized.json', 'r') as f:
            authorized_users = json.load(f)
            if login in authorized_users:
                if password == authorized_users[login]:
                    self.send_message('Вы успешно зашли в аккаунт')
                else:
                    self.send_message('Неверный пароль')
            else:
                self.send_message('Аккаунта не существует')

    def register(self):
        self.send_message('Введите желаемый логин -> ')
        login = self.user.recv(64).decode('utf-8')

        with open('authorized.json', 'r') as f:
            authorized_users = json.load(f)

        if login in authorized_users:
            self.send_message('Этот аккаунт уже существует')
        else:
            self.send_message('Введите желаемый пароль -> ')
            password = self.user.recv(64).decode('utf-8')

            with open('authorized.json', 'w') as f:
                authorized_users[login] = password
                json.dump(authorized_users, f, indent=2)

            self.send_message('Аккаунт успешно создан!')

    def send_message(self, message):
        self.user.send(message.encode('utf-8'))


if __name__ == '__main__':
    import time


    def abc():
        print('function!')


    x = 0
    point = 5
    for _ in range(5):
        while x < point:
            x += 1
            time.sleep(1)
            print(x)
        point += 5
        abc()
        print(point)
        print(x)
