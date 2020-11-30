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
    print("Enter a message to send. Or request to check if Host is online type 'ipcheck'")
    data=input()
    client.sendall(data.encode('ascii', 'strict'))

#receiving a message from the server.
    received=client.recv(1024).decode('ascii', 'strict')
    print(received)
    if input()=="quit":
        break





