import socket
import threading
import json
import os

HOST = '127.0.0.1'
PORT = 8086

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

#
# Thread nhận data
# #
def receive():
    buffer = ""

    while True:
        data = client.recv(1024).decode()
        if not data:
            break

        buffer += data

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)

            if line.strip() == "":
                continue

            msg = json.loads(line)

            print(f"[{msg['time']}] {msg['ip']}:{msg['port']}: {msg['content']}")

#
# Thread gửi data
# #
def send():
    while True:
        message = input()
        
        if message.strip() == "/bye":
            print("Đã thoát chat.")
            os._exit(0)
            break
        
        client.send((message + "\n").encode())

# 
# Cho 2 thread chạy song song
# #
threading.Thread(target=receive).start()
threading.Thread(target=send).start()