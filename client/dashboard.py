from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import get_all_data as ald
import get_a_data as ad
import select
import os, glob

BUFFER_SIZE = 1024 * 4

timeout = 1


class PopUp(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.pText = QLineEdit(self)
        self.pText.move(20, 20)
        self.pText.resize(280,40)
        self.pButton = QPushButton('Submit', self)
        self.pButton.move(20,80)
        self.show()

class Dashboard(QMainWindow):
    def __init__(self, client, ip, port):
        super().__init__()
        uic.loadUi("gui\\dashboard.ui", self)
        self.setWindowTitle("Dashboard")
        self.setFixedSize(320, 240)
        self.client = client
        self.addr = (ip, port)

        self.btn_back.clicked.connect(self.finish)

        self.btn_a_data.clicked.connect(self.send_name)
        self.btn_all_data.clicked.connect(self.get_all_data)

    def get_all_data(self):
        self.client.sendto(str.encode("GET ALL DATA"), self.addr)
        database = []
        n = int(self.client.recvfrom(BUFFER_SIZE)[0])
        for i in range(n):
            data = self.get_data_1()
            database.append(data)
        self.hide()
        print("Get database successfully!")
        self.w = ald.GetAllData(self.client, database)
        self.w.btn_back.clicked.connect(self.show)
        self.w.show()
    
    def send_name(self):
        self.popup = PopUp("Send destination name")
        self.popup.pButton.clicked.connect(self.get_a_data)

    def get_a_data(self):
        des = self.popup.pText.text()
        self.client.sendto(str.encode(str(des)), self.addr)
        self.popup.close()
        data = self.get_data_2()
        if type(data) == type(None):
            QMessageBox.about(self, "Notice", "Not found data in database")
            return
        self.hide()
        self.w = ad.GetAData(self.client, data)
        self.w.btn_back.clicked.connect(self.show)
        self.w.show()
    
    def get_data_1(self):
        data = dict()
        
        data["id"] = str(self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8"))
        print(data["id"])
        data["name"] = str(self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8"))
        print(data["name"])
        data["location"] = str(self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8"))
        print(data["location"])
        data["description"] = str(self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8"))
        print(data["description"])

        # _bytes = str.encode("RECEIVED!", "utf8")
        # self.client.sendto(_bytes, self.addr)

        print("Get data successfully!")
        return data
        


    def get_data_2(self):
        data = dict()

        tmp = self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8")
        if tmp == "Not found data in database!!":
            return None
        data["id"] = str(tmp)
        print(data["id"])
        data["name"] = str(self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8"))
        print(data["name"])
        data["location"] = str(self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8"))
        print(data["location"])
        data["description"] = str(self.client.recvfrom(BUFFER_SIZE)[0].decode("utf8"))
        print(data["description"])
        # f = open(f"data\\{file_name}.png")

        file_name = data["name"]
        f = open(f'data\\{file_name}.jpg', 'wb')
        
        while True:
            ready = select.select([self.client], [], [], timeout)
            if ready[0]:
                buffer = self.client.recvfrom(BUFFER_SIZE)[0]
                f.write(buffer)
            else:
                # _bytes = str.encode("RECEIVED!", "utf8")
                # self.client.sendto(_bytes, self.addr)
                print("Get data successfully!")
                data["img"] = 'data\\{file_name}.jpg'
                f.close()
                return data

    def finish(self):
        _bytes = str.encode("QUIT", "utf8")
        self.client.sendto(_bytes, self.addr)
        self.client.close()
        files = glob.glob("data\\*")
        for f in files:
            os.remove(f)
        self.close()


                