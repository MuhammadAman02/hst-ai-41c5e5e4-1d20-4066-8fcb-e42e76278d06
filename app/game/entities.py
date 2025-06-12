from typing import List, Tuple
from dataclasses import dataclass
import random
from app.config import settings

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Size:
    width: float
    height: float

class Player:
    def __init__(self, x: float, y: float):
        self.pos = Position(x, y)
        self.size = Size(settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = True
        self.ground_y = settings.GAME_HEIGHT - 100 - self.size.height
        
    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += settings.GRAVITY
            self.pos.y += self.velocity_y
            
            # Check if landed
            if self.pos.y >= self.ground_y:
                self.pos.y = self.ground_y
                self.velocity_y = 0
                self.on_ground = True
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = -settings.JUMP_FORCE
            self.on_ground = False
    
    def move_left(self):
        self.pos.x = max(0, self.pos.x - settings.PLAYER_SPEED)
    
    def move_right(self):
        self.pos.x = min(settings.GAME_WIDTH - self.size.width, 
                        self.pos.x + settings.PLAYER_SPEED)
    
    def get_rect(self) -> Tuple[float, float, float, float]:
        return (self.pos.x, self.pos.y, self.size.width, self.size.height)

class Obstacle:
    def __init__(self, x: float, y: float, width: float = 50, height: float = 50):
        self.pos = Position(x, y)
        self.size = Size(width, height)
        
    def update(self, speed: float):
        self.pos.x -= speed
    
    def is_off_screen(self) -> bool:
        return self.pos.x + self.size.width < 0
    
    def get_rect(self) -> Tuple[float, float, float, float]:
        return (self.pos.x, self.pos.y, self.size.width, self.size.height)

class Coin:
    def __init__(self, x: float, y: float):
        self.pos = Position(x, y)
        self.size = Size(20, 20)
        self.collected = False
        
    def update(self, speed: float):
        self.pos.x -= speed
    
    def is_off_screen(self) -> bool:
        return self.pos.x + self.size.width < 0
    
    def get_rect(self) -> Tuple[float, float, float, float]:
        return (self.pos.x, self.pos.y, self.size.width, self.size.height)

class Background:
    def __init__(self):
        self.buildings = []
        self.clouds = []
        self.ground_offset = 0
        self._generate_background()
    
    def _generate_background(self):
        # Generate buildings
        for i in range(10):
            building = {
                'x': i * 100,
                'y': settings.GAME_HEIGHT - 200 - random.randint(50, 150),
                'width': random.randint(60, 100),
                'height': random.randint(100, 200),
                'color': f"#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}"
            }
            self.buildings.append(building)
        
        # Generate clouds
        for i in range(5):
            cloud = {
                'x': random.randint(0, settings.GAME_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(30, 60)
            }
            self.clouds.append(cloud)
    
    def update(self, speed: float):
        # Move buildings
        for building in self.buildings:
            building['x'] -= speed * 0.5  # Parallax effect
            if building['x'] + building['width'] < 0:
                building['x'] = settings.GAME_WIDTH
                building['y'] = settings.GAME_HEIGHT - 200 - random.randint(50, 150)
                building['height'] = random.randint(100, 200)
        
        # Move clouds
        for cloud in self.clouds:
            cloud['x'] -= speed * 0.2  # Slower parallax
            if cloud['x'] + cloud['size'] < 0:
                cloud['x'] = settings.GAME_WIDTH + random.randint(0, 200)
                cloud['y'] = random.randint(50, 200)
        
        # Update ground
        self.ground_offset = (self.ground_offset + speed) % 100