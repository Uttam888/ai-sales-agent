from datetime import datetime

from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.follow_up import FollowUp
from app.models.communication import CommunicationHistory


# ============================================================
# SIMULATE MESSAGE SENDING
# ============================================================

def send_follow_up_message(
    db: Session,
    follow_up: FollowUp
):

    # --------------------------------------------------------
    # FIND LEAD
    # --------------------------------------------------------

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == follow_up.lead_id
        )
        .first()
    )

    if not lead:

        return {
            "success": False,
            "error": (
                f"Lead {follow_up.lead_id} "
                "was not found."
            )
        }

    # --------------------------------------------------------
    # VALIDATE MESSAGE
    # --------------------------------------------------------

    if not follow_up.message:

        return {
            "success": False,
            "error": "Follow-up message is empty."
        }

    # --------------------------------------------------------
    # TIMESTAMP
    # --------------------------------------------------------

    now = datetime.now()

    # --------------------------------------------------------
    # CREATE COMMUNICATION RECORD
    # --------------------------------------------------------

    communication = CommunicationHistory(

        lead_id=lead.id,

        follow_up_id=follow_up.id,

        channel="simulated",

        direction="outbound",

        message=follow_up.message,

        status="sent",

        sent_at=now,

        created_at=now
    )

    db.add(
        communication
    )

    # --------------------------------------------------------
    # SIMULATE MESSAGE SENDING
    # --------------------------------------------------------

    print(
        "\n"
        "==================================================\n"
        "              COMMUNICATION SIMULATOR\n"
        "=================================================="
    )

    print(
        f"To: {lead.name}"
    )

    print(
        f"Lead ID: {lead.id}"
    )

    print(
        f"Follow-up ID: {follow_up.id}"
    )

    print(
        "Channel: SIMULATED"
    )

    print(
        f"Message: {follow_up.message}"
    )

    print(
        f"Sent At: {now.isoformat()}"
    )

    print(
        "==================================================\n"
    )

    # --------------------------------------------------------
    # MARK FOLLOW-UP AS SENT
    # --------------------------------------------------------

    follow_up.status = "sent"

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()

    db.refresh(
        communication
    )

    db.refresh(
        follow_up
    )

    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "success": True,

        "follow_up_id":
            follow_up.id,

        "communication_id":
            communication.id,

        "lead_id":
            lead.id,

        "lead_name":
            lead.name,

        "channel":
            communication.channel,

        "message":
            communication.message,

        "sent_at":
            communication.sent_at.isoformat(),

        "status":
            communication.status
    }