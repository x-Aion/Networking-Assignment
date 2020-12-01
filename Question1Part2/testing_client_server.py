import socket
import threading
import time
import unittest
import warnings

import Server as ServerQ1P2


class MyTestCase(unittest.TestCase):
    # runs a the server and a fake client, then sends the server
    # a request to tell status of the port
    # processes that request then quits
    def test_server_Q1_P2(self):
        # ignored resource warnings (not exceptions)
        warnings.filterwarnings("ignore")

        # opening a thread where the server can run without bother
        thread = threading.Thread(target=ServerQ1P2.runServer, args=())
        thread.start()
        time.sleep(1)

        # starting the fake client and connecting to the server
        f_client = socket.socket()
        f_client.settimeout(1)
        hostip = socket.gethostbyname(socket.gethostname())
        f_client.connect((hostip, 4321))

        # asking server to check status of a hostname
        f_client.sendall("portcheck".encode('ascii', 'strict'))

        # saving response
        response = f_client.recv(1024).decode('ascii', 'strict')
        time.sleep(1)

        # telling the client to disconnect from the server
        f_client.sendall("quit".encode('ascii', 'strict'))

        thread.join()

        # checking if correct term is received from the server
        self.assertTrue(response.startswith("Port is open") or response.startswith("Port is closed"))

if __name__ == '__main__':
    unittest.main()
