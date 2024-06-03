import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
lock = threading.Lock()

def broadcast(msg, sender):
    with lock:
        for client, name in clients.items():
            if client != sender:
                client.send(f"{name}: {msg}".encode(FORMAT))

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("Enter your name: ".encode(FORMAT))
    name = conn.recv(1024).decode(FORMAT)
    with lock:
        clients[conn] = name

    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        if msg:
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                broadcast(msg, conn)

    with lock:
        del clients[conn]
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
