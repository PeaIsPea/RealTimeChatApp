#import các modules cần thiết
import socket
import threading
from colorama import Fore, Back, Style
HOST = '127.0.0.1'
PORT = 1234


def listen_from_sv(client):
    while 1:
        message = client.recv(2024).decode('utf-8')
        if message != '':
            username = message.split("@")[0]
            content = message.split('@')[1]
            print(f"[{username}] {content}")
        else:
            print("Tin nhắn từ client trống")

def send_message_to_sv(client):
    while 1:
        message = input("Nội dung : ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("Tin nhắn trống")

            exit(0)


def giaotiep_to_server(client):
    username = input("Nhập username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print(Fore.GREEN + "Tên không được nhập trống!!")
        exit(0)


    threading.Thread(target=listen_from_sv,args=(client, )).start()

    send_message_to_sv(client)



def main():
    #tạo một object socket 
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #kết nối đến server
    try:

        client.connect((HOST,PORT))
        print(f"Kết nối thành công đến máy chủ ")
    except:
        print(f"Khum thể kết nối đến máy chủ {HOST} {PORT}")

    giaotiep_to_server(client)


if __name__ == '__main__':
    main()