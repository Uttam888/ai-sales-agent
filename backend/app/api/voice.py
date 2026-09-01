from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import SessionLocal
from app.models.lead import Lead
from app.models.sales_action_outcome import SalesActionOutcome
from app.models.communication import CommunicationHistory

from app.services.lead_health import (
    calculate_lead_health
)

from app.services.sales_recommendation import (
    generate_sales_recommendation
)


router = APIRouter(
    prefix="/api/voice",
    tags=["Voice Agent"],
)


# ============================================================
# DATABASE
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# REQUEST SCHEMA
# ============================================================

class VoiceSessionRequest(BaseModel):
    lead_id: int


# ============================================================
# START VOICE SESSION
# ============================================================

@router.post("/session")
def start_voice_session(
    payload: VoiceSessionRequest,
    db: Session = Depends(get_db),
):
    lead = (
        db.query(Lead)
        .filter(
            Lead.id == payload.lead_id
        )
        .first()
    )

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found.",
        )

    # --------------------------------------------------------
    # EXISTING AI SALES RECOMMENDATION
    # --------------------------------------------------------

    try:
        recommendation = generate_sales_recommendation(
            lead=lead,
            db=db,
        )

    except TypeError:

        recommendation = generate_sales_recommendation(
            lead,
            db,
        )

    action = (
        recommendation.get(
            "next_best_action"
        )
        or "contact_lead"
    )

    suggested_message = (
        recommendation.get(
            "suggested_message"
        )
        or (
            f"Hi {lead.name}, "
            "I wanted to follow up regarding "
            "your property requirements and see "
            "how I can help."
        )
    )

    return {

        "success": True,

        "session": {
            "status": "READY",
            "lead_id": lead.id,
            "lead_name": lead.name,
        },

        "lead": {
            "id": lead.id,
            "name": lead.name,
            "phone": lead.phone,
            "lead_score": lead.lead_score or 0,
            "pipeline_stage": lead.pipeline_stage,
            "buying_intent": lead.buying_intent,
        },

        "sales_intelligence": {

            "next_best_action":
                action,

            "recommended_action":
                recommendation.get(
                    "recommended_action"
                ),

            "reason":
                recommendation.get(
                    "reason"
                ),

            "urgency":
                recommendation.get(
                    "urgency"
                ),

            "suggested_message":
                suggested_message,

            "learning":
                recommendation.get(
                    "learning"
                ),

            "adaptive_action":
                recommendation.get(
                    "adaptive_action"
                ),
        },

        "voice": {

            "opening_message":
                suggested_message,

            "mode":
                "browser",

            "speech_to_text":
                True,

            "text_to_speech":
                True,
        },
    }


# ============================================================
# VOICE SESSION COMPLETION REQUEST
# ============================================================

class VoiceSessionCompleteRequest(BaseModel):

    action: str

    outcome: str

    transcript: str = ""

    notes: str = ""


# ============================================================
# COMPLETE VOICE SESSION
# ============================================================

@router.post(
    "/{lead_id}/complete"
)
def complete_voice_session(
    lead_id: int,
    payload: VoiceSessionCompleteRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # CHECK LEAD
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # NORMALIZE INPUT
    # --------------------------------------------------------

    action = (
        payload.action
        or ""
    ).strip().lower()

    outcome = (
        payload.outcome
        or ""
    ).strip().lower()

    transcript = (
        payload.transcript
        or ""
    ).strip()

    notes = (
        payload.notes
        or ""
    ).strip()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not action:

        raise HTTPException(
            status_code=400,
            detail="Action is required."
        )

    if not outcome:

        raise HTTPException(
            status_code=400,
            detail="Outcome is required."
        )

    allowed_outcomes = {

        "pending",

        "successful",

        "customer_interested",

        "customer_declined",

        "no_response",

        "rescheduled",

        "converted",

        "lost",
    }

    if outcome not in allowed_outcomes:

        raise HTTPException(
            status_code=400,
            detail={
                "message":
                    "Invalid voice call outcome.",

                "allowed_outcomes":
                    sorted(
                        allowed_outcomes
                    )
            }
        )

    # ========================================================
    # RECORD VOICE TRANSCRIPT
    # ========================================================

    if transcript:

        communication = CommunicationHistory(

            lead_id=lead_id,

            channel="voice",

            direction="outbound",

            message=transcript,

            status="recorded",
        )

        db.add(
            communication
        )

    # ========================================================
    # RECORD SALES ACTION OUTCOME
    # ========================================================

    action_outcome = SalesActionOutcome(

        lead_id=lead_id,

        action=action,

        execution_status="executed",

        outcome=outcome,

        notes=(
            notes
            or "Voice Agent call completed."
        ),
    )

    db.add(
        action_outcome
    )

    # ========================================================
    # UPDATE LEAD FOR FINAL OUTCOMES
    # ========================================================

    if outcome == "converted":

        lead.pipeline_stage = (
            "CONVERTED"
        )

        lead.qualification_status = (
            "converted"
        )

    elif outcome == "lost":

        lead.pipeline_stage = (
            "LOST"
        )

        lead.qualification_status = (
            "lost"
        )

    # ========================================================
    # SAVE
    # ========================================================

    try:

        db.commit()

        db.refresh(
            action_outcome
        )

        db.refresh(
            lead
        )

    except Exception:

        db.rollback()

        raise

    # ========================================================
    # REFRESH AI INTELLIGENCE
    # ========================================================

    health = calculate_lead_health(

        db=db,

        lead=lead,
    )

    recommendation = generate_sales_recommendation(

        db=db,

        lead=lead,
    )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success":
            True,

        "message":
            "Voice session completed and sales outcome recorded.",

        "lead": {

            "id":
                lead.id,

            "name":
                lead.name,

            "pipeline_stage":
                lead.pipeline_stage,

            "qualification_status":
                lead.qualification_status,
        },

        "voice": {

            "transcript_recorded":
                bool(transcript),
        },

        "outcome": {

            "id":
                action_outcome.id,

            "action":
                action_outcome.action,

            "execution_status":
                action_outcome.execution_status,

            "outcome":
                action_outcome.outcome,

            "notes":
                action_outcome.notes,
        },

        "health":
            health,

        "next_best_action":
            recommendation.get(
                "next_best_action"
            ),

        "recommended_action":
            recommendation.get(
                "recommended_action"
            ),

        "reason":
            recommendation.get(
                "reason"
            ),

        "urgency":
            recommendation.get(
                "urgency"
            ),

        "learning":
            recommendation.get(
                "learning"
            ),

        "adaptive_action":
            recommendation.get(
                "adaptive_action"
            ),
    }