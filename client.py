import socket
import threading
from uuid import uuid1


class Client:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.NODE = uuid1().node
        self.recv_message = ''
        self.__connection_status = False
        self.__thread = threading.Thread(target=self.__connection_thread, daemon=True)

    def connect(self):
        self.__thread.start()

    def __connection_thread(self):
        while not self.__connection_status:
            try:
                self.user.connect((self.HOST, self.PORT))
                self.__connection_status = True
                self.recv_message = 'Connected successfull'
            except ConnectionRefusedError:
                self.recv_message = 'Waiting for connection...'

    def disconnect(self):
        self.user.close()
        self.__connection_status = False

    def is_connected(self):
        return self.__connection_status

    def send_message(self, message):
        if self.__connection_status:
            try:
                self.user.send(message.encode('utf-8'))
                self.recv_message = self.user.recv(1024).decode('utf-8')
            except ConnectionResetError:
                self.__connection_status = False
                print('Connection lost')


if __name__ == '__main__':
    client = Client('192.168.1.68', 65432)
    client.connect()
