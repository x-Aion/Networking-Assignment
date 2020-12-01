import socket
import sys
import threading
import time
import unittest
import warnings

from icmplib import ping

import Server as ServerQ2P1


class MyTestCase(unittest.TestCase):
    # testing if the server can accept multiple clients
    # also testing if the client can send icmp attacks
    # this is a long test when I run it

    def test_server_Q2_P1(self):
        # ignored resource warnings (not exceptions)
        warnings.filterwarnings("ignore")
        lock = threading.Lock()
        threadPingData = []

        def newClient():
            nonlocal threadPingData

            # starting the fake client and connecting to the server
            f_client = socket.socket()
            # f_client.settimeout(1)
            hostip = socket.gethostbyname(socket.gethostname())
            f_client.connect((hostip, 54321))

            # saving response
            response = f_client.recv(1024).decode()
            pingData = str(response).split(",", 3)
            pingData = ping(pingData[0], int(pingData[1]), int(pingData[2]), int(pingData[3]))

            with lock:
                # saving the ping data for later processing
                threadPingData.append(pingData)

            time.sleep(2)

            # telling the client to stop the attack
            f_client.sendall("n".encode('ascii', 'strict'))
            if len(threadPingData) == 2:
                sys.exit()

        # opening a thread where the server can run without bother
        threads = [threading.Thread(target=ServerQ2P1.runServer),
                   threading.Thread(target=newClient),
                   threading.Thread(target=newClient)]

        try:
            # starting the server thread and the client threads with delay inbetween
            for t in threads:
                # t.daemon = True
                t.start()
                time.sleep(4)

            for t in threads:
                t.join()
        except OSError:
            pass
            # expected exception due to how i closed the socket

        # if the amount of datapoints saved is not equal to
        # the amount we should have received uh oh
        self.assertTrue(len(threadPingData) == 2)
        print("passed first asser")

        # testing to see if the attacks worked or not
        # and if the packets sent match the the other info
        # retrieved
        for pData in threadPingData:
            if not (pData.packets_received == 0 and pData.packets_sent != 0 and not pData.is_alive):
                self.assertTrue(False)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
