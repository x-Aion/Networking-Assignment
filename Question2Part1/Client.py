# Name: Ryan Dreise
# Student Number: 105014618
# Description: Networking assignment

import socket
from icmplib import ping

cSocket = socket.socket()
name = socket.gethostname()
host = socket.gethostbyname(name)
port = 54321

try:
    cSocket.connect((host, port))  # Trying to connect to the server
    print('Connection Successful')
except socket.error as e:
    print(str(e))


response = cSocket.recv(1024)
response = response.decode()  # Gets the ICMP attack information from the server

while 1:
    # Pings the ICMP server using the information sent by the server (IP address, # of times to ping, # of
    # seconds between pings, timeout interval
    pingData = str(response).split(",", 3)
    pingData = ping(pingData[0], int(pingData[1]), int(pingData[2]), int(pingData[3]))
    print("Ping address: ", pingData.address,  # Displaying ping address
          "\nPKTs Sent: ", pingData.packets_sent,  # displaying number of packets send
          "\nPKTs Received: ", pingData.packets_received,  # Displaying number of packets received
          "\nIs Alive: ", pingData.is_alive)  # is alive?
    stop = input("Continue attack(y/n): ")  # Asking client if they wish to continue the attack
    cSocket.send(str.encode(stop))  # sends the ans to the server, server breaks connection if no
    if stop == 'n':
        break
cSocket.close()  # Closing connection if no
print("Attack stopped, connection closed")
