from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Body
)

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.lead import Lead
from app.models.follow_up import FollowUp
from app.models.site_visits import SiteVisit
from app.models.communication import CommunicationHistory
from app.models.sales_action_outcome import SalesActionOutcome



from app.schemas.lead import LeadCreate

from app.ai.agent import qualify_lead

from app.ai.tools import (
    next_best_action
)

from app.services.lead_scoring import (
    update_lead_score
)

from app.services.lead_health import (
    calculate_lead_health
)

from app.services.sales_recommendation import (
    generate_sales_recommendation
)

from app.services.follow_up_intelligence import (
    generate_follow_up_intelligence
)

from app.services.lead_opportunity import (
    generate_lead_opportunity
)

from app.services.action_learning import (
    generate_action_learning
)


router = APIRouter(
    prefix="/api/leads",
    tags=["Leads"]
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
# GET ALL LEADS
# ============================================================

@router.get("/")
def get_all_leads(

    db: Session = Depends(
        get_db
    )

):

    leads = (

        db.query(
            Lead
        )

        .order_by(
            Lead.created_at.desc()
        )

        .all()

    )


    return {

        "count":
            len(leads),

        "leads": [

            {

                "id":
                    lead.id,

                "name":
                    lead.name,

                "email":
                    lead.email,

                "phone":
                    lead.phone,

                "requirement":
                    lead.requirement,

                "budget":
                    lead.budget,

                "location":
                    lead.location,

                "property_type":
                    lead.property_type,

                "purpose":
                    lead.purpose,

                "timeline":
                    lead.timeline,

                "buying_intent":
                    lead.buying_intent,

                "qualification_status":
                    lead.qualification_status,

                "lead_score":
                    lead.lead_score,

                "pipeline_stage":
                    lead.pipeline_stage,

                "created_at":
                    lead.created_at,

                "updated_at":
                    lead.updated_at

            }

            for lead in leads

        ]

    }


# ============================================================
# CREATE LEAD
# ============================================================

@router.post("/")
def create_lead(

    lead: LeadCreate,

    db: Session = Depends(
        get_db
    )

):

    # --------------------------------------------------------
    # AI QUALIFICATION
    # --------------------------------------------------------

    qualification = qualify_lead(
        lead.requirement
    )


    # --------------------------------------------------------
    # DETERMINE QUALIFICATION STATUS
    # --------------------------------------------------------

    if qualification.buying_intent == "high":

        qualification_status = (
            "qualified"
        )

    elif qualification.buying_intent == "medium":

        qualification_status = (
            "potential"
        )

    else:

        qualification_status = (
            "low_intent"
        )


    # --------------------------------------------------------
    # CREATE LEAD
    # --------------------------------------------------------

    new_lead = Lead(

        name=lead.name,

        phone=lead.phone,

        requirement=lead.requirement,

        budget=qualification.budget,

        location=qualification.location,

        property_type=qualification.property_type,

        purpose=qualification.purpose,

        timeline=qualification.timeline,

        buying_intent=qualification.buying_intent,

        qualification_status=qualification_status

    )


    # --------------------------------------------------------
    # SAVE LEAD
    # --------------------------------------------------------

    try:

        db.add(
            new_lead
        )

        db.commit()

        db.refresh(
            new_lead
        )

    except Exception:

        db.rollback()

        raise


    # --------------------------------------------------------
    # CALCULATE SCORE + PIPELINE
    # --------------------------------------------------------

    try:

        update_lead_score(

            db=db,

            lead=new_lead

        )

    except Exception:

        db.rollback()

        raise


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "message":
            "Lead created and qualified successfully",

        "lead": {

            "id":
                new_lead.id,

            "name":
                new_lead.name,

            "email":
                new_lead.email,

            "phone":
                new_lead.phone,

            "requirement":
                new_lead.requirement,

            "budget":
                new_lead.budget,

            "location":
                new_lead.location,

            "property_type":
                new_lead.property_type,

            "purpose":
                new_lead.purpose,

            "timeline":
                new_lead.timeline,

            "buying_intent":
                new_lead.buying_intent,

            "qualification_status":
                new_lead.qualification_status,

            "lead_score":
                new_lead.lead_score,

            "pipeline_stage":
                new_lead.pipeline_stage

        }

    }


# ============================================================
# GET NEXT BEST ACTION
# ============================================================

