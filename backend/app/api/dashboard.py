from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.lead import Lead
from app.models.follow_up import FollowUp
from app.models.site_visits import SiteVisit
from app.models.sales_action_outcome import SalesActionOutcome

from app.services.lead_health import (
    calculate_lead_health
)

from app.services.sales_performance import (
    generate_sales_performance_insights
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
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
# DASHBOARD SUMMARY
# ============================================================

@router.get("/summary")
def dashboard_summary(

    db: Session = Depends(
        get_db
    )

):

    total_leads = (

        db.query(
            Lead
        )

        .count()

    )


    hot_leads = (

        db.query(
            Lead
        )

        .filter(
            Lead.lead_score >= 70
        )

        .count()

    )


    qualified_leads = (

        db.query(
            Lead
        )

        .filter(
            Lead.qualification_status
            == "qualified"
        )

        .count()

    )


    # --------------------------------------------------------
    # SITE VISITS
    # --------------------------------------------------------

    site_visits = (

        db.query(
            Lead
        )

        .filter(
            Lead.pipeline_stage
            == "SITE_VISIT"
        )

        .count()

    )


    pending_follow_ups = (

        db.query(
            FollowUp
        )

        .filter(
            FollowUp.status
            == "pending"
        )

        .count()

    )


    converted_leads = (

        db.query(
            Lead
        )

        .filter(
            Lead.pipeline_stage
            == "CONVERTED"
        )

        .count()

    )


    # --------------------------------------------------------
    # AVERAGE LEAD SCORE
    # --------------------------------------------------------

    average_score = 0


    if total_leads > 0:

        scores = (

            db.query(
                Lead.lead_score
            )

            .all()

        )


        score_values = [

            row[0] or 0

            for row in scores

        ]


        if score_values:

            average_score = round(

                sum(score_values)
                / len(score_values),

                2

            )


    return {

        "total_leads":
            total_leads,

        "hot_leads":
            hot_leads,

        "qualified_leads":
            qualified_leads,

        "site_visits":
            site_visits,

        "pending_follow_ups":
            pending_follow_ups,

        "converted_leads":
            converted_leads,

        "average_lead_score":
            average_score

    }


# ============================================================
# HOT LEADS
# ============================================================

@router.get("/hot-leads")
def get_hot_leads(

    db: Session = Depends(
        get_db
    )

):

    leads = (

        db.query(
            Lead
        )

        .filter(
            Lead.lead_score >= 70
        )

        .order_by(
            Lead.lead_score.desc()
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
                    lead.pipeline_stage

            }

            for lead in leads

        ]

    }


# ============================================================
# ALL LEADS
# ============================================================

@router.get("/leads")
def get_dashboard_leads(

    db: Session = Depends(
        get_db
    )

):

    leads = (

        db.query(
            Lead
        )

        .order_by(

            Lead.lead_score.desc(),

            Lead.updated_at.desc()

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
                    (
                        lead.created_at.isoformat()
                        if lead.created_at
                        else None
                    ),

                "updated_at":
                    (
                        lead.updated_at.isoformat()
                        if lead.updated_at
                        else None
                    )

            }

            for lead in leads

        ]

    }


# ============================================================
# PIPELINE SUMMARY
# ============================================================

@router.get("/pipeline")
def pipeline_summary(

    db: Session = Depends(
        get_db
    )

):

    stages = [

        "NEW",

        "CONTACTED",

        "QUALIFIED",

        "PROPERTY_INTEREST",

        "SITE_VISIT",

        "NEGOTIATION",

        "CONVERTED"

    ]


    result = {}


    for stage in stages:

        result[stage] = (

            db.query(
                Lead
            )

            .filter(
                Lead.pipeline_stage
                == stage
            )

            .count()

        )


    return {

        "pipeline":
            result

    }


# ============================================================
# SALES DASHBOARD INTELLIGENCE
# ============================================================

