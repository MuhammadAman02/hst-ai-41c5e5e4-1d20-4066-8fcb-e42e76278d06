from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
import time
from collections import defaultdict

from core.database import get_db
from models.schemas import ScoreSubmission, ScoreResponse, LeaderboardResponse
from models.database_models import Score

router = APIRouter()

# Simple rate limiting (in production, use Redis or similar)
rate_limit_store = defaultdict(list)

def check_rate_limit(ip: str, limit: int = 5, window: int = 60) -> bool:
    """Simple rate limiting check"""
    now = time.time()
    # Clean old entries
    rate_limit_store[ip] = [timestamp for timestamp in rate_limit_store[ip] if now - timestamp < window]
    
    if len(rate_limit_store[ip]) >= limit:
        return False
    
    rate_limit_store[ip].append(now)
    return True

@router.post("/submit", response_model=ScoreResponse)
async def submit_score(
    score_data: ScoreSubmission,
    request: Request,
    db: Session = Depends(get_db)
):
    """Submit a new score"""
    client_ip = request.client.host
    
    # Rate limiting
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many score submissions. Please wait.")
    
    # Basic validation
    if score_data.score < 0:
        raise HTTPException(status_code=400, detail="Score cannot be negative")
    
    if score_data.score > 1000000:  # Reasonable upper limit
        raise HTTPException(status_code=400, detail="Score seems unrealistic")
    
    # Create new score entry
    new_score = Score(
        score=score_data.score,
        player_name=score_data.player_name,
        ip_address=client_ip
    )
    
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    
    return ScoreResponse(
        id=new_score.id,
        score=new_score.score,
        player_name=new_score.player_name,
        created_at=new_score.created_at
    )

@router.get("/leaderboard", response_model=List[ScoreResponse])
async def get_leaderboard(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get the leaderboard"""
    scores = db.query(Score).order_by(desc(Score.score)).offset(offset).limit(limit).all()
    
    return [
        ScoreResponse(
            id=score.id,
            score=score.score,
            player_name=score.player_name or "Anonymous",
            created_at=score.created_at
        )
        for score in scores
    ]

@router.get("/leaderboard/full", response_model=LeaderboardResponse)
async def get_full_leaderboard(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get full leaderboard with metadata"""
    scores = db.query(Score).order_by(desc(Score.score)).offset(offset).limit(limit).all()
    total_count = db.query(Score).count()
    
    score_responses = [
        ScoreResponse(
            id=score.id,
            score=score.score,
            player_name=score.player_name or "Anonymous",
            created_at=score.created_at
        )
        for score in scores
    ]
    
    return LeaderboardResponse(
        scores=score_responses,
        total_count=total_count
    )

@router.get("/personal-best/{player_name}")
async def get_personal_best(player_name: str, db: Session = Depends(get_db)):
    """Get personal best score for a player"""
    best_score = db.query(Score).filter(
        Score.player_name == player_name
    ).order_by(desc(Score.score)).first()
    
    if not best_score:
        raise HTTPException(status_code=404, detail="No scores found for this player")
    
    return ScoreResponse(
        id=best_score.id,
        score=best_score.score,
        player_name=best_score.player_name,
        created_at=best_score.created_at
    )

@router.delete("/scores/{score_id}")
async def delete_score(score_id: int, db: Session = Depends(get_db)):
    """Delete a score (admin function)"""
    score = db.query(Score).filter(Score.id == score_id).first()
    
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    
    db.delete(score)
    db.commit()
    
    return {"message": "Score deleted successfully"}