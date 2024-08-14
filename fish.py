import random
import math
from PyQt5.QtCore import QPoint
from constants import *
from PyQt5.QtGui import QImage, QTransform, QPixmap
from PyQt5.QtCore import Qt

class Fish:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = random.uniform(0, 2 * math.pi)
        self.turn_factor = 0.2
        self.image = QImage(FISH_PATH)
        self.image.setAlphaChannel(self.image.createMaskFromColor(Qt.white, Qt.MaskOutColor))
        self.image = QPixmap(self.image).scaled(FISH_WIDTH, FISH_HEIGHT, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.force = 0
        
    def move(self, screen_width, screen_height, tank):
        # Change direction slightly
        self.direction += random.uniform(-self.turn_factor, self.turn_factor)
        
        new_x = self.x + self.speed * math.cos(self.direction)
        new_y = self.y + self.speed * math.sin(self.direction)
        

        if new_x - FISH_WIDTH//2 < 0 or new_x + FISH_WIDTH//2 > screen_width:
            self.direction = random.uniform(0, 2 * math.pi)
            return
        if new_y - FISH_HEIGHT//2< 0 or new_y + FISH_HEIGHT//2 > screen_height:
            self.direction = random.uniform(0, 2 * math.pi)
            return
        
        if not tank.is_inside_tank(new_x, new_y):
            self.direction = random.uniform(0, 2 * math.pi)
            # move slightly toward tank to avoid stucking on edge
            tank_center_x, tank_center_y = tank.x() + WINDOW_WIDTH//2, tank.y() + WINDOW_HEIGHT//2
            direction_to_tank = math.atan2(tank_center_y - self.y, tank_center_x - self.x)
            self.x += 4 * math.cos(direction_to_tank)
            self.y += 4 * math.sin(direction_to_tank)
            
            return
        
        if self.force != 0:
            new_x += self.force
            if self.force > 1:
                self.force = self.force - FORCE_REDUCE_FACTOR
            elif self.force < -1:
                self.force = self.force + FORCE_REDUCE_FACTOR
            else:
                self.force = 0
        
        self.x, self.y = new_x, new_y
    

    def is_stuck_on_edge(self, tank, is_right):
        if not tank.is_inside_tank(self.x, self.y):
            self.x = tank.find_nearest_valid_position(self.x, self.y, is_right)
                    
    def get_position(self):
        return self.x, self.y
    
    def get_image(self):
        trainsform = QTransform().rotate(math.degrees(self.direction))
        return self.image.transformed(trainsform)