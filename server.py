import socket
import threading
from datetime import datetime
import json

HOST = '127.0.0.1'
PORT = 8085
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server đang lắng nghe trên {HOST}:{PORT}...")

client_list = []
message_list = []

# 
# Định nghĩa class Message
# #
class Message:
    def __init__(self, client, addr, content):
        self.client = client
        self.addr = addr
        self.time = datetime.now().strftime("%H:%M:%S")
        self.content = content
    
    # Hàm convert sang json
    def to_dict(self):
        return {
            "time": self.time,
            "ip": self.addr[0],
            "port": self.addr[1],
            "content": self.content
        }

def handle_client(client, addr):
    global client_list
    global message_list
    
    print("Đã kết nối với:", addr)
    
    # Gửi toàn bộ message_list tới client
    for message in message_list:
        client.send((json.dumps(message) + "\n").encode())

    # #
    # Xử lý nhận data từ client
    # @param            data: dữ liệu mà client gửi cho server
    # #
    while(True):
        data = client.recv(1024)
        if not data:
            print(f"Client {addr} đã đóng kết nối")
            break

        raw_message = data.decode()
        message = Message(client, addr, raw_message)
        message_json = json.dumps(message.to_dict())
        message_list.append(message.to_dict())
        
        # Gửi tin nhắn cho tất cả user còn lại
        for client_online in client_list:
            client_online.send((message_json + "\n").encode())
    
    client.close()
    if client in client_list:
        client_list.remove(client)
    print(f"Số lượng client hoạt động: {len(client_list)}")

# #
# Sever chấp nhận kết nối từ 1 client
# @param socket     client: socket riêng của client
# @param (ip, port) addr: địa chỉ của client
# #
while(True):
    client, addr = server.accept()

    client_list.append(client)
    print(f"Số lượng client hoạt động: {len(client_list)}")    
    
    thread = threading.Thread(target=handle_client, args=(client, addr))
    thread.start()
