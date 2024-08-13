from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from fishtank import Fishtank

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        screen = QGuiApplication.primaryScreen()
        self.screen_size = screen.geometry()
        self.setGeometry(self.screen_size)
        
        self.tank = Fishtank(self)
        self.tank.show()

        self.show()