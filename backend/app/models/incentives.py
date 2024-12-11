from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Assuming you have a database.py file that initializes SQLAlchemy

class Incentive(Base):
    __tablename__ = 'incentives'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    value = Column(Float, nullable=False)  # Value of the incentive (e.g., in currency or points)
    type = Column(String(50), nullable=False)  # Type of incentive (e.g., 'cash', 'points', 'discount')
    eligibility_criteria = Column(String(255), nullable=True)  # Criteria for eligibility
    expiration_date = Column(DateTime, nullable=True)  # Expiration date of the incentive
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Assuming you have a User model
    user = relationship("User ", back_populates="incentives")  # Relationship with User model

    def __repr__(self):
        return f"<Incentive(name={self.name}, value={self.value}, type={self.type})>"

    def is_active(self):
        """Check if the incentive is still active based on the expiration date."""
        if self.expiration_date:
            return self.expiration_date > datetime.utcnow()
        return True  # If no expiration date, consider it active

# Example of a User model for relationship context
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    incentives = relationship("Incentive", back_populates="user")

    def __repr__(self):
        return f"<User (username={self.username})>"
