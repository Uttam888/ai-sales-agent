from datetime import datetime

from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.follow_up import FollowUp
from app.models.site_visits import SiteVisit
from app.models.communication import CommunicationHistory
from app.models.sales_action_outcome import SalesActionOutcome
from app.services.lead_health import calculate_lead_health
from app.ai.tools import next_best_action


# ============================================================
# BUILD SALES HISTORY CONTEXT
# ============================================================

def build_sales_history_context(
    db: Session,
    lead: Lead,
    limit: int = 8
):
    """
    Build a compact recent-history summary from existing CRM
    records. This is intentionally deterministic and does not
    call an LLM.
    """

    events = []

    # --------------------------------------------------------
    # FOLLOW-UPS
    # --------------------------------------------------------

    follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.lead_id == lead.id
        )
        .order_by(
            FollowUp.follow_up_date.desc(),
            FollowUp.id.desc()
        )
        .limit(limit)
        .all()
    )

    for item in follow_ups:

        events.append({
            "type": "follow_up",
            "date": item.follow_up_date,
            "status": item.status,
            "message": item.message
        })

    # --------------------------------------------------------
    # SITE VISITS
    # --------------------------------------------------------

    site_visits = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.lead_id == lead.id
        )
        .order_by(
            SiteVisit.visit_date.desc(),
            SiteVisit.id.desc()
        )
        .limit(limit)
        .all()
    )

    for item in site_visits:

        events.append({
            "type": "site_visit",
            "date": item.visit_date,
            "status": item.status,
            "notes": item.notes,
            "id": item.id
        })

    # --------------------------------------------------------
    # COMMUNICATIONS
    # --------------------------------------------------------

    communications = (
        db.query(CommunicationHistory)
        .filter(
            CommunicationHistory.lead_id == lead.id
        )
        .order_by(
            CommunicationHistory.sent_at.desc(),
            CommunicationHistory.id.desc()
        )
        .limit(limit)
        .all()
    )

    for item in communications:

        events.append({
            "type": "communication",
            "date": item.sent_at or item.created_at,
            "status": item.status,
            "channel": item.channel,
            "direction": item.direction,
            "message": item.message
        })

    # --------------------------------------------------------
    # SORT + LIMIT
    # --------------------------------------------------------

    events.sort(
        key=lambda event: event["date"] or datetime.min,
        reverse=True
    )

    events = events[:limit]

    # --------------------------------------------------------
    # DERIVE HIGH-VALUE SALES SIGNALS
    # --------------------------------------------------------

    scheduled_visits = [
        event
        for event in events
        if (
            event["type"] == "site_visit"
            and str(event.get("status") or "").lower()
            == "scheduled"
        )
    ]

    completed_visits = [
        event
        for event in events
        if (
            event["type"] == "site_visit"
            and str(event.get("status") or "").lower()
            == "completed"
        )
    ]

    cancelled_visits = [
        event
        for event in events
        if (
            event["type"] == "site_visit"
            and str(event.get("status") or "").lower()
            == "cancelled"
        )
    ]

    pending_follow_ups = [
        event
        for event in events
        if (
            event["type"] == "follow_up"
            and str(event.get("status") or "").lower()
            == "pending"
        )
    ]

    recent_communications = [
        event
        for event in events
        if event["type"] == "communication"
    ]

    history_insights = []

    if scheduled_visits:
        history_insights.append(
            "A site visit is currently scheduled."
        )

    if cancelled_visits:
        history_insights.append(
            "The lead has a previously cancelled site visit."
        )

    if completed_visits:
        history_insights.append(
            "The lead has previously completed a site visit."
        )

    if pending_follow_ups:
        history_insights.append(
            "The lead has a pending follow-up."
        )

    if recent_communications:
        history_insights.append(
            f"{len(recent_communications)} recent communication "
            "record(s) are available."
        )

    # Special contextual signal:
    # cancelled visit + replacement scheduled visit.
    if cancelled_visits and scheduled_visits:
        history_insights.append(
            "A previous site visit was cancelled and a "
            "replacement visit is now scheduled."
        )

       # --------------------------------------------------------
    # SALES ACTION OUTCOMES
    # --------------------------------------------------------
    #
    # Expose recent AI sales action outcomes to the frontend.
    # This allows:
    #   1. Pending actions to be resolved through the
    #      "Record Outcome" UI.
    #   2. The complete action outcome history to be displayed
    #      in the Sales History & Outcomes section.
    #

    action_outcomes = (
        db.query(SalesActionOutcome)
        .filter(
            SalesActionOutcome.lead_id == lead.id
        )
        .order_by(
            SalesActionOutcome.created_at.desc(),
            SalesActionOutcome.id.desc()
        )
        .limit(limit)
        .all()
    )

    action_outcome_events = []

    for item in action_outcomes:
        action_outcome_events.append({
            "id": item.id,
            "action": item.action,
            "execution_status": item.execution_status,
            "outcome": item.outcome,
            "notes": item.notes,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        })

    latest_action_outcome_data = (
        action_outcome_events[0]
        if action_outcome_events
        else None
    )

    if action_outcome_events:
        history_insights.append(
            f"{len(action_outcome_events)} recent sales action "
            "outcome record(s) are available."
        )

    return {
        "events": events,
        "insights": history_insights,
        "event_count": len(events),
        "action_outcomes": action_outcome_events,
        "latest_action_outcome": latest_action_outcome_data
    }


