#import các modules cần thiết
import socket
import threading
from colorama import Fore, Back, Style
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox


DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
FONT=("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)
WHITE = 'white'
BUTTON_FONT = ("Helvetica", 15)


#tạo một object socket 
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def add_mess(mess):
    mess_box.config(state=tk.NORMAL)
    mess_box.insert(tk.END, mess + '\n')
    mess_box.config(state=tk.DISABLED)


def connect():
    #kết nối đến server
    try:

        client.connect((HOST,PORT))
        print(f"Kết nối thành công đến máy chủ ")
        add_mess("[SERVER] Đã kết nối thành công đến máy chủ")
    except:
        messagebox.showerror("Thông báo", f"Khum thể kết nối đến máy chủ {HOST} {PORT}")
        
    username = name_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Thông báo", Fore.GREEN + "Tên không được nhập trống!!")
    
    threading.Thread(target=listen_from_sv,args=(client, )).start()

    name_textbox.config(state=tk.DISABLED)
    name_button.config(state=tk.DISABLED)
    
def send_mess():
    message = message_textbox.get()
    
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Thông báo","Tin nhắn trống")

        exit(0)




root = tk.Tk()
root.geometry("600x700")
root.title("Messenger Client")
root.resizable(False,False)


root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=4)
root.grid_rowconfigure(2,weight=1)

topframe = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
topframe.grid(row=0,column=0,sticky=tk.NSEW)


midframe = tk.Frame(root, width=600, height=400, bg= MEDIUM_GREY)
midframe.grid(row=1,column=0,sticky=tk.NSEW)


botframe = tk.Frame(root, width=600, height=100, bg= DARK_GREY)
botframe.grid(row=2,column=0,sticky=tk.NSEW)


name_label = tk.Label(topframe, text="Nhập tên người dùng: ", font=FONT, bg= DARK_GREY, fg=WHITE)
name_label.pack(side=tk.LEFT, padx = 10)

name_textbox = tk.Entry(topframe,font=FONT,bg=MEDIUM_GREY,fg=WHITE,width=21)
name_textbox.pack(side=tk.LEFT)

name_button = tk.Button(topframe, text="Join" , font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,command=connect)
name_button.pack(side=tk.LEFT, padx = 15)

message_textbox = tk.Entry(botframe,font=FONT,bg=MEDIUM_GREY,fg=WHITE,width=38)
message_textbox.pack(side=tk.LEFT, padx = 10)

message_button = tk.Button(botframe,text="Send" , font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,command=send_mess )

message_button.pack(side=tk.LEFT, padx = 10)

mess_box = scrolledtext.ScrolledText(midframe, font = SMALL_FONT,bg=MEDIUM_GREY,fg=WHITE,width=67,height = 30)
mess_box.config(state=tk.DISABLED)
mess_box.pack(side=tk.TOP)




HOST = '127.0.0.1'
PORT = 1234


def listen_from_sv(client):
    while 1:
        message = client.recv(2024).decode('utf-8')
        if message != '':
            username = message.split("@")[0]
            content = message.split('@')[1]
            add_mess(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Thông báo","Tin nhắn từ client trống")

def main():
    root.mainloop()


if __name__ == '__main__':
    main()