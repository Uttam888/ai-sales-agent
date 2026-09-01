from typing import Any, Dict, List


# ============================================================
# AI LEAD OPPORTUNITY DETECTION
# ============================================================

def generate_lead_opportunity(
    lead: Any,
    health: Dict[str, Any],
    recommendation: Dict[str, Any],
    follow_up_intelligence: Dict[str, Any],
):
    """
    Convert existing lead intelligence into an
    opportunity/attention classification.

    This service does not modify the lead or database.
    """

    # ========================================================
    # BASIC INTELLIGENCE
    # ========================================================

    score = (
        lead.lead_score
        or 0
    )

    lead_health = (
        health.get("health")
        or "UNKNOWN"
    )

    priority = (
        health.get("priority")
        or "LOW"
    )

    buying_intent = (
        health.get("buying_intent")
        or lead.buying_intent
        or "unknown"
    )

    next_action = (
        recommendation.get(
            "next_best_action"
        )
        or "contact_lead"
    )

    recommended_focus = (
        recommendation.get(
            "recommended_focus"
        )
        or health.get(
            "recommended_focus"
        )
        or "Review the lead."
    )

    follow_up_status = (
        follow_up_intelligence.get(
            "follow_up_status"
        )
        or "UNKNOWN"
    )

    # ========================================================
    # RESPECT FOLLOW-UP INTELLIGENCE
    # ========================================================
    #
    # If follow-up intelligence says WAIT and the recommendation
    # jumps ahead to a post-site-visit action, keep the
    # opportunity engine aligned with the current sales stage.
    #
    # Correct sequence:
    #
    # Scheduled visit
    #       ↓
    # WAIT
    #       ↓
    # Prepare / confirm visit
    #       ↓
    # Visit completed
    #       ↓
    # Follow up after visit

    if (
        follow_up_status == "WAIT"
        and next_action
        == "follow_up_after_site_visit"
    ):

        next_action = (
            "prepare_for_site_visit"
        )

    # ========================================================
    # RISKS
    # ========================================================

    risks = (
        health.get(
            "risks"
        )
        or recommendation.get(
            "risks"
        )
        or []
    )

    # ========================================================
    # OPPORTUNITY SIGNALS
    # ========================================================

    positive_signals: List[str] = []

    if score >= 80:

        positive_signals.append(
            "High lead score."
        )

    if lead_health == "HOT":

        positive_signals.append(
            "Lead health is HOT."
        )

    if (
        str(
            buying_intent
        ).lower()
        == "high"
    ):

        positive_signals.append(
            "High buying intent."
        )

    if next_action in {

        "prepare_for_site_visit",

        "follow_up_after_site_visit",

        "discuss_negotiation",

        "contact_high_intent_lead",

    }:

        positive_signals.append(
            "Lead is in an active sales stage."
        )

    # ========================================================
    # RISK SIGNALS
    # ========================================================

    risk_signals: List[str] = []

    risk_signals.extend(

        [
            str(risk)
            for risk in risks
            if risk
        ]

    )

    if follow_up_status == "ACT_NOW":

        risk_signals.append(
            "Lead requires immediate follow-up."
        )

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    if follow_up_status == "ACT_NOW":

        classification = (
            "AT_RISK"
        )

        action_priority = (
            "URGENT"
        )

    elif (

        score >= 80

        and lead_health == "HOT"

        and str(
            buying_intent
        ).lower()
        == "high"

    ):

        classification = (
            "TOP_OPPORTUNITY"
        )

        action_priority = (
            "HIGH"
        )

    elif score >= 70:

        classification = (
            "STRONG_OPPORTUNITY"
        )

        action_priority = (
            "HIGH"
        )

    elif score >= 50:

        classification = (
            "DEVELOPING"
        )

        action_priority = (
            "MEDIUM"
        )

    else:

        classification = (
            "LOW_OPPORTUNITY"
        )

        action_priority = (
            "LOW"
        )

    # ========================================================
    # PRIMARY REASON
    # ========================================================

    if classification == "AT_RISK":

        primary_reason = (

            risk_signals[0]

            if risk_signals

            else
            "The lead requires immediate attention."

        )

    elif positive_signals:

        primary_reason = (

            " ".join(

                positive_signals[:3]

            )

        )

    else:

        primary_reason = (

            "The lead currently has limited "
            "positive sales signals."

        )

    # ========================================================
    # RECOMMENDED ACTION
    # ========================================================

    if classification == "AT_RISK":

        recommended_action = (

            recommendation.get(
                "recommended_action"
            )

            or
            "Take immediate corrective action."

        )

    elif (
        next_action
        == "prepare_for_site_visit"
    ):

        recommended_action = (

            "Confirm the scheduled site visit "
            "and ensure the customer is prepared."

        )

    elif (
        next_action
        == "follow_up_after_site_visit"
    ):

        recommended_action = (

            recommendation.get(
                "recommended_action"
            )

            or
            "Follow up after the completed site visit."

        )

    else:

        recommended_action = (

            recommendation.get(
                "recommended_action"
            )

            or recommended_focus

        )

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "lead_id":
            lead.id,

        "lead_name":
            lead.name,

        "classification":
            classification,

        "action_priority":
            action_priority,

        "lead_score":
            score,

        "health":
            lead_health,

        "buying_intent":
            buying_intent,

        "follow_up_status":
            follow_up_status,

        "next_best_action":
            next_action,

        "primary_reason":
            primary_reason,

        "recommended_action":
            recommended_action,

        "recommended_focus":
            recommended_focus,

        "positive_signals":
            positive_signals,

        "risk_signals":
            risk_signals,

        "risk_count":
            len(
                risk_signals
            ),

    }