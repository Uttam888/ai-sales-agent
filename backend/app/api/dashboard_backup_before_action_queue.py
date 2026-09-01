from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.lead import Lead
from app.models.follow_up import FollowUp

from app.services.lead_health import (
    calculate_lead_health
)


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
    db: Session = Depends(get_db)
):

    total_leads = (
        db.query(Lead)
        .count()
    )


    hot_leads = (
        db.query(Lead)
        .filter(
            Lead.lead_score >= 70
        )
        .count()
    )


    qualified_leads = (
        db.query(Lead)
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
        db.query(Lead)
        .filter(
            Lead.pipeline_stage
            == "SITE_VISIT"
        )
        .count()
    )


    pending_follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "pending"
        )
        .count()
    )


    converted_leads = (
        db.query(Lead)
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
    db: Session = Depends(get_db)
):

    leads = (
        db.query(Lead)
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
    db: Session = Depends(get_db)
):

    leads = (
        db.query(Lead)
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
    db: Session = Depends(get_db)
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

            db.query(Lead)

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
    db: Session = Depends(get_db)
):

    leads = (
        db.query(Lead)
        .order_by(
            Lead.lead_score.desc()
        )
        .all()
    )


    # --------------------------------------------------------
    # HEALTH COUNTS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # ANALYZE EACH LEAD
    # --------------------------------------------------------

    for lead in leads:

        health = calculate_lead_health(

            db=db,

            lead=lead

        )


        health_status = (
            health.get("health")
            or "COLD"
        )


        priority = (
            health.get("priority")
            or "LOW"
        )


        health_counts[
            health_status
        ] = (
            health_counts.get(
                health_status,
                0
            ) + 1
        )


        priority_counts[
            priority
        ] = (
            priority_counts.get(
                priority,
                0
            ) + 1
        )


        # ----------------------------------------------------
        # PRIORITY LEAD
        # ----------------------------------------------------

        if priority in {
            "URGENT",
            "HIGH"
        }:

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

                "recommended_focus":
                    health.get(
                        "recommended_focus"
                    ),

                "risks":
                    health.get(
                        "risks",
                        []
                    )

            })


    # --------------------------------------------------------
    # SORT PRIORITY LEADS
    # --------------------------------------------------------

    priority_order = {

        "URGENT": 4,

        "HIGH": 3,

        "MEDIUM": 2,

        "LOW": 1

    }


    priority_leads.sort(

        key=lambda lead: (

            priority_order.get(
                lead["priority"],
                0
            ),

            lead["lead_score"]

        ),

        reverse=True

    )


    # --------------------------------------------------------
    # FOLLOW-UP COUNTS
    # --------------------------------------------------------

    pending_follow_ups = (

        db.query(FollowUp)

        .filter(
            FollowUp.status
            == "pending"
        )

        .count()

    )


    completed_follow_ups = (

        db.query(FollowUp)

        .filter(
            FollowUp.status
            == "completed"
        )

        .count()

    )


    cancelled_follow_ups = (

        db.query(FollowUp)

        .filter(
            FollowUp.status
            == "cancelled"
        )

        .count()

    )


    # --------------------------------------------------------
    # SITE VISIT PIPELINE COUNT
    # --------------------------------------------------------

    scheduled_site_visits = (

        db.query(Lead)

        .filter(
            Lead.pipeline_stage
            == "SITE_VISIT"
        )

        .count()

    )


    # --------------------------------------------------------
    # TOP LEADS
    # --------------------------------------------------------

    top_leads = priority_leads[:5]


    # --------------------------------------------------------
    # BUILD RESPONSE
    # --------------------------------------------------------

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