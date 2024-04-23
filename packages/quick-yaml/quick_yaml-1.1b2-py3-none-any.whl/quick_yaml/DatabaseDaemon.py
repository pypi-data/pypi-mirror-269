import copy
import os
import socket
import json
import sys
import threading
from threading import Thread
from .manager import QYAMLDBCoarse, QYAMLDB
import logging
from cryptography.fernet import Fernet

READ_COMMANDS = ['$query']
WRITE_COMMANDS = ['$insert', '$insert_many', '$update', '$update_many', '$delete'
    , '$delete_many', '$del_many', '$del', '$create_table']


# Declare a class DaemonError to denote that daemon cannot start
class DaemonError(Exception):
    pass


class DatabaseDaemonBase:
    def __init__(self, dbpath, key, encrypted, encryption_key=None, log_file="daemon.log"):
        """
        Initialize the DatabaseDaemon object.

        Parameters:
            dbpath (str): The path to the database.
            key (str): The encryption key.
            encrypted (bool): Flag indicating if the data is encrypted.
            encryption_key (str, optional): The encryption key to use. Defaults to None.
            log_file (str, optional): The log file path. Defaults to "daemon.log".

        Returns:
            None
        """
        self.db_path = dbpath
        self.key_path = key
        self.encrypted = encrypted
        self.encryption_key = encryption_key
        self.fernet = Fernet(encryption_key) if encryption_key else None
        self.database: QYAMLDB = None
        self.running = False

        # Setup logging
        self.logger = logging.getLogger('DatabaseDaemon')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.info("DatabaseDaemon initialized.")

    def _encrypt_message(self, message):
        if self.fernet:
            encrypted_message = self.fernet.encrypt(message.encode('utf-8'))
            self.logger.debug("Message encrypted.")
            return encrypted_message
        return message.encode('utf-8')

    def _decrypt_message(self, message):
        if self.fernet:
            decrypted_message = self.fernet.decrypt(message).decode('utf-8')
            self.logger.debug("Message decrypted.")
            return decrypted_message
        return message.decode('utf-8')

    def _setup_db(self):
        self.logger.info("Setting up database ...")
        print("Setting up database ....")
        self.database = QYAMLDBCoarse(self.db_path, self.key_path, self.encrypted)
        try:
            self.database.load_db()
            self.logger.info("Database loaded successfully.")
            print("Database Loaded Successfully")
        except Exception as e:
            self.logger.error(f"Initialization of the database failed: {e}")
            raise Exception(f"Initialization of the database failed: {e}")

    def start(self):
        self.running = True
        self._setup_db()
        self.logger.info("Database Daemon started.")

    def stop(self):
        self.running = False
        self.logger.info("Database Daemon stopped.")

    def _process_command(self, command):
        self.logger.info(f"Processing command: {command}")

        # Processing logic here...

    def run(self):
        self.logger.info("Daemon running.")
        # This should be implemented in subclass
        raise NotImplementedError("Daemon run loop not implemented.")


class DataBaseIPCDaemon(DatabaseDaemonBase):
    """A Database Daemon that listens to DB commands on separate thread
    Note: this class may not be thread safe and also this does not prevent any race condition.
    Use this when you have only one Thread accessing the object."""

    def __init__(self, dbpath, key, encrypted, socket_path, encryption_key=None, log_file="ipc_daemon.log"):
        # Initialize the base class with all required parameters
        super().__init__(dbpath=dbpath, key=key, encrypted=encrypted, encryption_key=encryption_key,
                         log_file=log_file)
        self.server_socket = None
        self.socket_path = socket_path

        self.logger.info("DataBaseIPCDaemon initialized.")

    def start(self):
        """
        Start the daemon by setting up the server socket and listening for incoming connections.
        Make sure to run this under a for your application
        """

        # connect,bind and listen in unix socket
        try:
            os.unlink(self.socket_path)
        except OSError:
            if os.path.exists(self.socket_path):
                self.logger.error('Socket path already exists')
                raise DaemonError('Socket path exists')
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._setup_db()
        try:
            self.server_socket.bind(self.socket_path)
            self.server_socket.listen(5)
            self.logger.info('Listening for client connections on {}'.format(self.socket_path))
            try:
                while True:
                    # Accept client connection
                    connection, address = self.server_socket.accept()
                    self.logger.info(" A Client has been connected")
                    # launch a separate thread handling client
                    ct = Thread(target=self._handle_client, args=(connection, address,))
                    ct.start()
            except KeyboardInterrupt:
                self.server_socket.close()
                self.logger.info('Socket connection has been terminated by user')
            # Print

        except OSError:
            print(f"Socket {self.socket_path} already in use. Use different path")
            self.logger.info(f"Socket {self.socket_path} already in use. Use different path")
        except KeyboardInterrupt:
            self.server_socket.close()
            self.logger.info('Socket connection has been terminated by user')
        finally:

            self.server_socket.close()
            self.logger.info('Socket connection has been terminated.')

    def _handle_client(self, client_socket, mask=None):
        """
        Handle the client connection by receiving, processing, and sending messages.

        Parameters:
        - client_socket: the socket object for the client connection
        - mask: optional parameter to be used for handling the client (default is None)

        Returns:
        This function does not return anything.
        """
        # First, receive the length of the incoming message
        data_length = client_socket.recv(8)

        if not data_length:
            print("Connection closed by the client.")
            self.logger.info("Connection closed by the client.")

            return

        # Convert the length to an integer
        message_length = int(data_length.decode('utf-8'))
        self.logger.info(f"Received message length: {message_length}")
        # Send ack after receiving length to signal
        client_socket.send("ACK".encode('utf-8'))
        # Now receive the rest of the message based on the length
        data = b''
        while len(data) < message_length:
            packet = client_socket.recv(message_length - len(data))
            if not packet:
                self.logger.info("Client closed connection.")
                client_socket.close()
                return
            data += packet
        print('Receive data: ', data.decode('utf-8'))
        # Now that the complete message has been received, proceed with decryption and processing
        try:
            decrypted_command = self._decrypt_message(data)
            command = json.loads(decrypted_command)
            response = self._process_command(command)
            encrypted_response = self._encrypt_message(json.dumps(response))

            # send the length of data
            response_length = str(len(encrypted_response))
            client_socket.send(response_length.encode('utf-8'))
            # wait for acknowledgement from the client.
            ack = client_socket.recv(1024).decode('utf-8')
            self.logger.info(f"Received acknowledgement from client: {ack}")
            # Send actual response
            client_socket.send(encrypted_response)

        except Exception as e:
            print(f"Error processing command: {e}")
            error_response = self._encrypt_message(json.dumps({'error': str(e)}))
            client_socket.send(len(error_response).to_bytes(4, byteorder='big') + error_response)

    def _process_command(self, command):
        """Process the received command."""

        status = self.database.begin_transaction(command)
        return status

    def stop(self):
        """
        Stops the daemon. Closes the server socket.
        """
        # Close the connection
        self.running = False
        self.server_socket.close()


