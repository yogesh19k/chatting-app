#!/usr/bin/env python3
import socket
import concurrent.futures
import time


HOST = '192.168.0.6'  # The server's hostname or IP address
PORT =  9999       # The port used by the server

run=True
hold=True
talkid=None
mlog=[]

def host_connect_and_bind():
    global HOST,PORT,s,mlog
    

    try:
        s = socket.socket()
        print("socket created")

    except:
        print("socket creation problem")

    try:
        s.connect((HOST, PORT))
        s.sendall(str.encode(input("Enter you ID:")))
        s.sendall(b"28log28")
        recv=(s.recv(1024).decode("utf-8"))
        if recv!="28nolog28":
            mlog=recv.split(" &:& ")
        
        for v in mlog:
            print(v)

        print(f"connected to{HOST}")

    except:
        print("connecting problem")

def sending():
    global s,run,f1,f2,hold,talkid
    datai="28change28"
    while run:
    
        if(datai=="28change28"):
            print("SYSTEM:> Please enter the talk to ID:",end="")
            datai=input()
            talkid=datai
            datai="28change28 "+datai
        else:
            datai=input()
            if "28change28" in datai:
                talkid=(datai).split(" ")[-1]
                
        print(f"You'r talking to {talkid}:>",end="")
    
        if datai=="quit":
            s.sendall(str.encode(datai))
            run=False
            time.sleep(2)
            s.close()
            break

        if(datai!=""):
            s.sendall(str.encode(datai))

def recveing():
    global s,run,f1,f2,hold,talkid
 
    while run:
        data=s.recv(1024).decode("utf-8")
        
        
        if data=="quit":
            if run:
                print("\nconnection closed.... press Enter to Exit")
            run=False
            break
        

        elif data=="28wait28":
            print(f"\nSYSTEM:>person not online but message will be sended when they come online\n You'r talking to {talkid}:>",end="")
        
        elif data=="28not28":
            print(f"\nSYSTEM:> Preson is not system in tell him to join\n You'r talking to {talkid}:> ",end="")
    
        elif data=="connected":
            
            print(f"\nSYSTEM:>connected\nYou'r talking to {talkid}:>",end="")

        elif data=="28Alive???28":
            pass
        else:
            print("\n\b\b",data,f"\nYou'r talking to {talkid}:>",end="")

def main():
    global f1,f2,s
    host_connect_and_bind()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1=executor.submit(sending)
        f2=executor.submit(recveing)
    s.close()
    # print("end")

main()








