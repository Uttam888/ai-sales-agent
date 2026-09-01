from datetime import datetime

from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.site_visits import SiteVisit
from app.models.follow_up import FollowUp
from app.models.communication import CommunicationHistory


# ============================================================
# LEAD HEALTH & PRIORITY
# ============================================================

def calculate_lead_health(
    db: Session,
    lead: Lead
):

    # --------------------------------------------------------
    # NORMALIZE LEAD DATA
    # --------------------------------------------------------

    score = lead.lead_score or 0

    status = (
        lead.qualification_status
        or ""
    ).strip().lower()

    stage = (
        lead.pipeline_stage
        or ""
    ).strip().upper()

    intent = (
        lead.buying_intent
        or ""
    ).strip().lower()

    now = datetime.now()


    # ========================================================
    # GET FOLLOW-UPS
    # ========================================================

    follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.lead_id == lead.id
        )
        .order_by(
            FollowUp.follow_up_date.asc(),
            FollowUp.id.asc()
        )
        .all()
    )


    pending_follow_ups = [

        follow_up

        for follow_up in follow_ups

        if (
            follow_up.status
            or ""
        ).strip().lower() == "pending"

    ]


    overdue_follow_ups = [

        follow_up

        for follow_up in pending_follow_ups

        if (
            follow_up.follow_up_date
            and follow_up.follow_up_date < now
        )

    ]


    # ========================================================
    # GET SITE VISITS
    # ========================================================

    site_visits = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.lead_id == lead.id
        )
        .order_by(
            SiteVisit.visit_date.desc(),
            SiteVisit.id.desc()
        )
        .all()
    )


    scheduled_visits = [

        visit

        for visit in site_visits

        if (
            visit.status
            or ""
        ).strip().lower() == "scheduled"

    ]


    completed_visits = [

        visit

        for visit in site_visits

        if (
            visit.status
            or ""
        ).strip().lower() == "completed"

    ]


    cancelled_visits = [

        visit

        for visit in site_visits

        if (
            visit.status
            or ""
        ).strip().lower() == "cancelled"

    ]


    # ========================================================
    # GET COMMUNICATION HISTORY
    # ========================================================

    communications = (
        db.query(
            CommunicationHistory
        )
        .filter(
            CommunicationHistory.lead_id
            == lead.id
        )
        .order_by(
            CommunicationHistory.sent_at.desc(),
            CommunicationHistory.id.desc()
        )
        .all()
    )


    # ========================================================
    # FIND LATEST COMMUNICATION
    # ========================================================

    latest_communication = None

    for communication in communications:

        communication_date = (

            communication.sent_at

            or communication.created_at

        )

        if communication_date:

            latest_communication = (
                communication_date
            )

            break


    # ========================================================
    # CALCULATE INACTIVITY
    # ========================================================

    inactivity_days = None


    if latest_communication:

        inactivity_delta = (

            now
            - latest_communication

        )

        inactivity_days = (
            inactivity_delta.days
        )

    elif lead.created_at:

        inactivity_delta = (

            now
            - lead.created_at

        )

        inactivity_days = (
            inactivity_delta.days
        )


    # ========================================================
    # ACTIVE LEAD DEFINITION
    # ========================================================

    active_pipeline_stages = {

        "QUALIFIED",

        "PROPERTY_INTEREST",

        "SITE_VISIT",

        "NEGOTIATION"

    }


    is_active_lead = (

        stage in active_pipeline_stages

        or intent == "high"

        or score >= 50

    )


    # ========================================================
    # COMMUNICATION INACTIVITY
    # ========================================================

    inactivity_risk = (

        is_active_lead

        and inactivity_days is not None

        and inactivity_days >= 7

        and not pending_follow_ups

        and not scheduled_visits

    )


    # ========================================================
    # MISSED SITE VISITS
    # ========================================================

    missed_visits = [

        visit

        for visit in scheduled_visits

        if (
            visit.visit_date
            and visit.visit_date < now
        )

    ]


    # ========================================================
    # RISK SIGNALS
    # ========================================================

    risks = []


    # --------------------------------------------------------
    # OVERDUE FOLLOW-UP
    # --------------------------------------------------------

    if overdue_follow_ups:

        risks.append(
            "Follow-up is overdue."
        )


    # --------------------------------------------------------
    # MISSED SITE VISIT
    # --------------------------------------------------------

    if missed_visits:

        risks.append(
            "A scheduled site visit has "
            "passed without completion."
        )


    # --------------------------------------------------------
    # CANCELLED SITE VISIT
    # --------------------------------------------------------

    if (
        cancelled_visits

        and not scheduled_visits

    ):

        risks.append(
            "A site visit was cancelled "
            "and no replacement visit is scheduled."
        )


    # --------------------------------------------------------
    # COMMUNICATION INACTIVITY
    # --------------------------------------------------------

    if inactivity_risk:

        risks.append(
            f"No communication with the lead "
            f"for {inactivity_days} days."
        )


    # --------------------------------------------------------
    # NO NEXT ACTION
    # --------------------------------------------------------

    if (

        stage in {

            "QUALIFIED",

            "PROPERTY_INTEREST",

            "SITE_VISIT",

            "NEGOTIATION"

        }

        and not pending_follow_ups

        and not scheduled_visits

    ):

        risks.append(
            "Lead currently has no pending "
            "follow-up or scheduled site visit."
        )


    # ========================================================
    # DETERMINE HEALTH
    # ========================================================

    # --------------------------------------------------------
    # CONVERTED
    # --------------------------------------------------------

    if (

        stage == "CONVERTED"

        or status == "converted"

    ):

        health = "CONVERTED"


    # --------------------------------------------------------
    # NEGOTIATION
    # --------------------------------------------------------

    elif (

        stage == "NEGOTIATION"

        or status == "negotiation"

    ):

        health = "HOT"


    # --------------------------------------------------------
    # SITE VISIT
    # --------------------------------------------------------

    elif (

        stage == "SITE_VISIT"

        or scheduled_visits

    ):

        health = "HOT"


    # --------------------------------------------------------
    # HIGH INTENT
    # --------------------------------------------------------

    elif (

        intent == "high"

        and score >= 70

    ):

        health = "HOT"


    # --------------------------------------------------------
    # WARM
    # --------------------------------------------------------

    elif (

        stage in {

            "QUALIFIED",

            "PROPERTY_INTEREST"

        }

        or (

            intent == "medium"

            and score >= 50

        )

    ):

        health = "WARM"


    # --------------------------------------------------------
    # HIGH SCORE
    # --------------------------------------------------------

    elif score >= 70:

        health = "WARM"


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    else:

        health = "COLD"


    # ========================================================
    # DETERMINE PRIORITY
    # ========================================================

    # --------------------------------------------------------
    # CONVERTED
    # --------------------------------------------------------

    if health == "CONVERTED":

        priority = "LOW"


    # --------------------------------------------------------
    # OVERDUE FOLLOW-UP
    # --------------------------------------------------------

    elif overdue_follow_ups:

        priority = "URGENT"


    # --------------------------------------------------------
    # MISSED SITE VISIT
    # --------------------------------------------------------

    elif missed_visits:

        priority = "HIGH"


    # --------------------------------------------------------
    # CANCELLED SITE VISIT
    # --------------------------------------------------------

    elif (

        cancelled_visits

        and not scheduled_visits

        and health == "HOT"

    ):

        priority = "HIGH"


    # --------------------------------------------------------
    # HOT + HIGH INTENT / SCORE / VISIT
    # --------------------------------------------------------

    elif (

        health == "HOT"

        and (

            intent == "high"

            or score >= 80

            or scheduled_visits

        )

    ):

        priority = "HIGH"


    # --------------------------------------------------------
    # HOT
    # --------------------------------------------------------

    elif health == "HOT":

        priority = "HIGH"


    # --------------------------------------------------------
    # WARM
    # --------------------------------------------------------

    elif health == "WARM":

        priority = "MEDIUM"


    # --------------------------------------------------------
    # COLD
    # --------------------------------------------------------

    else:

        priority = "LOW"


    # ========================================================
    # RECOMMENDED FOCUS
    # ========================================================

    # --------------------------------------------------------
    # OVERDUE FOLLOW-UP
    # --------------------------------------------------------

    if overdue_follow_ups:

        recommended_focus = (

            "Complete the overdue follow-up "
            "as soon as possible."

        )


    # --------------------------------------------------------
    # MISSED SITE VISIT
    # --------------------------------------------------------

    elif missed_visits:

        recommended_focus = (

            "Contact the lead about the missed "
            "site visit and reschedule it."

        )


    # --------------------------------------------------------
    # COMMUNICATION INACTIVITY
    # --------------------------------------------------------

    elif inactivity_risk:

        recommended_focus = (

            "Re-engage the lead because there "
            "has been no recent communication."

        )


    # --------------------------------------------------------
    # SCHEDULED SITE VISIT
    # --------------------------------------------------------

    elif scheduled_visits:

        recommended_focus = (

            "Confirm and prepare for the "
            "scheduled site visit."

        )


    # --------------------------------------------------------
    # COMPLETED SITE VISIT
    # --------------------------------------------------------

    elif completed_visits:

        recommended_focus = (

            "Follow up after the completed "
            "site visit and collect feedback."

        )


    # --------------------------------------------------------
    # NEGOTIATION
    # --------------------------------------------------------

    elif (

        stage == "NEGOTIATION"

        or status == "negotiation"

    ):

        recommended_focus = (

            "Address objections and move "
            "the lead toward closing."

        )


    # --------------------------------------------------------
    # PROPERTY INTEREST
    # --------------------------------------------------------

    elif (

        stage == "PROPERTY_INTEREST"

        or status == "property_interest"

    ):

        recommended_focus = (

            "Convert property interest into "
            "a scheduled site visit."

        )


    # --------------------------------------------------------
    # QUALIFIED
    # --------------------------------------------------------

    elif (

        stage == "QUALIFIED"

        or status == "qualified"

    ):

        recommended_focus = (

            "Recommend suitable properties "
            "and move the lead toward a visit."

        )


    # --------------------------------------------------------
    # HIGH INTENT
    # --------------------------------------------------------

    elif intent == "high":

        recommended_focus = (

            "Contact the high-intent lead "
            "promptly."

        )


    # --------------------------------------------------------
    # CONTACTED
    # --------------------------------------------------------

    elif stage == "CONTACTED":

        recommended_focus = (

            "Complete lead qualification."

        )


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    else:

        recommended_focus = (

            "Contact the lead and understand "
            "their requirements."

        )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "lead_id":
            lead.id,

        "health":
            health,

        "priority":
            priority,

        "lead_score":
            score,

        "pipeline_stage":
            lead.pipeline_stage,

        "qualification_status":
            lead.qualification_status,

        "buying_intent":
            lead.buying_intent,

        "signals": {

            "pending_follow_ups":
                len(
                    pending_follow_ups
                ),

            "overdue_follow_ups":
                len(
                    overdue_follow_ups
                ),

            "scheduled_site_visits":
                len(
                    scheduled_visits
                ),

            "completed_site_visits":
                len(
                    completed_visits
                ),

            "cancelled_site_visits":
                len(
                    cancelled_visits
                ),

            "communication_count":
                len(
                    communications
                ),

            "inactivity_days":
                inactivity_days

        },

        "risks":
            risks,

        "recommended_focus":
            recommended_focus

    }