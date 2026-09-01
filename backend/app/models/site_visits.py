from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from app.db.database import Base


class SiteVisit(Base):

    __tablename__ = "site_visits"


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
    # PROPERTY ID
    # ========================================================

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        nullable=False,
        index=True
    )


    # ========================================================
    # VISIT DATE
    # ========================================================

    visit_date = Column(
        DateTime,
        nullable=False
    )


    # ========================================================
    # STATUS
    # ========================================================

    status = Column(
        String(50),
        nullable=False,
        default="scheduled"
    )


    # ========================================================
    # NOTES
    # ========================================================

    notes = Column(
        Text,
        nullable=True
    )