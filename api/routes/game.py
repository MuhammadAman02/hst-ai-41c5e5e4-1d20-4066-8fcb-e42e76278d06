from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from core.database import get_db
from models.schemas import GameState, GameStats
from models.database_models import GameSession, Score

router = APIRouter()

@router.post("/start-session")
async def start_game_session(db: Session = Depends(get_db)):
    """Start a new game session"""
    session_id = str(uuid.uuid4())
    
    game_session = GameSession(
        session_id=session_id,
        start_time=datetime.utcnow()
    )
    
    db.add(game_session)
    db.commit()
    db.refresh(game_session)
    
    return {"session_id": session_id, "message": "Game session started"}

@router.put("/update-session/{session_id}")
async def update_game_session(
    session_id: str,
    game_state: GameState,
    db: Session = Depends(get_db)
):
    """Update game session with current state"""
    session = db.query(GameSession).filter(GameSession.session_id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    # Update session with current game state
    session.max_speed = max(session.max_speed or 0, game_state.game_speed)
    session.coins_collected = len([coin for coin in game_state.coins if coin.get('collected', False)])
    
    db.commit()
    
    return {"message": "Game session updated"}

@router.post("/end-session/{session_id}")
async def end_game_session(
    session_id: str,
    final_score: int,
    db: Session = Depends(get_db)
):
    """End a game session"""
    session = db.query(GameSession).filter(GameSession.session_id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    session.end_time = datetime.utcnow()
    session.final_score = final_score
    session.completed = True
    
    db.commit()
    
    return {"message": "Game session ended", "final_score": final_score}

@router.get("/stats", response_model=GameStats)
async def get_game_stats(db: Session = Depends(get_db)):
    """Get overall game statistics"""
    total_games = db.query(GameSession).filter(GameSession.completed == True).count()
    
    scores = db.query(Score.score).all()
    if scores:
        average_score = sum(score[0] for score in scores) / len(scores)
        highest_score = max(score[0] for score in scores)
    else:
        average_score = 0
        highest_score = 0
    
    total_players = db.query(Score).count()
    
    return GameStats(
        total_games=total_games,
        average_score=round(average_score, 2),
        highest_score=highest_score,
        total_players=total_players
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}