import socket

HOST = "192.168.1.68"
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

running = True

while running:
    msg = input()
    client.send(msg.encode('utf-8'))
    if msg == 'exit':
        running = False

client.close()
