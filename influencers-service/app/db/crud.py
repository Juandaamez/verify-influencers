from sqlalchemy.orm import Session
from app.db.models import Influencer, Claim

# CRUD Influencers
def get_influencers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Influencer).offset(skip).limit(limit).all()

def create_influencer(db: Session, name: str, handle: str, followers_count: int, description: str, platform: str):
    db_influencer = Influencer(
        name=name,
        handle=handle,
        followers_count=followers_count,
        description=description,
        platform=platform,
    )
    db.add(db_influencer)
    db.commit()
    db.refresh(db_influencer)
    return db_influencer

# CRUD Claims
def get_claims(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Claim).offset(skip).limit(limit).all()

def create_claim(db: Session, claim_text: str, category: str, status: str, confidence_score: int, influencer_id: int):
    db_claim = Claim(
        claim_text=claim_text,
        category=category,
        status=status,
        confidence_score=confidence_score,
        influencer_id=influencer_id,
    )
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim
