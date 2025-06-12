import math
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GameObject:
    x: float
    y: float
    width: float
    height: float
    velocity_x: float = 0
    velocity_y: float = 0

@dataclass
class Player(GameObject):
    lane: int = 1
    jumping: bool = False
    invulnerable: bool = False
    invulnerable_time: float = 0

@dataclass
class Obstacle(GameObject):
    obstacle_type: str = "barrier"
    lane: int = 0

@dataclass
class Coin(GameObject):
    collected: bool = False
    value: int = 10
    rotation: float = 0

class GameEngine:
    def __init__(self):
        self.game_width = 800
        self.game_height = 400
        self.lanes = [150, 350, 550]
        self.gravity = 0.8
        self.jump_power = -15
        self.base_speed = 5
        
        # Game state
        self.score = 0
        self.game_speed = self.base_speed
        self.time_elapsed = 0
        self.coins_collected = 0
        
        # Game objects
        self.player = Player(
            x=self.lanes[1],
            y=300,
            width=40,
            height=60,
            lane=1
        )
        self.obstacles: List[Obstacle] = []
        self.coins: List[Coin] = []
        
        # Spawn timers
        self.obstacle_spawn_timer = 0
        self.coin_spawn_timer = 0
        
    def update(self, delta_time: float) -> Dict:
        """Update game state"""
        self.time_elapsed += delta_time
        
        # Update player physics
        self._update_player_physics(delta_time)
        
        # Update game objects
        self._update_obstacles(delta_time)
        self._update_coins(delta_time)
        
        # Spawn new objects
        self._spawn_objects(delta_time)
        
        # Check collisions
        collision_result = self._check_collisions()
        
        # Update score and speed
        self._update_score_and_speed(delta_time)
        
        return {
            "player": self._serialize_player(),
            "obstacles": [self._serialize_obstacle(obs) for obs in self.obstacles],
            "coins": [self._serialize_coin(coin) for coin in self.coins],
            "score": self.score,
            "game_speed": self.game_speed,
            "collision": collision_result,
            "coins_collected": self.coins_collected
        }
    
    def _update_player_physics(self, delta_time: float):
        """Update player physics"""
        # Apply gravity
        if self.player.jumping:
            self.player.velocity_y += self.gravity
            self.player.y += self.player.velocity_y
            
            # Ground collision
            if self.player.y >= 300:
                self.player.y = 300
                self.player.velocity_y = 0
                self.player.jumping = False
        
        # Update invulnerability
        if self.player.invulnerable:
            self.player.invulnerable_time -= delta_time
            if self.player.invulnerable_time <= 0:
                self.player.invulnerable = False
    
    def _update_obstacles(self, delta_time: float):
        """Update obstacle positions"""
        for obstacle in self.obstacles[:]:
            obstacle.x -= self.game_speed
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)
    
    def _update_coins(self, delta_time: float):
        """Update coin positions and animations"""
        for coin in self.coins[:]:
            coin.x -= self.game_speed
            coin.rotation += 0.1
            if coin.x + coin.width < 0:
                self.coins.remove(coin)
    
    def _spawn_objects(self, delta_time: float):
        """Spawn obstacles and coins"""
        self.obstacle_spawn_timer += delta_time
        self.coin_spawn_timer += delta_time
        
        # Spawn obstacles
        obstacle_spawn_rate = max(0.5, 2.0 - (self.time_elapsed / 30))  # Increase spawn rate over time
        if self.obstacle_spawn_timer >= obstacle_spawn_rate:
            self._spawn_obstacle()
            self.obstacle_spawn_timer = 0
        
        # Spawn coins
        coin_spawn_rate = 1.5
        if self.coin_spawn_timer >= coin_spawn_rate:
            if random.random() < 0.7:  # 70% chance to spawn coin
                self._spawn_coin()
            self.coin_spawn_timer = 0
    
    def _spawn_obstacle(self):
        """Spawn a new obstacle"""
        lane = random.randint(0, 2)
        obstacle_types = ["barrier", "train", "sign"]
        obstacle_type = random.choice(obstacle_types)
        
        if obstacle_type == "train":
            width, height = 80, 100
            y = 250
        elif obstacle_type == "barrier":
            width, height = 40, 80
            y = 280
        else:  # sign
            width, height = 40, 80
            y = 280
        
        obstacle = Obstacle(
            x=self.game_width,
            y=y,
            width=width,
            height=height,
            lane=lane,
            obstacle_type=obstacle_type
        )
        
        self.obstacles.append(obstacle)
    
    def _spawn_coin(self):
        """Spawn a new coin"""
        lane = random.randint(0, 2)
        y = random.randint(200, 320)
        
        coin = Coin(
            x=self.game_width,
            y=y,
            width=20,
            height=20,
            value=10
        )
        
        self.coins.append(coin)
    
    def _check_collisions(self) -> Dict:
        """Check for collisions"""
        result = {"obstacle": False, "coin": False}
        
        if self.player.invulnerable:
            return result
        
        player_rect = (self.player.x - self.player.width/2, self.player.y - self.player.height,
                      self.player.width, self.player.height)
        
        # Check obstacle collisions
        for obstacle in self.obstacles:
            obstacle_rect = (obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            if self._rectangles_overlap(player_rect, obstacle_rect):
                result["obstacle"] = True
                break
        
        # Check coin collisions
        for coin in self.coins[:]:
            if not coin.collected:
                coin_rect = (coin.x, coin.y, coin.width, coin.height)
                if self._rectangles_overlap(player_rect, coin_rect):
                    coin.collected = True
                    self.coins.remove(coin)
                    self.score += coin.value
                    self.coins_collected += 1
                    result["coin"] = True
        
        return result
    
    def _rectangles_overlap(self, rect1: Tuple, rect2: Tuple) -> bool:
        """Check if two rectangles overlap"""
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def _update_score_and_speed(self, delta_time: float):
        """Update score and game speed"""
        # Increase score based on distance
        self.score += int(self.game_speed * delta_time)
        
        # Gradually increase game speed
        speed_increase_rate = 0.1
        max_speed = 15
        self.game_speed = min(max_speed, self.base_speed + (self.time_elapsed * speed_increase_rate))
    
    def move_player_left(self):
        """Move player to left lane"""
        if self.player.lane > 0:
            self.player.lane -= 1
            self.player.x = self.lanes[self.player.lane]
    
    def move_player_right(self):
        """Move player to right lane"""
        if self.player.lane < 2:
            self.player.lane += 1
            self.player.x = self.lanes[self.player.lane]
    
    def player_jump(self):
        """Make player jump"""
        if not self.player.jumping:
            self.player.velocity_y = self.jump_power
            self.player.jumping = True
    
    def activate_power_up(self, power_type: str):
        """Activate a power-up"""
        if power_type == "invulnerability":
            self.player.invulnerable = True
            self.player.invulnerable_time = 3.0  # 3 seconds
        elif power_type == "speed_boost":
            self.game_speed *= 1.5
        elif power_type == "coin_magnet":
            # Collect all coins on screen
            for coin in self.coins[:]:
                if not coin.collected:
                    coin.collected = True
                    self.score += coin.value
                    self.coins_collected += 1
            self.coins = [coin for coin in self.coins if coin.collected]
    
    def _serialize_player(self) -> Dict:
        """Serialize player for JSON response"""
        return {
            "x": self.player.x,
            "y": self.player.y,
            "width": self.player.width,
            "height": self.player.height,
            "lane": self.player.lane,
            "jumping": self.player.jumping,
            "invulnerable": self.player.invulnerable
        }
    
    def _serialize_obstacle(self, obstacle: Obstacle) -> Dict:
        """Serialize obstacle for JSON response"""
        return {
            "x": obstacle.x,
            "y": obstacle.y,
            "width": obstacle.width,
            "height": obstacle.height,
            "type": obstacle.obstacle_type,
            "lane": obstacle.lane
        }
    
    def _serialize_coin(self, coin: Coin) -> Dict:
        """Serialize coin for JSON response"""
        return {
            "x": coin.x,
            "y": coin.y,
            "width": coin.width,
            "height": coin.height,
            "rotation": coin.rotation,
            "value": coin.value,
            "collected": coin.collected
        }
    
    def reset(self):
        """Reset game to initial state"""
        self.score = 0
        self.game_speed = self.base_speed
        self.time_elapsed = 0
        self.coins_collected = 0
        
        self.player = Player(
            x=self.lanes[1],
            y=300,
            width=40,
            height=60,
            lane=1
        )
        
        self.obstacles.clear()
        self.coins.clear()
        
        self.obstacle_spawn_timer = 0
        self.coin_spawn_timer = 0