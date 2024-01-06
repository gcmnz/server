import socket
import threading
import json
import database
from dataclasses import dataclass


class Server:

    def __init__(self, host='127.0.0.1', port=12345):
        self.HOST = host
        self.PORT = port
        self.__starting = False
        self.user, self.addr = None, None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        self.__database = database.Database('database.db')

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
        user = User(ip=self.addr[0], port=self.addr[1])

        while True:
            msg = self.user.recv(1024).decode('utf-8')

            if len(msg) == 0:  # Выход пользователя
                if len(user.login):  # Если пользователь был авторизован
                    self.__database.update_query('Accounts', 'online_status', 'login', user.login, '0')

                print(f'{self.addr}   login:{user.login}    Disconnected!')
                break

            msg = msg.split('\t')
            type_, message, _, _ = msg
            if type_ == 'LOGIN':
                result = self.check_login(user=user, login=msg[1], password=msg[2], node=msg[3])
            elif type_ == 'REGISTER':
                result = self.check_authorization(user=user, login=msg[1], password=msg[2], node=msg[3])
            elif type_ == 'MESSAGE_SEND':
                result = self.user_message_send(user=msg[1], message=msg[2])
            else:
                result = 'error'

            self.send_message(result)

    def send_message(self, message):
        self.user.send(message.encode('utf-8'))

    def check_login(self, user, login, password, node) -> str:
        valid_login = self.__database.check('Accounts', {'login': login})
        valid_password = self.__database.check('Accounts', {'password': password})
        valid_node = self.__database.check('Accounts', {'node': node})
        valid_online_status = self.__database.check('Accounts', {'online_status': 0})

        if not valid_login:
            return 'Invalid login'
        elif not valid_password:
            return 'Invalid password'
        elif not valid_online_status:
            return 'The account is currently in use'
        elif not valid_node:
            return 'Invalid node'
        else:
            user.login = login
            user.password = password

            self.__database.update_query('Accounts', 'ip', 'login', login, self.addr[0])
            self.__database.update_query('Accounts', 'port', 'login', login, self.addr[1])
            self.__database.update_query('Accounts', 'online_status', 'login', login, '1')
            return 'Success'

    def check_authorization(self, user, login, password, node) -> str:
        login_exists = self.__database.check('Accounts', {'login': login})

        if login_exists:
            return 'Login already exists'
        else:

            user.login = login
            user.password = password

            self.__database.insert_to('Accounts', {'login': login, 'password': password, 'node': node,
                                                   'ip': self.addr[0], 'port': self.addr[1], 'online_status': '1'})
            return 'Success'

    @staticmethod
    def user_message_send(user, message) -> str:
        with open('base.json', 'r') as f:
            authorized_users = json.load(f)
            if user in authorized_users:
                pass

        return str(user in authorized_users)


@dataclass
class User:
    """
    Класс для хранения данных о подключившемся пользователе
    """
    login = ''
    password = ''
    ip: str
    port: int


if __name__ == '__main__':
    server = Server('127.0.0.1', 12345)
    server.start()
