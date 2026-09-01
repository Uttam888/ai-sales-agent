from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.lead import Lead
from app.models.conversation import Conversation
from app.ai.agent import run_agent_with_tools


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
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
# SAVE MESSAGE
# ============================================================

def save_message(
    db: Session,
    lead_id: int,
    role: str,
    message: str
):

    conversation = Conversation(
        lead_id=lead_id,
        role=role,
        message=message
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


# ============================================================
# GET CONVERSATION HISTORY
# ============================================================

def get_conversation_history(
    db: Session,
    lead_id: int
):

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.lead_id == lead_id
        )
        .order_by(
            Conversation.created_at.asc()
        )
        .all()
    )

    return [
        {
            "role": conversation.role,
            "message": conversation.message,
            "created_at": (
                conversation.created_at.isoformat()
                if conversation.created_at
                else None
            )
        }
        for conversation in conversations
    ]


# ============================================================
# GET CHAT HISTORY
# ============================================================

@router.get("/{lead_id}")
def get_chat(
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
            detail=f"Lead {lead_id} was not found."
        )

    return {
        "lead_id": lead_id,
        "conversations": get_conversation_history(
            db,
            lead_id
        )
    }


# ============================================================
# PROCESS CHAT MESSAGE
# ============================================================

@router.post("")
def chat(
    payload: dict,
    db: Session = Depends(get_db)
):

    lead_id = payload.get("lead_id")
    message = payload.get("message")


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if lead_id is None:

        raise HTTPException(
            status_code=400,
            detail="lead_id is required."
        )


    if message is None:

        raise HTTPException(
            status_code=400,
            detail="message is required."
        )


    message = str(message).strip()


    if not message:

        raise HTTPException(
            status_code=400,
            detail="message cannot be empty."
        )


    try:
        lead_id = int(lead_id)

    except (TypeError, ValueError):

        raise HTTPException(
            status_code=400,
            detail="lead_id must be an integer."
        )


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

        raise HTTPException(
            status_code=404,
            detail=f"Lead {lead_id} was not found."
        )


    # --------------------------------------------------------
    # GET HISTORY BEFORE NEW MESSAGE
    # --------------------------------------------------------

    conversation_history = (
        get_conversation_history(
            db,
            lead_id
        )
    )


    # --------------------------------------------------------
    # SAVE CUSTOMER MESSAGE
    # --------------------------------------------------------

    save_message(
        db=db,
        lead_id=lead_id,
        role="user",
        message=message
    )


    # --------------------------------------------------------
    # RUN AI AGENT
    # --------------------------------------------------------

    try:

        assistant_message = (
            run_agent_with_tools(
                message=message,
                lead_id=lead_id,
                db=db,
                conversation_history=(
                    conversation_history
                )
            )
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "AI Agent Error: "
                f"{type(e).__name__}: {str(e)}"
            )
        )


    # --------------------------------------------------------
    # SAVE AI RESPONSE
    # --------------------------------------------------------

    save_message(
        db=db,
        lead_id=lead_id,
        role="assistant",
        message=assistant_message
    )


    # --------------------------------------------------------
    # REFRESH LEAD
    # --------------------------------------------------------

    db.refresh(lead)


    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {
        "message": "Conversation processed successfully",

        "lead_id": lead_id,

        "response": assistant_message,

        "lead": {
            "id": lead.id,
            "name": lead.name,
            "budget": lead.budget,
            "location": lead.location,
            "property_type": lead.property_type,
            "purpose": lead.purpose,
            "timeline": lead.timeline,
            "buying_intent": lead.buying_intent,
            "qualification_status": (
                lead.qualification_status
            ),
            "lead_score": lead.lead_score,
            "pipeline_stage": lead.pipeline_stage
        }
    }