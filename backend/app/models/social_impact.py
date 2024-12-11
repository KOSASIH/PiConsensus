from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Assuming you have a Base class for your SQLAlchemy models

class SocialImpact(Base):
    __tablename__ = 'social_impacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    impact_score = Column(Float, nullable=False)  # A score representing the impact
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Assuming you have a User model

    user = relationship("User ", back_populates="social_impacts")  # Establishing a relationship with User

    def __repr__(self):
        return f"<SocialImpact(id={self.id}, project_name={self.project_name}, impact_score={self.impact_score})>"

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            "id": self.id,
            "project_name": self.project_name,
            "description": self.description,
            "impact_score": self.impact_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": self.user_id
  }
