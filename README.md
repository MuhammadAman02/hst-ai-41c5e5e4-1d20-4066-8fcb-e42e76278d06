# 🚇 Subway Surfers - Endless Runner Game

A thrilling endless runner game inspired by Subway Surfers, built with Python and NiceGUI!

## 🎮 Game Features

- **Smooth 60fps gameplay** with responsive controls
- **Endless running** with progressively increasing difficulty
- **Jump mechanics** with realistic physics and gravity
- **Obstacle avoidance** with dynamic barrier generation
- **Coin collection** system with bonus scoring
- **Beautiful graphics** with parallax scrolling background
- **Real-time scoring** tracking distance, coins, and points

## 🕹️ Controls

- **← → or A/D**: Move left and right
- **↑ or SPACE**: Jump over obstacles
- **P**: Pause/Resume game
- **R**: Restart game (when game over)

## 🚀 Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the game**:
   ```bash
   python main.py
   ```

3. **Open browser** to `http://localhost:8000`

4. **Start playing immediately!** 🎯

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t subway-surfers .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 subway-surfers
   ```

### Fly.io Deployment

1. **Install Fly CLI** and authenticate:
   ```bash
   curl -L https://fly.io/install.sh | sh
   flyctl auth login
   ```

2. **Deploy the app**:
   ```bash
   flyctl deploy
   ```

3. **Open your deployed game**:
   ```bash
   flyctl open
   ```

## 🎨 Game Mechanics

- **Progressive Difficulty**: Speed increases as you play longer
- **Smart Obstacle Spawning**: Random but balanced obstacle generation
- **Coin Distribution**: Strategic coin placement for risk/reward gameplay
- **Score System**: Points for distance + bonus for coins (10 points each)
- **Collision Detection**: Precise collision system with game over on impact

## 🏗️ Technical Architecture

- **Real-time Game Engine**: Custom physics simulation with 60fps performance
- **Entity Management**: Modular system for players, obstacles, and collectibles
- **Async Game Loop**: Non-blocking game updates using asyncio
- **SVG Rendering**: Scalable vector graphics for crisp visuals
- **Event-Driven Input**: Responsive keyboard controls with proper state management

## 🎯 Gameplay Tips

1. **Timing is Key**: Jump at the right moment to clear obstacles
2. **Collect Coins**: They're worth 10 points each and boost your score
3. **Stay Alert**: The game gets faster as your score increases
4. **Use the Edges**: Sometimes moving to the sides is safer than jumping
5. **Practice Makes Perfect**: Learn the obstacle patterns for higher scores

## 🔧 Configuration

The game uses environment variables for configuration:

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `ENVIRONMENT`: Environment mode (default: production)

## 📊 Scoring System

- **Distance**: 1 point per unit traveled
- **Coins**: 10 points per coin collected
- **Survival Bonus**: Longer survival = higher multiplier

## 🎪 Visual Features

- **Vibrant Color Scheme**: Inspired by the original Subway Surfers
- **Parallax Scrolling**: Dynamic cityscape background with buildings
- **Animated Character**: Detailed player sprite with visual feedback
- **Dynamic Obstacles**: Varied obstacle designs with visual depth
- **Glowing Coins**: Eye-catching collectibles with golden shine
- **Smooth Ground Patterns**: Scrolling track elements for immersion

Ready to start your endless running adventure? 🏃‍♂️💨

## 🐛 Troubleshooting

If you encounter any issues:

1. **Check Python Version**: Ensure you're using Python 3.11+
2. **Verify Dependencies**: Run `pip install -r requirements.txt`
3. **Port Conflicts**: Change the PORT environment variable if 8000 is in use
4. **Browser Compatibility**: Use a modern browser with JavaScript enabled

Enjoy the game! 🎮✨