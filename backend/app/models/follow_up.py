from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from app.db.database import Base


class FollowUp(Base):

    __tablename__ = "follow_ups"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False,
        index=True
    )

    follow_up_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="pending"
    )

    message = Column(
        Text,
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )