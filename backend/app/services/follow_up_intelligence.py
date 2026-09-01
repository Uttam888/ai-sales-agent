from datetime import datetime

from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.follow_up import FollowUp
from app.models.site_visits import SiteVisit

from app.services.lead_health import calculate_lead_health
from app.services.sales_recommendation import (
    generate_sales_recommendation
)


# ============================================================
# FOLLOW-UP INTELLIGENCE
# ============================================================

def generate_follow_up_intelligence(
    db: Session,
    lead: Lead
):
    """
    Determine whether a lead needs follow-up, when it should
    happen, and what the objective should be.

    This service does NOT send messages.

    It only decides:
        - follow-up status
        - recommended timing
        - objective
        - reason
        - priority
    """

    # ========================================================
    # CURRENT HEALTH
    # ========================================================

    health = calculate_lead_health(
        db=db,
        lead=lead
    )

    # ========================================================
    # CURRENT AI SALES RECOMMENDATION
    # ========================================================

    recommendation = generate_sales_recommendation(
        db=db,
        lead=lead
    )

    # ========================================================
    # NORMALIZE
    # ========================================================

    priority = (
        health.get("priority")
        or "LOW"
    ).upper()

    risks = (
        health.get("risks")
        or []
    )

    recommended_focus = (
        health.get("recommended_focus")
        or "Continue normal lead nurturing."
    )

    next_best_action = (
        recommendation.get("next_best_action")
        or "review_lead"
    )

    # ========================================================
    # LOAD FOLLOW-UPS
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
        item
        for item in follow_ups
        if (
            item.status or ""
        ).strip().lower() == "pending"
    ]

    overdue_follow_ups = [
        item
        for item in pending_follow_ups
        if (
            item.follow_up_date
            and item.follow_up_date < datetime.now()
        )
    ]

    # ========================================================
    # LOAD SITE VISITS
    # ========================================================

    site_visits = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.lead_id == lead.id
        )
        .order_by(
            SiteVisit.visit_date.asc(),
            SiteVisit.id.asc()
        )
        .all()
    )

    scheduled_visits = [
        visit
        for visit in site_visits
        if (
            visit.status or ""
        ).strip().lower() == "scheduled"
    ]

    missed_visits = [
        visit
        for visit in scheduled_visits
        if (
            visit.visit_date
            and visit.visit_date < datetime.now()
        )
    ]

    # ========================================================
    # DEFAULT
    # ========================================================

    follow_up_status = "WAIT"

    recommended_timing = "monitor"

    objective = (
        "Continue monitoring the lead and wait "
        "for the next meaningful sales event."
    )

    reason = (
        "No immediate follow-up trigger was detected."
    )

    # ========================================================
    # 1. MISSED SITE VISIT
    # ========================================================

    if missed_visits:

        follow_up_status = "ACT_NOW"

        recommended_timing = "immediately"

        objective = (
            "Contact the lead and reschedule "
            "the missed site visit."
        )

        reason = (
            "A scheduled site visit has passed "
            "without completion."
        )

    # ========================================================
    # 2. OVERDUE FOLLOW-UP
    # ========================================================

    elif overdue_follow_ups:

        follow_up_status = "ACT_NOW"

        recommended_timing = "immediately"

        objective = (
            "Complete the overdue follow-up and "
            "continue the sales conversation."
        )

        reason = (
            "The lead already has a follow-up that "
            "is past its scheduled date."
        )

    # ========================================================
    # 3. SCHEDULED SITE VISIT
    # ========================================================

    elif scheduled_visits:

        next_visit = scheduled_visits[0]

        follow_up_status = "WAIT"

        recommended_timing = "before_site_visit"

        objective = (
            "Confirm and prepare the customer "
            "for the scheduled site visit."
        )

        if next_visit.visit_date:

            reason = (
                "A site visit is already scheduled, "
                "so another generic follow-up should "
                "not be sent unnecessarily."
            )

        else:

            reason = (
                "A site visit is scheduled for this lead."
            )

    # ========================================================
    # 4. PENDING FOLLOW-UP
    # ========================================================

    elif pending_follow_ups:

        next_follow_up = pending_follow_ups[0]

        follow_up_status = "FOLLOW_UP"

        recommended_timing = "scheduled"

        objective = (
            "Complete the scheduled follow-up "
            "and continue the sales conversation."
        )

        if next_follow_up.follow_up_date:

            reason = (
                "The lead has an active scheduled "
                "follow-up."
            )

        else:

            reason = (
                "The lead has an active pending follow-up."
            )

    # ========================================================
    # 5. HIGH INTENT WITHOUT ACTIVE ACTION
    # ========================================================

    elif (
        lead.buying_intent
        and lead.buying_intent.strip().lower()
        == "high"
    ):

        follow_up_status = "FOLLOW_UP"

        recommended_timing = "soon"

        objective = (
            "Re-engage the high-intent lead and "
            "move the customer toward the next "
            "concrete sales step."
        )

        reason = (
            "The lead has high buying intent but "
            "does not currently have a pending "
            "follow-up or scheduled site visit."
        )

    # ========================================================
    # 6. ACTIVE LEAD WITHOUT NEXT ACTION
    # ========================================================

    elif (
        lead.pipeline_stage
        and lead.pipeline_stage.strip().upper()
        in {
            "QUALIFIED",
            "PROPERTY_INTEREST",
            "NEGOTIATION"
        }
    ):

        follow_up_status = "FOLLOW_UP"

        recommended_timing = "soon"

        objective = (
            recommended_focus
        )

        reason = (
            "The lead is active in the sales pipeline "
            "but does not currently have an upcoming "
            "follow-up or site visit."
        )

    # ========================================================
    # 7. COMMUNICATION INACTIVITY
    # ========================================================

    elif (
        health.get("signals", {})
        .get("inactivity_days") is not None
        and health.get("signals", {})
        .get("inactivity_days") >= 7
    ):

        follow_up_status = "FOLLOW_UP"

        recommended_timing = "soon"

        objective = (
            "Re-engage the lead and understand "
            "whether the property requirement is "
            "still active."
        )

        reason = (
            "There has been no recent communication "
            "with this active lead."
        )

    # ========================================================
    # 8. DEFAULT
    # ========================================================

    else:

        follow_up_status = "WAIT"

        recommended_timing = "monitor"

        objective = (
            "Continue normal lead nurturing."
        )

        reason = (
            "There is no immediate sales event "
            "requiring outreach."
        )

    # ========================================================
    # PRIORITY ADJUSTMENT
    # ========================================================

    if follow_up_status == "ACT_NOW":

        action_priority = "URGENT"

    elif (
        follow_up_status == "FOLLOW_UP"
        and priority in {
            "URGENT",
            "HIGH"
        }
    ):

        action_priority = "HIGH"

    elif follow_up_status == "FOLLOW_UP":

        action_priority = "MEDIUM"

    else:

        action_priority = priority

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "lead_id":
            lead.id,

        "lead_name":
            lead.name,

        "follow_up_status":
            follow_up_status,

        "recommended_timing":
            recommended_timing,

        "objective":
            objective,

        "reason":
            reason,

        "priority":
            action_priority,

        "health":
            health.get("health"),

        "lead_score":
            lead.lead_score or 0,

        "next_best_action":
            next_best_action,

        "risks":
            risks,

        "recommended_focus":
            recommended_focus
    }