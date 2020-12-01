# Name: Ryan Dreise
# Student Number: 105014618
# Description: Networking assignment

import socket
import sys
from _thread import *

num_connected_clients = 0
server = None

def new_client(csocket, address):
    global num_connected_clients, server
    print("Sending ICMP attack info to: ", address)  # Displaying the IP and port of the client that connected
    IPtoPing = '76.10.145.247'  # IP address that the client will launch the ICMP attack on
    numOfPing = '2'  # Number of times the client will ping the target
    intervalOfPing = '5'  # Number of seconds inbetween each ping
    timeout = '60'  # Timeout interval in seconds
    msg = IPtoPing + ',' + numOfPing + ',' + intervalOfPing + ',' + timeout  # Creating a single string of the attack info
    csocket.send(str.encode(msg))  # sending info to client
    while 1:  # waiting for continue response from the client
        response = csocket.recv(1024)
        response = response.decode()
        if response == 'n':  # If the client entered n, means they wish to stop, close connection
            csocket.close()
            num_connected_clients -= 1      # decreasing the client count when one leaves
            if num_connected_clients == 0:  # if clients all leave kill the server
                server.close()
            break

    print("Attack stopped for client: ", address)  # Displaying which client disconnected by IP address and port
    print("Stopped server: all clients have disconnected")

def runServer():
    global num_connected_clients, server
    server = socket.socket()  # Creating server socket
    host = socket.gethostname()  # Setting server IP Address
    port = 54321  # Setting server port number

    server.bind((host, port))  # Binding port and address to the server
    server.listen(5)  # waiting for connections
    print('Server started successfully')
    print('Waiting for clients')


    while 1:
        c, addr = server.accept()  # accept the connection
        start_new_thread(new_client, (c, addr))  # Create a new thread from the new connection
                                                 # This allows multiple clients to connect and communicate with the server
        num_connected_clients += 1

    server.close()

if __name__=="__main__":
    runServer()