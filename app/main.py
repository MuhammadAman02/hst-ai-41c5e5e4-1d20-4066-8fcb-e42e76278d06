from nicegui import ui, app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import API routes
from api.routes.game import router as game_router
from api.routes.scores import router as scores_router

# Configure FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(game_router, prefix="/api/game", tags=["game"])
app.include_router(scores_router, prefix="/api/scores", tags=["scores"])

# Serve React build files
if os.path.exists("frontend/dist"):
    app.mount("/static", StaticFiles(directory="frontend/dist/assets"), name="static")

@ui.page('/')
def index():
    ui.add_head_html('''
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Subway Surfers - Endless Runner</title>
        <style>
            body { 
                margin: 0; 
                padding: 0; 
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                overflow: hidden;
            }
            .game-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
            }
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .game-canvas {
                border: 4px solid #2c3e50;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                background: linear-gradient(to bottom, #87CEEB 0%, #98FB98 100%);
            }
            .game-ui {
                position: absolute;
                top: 20px;
                left: 20px;
                color: white;
                font-size: 24px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                z-index: 10;
            }
            .controls {
                position: absolute;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                color: white;
                text-align: center;
                font-size: 16px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .start-screen {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: white;
                z-index: 20;
            }
            .game-title {
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 20px;
                text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .start-button {
                padding: 15px 30px;
                font-size: 24px;
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                border: none;
                border-radius: 25px;
                color: white;
                cursor: pointer;
                transition: transform 0.3s ease;
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            }
            .start-button:hover {
                transform: scale(1.1);
            }
        </style>
    ''')
    
    with ui.element('div').classes('game-container'):
        # Game UI overlay
        with ui.element('div').classes('game-ui'):
            ui.label('Score: 0').props('id="score-display"')
            ui.label('High Score: 0').props('id="high-score-display"')
        
        # Start screen
        with ui.element('div').classes('start-screen').props('id="start-screen"'):
            ui.label('🚇 SUBWAY SURFERS').classes('game-title')
            ui.button('START GAME', on_click='startGame()').classes('start-button')
            ui.label('Use ARROW KEYS or WASD to move • SPACE to jump').style('margin-top: 20px; font-size: 16px;')
        
        # Game canvas
        ui.html('''
            <canvas id="gameCanvas" class="game-canvas" width="800" height="400" style="display: none;"></canvas>
        ''')
        
        # Controls info
        with ui.element('div').classes('controls'):
            ui.label('← → Move • ↑ Jump • P Pause • R Restart')

    # Game JavaScript
    ui.add_head_html('''
        <script>
            class SubwaySurfersGame {
                constructor() {
                    this.canvas = document.getElementById('gameCanvas');
                    this.ctx = this.canvas.getContext('2d');
                    this.gameWidth = 800;
                    this.gameHeight = 400;
                    
                    // Game state
                    this.gameStarted = false;
                    this.gameOver = false;
                    this.paused = false;
                    this.score = 0;
                    this.highScore = localStorage.getItem('subwaySurfersHighScore') || 0;
                    
                    // Player
                    this.player = {
                        x: 100,
                        y: 300,
                        width: 40,
                        height: 60,
                        velocityY: 0,
                        jumping: false,
                        lane: 1, // 0, 1, 2 (left, center, right)
                        color: '#FF6B6B'
                    };
                    
                    // Game objects
                    this.obstacles = [];
                    this.coins = [];
                    this.powerUps = [];
                    
                    // Game settings
                    this.gameSpeed = 5;
                    this.gravity = 0.8;
                    this.jumpPower = -15;
                    this.lanes = [150, 350, 550];
                    
                    // Bind events
                    this.bindEvents();
                    
                    // Update high score display
                    document.getElementById('high-score-display').textContent = `High Score: ${this.highScore}`;
                }
                
                bindEvents() {
                    document.addEventListener('keydown', (e) => this.handleKeyDown(e));
                    document.addEventListener('keyup', (e) => this.handleKeyUp(e));
                }
                
                handleKeyDown(e) {
                    if (!this.gameStarted || this.gameOver || this.paused) return;
                    
                    switch(e.code) {
                        case 'ArrowLeft':
                        case 'KeyA':
                            this.moveLeft();
                            break;
                        case 'ArrowRight':
                        case 'KeyD':
                            this.moveRight();
                            break;
                        case 'ArrowUp':
                        case 'KeyW':
                        case 'Space':
                            this.jump();
                            e.preventDefault();
                            break;
                        case 'KeyP':
                            this.togglePause();
                            break;
                        case 'KeyR':
                            this.restart();
                            break;
                    }
                }
                
                handleKeyUp(e) {
                    // Handle key releases if needed
                }
                
                moveLeft() {
                    if (this.player.lane > 0) {
                        this.player.lane--;
                        this.player.x = this.lanes[this.player.lane];
                    }
                }
                
                moveRight() {
                    if (this.player.lane < 2) {
                        this.player.lane++;
                        this.player.x = this.lanes[this.player.lane];
                    }
                }
                
                jump() {
                    if (!this.player.jumping) {
                        this.player.velocityY = this.jumpPower;
                        this.player.jumping = true;
                    }
                }
                
                togglePause() {
                    this.paused = !this.paused;
                    if (!this.paused) {
                        this.gameLoop();
                    }
                }
                
                restart() {
                    this.gameOver = false;
                    this.score = 0;
                    this.gameSpeed = 5;
                    this.player.x = this.lanes[1];
                    this.player.y = 300;
                    this.player.lane = 1;
                    this.player.velocityY = 0;
                    this.player.jumping = false;
                    this.obstacles = [];
                    this.coins = [];
                    this.powerUps = [];
                    this.gameLoop();
                }
                
                start() {
                    this.gameStarted = true;
                    document.getElementById('start-screen').style.display = 'none';
                    this.canvas.style.display = 'block';
                    this.player.x = this.lanes[1];
                    this.gameLoop();
                }
                
                update() {
                    if (this.gameOver || this.paused) return;
                    
                    // Update player physics
                    this.player.velocityY += this.gravity;
                    this.player.y += this.player.velocityY;
                    
                    // Ground collision
                    if (this.player.y >= 300) {
                        this.player.y = 300;
                        this.player.velocityY = 0;
                        this.player.jumping = false;
                    }
                    
                    // Update obstacles
                    this.obstacles.forEach(obstacle => {
                        obstacle.x -= this.gameSpeed;
                    });
                    this.obstacles = this.obstacles.filter(obstacle => obstacle.x + obstacle.width > 0);
                    
                    // Update coins
                    this.coins.forEach(coin => {
                        coin.x -= this.gameSpeed;
                        coin.rotation += 0.1;
                    });
                    this.coins = this.coins.filter(coin => coin.x + coin.width > 0);
                    
                    // Generate obstacles
                    if (Math.random() < 0.02) {
                        this.generateObstacle();
                    }
                    
                    // Generate coins
                    if (Math.random() < 0.03) {
                        this.generateCoin();
                    }
                    
                    // Check collisions
                    this.checkCollisions();
                    
                    // Update score
                    this.score += 1;
                    this.gameSpeed += 0.001; // Gradually increase speed
                    
                    // Update score display
                    document.getElementById('score-display').textContent = `Score: ${Math.floor(this.score)}`;
                }
                
                generateObstacle() {
                    const lane = Math.floor(Math.random() * 3);
                    const types = ['barrier', 'train', 'sign'];
                    const type = types[Math.floor(Math.random() * types.length)];
                    
                    this.obstacles.push({
                        x: this.gameWidth,
                        y: type === 'barrier' ? 280 : 250,
                        width: type === 'train' ? 80 : 40,
                        height: type === 'train' ? 100 : 80,
                        lane: lane,
                        type: type,
                        color: type === 'train' ? '#E74C3C' : type === 'barrier' ? '#F39C12' : '#9B59B6'
                    });
                }
                
                generateCoin() {
                    const lane = Math.floor(Math.random() * 3);
                    this.coins.push({
                        x: this.gameWidth,
                        y: 200 + Math.random() * 100,
                        width: 20,
                        height: 20,
                        lane: lane,
                        rotation: 0,
                        collected: false
                    });
                }
                
                checkCollisions() {
                    // Check obstacle collisions
                    this.obstacles.forEach(obstacle => {
                        if (this.isColliding(this.player, obstacle)) {
                            this.endGame();
                        }
                    });
                    
                    // Check coin collisions
                    this.coins.forEach(coin => {
                        if (!coin.collected && this.isColliding(this.player, coin)) {
                            coin.collected = true;
                            this.score += 50;
                            // Remove collected coin
                            const index = this.coins.indexOf(coin);
                            this.coins.splice(index, 1);
                        }
                    });
                }
                
                isColliding(rect1, rect2) {
                    return rect1.x < rect2.x + rect2.width &&
                           rect1.x + rect1.width > rect2.x &&
                           rect1.y < rect2.y + rect2.height &&
                           rect1.y + rect1.height > rect2.y;
                }
                
                endGame() {
                    this.gameOver = true;
                    
                    // Update high score
                    if (this.score > this.highScore) {
                        this.highScore = Math.floor(this.score);
                        localStorage.setItem('subwaySurfersHighScore', this.highScore);
                        document.getElementById('high-score-display').textContent = `High Score: ${this.highScore}`;
                    }
                    
                    // Submit score to backend
                    this.submitScore(Math.floor(this.score));
                }
                
                async submitScore(score) {
                    try {
                        await fetch('/api/scores/submit', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ score: score })
                        });
                    } catch (error) {
                        console.error('Failed to submit score:', error);
                    }
                }
                
                render() {
                    // Clear canvas
                    this.ctx.clearRect(0, 0, this.gameWidth, this.gameHeight);
                    
                    // Draw background
                    const gradient = this.ctx.createLinearGradient(0, 0, 0, this.gameHeight);
                    gradient.addColorStop(0, '#87CEEB');
                    gradient.addColorStop(1, '#98FB98');
                    this.ctx.fillStyle = gradient;
                    this.ctx.fillRect(0, 0, this.gameWidth, this.gameHeight);
                    
                    // Draw lanes
                    this.ctx.strokeStyle = '#34495E';
                    this.ctx.lineWidth = 3;
                    this.ctx.setLineDash([10, 10]);
                    for (let i = 1; i < 3; i++) {
                        const x = this.lanes[i] - 75;
                        this.ctx.beginPath();
                        this.ctx.moveTo(x, 0);
                        this.ctx.lineTo(x, this.gameHeight);
                        this.ctx.stroke();
                    }
                    this.ctx.setLineDash([]);
                    
                    // Draw ground
                    this.ctx.fillStyle = '#2C3E50';
                    this.ctx.fillRect(0, 360, this.gameWidth, 40);
                    
                    // Draw player
                    this.ctx.fillStyle = this.player.color;
                    this.ctx.fillRect(this.player.x - this.player.width/2, this.player.y - this.player.height, 
                                     this.player.width, this.player.height);
                    
                    // Draw player details (simple character)
                    this.ctx.fillStyle = '#2C3E50';
                    this.ctx.fillRect(this.player.x - 15, this.player.y - 50, 30, 20); // Head
                    this.ctx.fillStyle = '#FFFFFF';
                    this.ctx.fillRect(this.player.x - 10, this.player.y - 45, 8, 8); // Eyes
                    this.ctx.fillRect(this.player.x + 2, this.player.y - 45, 8, 8);
                    
                    // Draw obstacles
                    this.obstacles.forEach(obstacle => {
                        this.ctx.fillStyle = obstacle.color;
                        this.ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
                        
                        // Add details based on type
                        if (obstacle.type === 'train') {
                            this.ctx.fillStyle = '#FFFFFF';
                            this.ctx.fillRect(obstacle.x + 10, obstacle.y + 10, 60, 20);
                            this.ctx.fillStyle = '#2C3E50';
                            this.ctx.fillRect(obstacle.x + 5, obstacle.y + 80, 20, 20);
                            this.ctx.fillRect(obstacle.x + 55, obstacle.y + 80, 20, 20);
                        }
                    });
                    
                    // Draw coins
                    this.coins.forEach(coin => {
                        this.ctx.save();
                        this.ctx.translate(coin.x + coin.width/2, coin.y + coin.height/2);
                        this.ctx.rotate(coin.rotation);
                        this.ctx.fillStyle = '#F1C40F';
                        this.ctx.fillRect(-coin.width/2, -coin.height/2, coin.width, coin.height);
                        this.ctx.fillStyle = '#F39C12';
                        this.ctx.fillRect(-coin.width/2 + 3, -coin.height/2 + 3, coin.width - 6, coin.height - 6);
                        this.ctx.restore();
                    });
                    
                    // Draw game over screen
                    if (this.gameOver) {
                        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                        this.ctx.fillRect(0, 0, this.gameWidth, this.gameHeight);
                        
                        this.ctx.fillStyle = '#FFFFFF';
                        this.ctx.font = 'bold 48px Arial';
                        this.ctx.textAlign = 'center';
                        this.ctx.fillText('GAME OVER', this.gameWidth/2, this.gameHeight/2 - 50);
                        
                        this.ctx.font = '24px Arial';
                        this.ctx.fillText(`Final Score: ${Math.floor(this.score)}`, this.gameWidth/2, this.gameHeight/2);
                        this.ctx.fillText('Press R to Restart', this.gameWidth/2, this.gameHeight/2 + 50);
                    }
                    
                    // Draw pause screen
                    if (this.paused && !this.gameOver) {
                        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
                        this.ctx.fillRect(0, 0, this.gameWidth, this.gameHeight);
                        
                        this.ctx.fillStyle = '#FFFFFF';
                        this.ctx.font = 'bold 36px Arial';
                        this.ctx.textAlign = 'center';
                        this.ctx.fillText('PAUSED', this.gameWidth/2, this.gameHeight/2);
                        this.ctx.font = '18px Arial';
                        this.ctx.fillText('Press P to Resume', this.gameWidth/2, this.gameHeight/2 + 40);
                    }
                }
                
                gameLoop() {
                    if (!this.paused) {
                        this.update();
                        this.render();
                        
                        if (!this.gameOver) {
                            requestAnimationFrame(() => this.gameLoop());
                        }
                    }
                }
            }
            
            // Initialize game
            let game;
            
            function startGame() {
                if (!game) {
                    game = new SubwaySurfersGame();
                }
                game.start();
            }
            
            // Initialize when page loads
            document.addEventListener('DOMContentLoaded', function() {
                game = new SubwaySurfersGame();
            });
        </script>
    ''')

