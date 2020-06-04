import socket
import sys
import concurrent.futures
import threading
# import msvcrt

list_of_conn_active={}

all_connections = []
all_address = []

list_of_conn={}
crun=False
run=True
# Create a Socket ( connect two computers)

def create_socket():
    try:
        global host
        global port
        global s
        host = "192.168.0.6"
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
	
	for c in list_of_conn:
		list_of_conn[c]["conn"].close()

	
	list_of_conn.clear()
	details={"conn":None,
			 "add":None,	
			 "sendbuff":"",
			 "recevbuff":"",
			 "talk_to":"",
			 "conected":False,		
						}
	while run:
		try:
		
			conn, address = s.accept()
			s.setblocking(1)  # prevents timeout

			
			details["conn"]=conn
			details["add"]=address
			conn.setblocking(1)
			
			name=str(conn.recv(1024),"utf-8")
			details["talk_to"]=str(conn.recv(1024),"utf-8")

			if details["talk_to"] not in list_of_conn:
				#send them as we not found
				details["conn"].sendall(b"preson not online pls wait")

			list_of_conn.update({name:details})
			print(f"\nName ID:{name}    having ip:",details["add"],"   want to talk to ID:",details["talk_to"])
			
			details={"conn":None,
			 "add":None,	
			 "sendbuff":"",
			 "recevbuff":"",
			 "talk_to":"",
			 "conected":False,		
						}
			#print(f"total conection{len(all_address)}")
		except:

			print("Error accepting connections")

# Establish connection with a client (socket must be listening)

def m_executor():
	global list_of_conn,run,crun
	while run:
		
		try:
			for person in list_of_conn:	
			
				if (list_of_conn[person]["talk_to"] in list_of_conn) and (not list_of_conn[person]["conected"]):
					# print("conecting")
					list_of_conn[person]["conn"].sendall(b"connected")
					list_of_conn[person]["conected"]=True

				else:
					
					if list_of_conn[person]["sendbuff"] !="":
						# print("measseage conversion")
						if list_of_conn[person]["sendbuff"].decode("utf-8")=="quit":
							list_of_conn[list_of_conn[person]["talk_to"]]["recevbuff"]=list_of_conn[person]["sendbuff"]
							list_of_conn[person]["recevbuff"]=list_of_conn[person]["sendbuff"]
							list_of_conn[person]["sendbuff"]=""

						else:
							list_of_conn[list_of_conn[person]["talk_to"]]["recevbuff"]=list_of_conn[person]["sendbuff"]
							list_of_conn[person]["sendbuff"]=""
		except Exception as e :
			# print("exception:",e)
			pass
			
def console():
	global s,all_address,all_connections,run,list_of_conn,f1,f2,f3,f4,f5
	print("console started")
	while run:
		print("Con>>",end="")
		

		comand=input()
		if comand=="quit":
			try:
				for v in list_of_conn:
					
					list_of_conn[v]["conn"].sendall(b"quit")
			except:
				pass
			run=False	
			s.close()

		elif comand=="list":
			print(f"Total no of connections:{len(list_of_conn)}")
			for i,val in enumerate(list_of_conn):
				print(f"{i+1})ID-Name:{val}  having IP:",list_of_conn[val]["add"],"  want to talk to ID:",list_of_conn[val]["talk_to"],"  Connection :",list_of_conn[val]["conected"])


			for v in all_connections:
				print(v)

		elif comand=="clear":

			for c in list_of_conn:
				list_of_conn[c]["conn"].close()
			
			list_of_conn.clear()
		elif comand=="check":
			print("Active thread:",threading.active_count())
			print("Console thread Alive:",f1.running())
			print("Accepting_connections thread Alive:",f2.running())
			print("M_executor thread Alive:",f3.running())
			print("sending thread Alive:",f4.running())
			print("receving thread Alive:",f5.running())
				
def sending():
	while run:
		try:
			for person in list_of_conn:
				if list_of_conn[person]["conected"]:
					list_of_conn[person]["conn"].setblocking(False)
					try:
						list_of_conn[person]["sendbuff"]=list_of_conn[person]["conn"].recv(1024)
					except:
						pass
		except Exception as e :
			# print("exception:",e)
			pass
				
def receving():
	while run:
		try:
			for person in list_of_conn:
				if list_of_conn[person]["conected"] and list_of_conn[person]["recevbuff"]!="":
					list_of_conn[person]["conn"].setblocking(False)
					try:
						list_of_conn[person]["conn"].sendall(list_of_conn[person]["recevbuff"])
						list_of_conn[person]["recevbuff"]=""
					except:
						pass
		except Exception as e :
			# print("exception:",e)
			pass


def main():
	global f1,f2,f3,f4,f5
	create_socket()
	print("creat_socket")
	bind_socket()
	print("bind")
	with concurrent.futures.ThreadPoolExecutor() as executor:
		f2=executor.submit(accepting_connections)
		f3=executor.submit(m_executor)
		f4=executor.submit(sending)
		f5=executor.submit(receving)
		f1=executor.submit(console)


	print("ending")

main()