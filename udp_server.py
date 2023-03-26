import os
import time as t
import socket
import threading
import json
from datetime import datetime, time

LOCAL_PORT = 20001
BUFFER_SIZE = 1024 * 4
CUR_PATH = os.getcwd()
DATA = "database.json"


class Database:
    # init database
    def __init__(self, datapath):
        self.datapath = datapath
        with open(self.datapath, "r") as f:
            data = json.load(f)
        self.data = data

    # get data based on msg

    def find(self, msg):
        if (msg == "get all"):
            return self.data
        else:
            for dest in self.data:
                if (msg in dest["name"]):
                    return dest
            return None


class UDPServer:
    # function use for setting up host and port
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    # function print log of action in server
    def real_time_msg(self, msg):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'{current_time} {msg}')

    # setting up for server
    def setup(self):
        self.real_time_msg('Preparing create socket UDP: ')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.real_time_msg('Socket created!')
        self.real_time_msg('Waitting connection!')

    # SEND ALL DATA IN DATABASE

    def send_all_data(self, database, addr):
        _bytes = str.encode(str(len(database.data)))
        self.sock.sendto(_bytes, addr)
        for data in database.data:
            _bytes = str.encode(data["id"])
            self.sock.sendto(_bytes, addr)

            _bytes = str.encode(data["name"])
            self.sock.sendto(_bytes, addr)

            _bytes = str.encode(f'({data["latitude"]}, {data["longtitude"]})')
            self.sock.sendto(_bytes, addr)

            _bytes = str.encode(data["description"])
            self.sock.sendto(_bytes, addr)

            self.real_time_msg("Sended")

    # SEND DATA OF A DESTINATION

    def send_data(self, res, addr):
        if (type(res) == type(None)):
            _bytes = str.encode("Not found data in database!!")
            self.sock.sendto(_bytes, addr)
        elif (type(res) == dict):
            _bytes = str.encode(res["id"])
            self.sock.sendto(_bytes, addr)

            _bytes = str.encode(res["name"])
            self.sock.sendto(_bytes, addr)

            _bytes = str.encode(f'({res["latitude"]}, {res["longtitude"]})')
            self.sock.sendto(_bytes, addr)

            _bytes = str.encode(res["description"])
            self.sock.sendto(_bytes, addr)

            img = open(res["links"], "rb")
            self.real_time_msg("Sending")
            _bytes = img.read(BUFFER_SIZE)
            while (_bytes):
                if (self.sock.sendto(_bytes, addr)):
                    _bytes = img.read(BUFFER_SIZE)
                    t.sleep(0.02)
            img.close()

            self.real_time_msg("Sended")
                      
    def shutdown_server(self):
        self.real_time_msg('Shutting down server...')
        self.sock.close()


class UDPServerMultiClient(UDPServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket_lock = threading.Lock()

    # print information of client
    def handle_client(self, addr):
        self.real_time_msg(f'Connection received from {addr}')
        self.sock.sendto(str.encode("SUCCESS"), addr)

    def handle_request(self, msg, addr, database):
        msg = msg.decode("utf8")
        if (msg == "QUIT"):
            self.real_time_msg(f'Disconnection received from {addr}')
        elif (msg == "TEST"):
            self.handle_client(addr)
        elif (msg == "GET ALL DATA"):
            self.send_all_data(database, addr)
        elif (msg):
            res = database.find(msg)
            self.send_data(res, addr)

    def process(self, database):
        try:
            while True:
                try:
                    msg, addr = self.sock.recvfrom(BUFFER_SIZE)
                    c_thread = threading.Thread(target=self.handle_request, args=(msg, addr, database))
                    c_thread.daemon = True
                    c_thread.start()
                except OSError as err:
                    self.real_time_msg(err)
        except KeyboardInterrupt:
            self.shutdown_server()


hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
database = Database(DATA)
server = UDPServerMultiClient(host, LOCAL_PORT)
server.setup()
server.process(database)
