#import các modules cần thiết
import socket
import threading
from colorama import Fore, Back, Style

HOST = '127.0.0.1'
PORT = 1234 #có thể sử dụng bất kỳ cổng nào trong khoảng từ 0 to 65535
LISTENER_LIMIT = 5

ds_clients = []  #list này liệt kê tất cả tên người dùng đang kết nối

#Hàm để nghe bất cứ tin nhắn nào sắp tới
def listen_for_mess(client,username):
    while 1:
        message = client.recv(2024).decode('utf-8')
        if message != '':
            final_msg = username + '@' + message
            send_mess(final_msg)

        else:
            print(f"Tin nhắn từ {username} đó bị trống")



#Hàm gửi tin nhắn đến 1 client
def send_mess_to_client(client, message):
    client.sendall(message.encode())



#hàm này gửi tin nhắn đến mọi máy client hiện đang kết nối với server
def send_mess(message):
    for user in ds_clients:
        send_mess_to_client(user[1],message )





#hàm xử lý client
def client_handle(client):
    #máy chủ sẽ lắng nghe tin nhắn từ client với tên người dùng
    while 1:
        username = client.recv(2024).decode('utf-8') 
        if username != '':
            ds_clients.append((username,client))
            promt_message = "SERVER@" + f"{username} đã được thêm vào đoạn chat" 
            send_mess(promt_message)
            break

        else:
            print("Tên client bị trống!!")

        
    threading.Thread(target=listen_for_mess,args=(client,username, )).start()

#hàm chính nè
def main():

    #creating the socket class object
    #socket.AF_INET nghĩa là chúng ta sửa dụng IPv4 addresses
    #SOCK_STREAM nghĩa là sử dụng các gói TCP để giao tiếp
    sv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    

    #Kiểm tra định dạng
    try:
        #cung cấp cho máy chủ một địa chỉ in the form of # host IP and Port
        sv.bind((HOST,PORT))
        print(f"Máy chủ đang hoạt động trên {HOST} {PORT}")
    except:
        print(f"Khum thể kết nối đến {HOST} và cổng {PORT}")
    #đặt giới hạn máy chủ
    sv.listen(LISTENER_LIMIT)

    #Vòng lặp sẽ tiếp tục lắng nghe các kết nối từ máy client
    while 1:
        client, address = sv.accept()
        print(Fore.RED + f"Kết nối thành công đến Client {address[0]} {address[1]}")

        threading.Thread(target=client_handle, args=(client, )).start()
    

if __name__ == '__main__':
    main()