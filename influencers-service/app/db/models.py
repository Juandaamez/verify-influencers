from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    handle = Column(String, unique=True, nullable=False)
    followers_count = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)

    claims = relationship("Claim", back_populates="influencer")

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_text = Column(String, nullable=False)
    confidence_score = Column(Integer, nullable=False)
    influencer_id = Column(Integer, ForeignKey("influencers.id"), nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    influencer = relationship("Influencer", back_populates="claims")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    is_admin = Column(Integer, default=0)  # 1 for admin, 0 for regular user