@router.get(
    "/{lead_id}/next-best-action"
)
def get_next_best_action(

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
    # CALCULATE NEXT BEST ACTION
    # --------------------------------------------------------

    result = next_best_action(

        db=db,

        lead_id=lead_id

    )


    return result


# ============================================================
# GET LEAD HEALTH & PRIORITY
# ============================================================

@router.get(
    "/{lead_id}/health"
)
def get_lead_health(

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
    # CALCULATE HEALTH
    # --------------------------------------------------------

    result = calculate_lead_health(

        db=db,

        lead=lead

    )


    return result


# ============================================================
# GET AI SALES RECOMMENDATION
# ============================================================

@router.get(
    "/{lead_id}/sales-recommendation"
)
def get_sales_recommendation(

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
    # GENERATE SALES RECOMMENDATION
    # --------------------------------------------------------

    result = generate_sales_recommendation(

        db=db,

        lead=lead

    )


    return result


# ============================================================
# GET FOLLOW-UP INTELLIGENCE
# ============================================================

@router.get(
    "/{lead_id}/follow-up-intelligence"
)
def get_follow_up_intelligence(

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
    # GENERATE FOLLOW-UP INTELLIGENCE
    # --------------------------------------------------------

    result = generate_follow_up_intelligence(

        db=db,

        lead=lead

    )


    return result


# ============================================================
# GET LEAD OPPORTUNITY INTELLIGENCE
# ============================================================

@router.get(
    "/{lead_id}/opportunity"
)
def get_lead_opportunity(
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
    # EXISTING INTELLIGENCE
    # --------------------------------------------------------

    health = calculate_lead_health(
        db=db,
        lead=lead
    )

    recommendation = generate_sales_recommendation(
        db=db,
        lead=lead
    )

    follow_up_intelligence = generate_follow_up_intelligence(
        db=db,
        lead=lead
    )

    # --------------------------------------------------------
    # GENERATE OPPORTUNITY INTELLIGENCE
    # --------------------------------------------------------

    opportunity = generate_lead_opportunity(
        lead=lead,
        health=health,
        recommendation=recommendation,
        follow_up_intelligence=follow_up_intelligence
    )

    return opportunity


# ============================================================
# GET SALES ACTION LEARNING
# ============================================================

@router.get(
    "/action-learning"
)
def get_action_learning(
    db: Session = Depends(
        get_db
    )
):

    # --------------------------------------------------------
    # LOAD HISTORICAL SALES ACTION OUTCOMES
    # --------------------------------------------------------

    outcomes = (
        db.query(
            SalesActionOutcome
        )
        .order_by(
            SalesActionOutcome.created_at.desc(),
            SalesActionOutcome.id.desc()
        )
        .all()
    )

    # --------------------------------------------------------
    # GENERATE LEARNING
    # --------------------------------------------------------

    learning = generate_action_learning(
        outcomes=outcomes
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return learning


# ============================================================
# EXECUTE SALES ACTION
# ============================================================

@router.post(
    "/{lead_id}/execute-action"
)
def execute_sales_action(

    lead_id: int,

    payload: dict = Body(...),

    db: Session = Depends(
        get_db
    )

):

    # ========================================================
    # CHECK LEAD
    # ========================================================

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


    # ========================================================
    # READ ACTION
    # ========================================================

    requested_action = (
        payload.get("action")
        or ""
    ).strip().lower()


    if not requested_action:

        raise HTTPException(

            status_code=400,

            detail=(
                "Action is required."
            )

        )


    # ========================================================
    # OPTIONAL INPUTS
    # ========================================================

    follow_up_id = (
        payload.get("follow_up_id")
    )


    site_visit_id = (
        payload.get("site_visit_id")
    )


    property_id = (
        payload.get("property_id")
    )


    visit_date_value = (
        payload.get("visit_date")
    )


    custom_message = (
        payload.get("message")
        or ""
    ).strip()


    # ========================================================
    # SUPPORTED ACTIONS
    # ========================================================

    supported_actions = {

        "complete_overdue_follow_up",

        "contact_and_reschedule_site_visit",

        "reschedule_site_visit",

        "prepare_for_site_visit",

        "follow_up_after_site_visit",

        "schedule_site_visit",

        "recommend_properties",

        "discuss_negotiation",

        "contact_high_intent_lead",

        "qualify_lead",

        "contact_lead"

    }


    if requested_action not in supported_actions:

        raise HTTPException(

            status_code=400,

            detail={
                "message":
                    "Unsupported sales action.",

                "supported_actions":
                    sorted(
                        supported_actions
                    )
            }

        )


    # ========================================================
    # ACTION RESULT
    # ========================================================

    execution_message = ""

    communication_message = None


    # ========================================================
    # 1. COMPLETE OVERDUE FOLLOW-UP
    # ========================================================

    if (
        requested_action
        == "complete_overdue_follow_up"
    ):

        follow_up = None


        if follow_up_id:

            follow_up = (

                db.query(
                    FollowUp
                )

                .filter(
                    FollowUp.id == int(
                        follow_up_id
                    ),

                    FollowUp.lead_id
                    == lead_id
                )

                .first()

            )

        else:

            follow_up = (

                db.query(
                    FollowUp
                )

                .filter(

                    FollowUp.lead_id
                    == lead_id,

                    FollowUp.status
                    == "pending",

                    FollowUp.follow_up_date
                    < datetime.now()

                )

                .order_by(

                    FollowUp.follow_up_date.asc(),

                    FollowUp.id.asc()

                )

                .first()

            )


        if not follow_up:

            raise HTTPException(

                status_code=404,

                detail=(
                    "No overdue follow-up "
                    "was found for this lead."
                )

            )


        follow_up.status = (
            "completed"
        )


        execution_message = (
            "The overdue follow-up was marked "
            "as completed."
        )


        communication_message = (
            custom_message
            or
            f"Follow-up completed for {lead.name or 'the lead'}."
        )


    # ========================================================
    # 2. SCHEDULE SITE VISIT
    # ========================================================

    elif (
        requested_action
        == "schedule_site_visit"
    ):

        if not property_id:

            raise HTTPException(

                status_code=400,

                detail=(
                    "property_id is required "
                    "to schedule a site visit."
                )

            )


        if not visit_date_value:

            raise HTTPException(

                status_code=400,

                detail=(
                    "visit_date is required "
                    "to schedule a site visit."
                )

            )


        try:

            visit_date = datetime.fromisoformat(
                str(
                    visit_date_value
                ).replace(
                    "Z",
                    ""
                )
            )

        except ValueError:

            raise HTTPException(

                status_code=400,

                detail=(
                    "visit_date must be a valid "
                    "ISO datetime."
                )

            )


        visit = SiteVisit(

            lead_id=lead_id,

            property_id=int(
                property_id
            ),

            visit_date=visit_date,

            status="scheduled",

            notes=(
                custom_message
                or
                "Site visit scheduled from sales action."
            )

        )


        db.add(
            visit
        )


        lead.qualification_status = (
            "site_visit"
        )


        update_lead_score(

            db=db,

            lead=lead

        )


        execution_message = (
            "A new site visit was scheduled."
        )


        communication_message = (
            custom_message
            or
            f"Hi {lead.name or 'there'}, your site visit has been scheduled."
        )


    # ========================================================
    # 3. RESCHEDULE SITE VISIT
    # ========================================================

    elif requested_action in {

        "reschedule_site_visit",

        "contact_and_reschedule_site_visit"

    }:

        if not property_id:

            raise HTTPException(

                status_code=400,

                detail=(
                    "property_id is required "
                    "to reschedule a site visit."
                )

            )


        if not visit_date_value:

            raise HTTPException(

                status_code=400,

                detail=(
                    "visit_date is required "
                    "to reschedule a site visit."
                )

            )


        try:

            visit_date = datetime.fromisoformat(
                str(
                    visit_date_value
                ).replace(
                    "Z",
                    ""
                )
            )

        except ValueError:

            raise HTTPException(

                status_code=400,

                detail=(
                    "visit_date must be a valid "
                    "ISO datetime."
                )

            )


        old_visit = None


        if site_visit_id:

            old_visit = (

                db.query(
                    SiteVisit
                )

                .filter(

                    SiteVisit.id
                    == int(site_visit_id),

                    SiteVisit.lead_id
                    == lead_id

                )

                .first()

            )

        else:

            old_visit = (

                db.query(
                    SiteVisit
                )

                .filter(

                    SiteVisit.lead_id
                    == lead_id,

                    SiteVisit.status
                    == "scheduled"

                )

                .order_by(

                    SiteVisit.visit_date.desc(),

                    SiteVisit.id.desc()

                )

                .first()

            )


        if old_visit:

            old_visit.status = (
                "cancelled"
            )

            old_visit.notes = (
                (
                    old_visit.notes
                    or ""
                )
                + "\n"
                + (
                    "Visit replaced by a "
                    "new scheduled visit."
                )
            ).strip()


        new_visit = SiteVisit(

            lead_id=lead_id,

            property_id=int(
                property_id
            ),

            visit_date=visit_date,

            status="scheduled",

            notes=(
                custom_message
                or
                "Site visit rescheduled from sales action."
            )

        )


        db.add(
            new_visit
        )


        lead.qualification_status = (
            "site_visit"
        )


        update_lead_score(

            db=db,

            lead=lead

        )


        execution_message = (
            "The previous site visit was handled "
            "and a new site visit was scheduled."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "your site visit has been rescheduled. "
                "Please let me know if the new timing works for you."
            )
        )


    # ========================================================
    # 4. PREPARE FOR SITE VISIT
    # ========================================================

    elif (
        requested_action
        == "prepare_for_site_visit"
    ):

        scheduled_visit = (

            db.query(
                SiteVisit
            )

            .filter(

                SiteVisit.lead_id
                == lead_id,

                SiteVisit.status
                == "scheduled"

            )

            .order_by(

                SiteVisit.visit_date.asc(),

                SiteVisit.id.asc()

            )

            .first()

        )


        if not scheduled_visit:

            raise HTTPException(

                status_code=400,

                detail=(
                    "No scheduled site visit "
                    "was found for this lead."
                )

            )


        execution_message = (
            "The scheduled site visit was confirmed "
            "for preparation."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "just confirming your scheduled site visit. "
                "Please let me know if you need directions "
                "or any additional property details."
            )
        )


    # ========================================================
    # 5. FOLLOW UP AFTER SITE VISIT
    # ========================================================

    elif (
        requested_action
        == "follow_up_after_site_visit"
    ):

        completed_visit = (

            db.query(
                SiteVisit
            )

            .filter(

                SiteVisit.lead_id
                == lead_id,

                SiteVisit.status
                == "completed"

            )

            .order_by(

                SiteVisit.visit_date.desc(),

                SiteVisit.id.desc()

            )

            .first()

        )


        if not completed_visit:

            raise HTTPException(

                status_code=400,

                detail=(
                    "No completed site visit "
                    "was found for this lead."
                )

            )


        execution_message = (
            "Post-site-visit follow-up was initiated."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "I wanted to follow up after your recent "
                "site visit. I would love to hear your "
                "feedback and answer any questions."
            )
        )


    # ========================================================
    # 6. RECOMMEND PROPERTIES
    # ========================================================

    elif (
        requested_action
        == "recommend_properties"
    ):

        execution_message = (
            "The property recommendation action "
            "was recorded."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "based on your requirements, I can share "
                "some suitable property options with you."
            )
        )


    # ========================================================
    # 7. NEGOTIATION
    # ========================================================

    elif (
        requested_action
        == "discuss_negotiation"
    ):

        execution_message = (
            "The negotiation action was recorded."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "I wanted to follow up regarding the "
                "property and see if there are any "
                "questions or concerns about the pricing "
                "or terms that I can help address."
            )
        )


    # ========================================================
    # 8. HIGH INTENT LEAD
    # ========================================================

    elif (
        requested_action
        == "contact_high_intent_lead"
    ):

        execution_message = (
            "The high-intent lead contact action "
            "was recorded."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "I wanted to follow up regarding your "
                "property requirements. I can help you "
                "shortlist suitable options or arrange "
                "a site visit."
            )
        )


    # ========================================================
    # 9. QUALIFY LEAD
    # ========================================================

    elif (
        requested_action
        == "qualify_lead"
    ):

        execution_message = (
            "The lead qualification action "
            "was recorded."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "I wanted to understand your property "
                "requirements a little better so I can "
                "suggest the most suitable options."
            )
        )


    # ========================================================
    # 10. GENERIC CONTACT
    # ========================================================

    elif (
        requested_action
        == "contact_lead"
    ):

        execution_message = (
            "The lead contact action was recorded."
        )


        communication_message = (
            custom_message
            or
            (
                f"Hi {lead.name or 'there'}, "
                "I wanted to follow up regarding your "
                "property requirements and see how I can help."
            )
        )


    # ========================================================
    # RECORD COMMUNICATION
    # ========================================================

    if communication_message:

        communication = CommunicationHistory(

            lead_id=lead_id,

            channel="dashboard",

            direction="outbound",

            message=communication_message,

            status="recorded"

        )


        db.add(
            communication
        )


    # ========================================================
    # RECORD ACTION EXECUTION OUTCOME
    # ========================================================

    action_outcome = SalesActionOutcome(

        lead_id=lead_id,

        action=requested_action,

        execution_status="executed",

        outcome="pending",

        notes=(
            "Action executed successfully. "
            "Awaiting sales outcome."
        )

    )

    db.add(
        action_outcome
    )


    # ========================================================
    # SAVE ALL CHANGES
    # ========================================================

    try:

        db.commit()

        db.refresh(
            lead
        )

    except Exception:

        db.rollback()

        raise


    # ========================================================
    # REFRESH INTELLIGENCE
    # ========================================================

    health = calculate_lead_health(

        db=db,

        lead=lead

    )


    recommendation = generate_sales_recommendation(

        db=db,

        lead=lead

    )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success":
            True,

        "message":
            execution_message,

        "lead_id":
            lead.id,

        "action":
            requested_action,

        "action_outcome": {

            "id":
                action_outcome.id,

            "execution_status":
                action_outcome.execution_status,

            "outcome":
                action_outcome.outcome,

            "notes":
                action_outcome.notes

        },

        "communication_recorded":
            bool(
                communication_message
            ),

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

        "suggested_message":
            recommendation.get(
                "suggested_message"
            ),

        "risks":
            recommendation.get(
                "risks",
                []
            ),

        "recommended_focus":
            recommendation.get(
                "recommended_focus"
            )

    }


