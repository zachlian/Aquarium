from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QFont, QRegion
from constants import *
from hardware import HardwareMonitor
import math

class Fishtank(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.hardware_monitor = HardwareMonitor()
        self.update_hardware_info()
        self.start_animation()
        
    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.start_x = 0
        self.start_y = self.parent().height() - WINDOW_HEIGHT - ADJUST_HEIGHT
        self.setGeometry(self.start_x, self.start_y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowShape(IMAGE_PATH)

    def setWindowShape(self, img_path):
        self.tank_shape = QPixmap(img_path)
        self.tank_shape = self.tank_shape.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.mask = self.tank_shape.createMaskFromColor(MASK_COLOR, Qt.MaskOutColor)
        self.setMask(self.mask)

    def paintEvent(self, event):
        # Draw background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(self.rect(), BACKGROUND_COLOR)
        self.draw_hardware_info()

    def draw_hardware_info(self):
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.setFont(QFont('Courier', 16, QFont.Bold))

        x_offset = WINDOW_WIDTH//2 - 60
        y_offset = 150
        painter.drawText(x_offset, y_offset, f"CPU: {self.cpu_usage:04.1f}%")
        if self.gpu_usage is not None:
            y_offset += 20
            painter.drawText(x_offset, y_offset, f"GPU: {self.gpu_usage:04.1f}%")
        y_offset += 20
        painter.drawText(x_offset, y_offset, f"MEM: {self.memory_usage:04.1f}%")
        
    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'oldPos'):
            delta = QPoint(event.globalPos() - self.oldPos)
            if delta.x() > 0:
                dx = min(delta.x(), MAX_TANK_DELTA)
            else:
                dx = max(delta.x(), -MAX_TANK_DELTA)
            new_x = self.x() + dx
            #new_y = self.y() + delta.y()
            new_rect = self.geometry()
            new_rect.moveLeft(new_x)
            #new_rect.moveTop(new_y)
            
            if new_rect.left() < 0:
                new_rect.moveLeft(0)
            elif new_rect.right() > self.parent().width():
                new_rect.moveRight(self.parent().width())
            
            self.setGeometry(new_rect)
            self.oldPos = event.globalPos()
            self.update()
            
            for fish in self.parent().fishes:
                if dx > 0: # Tank moves to the right
                    fish.is_stuck_on_edge(self, True)
                else:
                    fish.is_stuck_on_edge(self, False)
                fish.force = dx * FORCE_FACTOR

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'oldPos'):
            del self.oldPos

    def start_animation(self):
        self.hardware_timer = QTimer(self)
        self.hardware_timer.timeout.connect(self.update_hardware_info)
        self.hardware_timer.start(1000)  # Update hardware info every 1000ms

    def update_hardware_info(self):
        self.cpu_usage = self.hardware_monitor.get_cpu_usage()
        self.memory_usage = self.hardware_monitor.get_memory_usage()
        self.gpu_usage = self.hardware_monitor.get_gpu_usage()
        self.update()
        
    def is_inside_tank(self, x, y):
        if ALLOW_FISH_EXIT and y < self.y():
            return True
        shape = QRegion(self.mask)
        FISH_SHAPE = max(FISH_WIDTH, FISH_HEIGHT)
        left_top = QPoint(int(x - self.x()), int(y - self.y()))
        right_top = QPoint(int(x + FISH_SHAPE - self.x()), int(y - self.y()))
        left_bottom = QPoint(int(x - self.x()), int(y + FISH_SHAPE - self.y()))
        right_bottom = QPoint(int(x + FISH_SHAPE - self.x()), int(y + FISH_SHAPE - self.y()))
        return shape.contains(left_top) and shape.contains(right_top) and shape.contains(left_bottom) and shape.contains(right_bottom)

    def find_nearest_valid_position(self, x, y, is_right):
        tank_pos = self.pos()
        for i in range(0, self.width()):
            if is_right:
                x = x + 1
            else:
                x = x - 1 - FISH_WIDTH
            if QRegion(self.mask).contains(QPoint(int(x - tank_pos.x()), int(y - tank_pos.y()))):
                return x
        return x