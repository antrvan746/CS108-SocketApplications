from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic


class GetAllData(QMainWindow):
    def __init__(self, client, data):
        super().__init__()
        uic.loadUi("gui\\getalldata.ui", self)
        self.setWindowTitle("Get All Data")
        self.setFixedSize(640, 480)
        self.client = client
        self.data = data
        if data:
            self.process()
    
        self.btn_back.clicked.connect(self.close)

    def process(self):    
        n = len(self.data)
        self.table_view.setRowCount(n)
        for i in range(n):
            self.table_view.setItem(i, 0, QTableWidgetItem(str(self.data[i]["id"])))
            self.table_view.setItem(i, 1, QTableWidgetItem(str(self.data[i]["name"])))
            self.table_view.setItem(i, 2, QTableWidgetItem(str(self.data[i]["location"])))
            self.table_view.setItem(i, 3, QTableWidgetItem(str(self.data[i]["description"])))
