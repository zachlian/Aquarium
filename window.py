from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QGuiApplication, QPainter, QColor, QRegion
from fishtank import Fishtank
from constants import *
import random
from fish import Fish

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fishes = []
        self.create_fishes(7)
        self.start_animation()
        

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        screen = QGuiApplication.primaryScreen()
        self.screen_size = screen.geometry()
        self.setGeometry(self.screen_size)
        
        self.tank = Fishtank(self)
        self.tank.show()
        self.show()
        
    def paintEvent(self, event):
        self.tank.update()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.transparent)
        
        for fish in self.fishes:
            x, y = fish.get_position()
            painter.setBrush(QColor(255, 100, 100))
            painter.drawEllipse(QPoint(int(x), int(y)), 10, 5)
    
    def create_fishes(self, count):
        for _ in range(count):
            while True:
                x = random.randint(0, self.tank.width()) + self.tank.x()
                y = random.randint(0, self.tank.height()) + self.tank.y()
                if self.tank.is_inside_tank(x, y):
                    self.fishes.append(Fish(x, y))
                    break
                
    def start_animation(self):
        self.fish_timer = QTimer(self)
        self.fish_timer.timeout.connect(self.update_fishes)
        self.fish_timer.start(50)  # Update fish every 50ms

    def update_fishes(self):
        for fish in self.fishes:
            fish.move(self.width(), self.height(), self.tank)
        self.update()
