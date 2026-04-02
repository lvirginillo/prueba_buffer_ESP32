import socket
import threading
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

HOST = '192.168.1.34'  # IP de tu ESP32
PORT = 1234
WINDOW_SIZE = 1000
data_buffer = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
lock = threading.Lock()

count = 0
last_time = time.time()

def tcp_receiver():
    global data_buffer, count, last_time
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    while True:
        try:
            raw = client.recv(2)  # 2 bytes = uint16_t
            if len(raw) < 2:
                continue
            value = int.from_bytes(raw, byteorder='little')
            with lock:
                data_buffer.append(value)
            count += 1
            if time.time() - last_time >= 1.0:
                print(f"Muestras por segundo: {count}")
                count = 0
                last_time = time.time()
        except Exception:
            continue

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 4096)
ax.set_xlim(0, WINDOW_SIZE)
ax.set_title("Lectura binaria en tiempo real - ESP32")
ax.set_xlabel("Muestras")
ax.set_ylabel("ADC")

def update(frame):
    with lock:
        y = list(data_buffer)
        x = np.arange(len(y))
        line.set_data(x, y)
    return line,

t = threading.Thread(target=tcp_receiver, daemon=True)
t.start()

ani = FuncAnimation(fig, update, interval=20, blit=True)
plt.show()