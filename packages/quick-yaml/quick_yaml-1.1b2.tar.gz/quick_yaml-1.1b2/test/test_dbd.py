"""
This is Work In Progress
"""
import random
import time
import unittest
import threading
import socket
import json
import os
from src.quick_yaml.DatabaseDaemon import DataBaseIPCDaemon
from src.quick_yaml.mock_generator import SetupDeviceTable


class TestDatabaseDaemon(unittest.TestCase):
    db_path = 'sample_databases/sample.ezdb'
    key = 'sample_databases/sample.key'
    log = 'test_ipc.log'
    socket_path = "/tmp/test_dbd_socket"
    encrypted = False
    sample_data = None
    key_file = ""
    db = None
    dbd_thread = None
    t1 = None

    def test_transaction(self):
        import requests
        r = requests.get('https://random-word-api.herokuapp.com/word?lang=en')
        # set the path
        self.socket_path = "/tmp/" + r.json()[0] + "_socket"
        d = SetupDeviceTable()

        transations = {
            'transaction_id': 100,
            'operations': [
                {'type': '$insert', '$table_name': 'devices_table',
                 '$data': d.generate_random_data(random.randint(100))}
            ]
        }
        self.dbd_thread = DataBaseIPCDaemon(self.db_path, None, self.encrypted, self.socket_path,

                                            log_file=self.log)
        # launch in a separate thread
        print(self.socket_path)
        t1 = threading.Thread(target=self.dbd_thread.start, daemon=True)
        t1.start()
        # setup socket client (AF UNIX)
        # wait for server to init
        time.sleep(1)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        if os.path.exists(self.socket_path):
            print(' Path Found')
            sock.connect(self.socket_path)
        else:
            print('No Path Found')
            exit(1)
        # Send length of message and wait for ack

        msg = json.dumps(transations).encode('utf-8')
        sock.send(str(len(msg)).encode('utf-8'))
        print("Sent length of message: ", len(msg))
        print('waiting for translation to be processed....')
        ack = sock.recv(1024).decode('utf-8')
        self.assertEqual(ack, 'ACK')
        sock.send(json.dumps(transations).encode('utf-8'))
        # Receive length of results in results_len as integer
        results_len = sock.recv(1024).decode('utf-8')
        # Send ACK to server
        sock.send("ACK".encode('utf-8'))
        results = sock.recv(int(results_len))

        print(results)

        sock.close()


# To Define additional class methods and tests here later


if __name__ == '__main__':
    unittest.main()
