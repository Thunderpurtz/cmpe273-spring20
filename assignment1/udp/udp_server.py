"""
Implement a simple acknowledgement protocol that you assign unique sequence id for each package you send to the server.
Once the package is received by the server, the server will send acknowledgement back to the client.
In case of package lost, the client did not receive the acknowledgement back from the server,
the client must resend the same package again until you get the acknowledgement.
To control the package order, the client will never send the next package until it gets the acknowledegement for the previous one.
"""

import socket


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "acknowledgment"
RESEND = "resend"
clients = {}

def get_client_id(s):
	count = 0
	idx = s.find(":")
	return s[0:idx]

def get_packet(s):
	idx = s.find(":")
	return get_client_id(s[idx+1:])

def get_data(s):
	colon = s.find(":")
	s = s[colon+1:]
	colon = s.find(":")
	return (s[colon+1:])


def listen_forever():
	print("Server started at port 4000.")
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("", UDP_PORT))
	s.settimeout(2.5)
	timeouts = 0
	while True:
		try:
			data, ip = s.recvfrom(BUFFER_SIZE)
			stripped = data.decode(encoding="utf-8").strip()
			client_id = get_client_id(stripped)
			packet = get_packet(stripped)
			ack_num = client_id + ":" + packet
			if stripped[-6:] == "Finish":
				print("Upload successfully completed.", flush=True)
				del clients[client_id]
			#first time client connects
			elif client_id not in clients:
				print("Accepting a file upload...", flush=True)
				clients[client_id] = [get_data(stripped)] #implicitly packet 0
				s.sendto(f"Received ack({ack_num}) from the server.".encode(), ip)

			elif int(get_packet(stripped)) == len(clients[client_id]):
				clients[client_id].append(get_data(stripped))
				s.sendto(f"Received ack({ack_num}) from the server.".encode(), ip)
			else: #packet sent was out of order, resend the requested packet
				print("resend", flush=True)
				s.sendto(RESEND.encode(), ip)
		except (socket.timeout, socket.error) as e:
			timeouts += 1
			if timeouts == 25:
				print("timeout limit exceeded, no more clients connecting, exiting", flush=True)
				exit()




listen_forever()



#string id format:

#clientid:packet#:data

#only handles one client sending information to it in its lifetime
# def listen_forever():
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	s.bind(("", UDP_PORT))
# 	s.settimeout(2.5)
# 	timeouts = 0
# 	integrity = 0 #this is the parity check for packet loss
# 	while True:
# 		try:
# 			# get the data sent to us
# 			data, ip = s.recvfrom(BUFFER_SIZE)
# 			# strip data
# 			stripped = data.decode(encoding="utf-8").strip()
# 			# parse out line number
# 			check = stripped[0:parse_string(stripped)]

# 			if int(check) == integrity + 1:
# 				# reply back to the client
# 				s.sendto(MESSAGE.encode(), ip)
# 				timeouts = 0
# 				integrity += 1
# 			else:
# 				s.sendto(RESEND.encode(), ip)
# 		except (socket.timeout, socket.error, Exception) as e:
# 			timeouts += 1
# 			if timeouts == 7:
# 				print("timeout limit exceeded, no more clients connecting, exiting")
# 				exit()
# 			print(str(e))
