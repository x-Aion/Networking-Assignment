import socket
#create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get host name
name = socket.gethostname()
print("The name of the host is: "+name)

#get ip of host
ip = socket.gethostbyname(name)
print("The IP of the host is: "+ip)

#opening up a connection to the server
port = 4321
adrs = (ip,port)
server.bind(adrs)
server.listen(1)
print("Started listening on ",ip,":",port)
client,addr = server.accept()
print("Obtained a Connection from ",addr[0]," : ",addr[1])

#continuous communication until client closes the connection
while 1:
    data = client.recv(1024)
    data=data.decode()
    print("Received ",data," from the client.")
    print("Processing...")
    if data=="exit":
        client.send("Closing connection, Goodbye.").encode()
        client.close()
        print("Connection Closed.")
        break
    else:
        msg="Message received. Thank you. Press ENTER to send another message or type 'exit' to end connection."
        client.send(msg.encode())
        print("reply sent.")


