import socket
import threading

client_socket = socket.socket()
ip_ad = input("Please enternter IP address of server: ")
port = int(input("Please enter port number of server: "))

nickname = input("Please enter your nickname: ")

#creating socket with server ip
client_socket.connect((ip_ad, port))


def receive_msg():
    while True:
        try:
            msg = client_socket.recv(4096).decode()
            if msg == 'nickname':
                client_socket.send(nickname.encode())
            else:
                print(msg)
        except:
            print("An error occurred")
            client_socket.close()
            break


def send_msg():
    while True:
        message = f"{nickname}: {input('')}"
        client_socket.send(message.encode())


rec_thread = threading.Thread(target=receive_msg)
rec_thread.start()

send_thread = threading.Thread(target=send_msg)
send_thread.start()



