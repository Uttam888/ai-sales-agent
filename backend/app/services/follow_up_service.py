import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from sqlalchemy.orm import Session

from app.models.follow_up import FollowUp
from app.models.lead import Lead
from app.models.conversation import Conversation

from app.services.communication import (
    send_follow_up_message
)


# ============================================================
# ENVIRONMENT
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../"
    )
)

load_dotenv(
    os.path.join(
        PROJECT_ROOT,
        ".env"
    )
)


# ============================================================
# GEMINI CLIENT
# ============================================================

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:

    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Check your .env file."
    )


client = genai.Client(
    api_key=api_key
)


MODEL_NAME = "gemini-3.5-flash-lite"


# ============================================================
# GET DUE FOLLOW-UPS
# ============================================================

def get_due_follow_ups(
    db: Session
):

    now = datetime.now()

    return (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "pending",
            FollowUp.follow_up_date <= now
        )
        .order_by(
            FollowUp.follow_up_date.asc()
        )
        .all()
    )


# ============================================================
# GET CONVERSATION HISTORY
# ============================================================

def get_lead_conversation_history(
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

    return conversations


# ============================================================
# BUILD CONVERSATION TEXT
# ============================================================

def build_conversation_text(
    conversations
):

    if not conversations:

        return (
            "No previous conversation "
            "is available."
        )


    conversation_lines = []


    for conversation in conversations:

        role = (
            "Customer"
            if conversation.role == "user"
            else "AI Sales Agent"
        )


        conversation_lines.append(
            f"{role}: {conversation.message}"
        )


    return "\n".join(
        conversation_lines
    )


# ============================================================
# GENERATE PERSONALIZED FOLLOW-UP
# ============================================================

def generate_follow_up_message(
    db: Session,
    lead: Lead,
    follow_up: FollowUp
):

    conversations = (
        get_lead_conversation_history(
            db,
            lead.id
        )
    )


    conversation_text = (
        build_conversation_text(
            conversations
        )
    )


    prompt = f"""
You are an AI real-estate sales assistant.

Your task is to write a short, natural,
personalized follow-up message for a property
buyer.

The message will be sent by a real estate
sales representative to the customer.

==================================================
LEAD INFORMATION
==================================================

Name:
{lead.name or "Not provided"}

Phone:
{lead.phone or "Not provided"}

Budget:
{lead.budget or "Not provided"}

Location:
{lead.location or "Not provided"}

Property Type:
{lead.property_type or "Not provided"}

Purpose:
{lead.purpose or "Not provided"}

Timeline:
{lead.timeline or "Not provided"}

Buying Intent:
{lead.buying_intent or "Not provided"}

Qualification Status:
{lead.qualification_status or "Not provided"}

Lead Score:
{lead.lead_score or 0}

Pipeline Stage:
{lead.pipeline_stage or "NEW"}


==================================================
CONVERSATION HISTORY
==================================================

{conversation_text}


==================================================
FOLLOW-UP CONTEXT
==================================================

Existing follow-up message:
{follow_up.message or "No existing message."}

Follow-up notes:
{follow_up.notes or "No notes."}


==================================================
IMPORTANT RULES
==================================================

1. Address the customer by name when available.

2. Use only information explicitly present
   in the lead information or conversation.

3. Make the message feel human and natural.

4. Keep the message concise.

5. Keep the message under approximately
   80 words.

6. Do not use markdown.

7. Do not use bullet points.

8. Do not invent properties.

9. Do not invent property prices.

10. Do not invent amenities.

11. Do not invent appointments.

12. Do not invent site visits.

13. Do not claim that a property was shown
    unless the conversation confirms it.

14. Do not claim that the customer agreed
    to anything unless the conversation confirms it.

15. Do not assume financing details.

16. Do not assume a specific sector unless
    explicitly mentioned.

17. Do not repeat every lead detail.

18. Focus on the most relevant next step.

19. If the customer asked a question in the
    conversation that has not been answered,
    prioritize that question.

20. If the customer expressed interest in
    properties, politely invite the customer
    to continue the discussion.

21. If there is not enough information for a
    highly specific message, write a simple,
    professional follow-up based only on the
    available facts.

22. Return ONLY the message text.
"""


    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=prompt
    )


    generated_message = getattr(
        response,
        "text",
        None
    )


    if not generated_message:

        return follow_up.message


    generated_message = (
        generated_message
        .strip()
    )


    if not generated_message:

        return follow_up.message


    return generated_message


# ============================================================
# PROCESS ONE FOLLOW-UP
# ============================================================

def process_follow_up(
    db: Session,
    follow_up: FollowUp
):

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == follow_up.lead_id
        )
        .first()
    )


    if not lead:

        follow_up.status = "failed"

        follow_up.notes = (
            "Lead was not found."
        )

        db.commit()


        return {

            "success": False,

            "follow_up_id":
                follow_up.id,

            "error":
                f"Lead {follow_up.lead_id} "
                "was not found."
        }


    # ========================================================
    # GENERATE AI MESSAGE
    # ========================================================

    try:

        personalized_message = (
            generate_follow_up_message(
                db=db,
                lead=lead,
                follow_up=follow_up
            )
        )

    except Exception as e:

        print(
            "[FOLLOW-UP AI] "
            "Message generation failed:",
            type(e).__name__,
            str(e)
        )

        personalized_message = (
            follow_up.message
        )


    # ========================================================
    # SAVE GENERATED MESSAGE
    # ========================================================

    if personalized_message:

        follow_up.message = (
            personalized_message
        )

        db.commit()

        db.refresh(
            follow_up
        )


    # ========================================================
    # SEND FOLLOW-UP
    # ========================================================

    try:

        communication_result = (
            send_follow_up_message(
                db=db,
                follow_up=follow_up
            )
        )

    except Exception as e:

        follow_up.status = "failed"

        follow_up.notes = (
            f"Communication error: {str(e)}"
        )

        db.commit()


        return {

            "success": False,

            "follow_up_id":
                follow_up.id,

            "lead_id":
                lead.id,

            "error":
                str(e)
        }


    # ========================================================
    # CHECK COMMUNICATION RESULT
    # ========================================================

    if not communication_result.get(
        "success"
    ):

        follow_up.status = "failed"

        follow_up.notes = (
            communication_result.get(
                "error",
                "Message sending failed."
            )
        )

        db.commit()


        return {

            "success": False,

            "follow_up_id":
                follow_up.id,

            "lead_id":
                lead.id,

            "error":
                communication_result.get(
                    "error",
                    "Message sending failed."
                )
        }


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "success": True,

        "follow_up_id":
            follow_up.id,

        "lead_id":
            lead.id,

        "lead_name":
            lead.name,

        "message":
            follow_up.message,

        "channel":
            communication_result.get(
                "channel"
            ),

        "sent_at":
            communication_result.get(
                "sent_at"
            ),

        "status":
            follow_up.status
    }


# ============================================================
# PROCESS ALL DUE FOLLOW-UPS
# ============================================================

def process_due_follow_ups(
    db: Session
):

    due_follow_ups = (
        get_due_follow_ups(
            db
        )
    )


    results = []


    for follow_up in due_follow_ups:

        try:

            result = process_follow_up(

                db,

                follow_up
            )

            results.append(
                result
            )

        except Exception as e:

            db.rollback()

            print(
                "[FOLLOW-UP WORKER] "
                "Unexpected error:",
                type(e).__name__,
                str(e)
            )

            results.append({

                "success": False,

                "follow_up_id":
                    follow_up.id,

                "error":
                    str(e)
            })


    return {

        "success": True,

        "processed":
            len(results),

        "follow_ups":
            results
    }