from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.lead import Lead
from app.models.follow_up import FollowUp

from app.services.follow_up_service import (
    process_due_follow_ups
)


router = APIRouter(

    prefix="/api/follow-ups",

    tags=["Follow-ups"]

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
# GET LEAD FOLLOW-UPS
# ============================================================

@router.get(
    "/lead/{lead_id}"
)
def get_lead_follow_ups(

    lead_id: int,

    db: Session = Depends(
        get_db
    )

):

    # --------------------------------------------------------
    # CHECK LEAD
    # --------------------------------------------------------

    lead = (

        db.query(
            Lead
        )

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


    # --------------------------------------------------------
    # GET FOLLOW-UPS
    # --------------------------------------------------------

    follow_ups = (

        db.query(
            FollowUp
        )

        .filter(

            FollowUp.lead_id
            == lead_id

        )

        .order_by(

            FollowUp.follow_up_date.asc(),

            FollowUp.id.asc()

        )

        .all()

    )


    results = []


    for follow_up in follow_ups:

        results.append(

            {

                "id":
                    follow_up.id,

                "lead_id":
                    follow_up.lead_id,

                "follow_up_date":
                    (
                        follow_up.follow_up_date.isoformat()
                        if follow_up.follow_up_date
                        else None
                    ),

                "status":
                    follow_up.status,

                "message":
                    follow_up.message,

                "notes":
                    follow_up.notes

            }

        )


    return {

        "lead_id":
            lead_id,

        "lead_name":
            lead.name,

        "count":
            len(results),

        "follow_ups":
            results

    }


# ============================================================
# COMPLETE FOLLOW-UP
# ============================================================

@router.patch(
    "/{follow_up_id}/complete"
)
def complete_follow_up(

    follow_up_id: int,

    db: Session = Depends(
        get_db
    )

):

    # --------------------------------------------------------
    # FIND FOLLOW-UP
    # --------------------------------------------------------

    follow_up = (

        db.query(
            FollowUp
        )

        .filter(
            FollowUp.id == follow_up_id
        )

        .first()

    )


    if not follow_up:

        raise HTTPException(

            status_code=404,

            detail=(
                f"Follow-up {follow_up_id} "
                "was not found."
            )

        )


    # --------------------------------------------------------
    # CHECK STATUS
    # --------------------------------------------------------

    if follow_up.status != "pending":

        raise HTTPException(

            status_code=400,

            detail=(
                "Only pending follow-ups "
                "can be marked as completed."
            )

        )


    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    follow_up.status = "completed"


    db.commit()

    db.refresh(
        follow_up
    )


    return {

        "success":
            True,

        "message":
            "Follow-up marked as completed.",

        "follow_up_id":
            follow_up.id,

        "status":
            follow_up.status

    }


# ============================================================
# CANCEL FOLLOW-UP
# ============================================================

@router.patch(
    "/{follow_up_id}/cancel"
)
def cancel_follow_up(

    follow_up_id: int,

    db: Session = Depends(
        get_db
    )

):

    # --------------------------------------------------------
    # FIND FOLLOW-UP
    # --------------------------------------------------------

    follow_up = (

        db.query(
            FollowUp
        )

        .filter(
            FollowUp.id == follow_up_id
        )

        .first()

    )


    if not follow_up:

        raise HTTPException(

            status_code=404,

            detail=(
                f"Follow-up {follow_up_id} "
                "was not found."
            )

        )


    # --------------------------------------------------------
    # CHECK STATUS
    # --------------------------------------------------------

    if follow_up.status != "pending":

        raise HTTPException(

            status_code=400,

            detail=(
                "Only pending follow-ups "
                "can be cancelled."
            )

        )


    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    follow_up.status = "cancelled"


    db.commit()

    db.refresh(
        follow_up
    )


    return {

        "success":
            True,

        "message":
            "Follow-up cancelled successfully.",

        "follow_up_id":
            follow_up.id,

        "status":
            follow_up.status

    }


# ============================================================
# PROCESS DUE FOLLOW-UPS
# ============================================================

@router.post(
    "/process"
)
def process_follow_ups(

    db: Session = Depends(
        get_db
    )

):

    return process_due_follow_ups(
        db
    )