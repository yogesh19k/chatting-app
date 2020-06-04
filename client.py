#!/usr/bin/env python3
import socket
import concurrent.futures


HOST = '192.168.0.6'  # The server's hostname or IP address
PORT =  9999       # The port used by the server

run=True

def host_connect_and_bind():
    global HOST,PORT,s
    # Yourid=str.encode(input("Enter you ID:"))
    # Talk_to_id=str.encode(input("Enter the presons ID:"))

    try:
        s = socket.socket()
        print("socket created")

    except:
        print("socket creation problem")

    try:
        s.connect((HOST, PORT))
        s.sendall(str.encode(input("Enter you ID:")))
        s.sendall(str.encode(input("Enter the presons ID:")))
        print(f"connected to{HOST}")

    except:
        print("connecting problem")



def sending():
    global s,run,f1,f2
    print("You:>",end="")
    # print("sending thread strated")
    while run:
        # if msvcrt.kbhit():
        datai=input()
        print("You:>",end="")
        if datai=="quit":
            s.sendall(str.encode(datai))
            run=False
            break

        if(datai!=""):
            s.sendall(str.encode(datai))

            

def recveing():
    global s,run,f1,f2quit
    # print("receving thread strated")
    while run:
        data=s.recv(1024).decode("utf-8")
        if data=="quit":
            if run:
                print("connection closed.... press Enter to Exit")
            run=False
            break
        else:
            
            print("\nReply:>",data,"\nYou:>",end="")

def main():
    global f1,f2,s
    host_connect_and_bind()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1=executor.submit(sending)
        f2=executor.submit(recveing)
    s.close()
    print("end")


main()









