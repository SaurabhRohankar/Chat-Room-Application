import socket
import threading

s = socket.socket()
ip_ad = socket.gethostbyname(socket.gethostname())
port = 5679
s.bind((ip_ad, port))
s.listen(5)
print(f"[+] SERVER is Listening at {ip_ad}:{port}...")

all_connections = []
nicknames = []

def broadcast(msg):
    for conn in all_connections:
        conn.send(msg)


def new_connection():
    while True:
        try:
            c, addr = s.accept()
            print("[+] New Connection with ", addr)
            all_connections.append(c)

            c.send('nickname'.encode())
            nickname = c.recv(1024).decode()
            nicknames.append(nickname)

            print(nickname, "joined the chat")
            broadcast(f"{nickname} joined the chat room!".encode())
            c.send("Welcome to the Chatroom!".encode())

            thread = threading.Thread(target=handle_client, args=(c,)) #starting thread for each client
            thread.start()

        except Exception as e:
            print("Error occured while connecting: ", e)


def handle_client(conn):
    while True:
        try:
            msg = conn.recv(5000) #not decoding bcoz sending it as it is encoded to other clients where it is decoded
            broadcast(msg)

        except:
            index = all_connections.index(conn)
            all_connections.remove(conn)
            conn.close()

            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!')
            nicknames.remove(nickname)
  
new_connection()