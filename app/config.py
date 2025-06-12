from pydantic_settings import BaseSettings
from typing import Optional

class GameSettings(BaseSettings):
    # Game Configuration
    GAME_WIDTH: int = 800
    GAME_HEIGHT: int = 600
    FPS: int = 60
    
    # Player Settings
    PLAYER_WIDTH: int = 40
    PLAYER_HEIGHT: int = 60
    PLAYER_SPEED: int = 8
    JUMP_FORCE: int = 15
    GRAVITY: float = 0.8
    
    # Game Mechanics
    GAME_SPEED: int = 6
    OBSTACLE_SPAWN_RATE: float = 0.02
    COIN_SPAWN_RATE: float = 0.015
    SPEED_INCREASE_RATE: float = 0.001
    
    # Visual Settings
    BACKGROUND_COLOR: str = "#87CEEB"
    PLAYER_COLOR: str = "#FF6B35"
    OBSTACLE_COLOR: str = "#2E86AB"
    COIN_COLOR: str = "#FFD23F"
    GROUND_COLOR: str = "#8B4513"
    
    class Config:
        env_file = ".env"

settings = GameSettings()