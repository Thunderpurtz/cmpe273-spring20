import socket
import threading
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
all_connections = []
all_addresses = []

def listen_forever():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    while True:
        s.listen(1)
        conn, addr = s.accept()
        all_connections.append(conn)
        all_addresses.append(addr)

def process_clients():
    while True:
        for idx, conn in enumerate(all_connections):
            data = conn.recv(BUFFER_SIZE)
            if not data:
                conn.close()
                del all_connections[idx]
                del all_addresses[idx]
                continue
            print(f"{data.decode()}", flush=True)
            conn.send("pong".encode())
        if len(all_connections) < 1:
            break


#thread to handle listening and to put connections in an array
print(f"Server started at port {TCP_PORT}.")
sys.stdout.flush()
t1 = threading.Thread(target=listen_forever)
t1.daemon = True
t1.start()
while True:
    if len(all_connections) > 0:
        process_clients()
