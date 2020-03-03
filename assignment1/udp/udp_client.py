import socket
import time


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "ping"


upload = []
with open("upload.txt", "r") as up:
    for line in up:
        upload.append(line)

def send(id=0):
    socket_timeouts = 0
    retry = 0 #attempts to send data
    resend = 0 #attempts to send data without packet loss

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2.5)
    packet = 0
    while True:
        try:
            print("packet in try=", packet)
            #s.sendto(f"{id}:{MESSAGE}".encode(), (UDP_IP, UDP_PORT))
            s.sendto(f"{id}:{packet}:{upload[0]}".encode(), (UDP_IP, UDP_PORT))
            print("sent data")
            data, ip = s.recvfrom(BUFFER_SIZE)

            #didnt receive an acknowledgment
            if not data:
                retry += 1
                if retry == 5:
                    print("Server not responding after repeated attempts. Exiting client...")
                    exit()
                continue
            elif data.decode(encoding="utf-8)").strip() == "resend":
                resend += 1
                if resend == 10:
                    print("max attempts to send data without packet loss reached, exiting")
                    exit()
            else: #acknowledge
                print("acknowledge")
                del upload[0]
                packet += 1
                print("packet in loop=", packet)
                if len(upload) == 0:
                    print("Finished sending.")
                    exit()
            print("received data: {}: {}".format(ip, data.decode()))
        except socket.timeout: #general socket timeout
            print("Socket time out, server didn't respond in time.")
            socket_timeouts += 1
            if socket_timeouts == 3:
                print("Socket time out limit reached, server didn't respond in time.")
                exit()
            continue
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()



def get_client_id():
    id = input("Enter client id:")
    return id

send(get_client_id())
