import socket
import threading
import time

HEADER = 64
MESSAGE_LENGTH = 2048 
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print("[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(MESSAGE_LENGTH)
        if len(msg) != 0:
            # mgs_length = int(mgs_length)
            #msg = conn.recv(MESSAGE_LENGTH)
            print(f"[{addr}] {msg}")
            conn.send(msg)
        else:
            print("[STOP CONNECTION] {addr} stopped.")
            connected = False

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()