@ui.page('/leaderboard')
def leaderboard():
    ui.add_head_html('<title>Leaderboard - Subway Surfers</title>')
    
    with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
        ui.label('🏆 LEADERBOARD').classes('text-4xl font-bold text-center mb-8')
        
        # Leaderboard will be populated via API call
        ui.html('<div id="leaderboard-content">Loading...</div>')
        
        ui.button('Back to Game', on_click=lambda: ui.open('/')).classes('mt-4')
    
    ui.run_javascript('''
        async function loadLeaderboard() {
            try {
                const response = await fetch('/api/scores/leaderboard');
                const scores = await response.json();
                
                let html = '<div class="space-y-4">';
                scores.forEach((score, index) => {
                    html += `
                        <div class="flex justify-between items-center p-4 bg-white rounded-lg shadow">
                            <span class="font-bold text-lg">#${index + 1}</span>
                            <span class="text-xl">${score.score}</span>
                            <span class="text-gray-500">${new Date(score.created_at).toLocaleDateString()}</span>
                        </div>
                    `;
                });
                html += '</div>';
                
                document.getElementById('leaderboard-content').innerHTML = html;
            } catch (error) {
                document.getElementById('leaderboard-content').innerHTML = 
                    '<p class="text-red-500">Failed to load leaderboard</p>';
            }
        }
        
        loadLeaderboard();
    ''')