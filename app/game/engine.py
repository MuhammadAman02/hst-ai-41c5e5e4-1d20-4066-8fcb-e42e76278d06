import random
from typing import List, Dict, Any
from app.game.entities import Player, Obstacle, Coin, Background
from app.game.physics import check_collision
from app.config import settings

class GameEngine:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.player = Player(100, settings.GAME_HEIGHT - 160)
        self.obstacles: List[Obstacle] = []
        self.coins: List[Coin] = []
        self.background = Background()
        
        self.score = 0
        self.coins_collected = 0
        self.distance = 0
        self.game_speed = settings.GAME_SPEED
        self.game_over = False
        self.paused = False
        
        # Game state
        self.keys_pressed = set()
        
    def handle_input(self, key: str, pressed: bool):
        """Handle keyboard input"""
        if pressed:
            self.keys_pressed.add(key)
        else:
            self.keys_pressed.discard(key)
    
    def update(self) -> Dict[str, Any]:
        """Update game state and return render data"""
        if self.game_over or self.paused:
            return self.get_render_data()
        
        # Handle continuous key presses
        if 'ArrowLeft' in self.keys_pressed or 'KeyA' in self.keys_pressed:
            self.player.move_left()
        if 'ArrowRight' in self.keys_pressed or 'KeyD' in self.keys_pressed:
            self.player.move_right()
        if 'Space' in self.keys_pressed or 'ArrowUp' in self.keys_pressed:
            self.player.jump()
        
        # Update player
        self.player.update()
        
        # Update background
        self.background.update(self.game_speed)
        
        # Spawn obstacles
        if random.random() < settings.OBSTACLE_SPAWN_RATE:
            obstacle_height = random.randint(40, 80)
            obstacle_y = settings.GAME_HEIGHT - 100 - obstacle_height
            self.obstacles.append(Obstacle(settings.GAME_WIDTH, obstacle_y, 
                                         random.randint(30, 60), obstacle_height))
        
        # Spawn coins
        if random.random() < settings.COIN_SPAWN_RATE:
            coin_y = random.randint(200, settings.GAME_HEIGHT - 150)
            self.coins.append(Coin(settings.GAME_WIDTH, coin_y))
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(self.game_speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
        
        # Update coins
        for coin in self.coins[:]:
            coin.update(self.game_speed)
            if coin.is_off_screen():
                self.coins.remove(coin)
        
        # Check collisions with obstacles
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if check_collision(player_rect, obstacle.get_rect()):
                self.game_over = True
                break
        
        # Check coin collection
        for coin in self.coins[:]:
            if not coin.collected and check_collision(player_rect, coin.get_rect()):
                coin.collected = True
                self.coins.remove(coin)
                self.coins_collected += 1
                self.score += 10
        
        # Update score and speed
        self.distance += self.game_speed
        self.score += 1
        self.game_speed += settings.SPEED_INCREASE_RATE
        
        return self.get_render_data()
    
    def get_render_data(self) -> Dict[str, Any]:
        """Get all data needed for rendering"""
        return {
            'player': {
                'x': self.player.pos.x,
                'y': self.player.pos.y,
                'width': self.player.size.width,
                'height': self.player.size.height
            },
            'obstacles': [
                {
                    'x': obs.pos.x,
                    'y': obs.pos.y,
                    'width': obs.size.width,
                    'height': obs.size.height
                }
                for obs in self.obstacles
            ],
            'coins': [
                {
                    'x': coin.pos.x,
                    'y': coin.pos.y,
                    'width': coin.size.width,
                    'height': coin.size.height
                }
                for coin in self.coins
            ],
            'background': {
                'buildings': self.background.buildings,
                'clouds': self.background.clouds,
                'ground_offset': self.background.ground_offset
            },
            'score': self.score,
            'coins_collected': self.coins_collected,
            'distance': int(self.distance),
            'game_over': self.game_over,
            'paused': self.paused
        }
    
    def pause_toggle(self):
        """Toggle game pause state"""
        self.paused = not self.paused
    
    def restart(self):
        """Restart the game"""
        self.reset_game()