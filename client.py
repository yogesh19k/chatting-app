#!/usr/bin/env python3
import socket
import concurrent.futures


HOST = '139.162.161.211'  # The server's hostname or IP address
PORT =  11988       # The port used by the server
run=True

def host_connect_and_bind():
    global HOST,PORT,s
    try:
        s = socket.socket()
        print("socket created")

    except:
        print("socket creation problem")

    try:
        s.connect((HOST, PORT))
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
    global s,run,f1,f2
    # print("receving thread strated")
    while run:
        data=s.recv(1024).decode("utf-8")
        if data=="quit":
            if run:
                print("connection closed.... Enter quit to exit\nYou:>",end="")
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









