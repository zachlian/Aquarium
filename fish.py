import random
import math
from PyQt5.QtCore import QPoint
from constants import *
from PyQt5.QtGui import QImage, QTransform, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
import numpy as np

class Fish:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = random.uniform(0, 2 * math.pi)
        self.turn_factor = 0.2
        self.image = self.setup_image(FISH_PATH)
        self.force = 0
        self.is_outside = False
    
    def setup_image(self, image_path):
        # 讀取圖像
        image = QImage(image_path)
        
        # 將QImage轉換為numpy數組
        buffer = image.bits().asstring(image.width() * image.height() * 4)
        arr = np.frombuffer(buffer, dtype=np.uint8).reshape((image.height(), image.width(), 4))
        
        arr = arr.copy()
        
        # 將白色背景轉為透明
        white = np.array([255, 255, 255, 255])
        mask = np.all(arr == white, axis=2)
        arr[mask] = [0, 0, 0, 0]
        
        # 將numpy數組轉回QImage
        height, width, channel = arr.shape
        bytes_per_line = channel * width
        q_image = QImage(arr.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        
        return QPixmap.fromImage(q_image).scaled(FISH_WIDTH, FISH_HEIGHT, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    def move(self, screen_width, screen_height, tank):
        # change direction slightly
        self.direction += random.uniform(-self.turn_factor, self.turn_factor)
        # calculate new position
        new_x = self.x + self.speed * math.cos(self.direction)
        new_y = self.y + self.speed * math.sin(self.direction)
        
        # bounce back
        if (new_x < 0 or new_x + FISH_WIDTH > screen_width) or (new_y < 0 or new_y + FISH_HEIGHT > screen_height):
            self.direction = random.uniform(0, 2 * math.pi)
            return
        
        # exit the tank
        if  ALLOW_FISH_EXIT and self.y < tank.y() + FISH_EXIT_RANGE:
            self.is_outside = True
        # enter the tank
        elif ALLOW_FISH_EXIT and self.y < tank.y() + FISH_EXIT_RANGE and tank.is_inside_tank(self.x, self.y) :
            self.is_outside = False
        
        if not tank.is_inside_tank(new_x, new_y) and not self.is_outside:
            # bounce back inside the tank
            self.direction = random.uniform(0, 2 * math.pi)
            # move slightly to avoid stucking on the edge
            tank_center_x, tank_center_y = tank.x() + WINDOW_WIDTH//2, tank.y() + WINDOW_HEIGHT//2
            direction_to_tank = math.atan2(tank_center_y - self.y, tank_center_x - self.x)
            self.x += 4 * math.cos(direction_to_tank)
            self.y += 4 * math.sin(direction_to_tank)
            return
        # elif tank.is_inside_tank(new_x, new_y) and self.is_outside and self.y > tank.y() + FISH_EXIT_RANGE:
        #     # bounce back outside the tank
        #     self.direction = random.uniform(0, 2 * math.pi)
        #     return 
        
        # inertial movement
        if self.force != 0 and not self.is_outside:
            new_x += self.force
            if self.force > 1:
                self.force = self.force - FORCE_REDUCE_FACTOR
            elif self.force < -1:
                self.force = self.force + FORCE_REDUCE_FACTOR
            else:
                self.force = 0
        
        # update position
        self.x, self.y = new_x, new_y
    

    def is_stuck_on_edge(self, tank, is_right):
        if not tank.is_inside_tank(self.x, self.y) and not self.is_outside:
            self.x = tank.find_nearest_valid_position(self.x, self.y, is_right)
                    
    def get_position(self):
        return self.x, self.y
    
    def get_image(self):
        trainsform = QTransform().rotate(math.degrees(self.direction))
        return self.image.transformed(trainsform)