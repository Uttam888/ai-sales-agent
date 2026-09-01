from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.lead import Lead
from app.models.site_visits import SiteVisit
from app.models.property import Property


router = APIRouter(
    prefix="/api/site-visits",
    tags=["Site Visits"]
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# GET LEAD SITE VISITS
# ============================================================

@router.get("/lead/{lead_id}")
def get_lead_site_visits(
    lead_id: int,
    db: Session = Depends(get_db)
):

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )

    if not lead:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Lead {lead_id} "
                "was not found."
            )
        )

    visits = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.lead_id == lead_id
        )
        .order_by(
            SiteVisit.visit_date.asc(),
            SiteVisit.id.asc()
        )
        .all()
    )

    results = []

    for visit in visits:

        property_data = (
            db.query(Property)
            .filter(
                Property.id == visit.property_id
            )
            .first()
        )

        results.append(
            {
                "id": visit.id,
                "lead_id": visit.lead_id,
                "property_id": visit.property_id,

                "property_title": (
                    property_data.title
                    if property_data
                    else None
                ),

                "property_location": (
                    property_data.location
                    if property_data
                    else None
                ),

                "property_type": (
                    property_data.property_type
                    if property_data
                    else None
                ),

                "property_price": (
                    property_data.price
                    if property_data
                    else None
                ),

                "visit_date": (
                    visit.visit_date.isoformat()
                    if visit.visit_date
                    else None
                ),

                "status": visit.status,
                "notes": visit.notes
            }
        )

    return {
        "lead_id": lead_id,
        "lead_name": lead.name,
        "count": len(results),
        "site_visits": results
    }


# ============================================================
# COMPLETE SITE VISIT
# ============================================================

@router.patch("/{visit_id}/complete")
def complete_site_visit(
    visit_id: int,
    db: Session = Depends(get_db)
):

    visit = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.id == visit_id
        )
        .first()
    )

    if not visit:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Site visit {visit_id} "
                "was not found."
            )
        )

    if visit.status == "completed":

        return {
            "success": True,
            "message": "Site visit is already completed.",
            "visit_id": visit.id,
            "status": visit.status
        }

    if visit.status == "cancelled":

        raise HTTPException(
            status_code=400,
            detail=(
                "A cancelled site visit "
                "cannot be completed."
            )
        )

    visit.status = "completed"

    try:

        db.commit()
        db.refresh(visit)

    except Exception:

        db.rollback()
        raise

    return {
        "success": True,
        "message": "Site visit marked as completed.",
        "visit_id": visit.id,
        "status": visit.status
    }


# ============================================================
# CANCEL SITE VISIT
# ============================================================

@router.patch("/{visit_id}/cancel")
def cancel_site_visit(
    visit_id: int,
    db: Session = Depends(get_db)
):

    visit = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.id == visit_id
        )
        .first()
    )

    if not visit:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Site visit {visit_id} "
                "was not found."
            )
        )

    if visit.status == "cancelled":

        return {
            "success": True,
            "message": "Site visit is already cancelled.",
            "visit_id": visit.id,
            "status": visit.status
        }

    if visit.status == "completed":

        raise HTTPException(
            status_code=400,
            detail=(
                "A completed site visit "
                "cannot be cancelled."
            )
        )

    visit.status = "cancelled"

    try:

        db.commit()
        db.refresh(visit)

    except Exception:

        db.rollback()
        raise

    return {
        "success": True,
        "message": "Site visit cancelled successfully.",
        "visit_id": visit.id,
        "status": visit.status
    }