# ============================================================
# SALES ACTION LEARNING
# ============================================================

def calculate_learned_action_score(
    db: Session,
    action: str
):
    """
    Calculate historical performance for one sales action.

    Outcomes:
      - successful / progressing = positive
      - negative = negative
      - pending = undecided

    The learner is intentionally descriptive and confidence-aware.
    It does not replace the deterministic next-best-action engine.
    """

    outcomes = (
        db.query(SalesActionOutcome)
        .filter(
            SalesActionOutcome.action == action
        )
        .order_by(
            SalesActionOutcome.created_at.desc(),
            SalesActionOutcome.id.desc()
        )
        .all()
    )

    positive = 0
    negative = 0
    pending = 0

    for item in outcomes:

        outcome = str(
            item.outcome or ""
        ).strip().lower()

        if outcome in {
            "successful",
            "progressing",
            "customer_interested",
        }:
            positive += 1

        elif outcome in {
            "negative",
            "customer_declined",
            "no_response",
            "lost",
        }:
            negative += 1

        else:
            pending += 1

    decided = positive + negative

    if decided == 0:

        positive_rate = 0.0
        learning_score = 0.0
        confidence = "NONE"

    else:

        positive_rate = (
            positive / decided
        ) * 100

        learning_score = positive_rate

        if decided < 3:
            confidence = "LOW"

        elif decided < 6:
            confidence = "MEDIUM"

        elif decided < 10:
            confidence = "HIGH"

        else:
            confidence = "VERY_HIGH"

    return {
        "action": action,
        "learning_score": round(
            learning_score,
            2
        ),
        "confidence": confidence,
        "positive_rate": round(
            positive_rate,
            2
        ),
        "sample_size": decided,
        "positive_outcomes": positive,
        "negative_outcomes": negative,
        "pending_outcomes": pending,
    }


