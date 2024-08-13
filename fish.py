import random
import math
from PyQt5.QtCore import QPoint

class Fish:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = random.uniform(0, 2 * math.pi)
        self.turn_factor = 0.2

    def move(self, tank_shape):
        self.direction += random.uniform(-self.turn_factor, self.turn_factor)
        
        new_x = self.x + self.speed * math.cos(self.direction)
        new_y = self.y + self.speed * math.sin(self.direction)
        
        if not tank_shape.contains(QPoint(int(new_x), int(new_y))):
            self.direction = random.uniform(0, 2 * math.pi)
            return
        
        self.x, self.y = new_x, new_y

    def get_position(self):
        return self.x, self.y