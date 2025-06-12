from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ScoreSubmission(BaseModel):
    score: int = Field(..., ge=0, description="Player's score")
    player_name: Optional[str] = Field(None, max_length=50, description="Player's name")

class ScoreResponse(BaseModel):
    id: int
    score: int
    player_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class LeaderboardResponse(BaseModel):
    scores: List[ScoreResponse]
    total_count: int

class GameState(BaseModel):
    player_x: float
    player_y: float
    player_lane: int
    score: int
    game_speed: float
    obstacles: List[dict]
    coins: List[dict]

class GameStats(BaseModel):
    total_games: int
    average_score: float
    highest_score: int
    total_players: int