# ============================================================
# RECORD SALES ACTION OUTCOME
# ============================================================

@router.post(
    "/{lead_id}/action-outcome"
)
def record_sales_action_outcome(

    lead_id: int,

    payload: dict = Body(...),

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
    # READ INPUT
    # --------------------------------------------------------

    action = (
        payload.get("action")
        or ""
    ).strip().lower()

    outcome = (
        payload.get("outcome")
        or ""
    ).strip().lower()

    notes = (
        payload.get("notes")
        or ""
    ).strip()

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

    # --------------------------------------------------------
    # VALIDATE OUTCOME
    # --------------------------------------------------------

    allowed_outcomes = {

        "pending",
        "successful",
        "customer_interested",
        "customer_declined",
        "no_response",
        "rescheduled",
        "converted",
        "lost"

    }

    if outcome not in allowed_outcomes:

        raise HTTPException(
            status_code=400,
            detail={
                "message":
                    "Invalid sales action outcome.",

                "allowed_outcomes":
                    sorted(
                        allowed_outcomes
                    )
            }
        )

    # --------------------------------------------------------
    # CREATE OUTCOME
    # --------------------------------------------------------

    action_outcome = SalesActionOutcome(

        lead_id=lead_id,

        action=action,

        execution_status="executed",

        outcome=outcome,

        notes=notes or None

    )

    db.add(
        action_outcome
    )

    # --------------------------------------------------------
    # UPDATE LEAD FOR FINAL OUTCOMES
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # REFRESH INTELLIGENCE
    # --------------------------------------------------------

    health = calculate_lead_health(

        db=db,

        lead=lead

    )

    recommendation = generate_sales_recommendation(

        db=db,

        lead=lead

    )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success":
            True,

        "message":
            "Sales action outcome recorded.",

        "outcome": {

            "id":
                action_outcome.id,

            "lead_id":
                action_outcome.lead_id,

            "action":
                action_outcome.action,

            "execution_status":
                action_outcome.execution_status,

            "outcome":
                action_outcome.outcome,

            "notes":
                action_outcome.notes,

            "created_at":
                (
                    action_outcome.created_at.isoformat()
                    if action_outcome.created_at
                    else None
                )

        },

        "lead": {

            "id":
                lead.id,

            "pipeline_stage":
                lead.pipeline_stage,

            "qualification_status":
                lead.qualification_status

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
            )

    }


# ============================================================
# GET SALES ACTION OUTCOMES
# ============================================================

@router.get(
    "/{lead_id}/action-outcomes"
)
def get_sales_action_outcomes(

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
    # GET OUTCOMES
    # --------------------------------------------------------

    outcomes = (
        db.query(
            SalesActionOutcome
        )
        .filter(
            SalesActionOutcome.lead_id
            == lead_id
        )
        .order_by(
            SalesActionOutcome.created_at.desc(),
            SalesActionOutcome.id.desc()
        )
        .all()
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "lead_id":
            lead_id,

        "count":
            len(outcomes),

        "outcomes": [

            {

                "id":
                    item.id,

                "action":
                    item.action,

                "execution_status":
                    item.execution_status,

                "outcome":
                    item.outcome,

                "notes":
                    item.notes,

                "created_at":
                    (
                        item.created_at.isoformat()
                        if item.created_at
                        else None
                    ),

                "updated_at":
                    (
                        item.updated_at.isoformat()
                        if item.updated_at
                        else None
                    )

            }

            for item in outcomes

        ]

    }