@router.get("/intelligence")
def dashboard_intelligence(

    db: Session = Depends(
        get_db
    )

):

    leads = (

        db.query(
            Lead
        )

        .order_by(
            Lead.lead_score.desc()
        )

        .all()

    )


    now = datetime.now()


    # ========================================================
    # HEALTH COUNTS
    # ========================================================

    health_counts = {

        "HOT": 0,

        "WARM": 0,

        "COLD": 0,

        "CONVERTED": 0

    }


    priority_counts = {

        "URGENT": 0,

        "HIGH": 0,

        "MEDIUM": 0,

        "LOW": 0

    }


    priority_leads = []


    # ========================================================
    # ANALYZE EACH LEAD
    # ========================================================

    for lead in leads:

        health = calculate_lead_health(

            db=db,

            lead=lead

        )


        health_status = (

            health.get(
                "health"
            )

            or "COLD"

        )


        priority = (

            health.get(
                "priority"
            )

            or "LOW"

        )


        signals = (

            health.get(
                "signals"
            )

            or {}

        )


        risks = (

            health.get(
                "risks"
            )

            or []

        )


        # ====================================================
        # UPDATE COUNTS
        # ====================================================

        health_counts[
            health_status
        ] = (

            health_counts.get(
                health_status,
                0
            )

            + 1

        )


        priority_counts[
            priority
        ] = (

            priority_counts.get(
                priority,
                0
            )

            + 1

        )


        # ====================================================
        # ONLY ACTIONABLE LEADS
        # ====================================================

        if priority not in {

            "URGENT",

            "HIGH"

        }:

            continue


        # ====================================================
        # ACTIVITY SIGNALS
        # ====================================================

        pending_follow_ups = (

            signals.get(
                "pending_follow_ups",
                0
            )

            or 0

        )


        overdue_follow_ups = (

            signals.get(
                "overdue_follow_ups",
                0
            )

            or 0

        )


        scheduled_site_visits = (

            signals.get(
                "scheduled_site_visits",
                0
            )

            or 0

        )


        completed_site_visits = (

            signals.get(
                "completed_site_visits",
                0
            )

            or 0

        )


        cancelled_site_visits = (

            signals.get(
                "cancelled_site_visits",
                0
            )

            or 0

        )


        # ====================================================
        # DETECT MISSED SITE VISIT
        # ====================================================

        missed_site_visit = False


        site_visits = (

            db.query(
                SiteVisit
            )

            .filter(
                SiteVisit.lead_id
                == lead.id
            )

            .all()

        )


        for visit in site_visits:

            visit_status = (

                str(
                    visit.status
                    or ""
                )

                .strip()
                .lower()

            )


            if (

                visit_status
                == "scheduled"

                and visit.visit_date

                and visit.visit_date < now

            ):

                missed_site_visit = True

                break


        # ====================================================
        # ACTION URGENCY
        # ====================================================

        action_urgency = 0


        urgency_reason = (

            "No immediate urgency signal detected."

        )


        urgency_level = "UPCOMING"


        # ====================================================
        # MISSED SITE VISIT
        # ====================================================

        if missed_site_visit:

            action_urgency += 100

            urgency_level = "ACT NOW"

            urgency_reason = (

                "A scheduled site visit "
                "has already passed without "
                "completion."

            )


        # ====================================================
        # OVERDUE FOLLOW-UP
        # ====================================================

        elif overdue_follow_ups > 0:

            action_urgency += 90

            urgency_level = "ACT NOW"

            urgency_reason = (

                f"{overdue_follow_ups} overdue "
                "follow-up(s) require attention."

            )


        # ====================================================
        # SCHEDULED SITE VISIT
        # ====================================================

        elif scheduled_site_visits > 0:

            action_urgency += 70

            urgency_level = "UPCOMING"

            urgency_reason = (

                "A site visit is currently "
                "scheduled."

            )


        # ====================================================
        # PENDING FOLLOW-UP
        # ====================================================

        elif pending_follow_ups > 0:

            action_urgency += 60

            urgency_level = "DO NEXT"

            urgency_reason = (

                f"{pending_follow_ups} pending "
                "follow-up(s) require attention."

            )


        # ====================================================
        # HIGH BUYING INTENT
        # ====================================================

        if (

            str(
                lead.buying_intent
                or ""
            )

            .strip()
            .lower()

            == "high"

        ):

            action_urgency += 25


        # ====================================================
        # CANCELLED VISIT HISTORY
        # ====================================================

        if cancelled_site_visits > 0:

            action_urgency += 10


            if urgency_level == "UPCOMING":

                urgency_reason = (

                    "A scheduled site visit exists "
                    "and the lead has previous "
                    "cancelled visit history."

                )


        # ====================================================
        # NO ACTIVE SALES ACTION
        # ====================================================

        if (

            pending_follow_ups == 0

            and scheduled_site_visits == 0

            and not missed_site_visit

            and overdue_follow_ups == 0

        ):

            action_urgency += 20

            urgency_level = "DO NEXT"

            urgency_reason = (

                "The lead is high priority "
                "but currently has no active "
                "follow-up or scheduled visit."

            )


        # ====================================================
        # ADD TO ACTION QUEUE
        # ====================================================

        priority_leads.append({

            "id":
                lead.id,

            "name":
                lead.name,

            "lead_score":
                lead.lead_score,

            "health":
                health_status,

            "priority":
                priority,

            "pipeline_stage":
                lead.pipeline_stage,

            "buying_intent":
                lead.buying_intent,

            "action_urgency":
                action_urgency,

            "urgency_level":
                urgency_level,

            "urgency_reason":
                urgency_reason,

            "recommended_focus":
                health.get(
                    "recommended_focus"
                ),

            "risks":
                risks,

            "signals": {

                "pending_follow_ups":
                    pending_follow_ups,

                "overdue_follow_ups":
                    overdue_follow_ups,

                "scheduled_site_visits":
                    scheduled_site_visits,

                "completed_site_visits":
                    completed_site_visits,

                "cancelled_site_visits":
                    cancelled_site_visits,

                "missed_site_visit":
                    missed_site_visit

            }

        })


    # ========================================================
    # SORT AI ACTION QUEUE
    # ========================================================

    priority_order = {

        "URGENT": 4,

        "HIGH": 3,

        "MEDIUM": 2,

        "LOW": 1

    }


    priority_leads.sort(

        key=lambda lead: (

            lead["action_urgency"],

            priority_order.get(
                lead["priority"],
                0
            ),

            lead["lead_score"]

        ),

        reverse=True

    )


    # ========================================================
    # FOLLOW-UP COUNTS
    # ========================================================

    pending_follow_ups = (

        db.query(
            FollowUp
        )

        .filter(
            FollowUp.status
            == "pending"
        )

        .count()

    )


    completed_follow_ups = (

        db.query(
            FollowUp
        )

        .filter(
            FollowUp.status
            == "completed"
        )

        .count()

    )


    cancelled_follow_ups = (

        db.query(
            FollowUp
        )

        .filter(
            FollowUp.status
            == "cancelled"
        )

        .count()

    )


    # ========================================================
    # SITE VISIT PIPELINE COUNT
    # ========================================================

    scheduled_site_visits = (

        db.query(
            Lead
        )

        .filter(
            Lead.pipeline_stage
            == "SITE_VISIT"
        )

        .count()

    )


    # ========================================================
    # TOP ACTIONABLE LEADS
    # ========================================================

    top_leads = (
        priority_leads[:5]
    )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "total_leads":
            len(leads),

        "health": {

            "hot":
                health_counts["HOT"],

            "warm":
                health_counts["WARM"],

            "cold":
                health_counts["COLD"],

            "converted":
                health_counts["CONVERTED"]

        },

        "priority": {

            "urgent":
                priority_counts["URGENT"],

            "high":
                priority_counts["HIGH"],

            "medium":
                priority_counts["MEDIUM"],

            "low":
                priority_counts["LOW"]

        },

        "activities": {

            "pending_follow_ups":
                pending_follow_ups,

            "completed_follow_ups":
                completed_follow_ups,

            "cancelled_follow_ups":
                cancelled_follow_ups,

            "scheduled_site_visits":
                scheduled_site_visits

        },

        "priority_leads":
            priority_leads,

        "top_leads":
            top_leads

    }


