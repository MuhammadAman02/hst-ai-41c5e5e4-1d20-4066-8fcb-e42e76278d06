from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from core.database import Base

class Score(Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False, index=True)
    player_name = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45), nullable=True)  # For basic spam prevention
    
class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    final_score = Column(Integer, nullable=True)
    max_speed = Column(Float, nullable=True)
    coins_collected = Column(Integer, default=0)
    obstacles_avoided = Column(Integer, default=0)
    completed = Column(Boolean, default=False)