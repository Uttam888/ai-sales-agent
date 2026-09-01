from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.property import Property


router = APIRouter(
    prefix="/api/properties",
    tags=["Properties"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_properties(
    db: Session = Depends(get_db)
):
    properties = (
        db.query(Property)
        .order_by(Property.id.asc())
        .all()
    )

    return {
        "count": len(properties),
        "properties": [
            {
                "id": property_item.id,
                "title": property_item.title,
                "location": property_item.location,
                "property_type": property_item.property_type,
                "price": property_item.price,
                "bedrooms": property_item.bedrooms,
                "bathrooms": property_item.bathrooms,
                "area_sqft": property_item.area_sqft,
                "description": property_item.description,
                "amenities": property_item.amenities,
                "available": property_item.available,
            }
            for property_item in properties
        ],
    }
