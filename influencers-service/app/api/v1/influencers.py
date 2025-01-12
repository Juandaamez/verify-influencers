import logging
from fastapi import APIRouter, Depends, HTTPException, Body
import openai
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Influencer, Claim
from app.services.twitter_client import fetch_tweets
from app.services.claim_processing import extract_claims, verify_claim
from app.core.security import get_current_user

router = APIRouter()

@router.get("/all", tags=["Influencers"])
def get_all_influencers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    influencers = db.query(Influencer).all()
    if not influencers:
        raise HTTPException(status_code=404, detail="No influencers found.")
    
    return [
        {
            "id": influencer.id,
            "name": influencer.name,
            "handle": influencer.handle,
            "followers_count": influencer.followers_count,
        }
        for influencer in influencers
    ]

@router.post("/discover", tags=["Influencers"])
def discover_influencers(
    keywords: list[str] = Body(
        ...,
        example=["health", "wellness"]
    ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    new_influencers = fetch_tweets(keywords)
    for influencer_data in new_influencers:
        influencer = Influencer(
            name=influencer_data["name"],
            handle=influencer_data["handle"],
            followers_count=influencer_data["followers_count"]
        )
        db.add(influencer)
    db.commit()
    return {"message": "New influencers discovered.", "count": len(new_influencers)}

@router.post("/analyze", tags=["Influencers"])
def analyze_influencer(
    influencer_id: int,
    time_range: str,
    claims_to_analyze: int,
    journals: list[str],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    influencer = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found.")

    try:
        tweets = fetch_tweets([influencer.handle])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tweets: {str(e)}")

    processed_claims = []
    for tweet in tweets[:claims_to_analyze]:
        claims = extract_claims(tweet["text"])
        for claim_text in claims:
            verification = verify_claim(claim_text, journals)
            processed_claims.append({
                "claim_text": claim_text,
                "status": verification["status"],
                "confidence_score": verification["confidence_score"]
            })

    trust_score = sum(c["confidence_score"] for c in processed_claims) / len(processed_claims) if processed_claims else 0

    return {
        "message": "Analysis completed.",
        "influencer_id": influencer_id,
        "trust_score": trust_score,
        "processed_claims": processed_claims
    }

@router.get("/leaderboard", tags=["Influencers"])
def leaderboard(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    influencers = db.query(Influencer).all()

    if not influencers:
        return {
            "leaderboard": [],
            "statistics": {
                "active_influencers": 0,
                "claims_verified": 0,
                "average_trust_score": 0,
            }
        }

    leaderboard = []
    total_followers = 0
    total_claims = 0
    total_scores = 0

    for influencer in influencers:
        claims = influencer.claims
        claims_count = len(claims)
        total_followers += influencer.followers_count
        total_claims += claims_count
        average_score = (
            sum(claim.confidence_score for claim in claims) / claims_count
            if claims_count > 0 else 0
        )
        total_scores += average_score

        leaderboard.append({
            "id": influencer.id,
            "name": influencer.name,
            "category": influencer.category,
            "followers_count": influencer.followers_count,
            "average_score": average_score,
        })

    leaderboard.sort(key=lambda x: x["average_score"], reverse=True)

    average_trust_score = (total_scores / len(influencers)) if influencers else 0

    return {
        "leaderboard": leaderboard,
        "statistics": {
            "active_influencers": len(influencers),
            "claims_verified": total_claims,
            "average_trust_score": round(average_trust_score, 2),
        }
    }

@router.get("/{influencer_id}", tags=["Influencers"])
def get_influencer_details(
    influencer_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    influencer = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found.")

    return {
        "id": influencer.id,
        "name": influencer.name,
        "handle": influencer.handle,  # Agregado
        "description": influencer.description,  # Agregado
        "category": influencer.category,
        "followers_count": influencer.followers_count,
        "average_score": sum(claim.confidence_score for claim in influencer.claims) / len(influencer.claims)
        if influencer.claims else 0,
    }


@router.get("/{influencer_id}/claims", tags=["Influencers"])
def get_claims_by_influencer(
    influencer_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Protegido
):

    influencer = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found.")

    claims = db.query(Claim).filter(Claim.influencer_id == influencer_id).all()
    if not claims:
        return {"message": "No claims found for this influencer.", "claims": []}

    return {
        "influencer_id": influencer_id,
        "claims": [
            {
                "id": claim.id,
                "claim_text": claim.claim_text,
                "confidence_score": claim.confidence_score,
                "date": claim.date.isoformat(),
            }
            for claim in claims
        ],
    }

