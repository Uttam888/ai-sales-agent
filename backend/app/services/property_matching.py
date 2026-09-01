from typing import Optional

from sqlalchemy.orm import Session

from app.models.property import Property


# ============================================================
# PROPERTY MATCHING
# ============================================================

def find_matching_properties(
    db: Session,
    location: Optional[str] = None,
    property_type: Optional[str] = None,
    budget: Optional[str] = None,
    bedrooms: Optional[int] = None,
    limit: int = 5
):
    """
    Search the real properties stored in PostgreSQL.

    Matching is intentionally flexible:
    - location uses case-insensitive partial matching
    - property type uses case-insensitive partial matching
    - bedrooms can be matched exactly
    - budget is returned to the caller for AI reasoning
      because property prices are stored as strings
    """

    query = (
        db.query(Property)
        .filter(
            Property.available == True
        )
    )

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    if location:

        query = query.filter(
            Property.location.ilike(
                f"%{location.strip()}%"
            )
        )


    # --------------------------------------------------------
    # PROPERTY TYPE
    # --------------------------------------------------------

    if property_type:

        query = query.filter(
            Property.property_type.ilike(
                f"%{property_type.strip()}%"
            )
        )


    # --------------------------------------------------------
    # BEDROOMS
    # --------------------------------------------------------

    if bedrooms is not None:

        query = query.filter(
            Property.bedrooms == bedrooms
        )


    properties = (
        query
        .limit(limit)
        .all()
    )


    # --------------------------------------------------------
    # RETURN SAFE PROPERTY DATA
    # --------------------------------------------------------

    results = []

    for property_item in properties:

        results.append({

            "id":
                property_item.id,

            "title":
                property_item.title,

            "location":
                property_item.location,

            "property_type":
                property_item.property_type,

            "price":
                property_item.price,

            "bedrooms":
                property_item.bedrooms,

            "bathrooms":
                property_item.bathrooms,

            "area_sqft":
                property_item.area_sqft,

            "description":
                property_item.description,

            "amenities":
                property_item.amenities,

            "available":
                property_item.available
        })


    return results