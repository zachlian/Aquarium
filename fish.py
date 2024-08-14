import random
import math
from PyQt5.QtCore import QPoint
from constants import *

class Fish:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = speed
        self.direction = random.uniform(0, 2 * math.pi)
        self.turn_factor = 0.2

    def move(self, screen_width, screen_height, tank):
        # Change direction slightly
        self.direction += random.uniform(-self.turn_factor, self.turn_factor)
        
        dx = self.speed * math.cos(self.direction) + self.vx
        dy = self.speed * math.sin(self.direction) + self.vy
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 檢查是否碰到屏幕邊緣
        if new_x < 0 or new_x > screen_width:
            self.direction = math.pi - self.direction
        if new_y < 0 or new_y > screen_height:
            self.direction = -self.direction
        
        # 檢查是否碰到魚缸非頂部邊緣
        if not tank.is_inside_tank(new_x, new_y):
            self.direction = random.uniform(0, 2 * math.pi)
            return
        
        self.x, self.y = new_x, new_y

    def is_stuck_on_edge(self, tank, is_right):
        if not tank.is_inside_tank(self.x, self.y):
            if is_right:
                self.x = min(self.x, tank.x())
            else:
                self.x = max(self.x, tank.x() + tank.width())
    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy
    
    def get_position(self):
        return self.x, self.y