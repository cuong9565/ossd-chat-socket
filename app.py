import streamlit as st
import socket
import threading
import json
import queue
from streamlit_autorefresh import st_autorefresh

# =========================
# CẤU HÌNH & REFRESH
# =========================
st.set_page_config(page_title="Socket Chat", page_icon="💬")
st_autorefresh(interval=1000, key="autorefresh")

HOST = '192.168.213.220' 
PORT = 8085

# =========================
# KHỞI TẠO SESSION STATE
# =========================
if "initialized" not in st.session_state:
    st.session_state.messages = []
    st.session_state.msg_queue = queue.Queue()
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        st.session_state.client_socket = client_socket
        st.session_state.initialized = True # Đánh dấu thành công
    except Exception as e:
        st.error(f" Không thể kết nối tới Server ({HOST}:{PORT}). Lỗi: {e}")
        st.stop() # Dừng app nếu không kết nối được

# =========================
# THREAD NHẬN DATA
# =========================
def receive_thread_func(sock, q):
    buffer = ""
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.strip():
                    msg_json = json.loads(line)
                    # Lưu tin nhắn theo định dạng đẹp hơn
                    formatted = f"[{msg_json['time']}] {msg_json['ip']}:{msg_json['port']} -> {msg_json['content']}"
                    q.put(formatted)
        except:
            break

# Chạy Thread nhận tin nhắn (chỉ chạy 1 lần duy nhất)
if "thread_started" not in st.session_state and st.session_state.get("initialized"):
    thread = threading.Thread(
        target=receive_thread_func,
        args=(st.session_state.client_socket, st.session_state.msg_queue),
        daemon=True
    )
    thread.start()
    st.session_state.thread_started = True

# =========================
# LOGIC XỬ LÝ TIN NHẮN
# =========================
def send_message():
    # Lấy dữ liệu từ widget có key="user_input"
    msg_text = st.session_state.user_input.strip()
    if msg_text:
        try:
            st.session_state.client_socket.send((msg_text + "\n").encode('utf-8'))
            st.session_state.user_input = "" # Xóa input sau khi gửi
        except Exception as e:
            st.error(f"Lỗi gửi tin nhắn: {e}")

# Lấy tin nhắn mới từ queue chuyển vào list messages
while not st.session_state.msg_queue.empty():
    st.session_state.messages.append(st.session_state.msg_queue.get())

# =========================
# GIAO DIỆN (UI)
# =========================
st.title(" Socket Chat Client")

# Hiển thị lịch sử chat
chat_container = st.container(height=400, border=True)
with chat_container:
    if not st.session_state.messages:
        st.info("Chưa có tin nhắn nào.")
    for msg in st.session_state.messages:
        st.write(msg)

    # Khu vực nhập tin nhắn
if prompt := st.chat_input("Nhập nội dung tin nhắn..."):
    try:
        st.session_state.client_socket.send((prompt + "\n").encode('utf-8'))
    except Exception as e:
        st.error(f"Lỗi gửi: {e}")
