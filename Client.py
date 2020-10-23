import socket
#create socket
client=socket.socket()

#get ip
host=socket.gethostname()
hostip=socket.gethostbyname(host)

#connect to server
client.connect((hostip,4321))

while 1:
#sending a message to server
    print("Enter a message to send.")
    data=input()
    client.send(data.encode())

#receiving a message from the server.
    received=client.recv(1024).decode()
    print(received)
    if input()=="exit":
        break





