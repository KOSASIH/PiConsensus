from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ProposalStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

class GovernanceProposal(Base):
    __tablename__ = 'governance_proposals'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(ProposalStatus), default=ProposalStatus.PENDING)

    creator = relationship("User ", back_populates="proposals")
    votes = relationship("Vote", back_populates="proposal")

    def __init__(self, title, description, creator_id, duration_days):
        self.title = title
        self.description = description
        self.creator_id = creator_id
        self.end_time = datetime.utcnow() + timedelta(days=duration_days)

    def is_active(self):
        """Check if the proposal is still active."""
        return datetime.utcnow() < self.end_time

    def tally_votes(self):
        """Tally votes and update the proposal status."""
        if not self.is_active():
            yes_votes = sum(1 for vote in self.votes if vote.vote_type == VoteType.YES)
            no_votes = sum(1 for vote in self.votes if vote.vote_type == VoteType.NO)

            if yes_votes > no_votes:
                self.status = ProposalStatus.APPROVED
            else:
                self.status = ProposalStatus.REJECTED
            self.end_time = datetime.utcnow()  # Mark as completed
            return self.status
        return None

class VoteType(enum.Enum):
    YES = "yes"
    NO = "no"

class Vote(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey('governance_proposals.id'), nullable=False)
    voter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("GovernanceProposal", back_populates="votes")
    voter = relationship("User ", back_populates="votes")

    def __init__(self, proposal_id, voter_id, vote_type):
        self.proposal_id = proposal_id
        self.voter_id = voter_id
        self.vote_type = vote_type

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    proposals = relationship("GovernanceProposal", back_populates="creator")
    votes = relationship("Vote", back_populates="voter")

    def __init__(self, username):
        self.username = username

# Example usage
if __name__ == "__main__":
    # This section is for demonstration purposes and should be removed in production code.
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Create a SQLite database in memory for demonstration
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a user
    user = User(username="alice")
    session.add(user)
    session.commit()

    # Create a governance proposal
    proposal = GovernanceProposal(title="Increase Block Size", description="Proposal to increase the block size limit.", creator_id=user.id, duration_days=7)
    session.add(proposal)
    session.commit()

    # User votes on the proposal
    vote = Vote(proposal_id=proposal.id, voter_id=user.id, vote_type=VoteType.YES)
    session.add(vote)
    session.commit()

    # Tally votes and update proposal status
    proposal.tally_votes()
    session.commit()

    print(f"Proposal '{proposal.title}' status: {proposal.status.value}")
