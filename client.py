import socket


'''running = True

while running:
    msg = input()
    client.send(msg.encode('utf-8'))
    if msg == 'exit':
        running = False
    elif msg == 'login':
        answer_login = client.recv(64).decode('utf-8')
        login = input(answer_login)
        client.send(login.encode('utf-8'))


client.close()'''


class Client:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.user.connect((self.HOST, self.PORT))
        reg_or_login = self.user.recv(512).decode('utf-8')
        choice = input(reg_or_login)
        while choice not in ['0', '1']:
            print('Неверное значение')
            choice = input(reg_or_login)

        self.send_message(choice)
        if choice == '1':
            self.login()
        elif choice == '0':
            self.register()

    def login(self):
        login = self.user.recv(512).decode('utf-8')
        self.send_message(input(login))
        password = self.user.recv(512).decode('utf-8')
        self.send_message(input(password))
        result = self.user.recv(512).decode('utf-8')
        print(result)

    def register(self):
        login = self.user.recv(512).decode('utf-8')
        self.send_message(input(login))
        password = self.user.recv(512).decode('utf-8')
        self.send_message(input(password))
        result = self.user.recv(512).decode('utf-8')
        print(result)

    def send_message(self, message):
        self.user.send(message.encode('utf-8'))


if __name__ == '__main__':
    client = Client('192.168.1.68', 65432)
    client.connect()
