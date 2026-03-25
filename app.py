
import streamlit as st
import socket
import threading
import json
import queue
import time
from streamlit_autorefresh import st_autorefresh


# =========================
# AUTO REFRESH UI sử dụng st_autorefresh
# =========================
st_autorefresh(interval=1000, key="autorefresh")

# =========================
# GLOBAL STATE
# =========================
HOST = '127.0.0.1'
PORT = 8085

if "initialized" not in st.session_state:
    st.session_state.initialized = True

    # socket
    st.session_state.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    st.session_state.client_socket.connect((HOST, PORT))

    # data
    st.session_state.messages = []
    st.session_state.running = True
    st.session_state.msg_queue = queue.Queue()

# =========================
# THREAD NHẬN DATA
# =========================
def receive(client_socket, msg_queue):
    buffer = ""
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            continue
        buffer += data
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            if not line.strip():
                continue
            msg = json.loads(line)
            formatted = f"[{msg['time']}] {msg['ip']}:{msg['port']}: {msg['content']}"
            msg_queue.put(formatted)

def send_message():
    msg = st.session_state.input.strip()

    if msg:
        st.session_state.client_socket.send((msg + "\n").encode())

    st.session_state.input = ""

# =========================
# START THREAD 1 LẦN
# =========================
if "thread_started" not in st.session_state:
    thread = threading.Thread(
        target=receive,
        args=(st.session_state.client_socket, st.session_state.msg_queue),
        daemon=True
    )
    thread.start()
    st.session_state.thread_started = True

# =========================
# UI
# =========================
st.title(":material/chat_bubble: Chat Client")


# Lấy tin nhắn mới từ queue và thêm vào messages
while not st.session_state.msg_queue.empty():
    new_msg = st.session_state.msg_queue.get()
    st.session_state.messages.append(new_msg)

# Chat History
for msg in st.session_state.messages:
    st.markdown(f"💬 {msg}")

# Send message
col1, col2 = st.columns([4, 1])
user_input = col1.text_input("Nhập tin nhắn", key="input", label_visibility="collapsed")
col2.button("Gửi", on_click=send_message)