import socket
import sys
import concurrent.futures


all_connections = []
all_address = []
run=True
# Create a Socket ( connect two computers)

def create_socket():
    try:
        global host
        global port
        global s
        host = "165.22.214.8"
        port = 9999
        s = socket.socket()
        print("create_socket")
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections

def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

def accepting_connections():
	global run
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_address[:]
	while run:
		try:
			
			conn, address = s.accept()
			s.setblocking(1)  # prevents timeout
			all_connections.append(conn)
			all_address.append(address)
			print(f"{len(all_address)})Connection has been established :{address[0]}")

			#print(f"total conection{len(all_address)}")
		except:

			print("Error accepting connections")

# Establish connection with a client (socket must be listening)

def conversation():
	global	run
	print("conversation thread started")
	while run:
		if len(all_connections)>=2:
			# print(len(all_connections))
			all_connections[0].setblocking(False)
			all_connections[1].setblocking(False)
			try:	
				data =all_connections[0].recv(1024)
				# print(f"data receved {all_address[0]} to {all_address[1]}  and data is :{data} ")
				if str(data,"utf-8")=="quit":
					print("ecoing quit")
					all_connections[1].sendall(data)
					all_connections[0].sendall(b"quit")
					print("All conections are removed")
					
					for c in all_connections:
						c.close()
					del all_connections[:]
					del all_address[:]

				elif str(data,"utf-8")=="exit":
					print("quiting")
					for c in all_connections:
						c.close()
					all_connections[0].sendall(b"quit")
					all_connections[1].sendall(b"quit")
					run=False
					s.close()
					break
				else:
					all_connections[1].sendall(data)
				continue
			except:
				pass

			try:
				data = all_connections[1].recv(1024)
				if str(data,"utf-8")=="quit":
					print("ecoing quit")
					all_connections[0].sendall(data)
					all_connections[1].sendall(b"quit")
					print("All conections are removed")
					for c in all_connections:
						c.close()
					del all_connections[:]
					del all_address[:]

				elif str(data,"utf-8")=="exit":
					print("quiting")
					for c in all_connections:
						c.close()
					all_connections[0].sendall(b"quit")
					all_connections[1].sendall(b"quit")
					run=False		
					s.close()			
					break
				else:
					all_connections[0].sendall(data)
				continue
			except:
				pass


def console():
	global s,all_address,all_connections,run
	print("console started")
	while run:
		print("Con>>",end="")
		comand=input()
		if comand=="quit":
			run=False
			s.close()
		elif comand=="list":
			print(f"Total no of connections:{len(all_address)}")
			for i,add in enumerate(all_address):
				print(f"{i+1}){add}")
		elif comand=="clear":
			for c in all_connections:
				c.close()
			del all_connections[:]
			del all_address[:]

			

def main():
	create_socket()
	print("creat_socket")
	bind_socket()
	print("bind")
	with concurrent.futures.ThreadPoolExecutor() as executor:
		f1=executor.submit(conversation)
		f3=executor.submit(console)
		f2=executor.submit(accepting_connections)
		


	print("ending")

main()