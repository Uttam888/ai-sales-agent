from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from app.db.database import Base


class CommunicationHistory(Base):

    __tablename__ = "communication_history"

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

    follow_up_id = Column(
        Integer,
        ForeignKey("follow_ups.id"),
        nullable=True,
        index=True
    )

    channel = Column(
        String(50),
        nullable=False
    )

    direction = Column(
        String(20),
        nullable=False,
        default="outbound"
    )

    message = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="sent"
    )

    sent_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )