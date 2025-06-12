from nicegui import ui, events
import asyncio
import random
import math
from typing import List, Dict, Any
import time

# Game constants
GAME_WIDTH = 800
GAME_HEIGHT = 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 80
COIN_SIZE = 20
INITIAL_SPEED = 3
SPEED_INCREMENT = 0.1
JUMP_POWER = 15
GRAVITY = 0.8

class GameObject:
    def __init__(self, x: float, y: float, width: float, height: float, color: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity_y = 0
        self.on_ground = False

class GameState:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.running = False
        self.paused = False
        self.game_over = False
        self.score = 0
        self.distance = 0
        self.coins_collected = 0
        self.speed = INITIAL_SPEED
        self.player = GameObject(100, GAME_HEIGHT - 150 - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, '#FF6B6B')
        self.obstacles: List[GameObject] = []
        self.coins: List[GameObject] = []
        self.background_x = 0
        self.ground_y = GAME_HEIGHT - 150
        self.keys_pressed = set()

game_state = GameState()

def check_collision(obj1: GameObject, obj2: GameObject) -> bool:
    """Check if two game objects are colliding"""
    return (obj1.x < obj2.x + obj2.width and
            obj1.x + obj1.width > obj2.x and
            obj1.y < obj2.y + obj2.height and
            obj1.y + obj1.height > obj2.y)

def spawn_obstacle():
    """Spawn a new obstacle at the right edge of the screen"""
    obstacle_y = game_state.ground_y - OBSTACLE_HEIGHT
    obstacle = GameObject(GAME_WIDTH, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, '#4ECDC4')
    game_state.obstacles.append(obstacle)

def spawn_coin():
    """Spawn a new coin at a random position"""
    coin_x = GAME_WIDTH + random.randint(50, 200)
    coin_y = random.randint(game_state.ground_y - 200, game_state.ground_y - 50)
    coin = GameObject(coin_x, coin_y, COIN_SIZE, COIN_SIZE, '#FFD93D')
    game_state.coins.append(coin)

def update_player():
    """Update player physics and position"""
    player = game_state.player
    
    # Handle jumping
    if not player.on_ground:
        player.velocity_y += GRAVITY
    
    # Update position
    player.y += player.velocity_y
    
    # Ground collision
    if player.y + player.height >= game_state.ground_y:
        player.y = game_state.ground_y - player.height
        player.velocity_y = 0
        player.on_ground = True
    else:
        player.on_ground = False
    
    # Horizontal movement
    if 'ArrowLeft' in game_state.keys_pressed or 'KeyA' in game_state.keys_pressed:
        player.x = max(0, player.x - 5)
    if 'ArrowRight' in game_state.keys_pressed or 'KeyD' in game_state.keys_pressed:
        player.x = min(GAME_WIDTH - player.width, player.x + 5)

def update_game():
    """Update game logic"""
    if not game_state.running or game_state.paused or game_state.game_over:
        return
    
    # Update player
    update_player()
    
    # Move obstacles
    for obstacle in game_state.obstacles[:]:
        obstacle.x -= game_state.speed
        if obstacle.x + obstacle.width < 0:
            game_state.obstacles.remove(obstacle)
    
    # Move coins
    for coin in game_state.coins[:]:
        coin.x -= game_state.speed
        if coin.x + coin.width < 0:
            game_state.coins.remove(coin)
    
    # Spawn new obstacles
    if len(game_state.obstacles) == 0 or game_state.obstacles[-1].x < GAME_WIDTH - 300:
        if random.random() < 0.3:  # 30% chance to spawn obstacle
            spawn_obstacle()
    
    # Spawn new coins
    if random.random() < 0.1:  # 10% chance to spawn coin
        spawn_coin()
    
    # Check collisions with obstacles
    for obstacle in game_state.obstacles:
        if check_collision(game_state.player, obstacle):
            game_state.game_over = True
            return
    
    # Check collisions with coins
    for coin in game_state.coins[:]:
        if check_collision(game_state.player, coin):
            game_state.coins.remove(coin)
            game_state.coins_collected += 1
            game_state.score += 10
    
    # Update score and speed
    game_state.distance += game_state.speed
    game_state.score += 1
    game_state.speed += SPEED_INCREMENT / 100
    
    # Update background
    game_state.background_x -= game_state.speed / 2

def draw_game(canvas_content: str) -> str:
    """Generate SVG content for the game"""
    if not game_state.running:
        return '''
        <svg width="800" height="600" style="background: linear-gradient(to bottom, #87CEEB, #4682B4);">
            <text x="400" y="250" text-anchor="middle" fill="#FFD93D" font-size="48" font-weight="bold">
                SUBWAY SURFERS
            </text>
            <text x="400" y="300" text-anchor="middle" fill="white" font-size="24">
                Press SPACE or ↑ to Start
            </text>
            <text x="400" y="350" text-anchor="middle" fill="white" font-size="18">
                Use ← → or A D to move, SPACE or ↑ to jump
            </text>
        </svg>
        '''
    
    svg_content = f'''
    <svg width="{GAME_WIDTH}" height="{GAME_HEIGHT}" style="background: linear-gradient(to bottom, #87CEEB, #4682B4);">
        <!-- Background buildings -->
        <rect x="{int(game_state.background_x) % 200}" y="400" width="100" height="200" fill="#2C3E50" opacity="0.3"/>
        <rect x="{int(game_state.background_x) % 200 + 150}" y="350" width="80" height="250" fill="#34495E" opacity="0.3"/>
        <rect x="{int(game_state.background_x) % 200 + 300}" y="380" width="120" height="220" fill="#2C3E50" opacity="0.3"/>
        
        <!-- Ground -->
        <rect x="0" y="{game_state.ground_y}" width="{GAME_WIDTH}" height="{GAME_HEIGHT - game_state.ground_y}" fill="#95A5A6"/>
        
        <!-- Ground pattern -->
        <rect x="{int(game_state.background_x * 2) % 100}" y="{game_state.ground_y + 10}" width="50" height="5" fill="#7F8C8D"/>
        <rect x="{int(game_state.background_x * 2) % 100 + 100}" y="{game_state.ground_y + 10}" width="50" height="5" fill="#7F8C8D"/>
        <rect x="{int(game_state.background_x * 2) % 100 + 200}" y="{game_state.ground_y + 10}" width="50" height="5" fill="#7F8C8D"/>
        
        <!-- Player -->
        <rect x="{game_state.player.x}" y="{game_state.player.y}" width="{game_state.player.width}" height="{game_state.player.height}" 
              fill="{game_state.player.color}" rx="5" stroke="#E74C3C" stroke-width="2"/>
        
        <!-- Player details -->
        <circle cx="{game_state.player.x + 15}" cy="{game_state.player.y + 15}" r="8" fill="#F39C12"/>
        <rect x="{game_state.player.x + 10}" y="{game_state.player.y + 25}" width="20" height="25" fill="#3498DB"/>
        
        <!-- Obstacles -->
    '''
    
    for obstacle in game_state.obstacles:
        svg_content += f'''
        <rect x="{obstacle.x}" y="{obstacle.y}" width="{obstacle.width}" height="{obstacle.height}" 
              fill="{obstacle.color}" rx="5" stroke="#16A085" stroke-width="3"/>
        <rect x="{obstacle.x + 10}" y="{obstacle.y + 10}" width="{obstacle.width - 20}" height="10" fill="#1ABC9C"/>
        '''
    
    # Coins
    for coin in game_state.coins:
        svg_content += f'''
        <circle cx="{coin.x + coin.width/2}" cy="{coin.y + coin.height/2}" r="{coin.width/2}" 
                fill="{coin.color}" stroke="#F1C40F" stroke-width="2"/>
        <text x="{coin.x + coin.width/2}" y="{coin.y + coin.height/2 + 5}" text-anchor="middle" 
              fill="#E67E22" font-size="12" font-weight="bold">$</text>
        '''
    
    # UI Elements
    svg_content += f'''
        <!-- Score -->
        <rect x="10" y="10" width="200" height="80" fill="rgba(0,0,0,0.7)" rx="10"/>
        <text x="20" y="35" fill="#FFD93D" font-size="18" font-weight="bold">Score: {game_state.score}</text>
        <text x="20" y="55" fill="#4ECDC4" font-size="16">Distance: {int(game_state.distance)}</text>
        <text x="20" y="75" fill="#FF6B6B" font-size="16">Coins: {game_state.coins_collected}</text>
        
        <!-- Speed indicator -->
        <rect x="{GAME_WIDTH - 120}" y="10" width="100" height="30" fill="rgba(0,0,0,0.7)" rx="5"/>
        <text x="{GAME_WIDTH - 115}" y="30" fill="white" font-size="14">Speed: {game_state.speed:.1f}</text>
    '''
    
    if game_state.paused:
        svg_content += '''
        <rect x="0" y="0" width="800" height="600" fill="rgba(0,0,0,0.5)"/>
        <text x="400" y="280" text-anchor="middle" fill="#FFD93D" font-size="36" font-weight="bold">PAUSED</text>
        <text x="400" y="320" text-anchor="middle" fill="white" font-size="18">Press P to Resume</text>
        '''
    
    if game_state.game_over:
        svg_content += f'''
        <rect x="0" y="0" width="800" height="600" fill="rgba(0,0,0,0.7)"/>
        <rect x="200" y="200" width="400" height="200" fill="#2C3E50" rx="20" stroke="#E74C3C" stroke-width="3"/>
        <text x="400" y="240" text-anchor="middle" fill="#E74C3C" font-size="32" font-weight="bold">GAME OVER!</text>
        <text x="400" y="270" text-anchor="middle" fill="#FFD93D" font-size="20">Final Score: {game_state.score}</text>
        <text x="400" y="295" text-anchor="middle" fill="#4ECDC4" font-size="18">Distance: {int(game_state.distance)}</text>
        <text x="400" y="320" text-anchor="middle" fill="#FF6B6B" font-size="18">Coins: {game_state.coins_collected}</text>
        <text x="400" y="350" text-anchor="middle" fill="white" font-size="16">Press R to Restart</text>
        '''
    
    svg_content += '</svg>'
    return svg_content

async def game_loop():
    """Main game loop"""
    while True:
        if game_state.running:
            update_game()
            # Update the canvas
            canvas.content = draw_game('')
        await asyncio.sleep(1/60)  # 60 FPS

def handle_keydown(e: events.KeyEventArguments):
    """Handle key press events"""
    game_state.keys_pressed.add(e.key)
    
    if e.key == 'Space' or e.key == 'ArrowUp':
        if not game_state.running:
            start_game()
        elif game_state.player.on_ground and not game_state.game_over:
            game_state.player.velocity_y = -JUMP_POWER
    elif e.key == 'KeyP':
        if game_state.running and not game_state.game_over:
            game_state.paused = not game_state.paused
    elif e.key == 'KeyR':
        if game_state.game_over:
            restart_game()

def handle_keyup(e: events.KeyEventArguments):
    """Handle key release events"""
    game_state.keys_pressed.discard(e.key)

def start_game():
    """Start the game"""
    game_state.running = True
    game_state.paused = False
    game_state.game_over = False

def restart_game():
    """Restart the game"""
    game_state.reset()
    start_game()

# Create the main page
@ui.page('/')
async def main_page():
    ui.add_head_html('''
    <style>
        body { 
            margin: 0; 
            padding: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
        }
        .game-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .game-title {
            color: #FFD93D;
            font-size: 3rem;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 20px;
            text-align: center;
        }
        .game-canvas {
            border: 4px solid #2C3E50;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            background: white;
        }
        .controls-info {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.7);
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .control-item {
            margin: 5px 0;
            font-size: 14px;
        }
    </style>
    ''')
    
    with ui.column().classes('game-container'):
        ui.html('<h1 class="game-title">🚇 SUBWAY SURFERS 🏃‍♂️</h1>')
        
        global canvas
        canvas = ui.html(draw_game('')).classes('game-canvas')
        
        with ui.card().classes('controls-info'):
            ui.html('''
            <div class="control-item"><strong>🎮 CONTROLS:</strong></div>
            <div class="control-item">← → or A D: Move left/right</div>
            <div class="control-item">↑ or SPACE: Jump</div>
            <div class="control-item">P: Pause/Resume</div>
            <div class="control-item">R: Restart (when game over)</div>
            <div class="control-item" style="margin-top: 10px;"><strong>🎯 GOAL:</strong> Avoid obstacles, collect coins!</div>
            ''')
    
    # Set up keyboard event handlers
    ui.keyboard(on_key=handle_keydown, events=['keydown'])
    ui.keyboard(on_key=handle_keyup, events=['keyup'])
    
    # Start the game loop
    asyncio.create_task(game_loop())

# Health check endpoint for Fly.io
@ui.page('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': time.time()}