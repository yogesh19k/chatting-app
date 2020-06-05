#!/usr/bin/env python3
import socket
import concurrent.futures


HOST = '192.168.0.6'  # The server's hostname or IP address
PORT =  9999       # The port used by the server

run=True
hold=True
talkid=None

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
        # s.sendall(str.encode(input("Enter the presons ID:")))
        print(f"connected to{HOST}")

    except:
        print("connecting problem")



def sending():
    global s,run,f1,f2,hold,talkid
    # print("You:>",end="")
    datai="28change28"
    # print("sending thread strated")
    while run:
        # if msvcrt.kbhit():
    
        if(datai=="28change28"):
            print("SYSTEM:> Please enter the talk to ID:",end="")
            datai=input()
            talkid=datai
            datai="28change28 "+datai
        else:
            datai=input()
        print(f"You'r talking to {talkid}:>",end="")
    
        if datai=="quit":
            s.sendall(str.encode(datai))
            run=False
            break

        if(datai!=""):
            s.sendall(str.encode(datai))


            

def recveing():
    global s,run,f1,f2,hold,talkid
    # print("receving thread strated")
    while run:
        data=s.recv(1024).decode("utf-8")
        
        # print(data)
        if data=="quit":
            if run:
                print("connection closed.... press Enter to Exit")
            run=False
            break
        
        # elif data=="28setup28":
        #     print("\nSYSTEM:> Please enter the talk to ID:")
        #     hold=False


        elif data=="28wait28":
            print("\nSYSTEM:> Please wait preson is not online",end="")
        #     hold=True
    
        elif data=="connected":
            
            print(f"\nSYSTEM:>connected\nYou'r talking to {talkid}:>",end="")


        else:
            print("\n\b\b",data,f"\nYou'r talking to {talkid}:>",end="")

        

def main():
    global f1,f2,s
    host_connect_and_bind()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1=executor.submit(sending)
        f2=executor.submit(recveing)
    s.close()
    print("end")


main()









