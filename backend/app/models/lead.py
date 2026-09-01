from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from app.db.database import Base


class Lead(Base):

    __tablename__ = "leads"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=True
    )

    email = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    requirement = Column(
        String,
        nullable=False
    )

    budget = Column(
        String,
        nullable=True
    )

    location = Column(
        String,
        nullable=True
    )

    property_type = Column(
        String,
        nullable=True
    )

    purpose = Column(
        String,
        nullable=True
    )

    timeline = Column(
        String,
        nullable=True
    )

    buying_intent = Column(
        String,
        nullable=True
    )

    qualification_status = Column(
        String,
        nullable=True,
        default="new"
    )

    lead_score = Column(
        Integer,
        nullable=False,
        default=0
    )

    pipeline_stage = Column(
        String,
        nullable=False,
        default="NEW"
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )