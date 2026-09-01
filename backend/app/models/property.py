from sqlalchemy import Column, Integer, String, Text, Boolean

from app.db.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    location = Column(
        String(255),
        nullable=False,
        index=True
    )

    property_type = Column(
        String(100),
        nullable=False,
        index=True
    )

    price = Column(
        String(100),
        nullable=False
    )

    bedrooms = Column(
        Integer,
        nullable=True
    )

    bathrooms = Column(
        Integer,
        nullable=True
    )

    area_sqft = Column(
        Integer,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    amenities = Column(
        Text,
        nullable=True
    )

    available = Column(
        Boolean,
        default=True,
        nullable=False
    )