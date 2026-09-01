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


class SalesActionOutcome(Base):

    __tablename__ = "sales_action_outcomes"

    # ========================================================
    # ID
    # ========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ========================================================
    # LEAD ID
    # ========================================================

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False,
        index=True
    )

    # ========================================================
    # ACTION
    # ========================================================

    action = Column(
        String(100),
        nullable=False,
        index=True
    )

    # ========================================================
    # EXECUTION STATUS
    # ========================================================

    execution_status = Column(
        String(50),
        nullable=False,
        default="executed"
    )

    # ========================================================
    # OUTCOME
    # ========================================================

    outcome = Column(
        String(100),
        nullable=False,
        default="pending",
        index=True
    )

    # ========================================================
    # NOTES
    # ========================================================

    notes = Column(
        Text,
        nullable=True
    )

    # ========================================================
    # CREATED AT
    # ========================================================

    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    # ========================================================
    # UPDATED AT
    # ========================================================

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )
    