# ============================================================
# SALES ANALYTICS
# ============================================================

@router.get("/analytics")
def sales_analytics(
    db: Session = Depends(
        get_db
    )
):

    # --------------------------------------------------------
    # LEAD COUNTS
    # --------------------------------------------------------

    total_leads = (
        db.query(
            Lead
        )
        .count()
    )

    converted_leads = (
        db.query(
            Lead
        )
        .filter(
            Lead.pipeline_stage
            == "CONVERTED"
        )
        .count()
    )

    conversion_rate = 0

    if total_leads > 0:
        conversion_rate = round(
            (
                converted_leads
                / total_leads
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # LEAD SCORE
    # --------------------------------------------------------

    score_rows = (
        db.query(
            Lead.lead_score
        )
        .all()
    )

    score_values = [
        row[0] or 0
        for row in score_rows
    ]

    average_lead_score = 0

    if score_values:
        average_lead_score = round(
            sum(score_values)
            / len(score_values),
            2
        )

    # --------------------------------------------------------
    # PIPELINE DISTRIBUTION
    # --------------------------------------------------------

    pipeline_stages = [
        "NEW",
        "CONTACTED",
        "QUALIFIED",
        "PROPERTY_INTEREST",
        "SITE_VISIT",
        "NEGOTIATION",
        "CONVERTED"
    ]

    pipeline = {}

    for stage in pipeline_stages:

        pipeline[stage] = (
            db.query(
                Lead
            )
            .filter(
                Lead.pipeline_stage
                == stage
            )
            .count()
        )

    # --------------------------------------------------------
    # SALES ACTION OUTCOMES
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

    total_action_outcomes = len(
        outcomes
    )

    pending_outcomes = 0
    successful_outcomes = 0
    progressing_outcomes = 0
    negative_outcomes = 0

    outcome_breakdown = {}
    action_performance = {}

    positive_outcomes = {
        "successful",
        "customer_interested",
        "rescheduled",
        "converted"
    }

    negative_outcome_values = {
        "customer_declined",
        "no_response",
        "lost"
    }

    progressing_outcome_values = {
        "rescheduled",
        "customer_interested"
    }

    for item in outcomes:

        outcome = (
            str(
                item.outcome
                or "pending"
            )
            .strip()
            .lower()
        )

        action = (
            str(
                item.action
                or "unknown"
            )
            .strip()
            .lower()
        )

        outcome_breakdown[outcome] = (
            outcome_breakdown.get(
                outcome,
                0
            ) + 1
        )

        if outcome == "pending":

            pending_outcomes += 1

        # Keep outcome categories mutually clear:
        # progressing outcomes are not counted as fully successful.
        if outcome in progressing_outcome_values:

            progressing_outcomes += 1

        elif outcome in positive_outcomes:

            successful_outcomes += 1

        elif outcome in negative_outcome_values:

            negative_outcomes += 1

        if action not in action_performance:

            action_performance[action] = {
                "total": 0,
                "successful": 0,
                "progressing": 0,
                "negative": 0,
                "pending": 0
            }

        stats = action_performance[action]

        stats["total"] += 1

        if outcome == "pending":
            stats["pending"] += 1

        elif outcome in negative_outcome_values:
            stats["negative"] += 1

        elif outcome in progressing_outcome_values:
            stats["progressing"] += 1

        elif outcome in positive_outcomes:
            stats["successful"] += 1

    # --------------------------------------------------------
    # ACTION SUCCESS RATES
    # --------------------------------------------------------

    for action, stats in action_performance.items():

        decided = (
            stats["successful"]
            + stats["negative"]
        )

        if decided > 0:

            stats["success_rate"] = round(
                (
                    stats["successful"]
                    / decided
                ) * 100,
                2
            )

        else:

            stats["success_rate"] = 0

    # --------------------------------------------------------
    # FOLLOW-UP PERFORMANCE
    # --------------------------------------------------------

    total_follow_ups = (
        db.query(
            FollowUp
        )
        .count()
    )

    completed_follow_ups = (
        db.query(
            FollowUp
        )
        .filter(
            FollowUp.status
            == "completed"
        )
        .count()
    )

    cancelled_follow_ups = (
        db.query(
            FollowUp
        )
        .filter(
            FollowUp.status
            == "cancelled"
        )
        .count()
    )

    pending_follow_ups = (
        db.query(
            FollowUp
        )
        .filter(
            FollowUp.status
            == "pending"
        )
        .count()
    )

    follow_up_completion_rate = 0

    if total_follow_ups > 0:

        follow_up_completion_rate = round(
            (
                completed_follow_ups
                / total_follow_ups
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # SITE VISIT PERFORMANCE
    # --------------------------------------------------------

    total_site_visits = (
        db.query(
            SiteVisit
        )
        .count()
    )

    completed_site_visits = (
        db.query(
            SiteVisit
        )
        .filter(
            SiteVisit.status
            == "completed"
        )
        .count()
    )

    cancelled_site_visits = (
        db.query(
            SiteVisit
        )
        .filter(
            SiteVisit.status
            == "cancelled"
        )
        .count()
    )

    scheduled_site_visits = (
        db.query(
            SiteVisit
        )
        .filter(
            SiteVisit.status
            == "scheduled"
        )
        .count()
    )

    site_visit_completion_rate = 0

    if total_site_visits > 0:

        site_visit_completion_rate = round(
            (
                completed_site_visits
                / total_site_visits
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # OUTCOME RATE
    # --------------------------------------------------------

    decided_outcomes = (
        successful_outcomes
        + progressing_outcomes
        + negative_outcomes
    )

    action_success_rate = 0

    if decided_outcomes > 0:

        action_success_rate = round(
            (
                successful_outcomes
                / decided_outcomes
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # RETURN ANALYTICS
    # --------------------------------------------------------

    return {

        "leads": {
            "total": total_leads,
            "converted": converted_leads,
            "conversion_rate": conversion_rate,
            "average_score": average_lead_score
        },

        "pipeline":
            pipeline,

        "sales_actions": {

            "total": total_action_outcomes,

            "pending": pending_outcomes,

            "successful": successful_outcomes,

            "progressing": progressing_outcomes,

            "negative": negative_outcomes,

            "success_rate":
                action_success_rate,

            "success_rate_definition":
                "Fully successful, progressing, and negative outcomes are treated as decided; pending outcomes are excluded.",

            "outcome_breakdown":
                outcome_breakdown,

            "action_performance":
                action_performance

        },

        "follow_ups": {

            "total":
                total_follow_ups,

            "pending":
                pending_follow_ups,

            "completed":
                completed_follow_ups,

            "cancelled":
                cancelled_follow_ups,

            "completion_rate":
                follow_up_completion_rate

        },

        "site_visits": {

            "total":
                total_site_visits,

            "scheduled":
                scheduled_site_visits,

            "completed":
                completed_site_visits,

            "cancelled":
                cancelled_site_visits,

            "completion_rate":
                site_visit_completion_rate

        }

    }

# ============================================================
# AI SALES PERFORMANCE INSIGHTS
# ============================================================

@router.get("/performance-insights")
def get_sales_performance_insights(
    db: Session = Depends(
        get_db
    )
):

    # --------------------------------------------------------
    # GET CURRENT SALES ANALYTICS
    # --------------------------------------------------------

    analytics = sales_analytics(
        db=db
    )

    # --------------------------------------------------------
    # GENERATE MANAGEMENT INSIGHTS
    # --------------------------------------------------------

    performance = (
        generate_sales_performance_insights(
            analytics=analytics
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {
        "analytics": analytics,
        "performance": performance
    }

