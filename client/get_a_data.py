from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt
import matplotlib.image as mpimg




class GetAData(QMainWindow):
    def __init__(self, client, data):
        super().__init__()
        self.client = client
        uic.loadUi("gui\\getadata.ui", self)
        self.setWindowTitle("A destination")
        self.setFixedSize(766, 480)
        self.img = QPixmap()
        self.data = data

        self.process()

        self.btn_view.clicked.connect(self.view)
        self.btn_back.clicked.connect(self.close)

    def process(self):
        # self.img.loadFromData(self.data["img"])
        # self.img = self.img.scaled(620, 370)
        filename = f'{self.data["name"]}.jpg'
        self.view_image.setPixmap(QPixmap(f"data\\{filename}").scaled(390, 320))

        self.text_name.setText(str(self.data["name"]))
        self.text_id.setText(str(self.data["id"]))
        self.text_geolocate.setText(str(self.data["location"]))
        self.text_description.setText(str(self.data["description"]))
    
    def view(self):
        filename = f'{self.data["name"]}.jpg'
        img = mpimg.imread(f"data\\{filename}")
        imgplot = plt.imshow(img)
        plt.show()



    