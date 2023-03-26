from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys
import socket
import dashboard as db

LOCAL_PORT = 20001
BUFFER_SIZE = 1024 * 4
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Client(QMainWindow):
   # function use for setting up host and port
    def __init__(self, client):
        super().__init__()
        uic.loadUi("gui\\startup.ui", self)
        self.setWindowTitle("Client")
        self.setFixedSize(320, 240)
        self.client = client
        self.lineEdit.setText("Input IP")
        self.lineEdit.returnPressed.connect(self.process)

    # function send data to server
    def process(self):
        ip = self.lineEdit.text()
        try:
            self.client.connect((ip, LOCAL_PORT))
            self.client.sendto(str.encode("TEST"), (ip, LOCAL_PORT))
            self.client.settimeout(3)
            msg = self.client.recvfrom(BUFFER_SIZE)[0].decode("utf-8")
            if msg == "SUCCESS":
                QMessageBox.about(self, "Notice", "Connect successfully")
                self.hide()
                self.dashboard(self.client, ip, LOCAL_PORT)
            else:
                QMessageBox.about(self, "Notice", "Connection failed")
        except:
            QMessageBox.about(self, "Notice", "Connection failed")


    def dashboard(self, client, ip, port):
        self.db = db.Dashboard(client, ip, port)
        self.db.show()
    


app = QApplication(sys.argv)
ui = Client(client)
ui.show()
app.exec()