def calculate_adaptive_action_score(
    lead: Lead,
    learned_action: dict
):
    """
    Apply a conservative, confidence-weighted historical
    adjustment to the lead score.

    The existing next_best_action() remains authoritative.
    Learning changes the score only; it does not silently
    change the selected action.
    """

    base_score = float(
        lead.lead_score or 0
    )

    sample_size = int(
        learned_action.get(
            "sample_size",
            0
        ) or 0
    )

    positive_rate = float(
        learned_action.get(
            "positive_rate",
            0
        ) or 0
    )

    confidence = (
        learned_action.get(
            "confidence"
        )
        or "NONE"
    )

    if sample_size == 0:

        return {
            "base_score": round(
                base_score,
                2
            ),
            "historical_positive_rate": 0.0,
            "historical_sample_size": 0,
            "learning_adjustment": 0.0,
            "adaptive_score": round(
                base_score,
                2
            ),
            "confidence": "NONE",
        }

    if sample_size < 3:
        confidence_factor = 0.25

    elif sample_size < 6:
        confidence_factor = 0.50

    elif sample_size < 10:
        confidence_factor = 0.75

    else:
        confidence_factor = 1.00

    # 50% historical performance is neutral.
    raw_adjustment = (
        positive_rate - 50
    ) * 0.20

    learning_adjustment = (
        raw_adjustment
        * confidence_factor
    )

    # Keep historical learning deliberately bounded.
    learning_adjustment = max(
        -10.0,
        min(
            10.0,
            learning_adjustment
        )
    )

    adaptive_score = (
        base_score
        + learning_adjustment
    )

    adaptive_score = max(
        0.0,
        min(
            100.0,
            adaptive_score
        )
    )

    return {
        "base_score": round(
            base_score,
            2
        ),
        "historical_positive_rate": round(
            positive_rate,
            2
        ),
        "historical_sample_size": sample_size,
        "learning_adjustment": round(
            learning_adjustment,
            2
        ),
        "adaptive_score": round(
            adaptive_score,
            2
        ),
        "confidence": confidence,
    }


# ============================================================
# AI SALES RECOMMENDATION
# ============================================================

