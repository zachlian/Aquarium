from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QPixmap, QRegion
from fish import Fish
from constants import *
import random

class Fishtank(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.fishes = []
        self.create_fishes(5)
        self.start_animation()

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, self.parent().height() - WINDOW_HEIGHT + ADJUST_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowShape(IMAGE_PATH)

    def setWindowShape(self, img_path):
        self.tank_shape = QPixmap(img_path)
        self.tank_shape = self.tank_shape.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.mask = self.tank_shape.createMaskFromColor(MASK_COLOR, Qt.MaskOutColor)
        self.setMask(self.mask)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(self.rect(), BACKGROUND_COLOR)

        for fish in self.fishes:
            x, y = fish.get_position()
            painter.setBrush(QColor(255, 100, 100))
            painter.drawEllipse(QPoint(int(x), int(y)), 10, 5)

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'oldPos'):
            delta = QPoint(event.globalPos() - self.oldPos)
            new_x = self.x() + delta.x()
            new_rect = self.geometry()
            new_rect.moveLeft(new_x)
            
            if new_rect.left() < 0:
                new_rect.moveLeft(0)
            elif new_rect.right() > self.parent().width():
                new_rect.moveRight(self.parent().width())
            
            self.setGeometry(new_rect)
            self.oldPos = event.globalPos()
            self.update()

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'oldPos'):
            del self.oldPos

    def create_fishes(self, count):
        for _ in range(count):
            while True:
                x = random.randint(0, self.width())
                y = random.randint(0, self.height())
                shape = QRegion(self.mask)
                if shape.contains(QPoint(x, y)):
                    self.fishes.append(Fish(x, y))
                    break

    def start_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_fishes)
        self.timer.start(50)

    def update_fishes(self):
        for fish in self.fishes:
            fish.move(QRegion(self.mask))
        self.update()