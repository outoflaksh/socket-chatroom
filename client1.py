import socket
import threading
import os
import sys

class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            sys.stdout.flush()
            
            
            my_msg = input()
            
            
            

            if my_msg.lower() =="quit":
                self.sock.sendall(f"{self.name} is quitting the chat...".encode("utf-8"))
                break
            else:
                self.sock.sendall(f"<<{self.name}>> : {my_msg}".encode("utf-8"))
        print("Quitting chat...\n")
        os._exit(0)

class Recieve(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
    
    def run(self):
        while True:
            msg = self.sock.recv(2048).decode("utf-8")
            if msg:
                print(msg)
                print('\n<<You>> :',end='')
            else:
                print("Looks like the connection is lost...\nQuitting...\n")
                self.sock.close()
                os._exit(0)
        
class Client():
    def __init__(self , host , port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print(f"Trying to connect to [ {self.host} : {self.port} ]...")
        self.sock.connect((self.host, self.port))
        print(f"Connected to host...")
        print()
        name = input("Your name: ")
        
        send = Send(self.sock , name)
        recieve = Recieve(self.sock, name)

        
        print()
        print("All set, type 'QUIT' to leave...\n<<You>> :",end='')
        recieve.start()
        send.start()
        
        self.sock.sendall(f"{name} has entered the chat! ".encode("utf-8"))

if __name__ =="__main__":
    client = Client(socket.gethostbyname(socket.gethostname()) , 5000)
    client.start()