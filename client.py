

import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.0.187"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
        except:
            print("An error occurred!")
            client.close()
            break

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

name = input("Digite seu nome: ")
client.send(name.encode(FORMAT))

print("Digite suas mensagens abaixo:")
while True:
    msg = input()
    send(msg)
    if msg == DISCONNECT_MESSAGE:
        break
