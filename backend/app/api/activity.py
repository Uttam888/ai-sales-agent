from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.lead import Lead
from app.models.property import Property
from app.models.site_visits import SiteVisit
from app.models.follow_up import FollowUp
from app.models.communication import CommunicationHistory


router = APIRouter(
    prefix="/api/activity",
    tags=["CRM Activity"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# ALL SITE VISITS
# ============================================================

@router.get("/site-visits")
def get_all_site_visits(
    db: Session = Depends(get_db)
):

    visits = (
        db.query(
            SiteVisit,
            Lead,
            Property
        )
        .join(
            Lead,
            Lead.id == SiteVisit.lead_id
        )
        .outerjoin(
            Property,
            Property.id == SiteVisit.property_id
        )
        .order_by(
            SiteVisit.visit_date.asc(),
            SiteVisit.id.asc()
        )
        .all()
    )

    return {
        "count": len(visits),

        "site_visits": [

            {
                "id": visit.id,

                "lead_id": lead.id,

                "lead_name": lead.name,

                "property_id": visit.property_id,

                "property_title": (
                    property_item.title
                    if property_item
                    else None
                ),

                "property_location": (
                    property_item.location
                    if property_item
                    else None
                ),

                "property_type": (
                    property_item.property_type
                    if property_item
                    else None
                ),

                "property_price": (
                    property_item.price
                    if property_item
                    else None
                ),

                "visit_date": (
                    visit.visit_date.isoformat()
                    if visit.visit_date
                    else None
                ),

                "status": visit.status,

                "notes": visit.notes,
            }

            for visit, lead, property_item in visits
        ],
    }


# ============================================================
# ALL FOLLOW-UPS
# ============================================================

@router.get("/follow-ups")
def get_all_follow_ups(
    db: Session = Depends(get_db)
):

    follow_ups = (
        db.query(
            FollowUp,
            Lead
        )
        .join(
            Lead,
            Lead.id == FollowUp.lead_id
        )
        .order_by(
            FollowUp.follow_up_date.asc(),
            FollowUp.id.asc()
        )
        .all()
    )

    return {
        "count": len(follow_ups),

        "follow_ups": [

            {
                "id": follow_up.id,

                "lead_id": lead.id,

                "lead_name": lead.name,

                "follow_up_date": (
                    follow_up.follow_up_date.isoformat()
                    if follow_up.follow_up_date
                    else None
                ),

                "status": follow_up.status,

                "message": follow_up.message,

                "notes": follow_up.notes,

                "created_at": (
                    follow_up.created_at.isoformat()
                    if getattr(
                        follow_up,
                        "created_at",
                        None
                    )
                    else None
                ),
            }

            for follow_up, lead in follow_ups
        ],
    }


# ============================================================
# LEAD ACTIVITY TIMELINE
# ============================================================

@router.get("/lead/{lead_id}")
def get_lead_activity(
    lead_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # FIND LEAD
    # --------------------------------------------------------

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )

    if not lead:

        return {
            "lead_id": lead_id,
            "lead": None,
            "activities": []
        }


    activities = []


    # --------------------------------------------------------
    # LEAD CREATED
    # --------------------------------------------------------

    if lead.created_at:

        activities.append({

            "type": "lead_created",

            "title": "Lead Created",

            "description": (
                f"Lead {lead.name} was created."
            ),

            "date": lead.created_at.isoformat(),

            "status": "completed",

            "metadata": {
                "lead_id": lead.id
            }
        })


    # --------------------------------------------------------
    # SITE VISITS
    # --------------------------------------------------------

    visits = (
        db.query(
            SiteVisit,
            Property
        )
        .outerjoin(
            Property,
            Property.id == SiteVisit.property_id
        )
        .filter(
            SiteVisit.lead_id == lead_id
        )
        .order_by(
            SiteVisit.visit_date.asc()
        )
        .all()
    )


    for visit, property_item in visits:

        property_name = (

            property_item.title

            if property_item

            else "Property"

        )


        activities.append({

            "type": "site_visit",

            "title": "Site Visit",

            "description": (
                f"Site visit for {property_name}."
            ),

            "date": (
                visit.visit_date.isoformat()
                if visit.visit_date
                else None
            ),

            "status": visit.status,

            "metadata": {

                "site_visit_id": visit.id,

                "property_id": visit.property_id,

                "property_title": (
                    property_item.title
                    if property_item
                    else None
                ),

                "property_location": (
                    property_item.location
                    if property_item
                    else None
                ),

                "property_type": (
                    property_item.property_type
                    if property_item
                    else None
                ),

                "property_price": (
                    property_item.price
                    if property_item
                    else None
                ),

                "notes": visit.notes
            }
        })


    # --------------------------------------------------------
    # FOLLOW-UPS
    # --------------------------------------------------------

    follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.lead_id == lead_id
        )
        .order_by(
            FollowUp.follow_up_date.asc()
        )
        .all()
    )


    for follow_up in follow_ups:

        activities.append({

            "type": "follow_up",

            "title": "Follow-up",

            "description": (
                follow_up.message
                or "Follow-up scheduled."
            ),

            "date": (
                follow_up.follow_up_date.isoformat()
                if follow_up.follow_up_date
                else None
            ),

            "status": follow_up.status,

            "metadata": {

                "follow_up_id": follow_up.id,

                "notes": follow_up.notes
            }
        })


    # --------------------------------------------------------
    # COMMUNICATIONS
    # --------------------------------------------------------

    communications = (
        db.query(
            CommunicationHistory
        )
        .filter(
            CommunicationHistory.lead_id == lead_id
        )
        .order_by(
            CommunicationHistory.created_at.asc()
        )
        .all()
    )


    for communication in communications:

        activities.append({

            "type": "communication",

            "title": "Communication",

            "description": (
                communication.message
                or "Communication sent."
            ),

            "date": (
                communication.created_at.isoformat()
                if communication.created_at
                else (
                    communication.sent_at.isoformat()
                    if communication.sent_at
                    else None
                )
            ),

            "status": communication.status,

            "metadata": {

                "communication_id":
                    communication.id,

                "follow_up_id":
                    communication.follow_up_id,

                "channel":
                    communication.channel,

                "direction":
                    communication.direction
            }
        })


    # --------------------------------------------------------
    # SORT EVERYTHING CHRONOLOGICALLY
    # --------------------------------------------------------

    activities.sort(
        key=lambda activity: (
            activity["date"]
            if activity["date"]
            else ""
        )
    )


    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "lead_id": lead.id,

        "lead": {

            "id": lead.id,

            "name": lead.name,

            "email": lead.email,

            "phone": lead.phone,

            "budget": lead.budget,

            "location": lead.location,

            "property_type":
                lead.property_type,

            "purpose": lead.purpose,

            "timeline": lead.timeline,

            "buying_intent":
                lead.buying_intent,

            "qualification_status":
                lead.qualification_status,

            "lead_score":
                lead.lead_score,

            "pipeline_stage":
                lead.pipeline_stage,

            "created_at": (
                lead.created_at.isoformat()
                if lead.created_at
                else None
            ),

            "updated_at": (
                lead.updated_at.isoformat()
                if lead.updated_at
                else None
            )
        },

        "count": len(activities),

        "activities": activities
    }