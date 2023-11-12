import socket

HOST = "192.168.1.68"
PORT = 65432


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

while True:
    user, addr = server.accept()
    print(user, addr)
    while True:
        data = user.recv(1024).decode('utf-8')
        print(data)
        if data == 'exit':
            break