def generate_sales_recommendation(
    db: Session,
    lead: Lead
):

    # ========================================================
    # LEAD HEALTH
    # ========================================================

    health = calculate_lead_health(
        db=db,
        lead=lead
    )

    # ========================================================
    # SALES HISTORY
    # ========================================================

    sales_history = build_sales_history_context(
        db=db,
        lead=lead
    )

    # ========================================================
    # NEXT BEST ACTION
    # ========================================================

    action_result = next_best_action(
        db=db,
        lead_id=lead.id
    )

    action = (
        action_result.get("action")
        or "review_lead"
    )

    # ========================================================
    # HISTORICAL ACTION LEARNING
    # ========================================================

    learned_action = calculate_learned_action_score(
        db=db,
        action=action
    )

    adaptive_action = calculate_adaptive_action_score(
        lead=lead,
        learned_action=learned_action
    )

    reason = (
        action_result.get("reason")
        or (
            "Review the lead and determine "
            "the next sales step."
        )
    )

    # ========================================================
    # NORMALIZE VALUES
    # ========================================================

    stage = (
        lead.pipeline_stage
        or "NEW"
    ).strip().upper()

    intent = (
        lead.buying_intent
        or "unknown"
    ).strip().lower()

    health_status = (
        health.get("health")
        or "COLD"
    )

    priority = (
        health.get("priority")
        or "LOW"
    )

    score = (
        lead.lead_score
        or 0
    )

    risks = (
        health.get("risks")
        or []
    )

    recommended_focus = (
        health.get("recommended_focus")
        or "Review the lead and determine the next action."
    )

    # --------------------------------------------------------
    # HISTORY-AWARE CONTEXT
    # --------------------------------------------------------

    history_insights = sales_history.get(
        "insights",
        []
    )

    if (
        action == "prepare_for_site_visit"
        and "A previous site visit was cancelled and a "
            "replacement visit is now scheduled."
            in history_insights
    ):

        reason = (
            reason
            + " The lead previously had a cancelled site "
            "visit, but a replacement visit is now scheduled, "
            "so the immediate focus is confirming the new visit."
        )

        recommended_focus = (
            "Confirm the replacement site visit and ensure "
            "the customer is prepared."
        )

    # --------------------------------------------------------
    # LEARNING-AWARE EXPLANATION
    # --------------------------------------------------------

    if learned_action["sample_size"] > 0:

        learning_context = (
            f"Historical outcomes for '{action}' show a "
            f"{learned_action['positive_rate']:.1f}% positive rate "
            f"across {learned_action['sample_size']} decided "
            f"outcome(s). Learning confidence is "
            f"{learned_action['confidence']}."
        )

    else:

        learning_context = (
            f"No decided historical outcomes are available "
            f"yet for '{action}'."
        )

    # ========================================================
    # RECOMMENDED ACTION
    # ========================================================

    if action == "complete_overdue_follow_up":

        recommended_action = (
            "Complete the overdue follow-up immediately."
        )

    elif action == "contact_and_reschedule_site_visit":

        recommended_action = (
            "Contact the customer and reschedule "
            "the missed site visit."
        )

    elif action == "reschedule_site_visit":

        recommended_action = (
            "Contact the customer and arrange "
            "a replacement site visit."
        )

    elif action == "prepare_for_site_visit":

        recommended_action = (
            "Confirm the scheduled site visit."
        )

    elif action == "follow_up_after_site_visit":

        recommended_action = (
            "Follow up after the site visit, "
            "collect feedback, and identify "
            "remaining objections."
        )

    elif action == "schedule_site_visit":

        recommended_action = (
            "Convert the lead's property interest "
            "into a scheduled site visit."
        )

    elif action == "recommend_properties":

        recommended_action = (
            "Recommend suitable properties based "
            "on the customer's requirements."
        )

    elif action == "discuss_negotiation":

        recommended_action = (
            "Address objections and move the "
            "lead toward negotiation and closing."
        )

    elif action == "contact_high_intent_lead":

        recommended_action = (
            "Contact the high-intent lead promptly "
            "and move them toward property selection "
            "or a site visit."
        )

    elif action == "qualify_lead":

        recommended_action = (
            "Complete the lead qualification process "
            "and confirm the customer's requirements."
        )

    elif action == "contact_lead":

        recommended_action = (
            "Contact the lead and understand "
            "their requirements."
        )

    # --------------------------------------------------------
    # BACKWARD COMPATIBILITY
    # --------------------------------------------------------

    elif action == "follow_up":

        recommended_action = (
            "Contact the lead and continue the "
            "sales conversation."
        )

    elif action == "negotiate":

        recommended_action = (
            "Address objections and move the "
            "lead toward negotiation."
        )

    elif action == "close":

        recommended_action = (
            "Move the lead toward conversion."
        )

    else:

        recommended_action = (
            recommended_focus
        )

    # ========================================================
    # URGENCY
    # ========================================================

    if priority == "URGENT":

        urgency = (
            "Act immediately."
        )

    elif priority == "HIGH":

        urgency = (
            "Act today."
        )

    elif priority == "MEDIUM":

        urgency = (
            "Follow up soon."
        )

    else:

        urgency = (
            "Continue normal lead nurturing."
        )

    # ========================================================
    # SUGGESTED MESSAGE
    # ========================================================

    lead_name = (
        lead.name
        or "there"
    )

    # --------------------------------------------------------
    # OVERDUE FOLLOW-UP
    # --------------------------------------------------------

    if action == "complete_overdue_follow_up":

        suggested_message = (
            f"Hi {lead_name}, I wanted to follow up "
            "regarding our previous conversation. "
            "Please let me know if you are still "
            "looking for a property and if there is "
            "anything I can help you with."
        )

    # --------------------------------------------------------
    # MISSED SITE VISIT
    # --------------------------------------------------------

    elif action == "contact_and_reschedule_site_visit":

        suggested_message = (
            f"Hi {lead_name}, I wanted to check in "
            "regarding your scheduled site visit. "
            "It looks like the visit may not have "
            "been completed. Please let me know if "
            "you would like to reschedule it for a "
            "more convenient time."
        )

    # --------------------------------------------------------
    # CANCELLED SITE VISIT
    # --------------------------------------------------------

    elif action == "reschedule_site_visit":

        suggested_message = (
            f"Hi {lead_name}, I noticed that your "
            "previous site visit was cancelled. "
            "Would you like me to help arrange "
            "another convenient time for the visit?"
        )

    # --------------------------------------------------------
    # UPCOMING SITE VISIT
    # --------------------------------------------------------

    elif action == "prepare_for_site_visit":

        suggested_message = (
            f"Hi {lead_name}, just confirming your "
            "scheduled site visit. Please let me know "
            "if you need directions or any additional "
            "property details before your visit."
        )

    # --------------------------------------------------------
    # AFTER SITE VISIT
    # --------------------------------------------------------

    elif action == "follow_up_after_site_visit":

        suggested_message = (
            f"Hi {lead_name}, I wanted to follow up "
            "after your recent site visit. I would "
            "love to hear your feedback and know if "
            "you have any questions or concerns about "
            "the property."
        )

    # --------------------------------------------------------
    # SCHEDULE SITE VISIT
    # --------------------------------------------------------

    elif action == "schedule_site_visit":

        suggested_message = (
            f"Hi {lead_name}, I wanted to check if "
            "you would like to schedule a site visit "
            "for one of the properties we discussed."
        )

    # --------------------------------------------------------
    # RECOMMEND PROPERTIES
    # --------------------------------------------------------

    elif action == "recommend_properties":

        suggested_message = (
            f"Hi {lead_name}, based on your requirements, "
            "I can share some suitable property options "
            "with you. Please let me know if you would "
            "like to review them."
        )

    # --------------------------------------------------------
    # NEGOTIATION
    # --------------------------------------------------------

    elif action == "discuss_negotiation":

        suggested_message = (
            f"Hi {lead_name}, I wanted to follow up "
            "regarding the property and see if there "
            "are any questions or concerns about the "
            "pricing or terms that I can help address."
        )

    # --------------------------------------------------------
    # HIGH INTENT
    # --------------------------------------------------------

    elif action == "contact_high_intent_lead":

        suggested_message = (
            f"Hi {lead_name}, I wanted to follow up "
            "regarding your property requirements. "
            "I can help you shortlist suitable options "
            "or arrange a site visit based on your "
            "preferences."
        )

    # --------------------------------------------------------
    # QUALIFICATION
    # --------------------------------------------------------

    elif action == "qualify_lead":

        suggested_message = (
            f"Hi {lead_name}, I wanted to understand "
            "your property requirements a little better "
            "so I can suggest the most suitable options. "
            "Please let me know your preferred location, "
            "budget, property type, and timeline."
        )

    # --------------------------------------------------------
    # GENERIC CONTACT
    # --------------------------------------------------------

    else:

        suggested_message = (
            f"Hi {lead_name}, I wanted to follow up "
            "regarding your property requirements and "
            "see how I can help."
        )

    # ========================================================
    # BUILD RECOMMENDATION
    # ========================================================

    return {

        "lead_id":
            lead.id,

        "lead_name":
            lead.name,

        "health":
            health_status,

        "priority":
            priority,

        "lead_score":
            score,

        "pipeline_stage":
            stage,

        "buying_intent":
            intent,

        "next_best_action":
            action,

        "recommended_action":
            recommended_action,

        "reason":
            reason,

        "urgency":
            urgency,

        "suggested_message":
            suggested_message,

        "risks":
            risks,

        "recommended_focus":
            recommended_focus,

        # ----------------------------------------------------
        # SALES HISTORY
        # ----------------------------------------------------

        "sales_history":
            sales_history,

        # ----------------------------------------------------
        # HISTORICAL LEARNING
        # ----------------------------------------------------

        "learning":
            learned_action,

        "adaptive_action":
            adaptive_action,

        "learning_context":
            learning_context

    }