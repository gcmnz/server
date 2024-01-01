import socket
import threading


class Client:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_message = None
        self.__connection_status = False
        self.__thread = threading.Thread(target=self.__connection_thread, daemon=True)

    def connect(self):
        self.__thread.start()

    def __connection_thread(self):
        try:
            self.user.connect((self.HOST, self.PORT))
            self.__connection_status = True
        except ConnectionRefusedError:
            print('No connection')

    def disconnect(self):
        self.user.close()
        self.__connection_status = False

    def send_message(self, message):
        if self.__connection_status:
            self.user.send(message.encode('utf-8'))
            self.recv_message = self.user.recv(1024).decode('utf-8')
        else:
            print('client: no connection status')


if __name__ == '__main__':
    client = Client('192.168.1.68', 65432)
    client.connect()
