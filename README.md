# 🚇 Subway Surfers - Endless Runner Game

A thrilling endless runner game inspired by Subway Surfers, built with Python and NiceGUI. Run, jump, and collect coins while avoiding obstacles in this fast-paced adventure!

## 🎮 Game Features

- **Endless Running**: Infinite gameplay with increasing difficulty
- **Smooth Controls**: Responsive keyboard controls for fluid movement
- **Obstacle Avoidance**: Dynamic obstacles that require quick reflexes
- **Coin Collection**: Collect golden coins for bonus points
- **Progressive Difficulty**: Game speed increases as you progress
- **Beautiful Graphics**: Colorful, cartoon-style visuals
- **Score Tracking**: Track your distance, score, and coins collected

## 🎯 How to Play

### Controls
- **← → or A D**: Move left and right
- **↑ or SPACE**: Jump over obstacles
- **P**: Pause/Resume game

### Objective
- Avoid hitting obstacles by moving or jumping
- Collect golden coins for extra points
- Survive as long as possible to achieve a high score
- The game gets faster and more challenging over time!

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation & Running

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the game**:
   ```bash
   python main.py
   ```
4. **Open your browser** and go to `http://localhost:8000`
5. **Start playing immediately!**

## 🎨 Game Mechanics

### Player Character
- Animated character with smooth movement
- Jump physics with gravity
- Collision detection with obstacles and coins

### Obstacles
- Randomly generated barriers
- Various sizes and positions
- Must be avoided to continue playing

### Coins
- Golden collectibles scattered throughout the level
- Each coin adds 10 points to your score
- Bonus scoring system for coin collection

### Scoring System
- **Distance Points**: 1 point per game tick
- **Coin Bonus**: 10 points per coin collected
- **Progressive Speed**: Game speed increases over time

## 🏗️ Technical Architecture

### Game Engine
- **Real-time Game Loop**: 60 FPS smooth gameplay
- **Physics System**: Gravity, collision detection, movement
- **Entity Management**: Player, obstacles, coins, background
- **State Management**: Game state, scoring, input handling

### Technologies Used
- **NiceGUI**: Modern Python web UI framework
- **Canvas Rendering**: HTML5 Canvas for smooth graphics
- **Async Programming**: Non-blocking game loop
- **Pydantic**: Data validation and settings management

## 🎪 Game Components

### Entities
- **Player**: Main character with movement and jumping
- **Obstacles**: Dynamic barriers to avoid
- **Coins**: Collectible items for bonus points
- **Background**: Parallax scrolling cityscape

### Systems
- **Input System**: Keyboard event handling
- **Physics System**: Collision detection and movement
- **Rendering System**: Canvas-based graphics
- **Scoring System**: Points and statistics tracking

## 🔧 Configuration

Game settings can be customized in `app/config.py`:

```python
# Game dimensions
GAME_WIDTH = 800
GAME_HEIGHT = 600

# Player settings
PLAYER_SPEED = 8
JUMP_FORCE = 15

# Game mechanics
GAME_SPEED = 6
OBSTACLE_SPAWN_RATE = 0.02
COIN_SPAWN_RATE = 0.015
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Docker Deployment
```bash
docker build -t subway-surfers .
docker run -p 8000:8000 subway-surfers
```

### Fly.io Deployment
```bash
fly deploy
```

## 🎯 Game Tips

1. **Master the Controls**: Practice moving and jumping smoothly
2. **Watch Ahead**: Look for upcoming obstacles and plan your moves
3. **Collect Coins**: They provide significant bonus points
4. **Stay Calm**: The game gets faster, but panic leads to mistakes
5. **Practice Timing**: Learn the jump timing for different obstacles

## 🏆 High Score Strategies

- **Coin Priority**: Focus on collecting coins when safe
- **Risk Management**: Don't risk collision for coins
- **Pattern Recognition**: Learn common obstacle patterns
- **Consistent Movement**: Smooth, controlled movements are key

## 🎨 Visual Design

The game features a vibrant, cartoon-style aesthetic inspired by Subway Surfers:
- **Bright Color Palette**: Blues, oranges, yellows, and greens
- **Parallax Background**: Moving cityscape with buildings and clouds
- **Smooth Animations**: 60 FPS gameplay with fluid character movement
- **Visual Effects**: Coin shine effects and detailed character sprites

## 🔄 Game Loop

1. **Input Processing**: Handle keyboard events
2. **Physics Update**: Apply gravity, movement, collision detection
3. **Entity Management**: Spawn/remove obstacles and coins
4. **Rendering**: Draw all game elements on canvas
5. **Score Update**: Calculate points and statistics
6. **State Management**: Handle game over, pause, restart

## 🎵 Future Enhancements

Potential features for future versions:
- Sound effects and background music
- Power-ups and special abilities
- Multiple characters to choose from
- Different environments and themes
- Leaderboard system
- Mobile touch controls
- Particle effects and animations

## 🐛 Troubleshooting

### Common Issues
- **Game not starting**: Check Python version (3.10+ required)
- **Slow performance**: Close other browser tabs, check system resources
- **Controls not working**: Click on the game area to focus
- **Display issues**: Try refreshing the browser page

### Performance Tips
- Use a modern web browser (Chrome, Firefox, Safari)
- Close unnecessary applications
- Ensure stable internet connection
- Clear browser cache if needed

## 📝 License

This project is created for educational and entertainment purposes. Inspired by the original Subway Surfers game.

---

**Ready to run? Start your endless adventure now!** 🏃‍♂️💨

Enjoy the game and try to beat your high score! 🏆