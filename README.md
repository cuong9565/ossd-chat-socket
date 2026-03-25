# Hướng dẫn chạy project

## 1. Setup

1. Clone project về máy:
```bash
git clone https://github.com/cuong9565/ossd-chat-socket.git
cd ossd-chat-socket
```
2. Chạy file run.sh
```bash
bash run.sh
```
## 2. Chạy chương trình

1. Chạy môi trường
```bash
source venv/bin/activate
```

2. Tạo 1 terminal chạy server.py
```bash
python3 server.py
```

3. Tạo 1 terminal chạy app.py
```bash
streamlit run app.py
```

4. Kết nối mạng
```bash
netsh interface portproxy add v4tov4 listenport=8085 listenaddress=0.0.0.0 connectport=8085 connectaddress=172.23.66.124
netsh advfirewall firewall add rule name="Open 8085" dir=in action=allow protocol=TCP localport=8085
```