import socket
import threading
import time
import unittest
import warnings
import Server as ServerQ1P1



class MyTestCase(unittest.TestCase):
    # runs a the server and a fake client, then sends the server
    # a request to tell it if a host name is online or not
    # processes that request then quits
    def test_server_Q1_P1(self):
        # ignored resource warnings (not exceptions)
        warnings.filterwarnings("ignore")

        # opening a thread where the server can run without bother
        thread = threading.Thread(target=ServerQ1P1.runServer, args=())
        thread.daemon = True
        thread.start()
        time.sleep(1)

        # starting the fake client and connecting to the server
        f_client = socket.socket()
        f_client.settimeout(1)
        hostip = socket.gethostbyname(socket.gethostname())
        f_client.connect((hostip, 4321))

        # asking server to check status of a hostname
        f_client.sendall("ipcheck".encode('ascii', 'strict'))

        # saving response
        response = f_client.recv(1024).decode('ascii', 'strict')
        time.sleep(1)

        # telling the client to disconnect from the server
        f_client.sendall("quit".encode('ascii', 'strict'))

        thread.join()

        # checking if correct term is received from the server
        self.assertTrue(response.startswith("Host is online") or response.startswith("Host is offline"))

        # runs a the server and a fake client, then sends the server
        # a request to tell it if a host name is online or not
        # processes that request then quits ( this might be a longer test)

if __name__ == '__main__':
    unittest.main()
