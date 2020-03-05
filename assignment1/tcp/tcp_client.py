import socket
import time
import sys


TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"

def send(id=0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    #s.send(f"{id}:{MESSAGE}".encode())
    s.send(f"Connected Client:{id}.".encode())
    data = s.recv(BUFFER_SIZE)
    for _ in range(int(sys.argv[3])):
        print(f"Sending data:{MESSAGE}", flush=True)
        s.send(f"Received data:{id}:{MESSAGE}".encode())
        data = s.recv(BUFFER_SIZE)
        print("Received data:", data.decode(), flush=True)
        time.sleep(int(sys.argv[2]))

    s.close()


def get_client_id():
    id = sys.argv[1]
    return id

send(get_client_id())
