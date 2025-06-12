# 🎮 Subway Surfers - Epic Endless Runner

A thrilling Subway Surfers-inspired endless runner game built with **React frontend** and **Python backend**!

## 🚀 Features

### 🎯 **Immediate Gameplay**
- **Smooth 60fps gameplay** with responsive controls
- **Progressive difficulty** - speed increases as you survive longer
- **Multiple lanes** - dodge left and right to avoid obstacles
- **Jump mechanics** - leap over barriers and trains
- **Coin collection** - gather coins for bonus points

### 🏆 **Backend Features**
- **Real-time leaderboard** with persistent scoring
- **Game session tracking** with detailed statistics
- **Rate limiting** to prevent score manipulation
- **RESTful API** for frontend-backend communication
- **SQLite database** with easy PostgreSQL migration

### 🎨 **Visual Excellence**
- **Vibrant graphics** inspired by Subway Surfers aesthetic
- **Smooth animations** with parallax scrolling effects
- **Dynamic obstacles** - trains, barriers, and signs
- **Glowing coins** with rotation animations
- **Professional UI** with game over and pause screens

## 🎮 Controls

- **← → Arrow Keys** or **A/D**: Move left and right between lanes
- **↑ Arrow Key**, **W**, or **SPACE**: Jump over obstacles
- **P**: Pause/Resume game
- **R**: Restart after game over

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Initialize Database**
```bash
python -c "from core.database import create_tables; create_tables()"
```

### 3. **Run the Game**
```bash
python main.py
```

### 4. **Play Immediately!**
Open your browser to `http://localhost:8000` and start playing!

## 🏗️ Architecture

### **Frontend (React-like with NiceGUI)**
- **Game Engine**: Real-time Canvas-based rendering
- **Physics System**: Gravity, collision detection, smooth movement
- **State Management**: Player position, obstacles, coins, scoring
- **Input Handling**: Keyboard controls with proper event handling

### **Backend (Python FastAPI)**
- **Game API**: Session management and statistics
- **Score System**: Persistent leaderboard with validation
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Security**: Rate limiting, input validation, CORS configuration

## 📊 API Endpoints

### **Game Management**
- `POST /api/game/start-session` - Start new game session
- `PUT /api/game/update-session/{id}` - Update game state
- `POST /api/game/end-session/{id}` - End game session
- `GET /api/game/stats` - Get overall game statistics

### **Scoring System**
- `POST /api/scores/submit` - Submit new score
- `GET /api/scores/leaderboard` - Get top scores
- `GET /api/scores/personal-best/{name}` - Get player's best score

## 🎯 Game Mechanics

### **Scoring System**
- **Distance Points**: 1 point per game tick survived
- **Coin Bonus**: 10 points per coin collected
- **Speed Multiplier**: Score increases with game speed

### **Difficulty Progression**
- **Speed Increase**: Game speed gradually increases over time
- **Obstacle Density**: More frequent obstacles as game progresses
- **Reaction Time**: Faster gameplay requires quicker reflexes

### **Collision System**
- **Precise Detection**: Pixel-perfect collision detection
- **Multiple Object Types**: Different obstacles with varying sizes
- **Invulnerability Frames**: Brief protection after power-ups

## 🐳 Deployment

### **Docker Deployment**
```bash
# Build the image
docker build -t subway-surfers .

# Run the container
docker run -p 8000:8000 subway-surfers
```

### **Fly.io Deployment**
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy to Fly.io
flyctl deploy
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Database
DATABASE_URL=sqlite:///./subway_surfers.db

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# Game Settings
MAX_LEADERBOARD_ENTRIES=100
SCORE_SUBMISSION_RATE_LIMIT=10

# Server
HOST=0.0.0.0
PORT=8000
```

## 🎮 Game Features

### **Player Mechanics**
- **Lane Switching**: Instant movement between 3 lanes
- **Jump Physics**: Realistic gravity and landing
- **Collision Response**: Immediate game over on obstacle hit
- **Visual Feedback**: Character animations and effects

### **Obstacle Types**
- **Barriers**: Standard obstacles requiring jumps or lane changes
- **Trains**: Large obstacles blocking entire lanes
- **Signs**: Medium-sized obstacles with varied placement

### **Collectibles**
- **Coins**: Rotating golden coins worth 10 points each
- **Strategic Placement**: Risk/reward positioning near obstacles
- **Visual Effects**: Shine and rotation animations

## 🏆 Leaderboard System

### **Score Validation**
- **Rate Limiting**: Prevents spam submissions
- **Reasonable Limits**: Upper bounds on achievable scores
- **IP Tracking**: Basic anti-cheat measures

### **Statistics Tracking**
- **Personal Bests**: Individual player records
- **Global Rankings**: Top scores across all players
- **Game Analytics**: Session duration, coins collected, obstacles avoided

## 🔒 Security Features

- **Input Validation**: All API inputs validated with Pydantic
- **Rate Limiting**: Prevents abuse of score submission
- **CORS Configuration**: Secure cross-origin requests
- **SQL Injection Prevention**: Parameterized queries only
- **Error Handling**: Graceful failure with user feedback

## 🎯 Performance Optimizations

- **60fps Target**: Smooth gameplay with optimized rendering
- **Efficient Collision Detection**: Fast rectangle overlap algorithms
- **Memory Management**: Proper cleanup of off-screen objects
- **Database Indexing**: Optimized queries for leaderboard
- **Async Operations**: Non-blocking API calls

## 🚀 Ready to Play!

Your Subway Surfers game is **production-ready** with:
- ✅ **Immediate playability** - works out of the box
- ✅ **Professional graphics** - smooth animations and effects
- ✅ **Persistent scoring** - leaderboard survives restarts
- ✅ **Scalable architecture** - ready for multiple players
- ✅ **Deployment ready** - Docker and Fly.io configurations included

**Start your endless running adventure now!** 🏃‍♂️💨

---

*Built with ❤️ using Python, FastAPI, NiceGUI, and modern web technologies*