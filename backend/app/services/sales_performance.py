from typing import Any, Dict, List


# ============================================================
# SALES PERFORMANCE INSIGHTS
# ============================================================

def generate_sales_performance_insights(
    analytics: Dict[str, Any]
):
    """
    Convert raw sales analytics into actionable
    management-level insights.

    This service does not modify database data.
    It only interprets the analytics already calculated
    by the dashboard analytics endpoint.
    """

    leads = analytics.get(
        "leads",
        {}
    )

    pipeline = analytics.get(
        "pipeline",
        {}
    )

    sales_actions = analytics.get(
        "sales_actions",
        {}
    )

    follow_ups = analytics.get(
        "follow_ups",
        {}
    )

    site_visits = analytics.get(
        "site_visits",
        {}
    )

    insights: List[Dict[str, Any]] = []

    # ========================================================
    # LEAD CONVERSION
    # ========================================================

    total_leads = (
        leads.get("total")
        or 0
    )

    converted_leads = (
        leads.get("converted")
        or 0
    )

    conversion_rate = (
        leads.get("conversion_rate")
        or 0
    )

    if total_leads == 0:

        insights.append({
            "type": "info",
            "category": "conversion",
            "priority": "LOW",
            "title": "No leads available",
            "message": (
                "There are currently no leads in the sales pipeline."
            )
        })

    elif converted_leads == 0:

        insights.append({
            "type": "warning",
            "category": "conversion",
            "priority": "HIGH",
            "title": "No conversions yet",
            "message": (
                "No leads have converted yet. "
                "Focus on moving active leads toward "
                "completed site visits, negotiation, and conversion."
            )
        })

    elif conversion_rate < 10:

        insights.append({
            "type": "warning",
            "category": "conversion",
            "priority": "HIGH",
            "title": "Low conversion rate",
            "message": (
                f"Current conversion rate is {conversion_rate}%. "
                "Review stalled leads and strengthen follow-up "
                "after high-intent interactions."
            )
        })

    else:

        insights.append({
            "type": "positive",
            "category": "conversion",
            "priority": "MEDIUM",
            "title": "Conversions are progressing",
            "message": (
                f"{converted_leads} lead(s) have converted, "
                f"giving a {conversion_rate}% conversion rate."
            )
        })

    # ========================================================
    # PIPELINE CONCENTRATION
    # ========================================================

    if total_leads > 0:

        stage_counts = {
            str(stage): int(count or 0)
            for stage, count in pipeline.items()
        }

        non_zero_stages = {
            stage: count
            for stage, count in stage_counts.items()
            if count > 0
        }

        if non_zero_stages:

            dominant_stage = max(
                non_zero_stages,
                key=non_zero_stages.get
            )

            dominant_count = non_zero_stages[
                dominant_stage
            ]

            dominant_percentage = round(
                (
                    dominant_count
                    / total_leads
                ) * 100,
                2
            )

            if dominant_percentage >= 50:

                insights.append({
                    "type": "warning",
                    "category": "pipeline",
                    "priority": "HIGH",
                    "title": "Pipeline is concentrated",
                    "message": (
                        f"{dominant_count} of {total_leads} leads "
                        f"({dominant_percentage}%) are currently in "
                        f"{dominant_stage.replace('_', ' ')}."
                    ),
                    "stage": dominant_stage,
                    "lead_count": dominant_count,
                    "percentage": dominant_percentage
                })

            else:

                insights.append({
                    "type": "info",
                    "category": "pipeline",
                    "priority": "MEDIUM",
                    "title": "Dominant pipeline stage",
                    "message": (
                        f"{dominant_stage.replace('_', ' ')} currently "
                        f"contains the largest number of leads "
                        f"({dominant_count})."
                    ),
                    "stage": dominant_stage,
                    "lead_count": dominant_count,
                    "percentage": dominant_percentage
                })

    # ========================================================
    # FOLLOW-UP PERFORMANCE
    # ========================================================

    total_follow_ups = (
        follow_ups.get("total")
        or 0
    )

    pending_follow_ups = (
        follow_ups.get("pending")
        or 0
    )

    completed_follow_ups = (
        follow_ups.get("completed")
        or 0
    )

    follow_up_completion_rate = (
        follow_ups.get("completion_rate")
        or 0
    )

    if total_follow_ups > 0:

        if follow_up_completion_rate < 50:

            insights.append({
                "type": "warning",
                "category": "follow_up",
                "priority": "HIGH",
                "title": "Follow-up execution is low",
                "message": (
                    f"Only {follow_up_completion_rate}% of follow-ups "
                    f"have been completed. {pending_follow_ups} "
                    "follow-up(s) remain pending."
                ),
                "completion_rate":
                    follow_up_completion_rate,
                "pending":
                    pending_follow_ups
            })

        elif follow_up_completion_rate < 80:

            insights.append({
                "type": "warning",
                "category": "follow_up",
                "priority": "MEDIUM",
                "title": "Follow-up completion can improve",
                "message": (
                    f"Follow-up completion is currently "
                    f"{follow_up_completion_rate}%."
                ),
                "completion_rate":
                    follow_up_completion_rate,
                "pending":
                    pending_follow_ups
            })

        else:

            insights.append({
                "type": "positive",
                "category": "follow_up",
                "priority": "LOW",
                "title": "Strong follow-up execution",
                "message": (
                    f"{follow_up_completion_rate}% of follow-ups "
                    "have been completed."
                ),
                "completion_rate":
                    follow_up_completion_rate
            })

    # ========================================================
    # SALES ACTION PERFORMANCE
    # ========================================================

    total_actions = (
        sales_actions.get("total")
        or 0
    )

    pending_actions = (
        sales_actions.get("pending")
        or 0
    )

    action_success_rate = (
        sales_actions.get("success_rate")
        or 0
    )

    negative_actions = (
        sales_actions.get("negative")
        or 0
    )

    if total_actions > 0:

        if pending_actions > 0:

            insights.append({
                "type": "info",
                "category": "sales_actions",
                "priority": "MEDIUM",
                "title": "Sales actions awaiting outcomes",
                "message": (
                    f"{pending_actions} sales action(s) "
                    "have been executed but are still "
                    "awaiting an outcome."
                ),
                "pending":
                    pending_actions
            })

        if action_success_rate >= 80:

            insights.append({
                "type": "positive",
                "category": "sales_actions",
                "priority": "LOW",
                "title": "Strong action performance",
                "message": (
                    f"Sales actions have a {action_success_rate}% "
                    "success rate among decided outcomes."
                ),
                "success_rate":
                    action_success_rate
            })

        elif action_success_rate < 50:

            insights.append({
                "type": "warning",
                "category": "sales_actions",
                "priority": "HIGH",
                "title": "Sales action performance is weak",
                "message": (
                    f"Sales action success rate is only "
                    f"{action_success_rate}%. Review action "
                    "selection and customer responses."
                ),
                "success_rate":
                    action_success_rate
            })

        if negative_actions > 0:

            insights.append({
                "type": "warning",
                "category": "sales_actions",
                "priority": "HIGH",
                "title": "Negative sales outcomes detected",
                "message": (
                    f"{negative_actions} sales action outcome(s) "
                    "were negative. These leads may require "
                    "objection handling or a different approach."
                ),
                "negative":
                    negative_actions
            })

    # ========================================================
    # SITE VISIT PERFORMANCE
    # ========================================================

    total_site_visits = (
        site_visits.get("total")
        or 0
    )

    scheduled_site_visits = (
        site_visits.get("scheduled")
        or 0
    )

    completed_site_visits = (
        site_visits.get("completed")
        or 0
    )

    cancelled_site_visits = (
        site_visits.get("cancelled")
        or 0
    )

    site_visit_completion_rate = (
        site_visits.get("completion_rate")
        or 0
    )

    if total_site_visits > 0:

        if cancelled_site_visits > completed_site_visits:

            insights.append({
                "type": "warning",
                "category": "site_visits",
                "priority": "HIGH",
                "title": "Site-visit cancellations are high",
                "message": (
                    f"There are {cancelled_site_visits} cancelled "
                    f"site visit(s) versus {completed_site_visits} "
                    "completed visit(s)."
                ),
                "cancelled":
                    cancelled_site_visits,
                "completed":
                    completed_site_visits
            })

        elif site_visit_completion_rate < 50:

            insights.append({
                "type": "warning",
                "category": "site_visits",
                "priority": "MEDIUM",
                "title": "Site-visit completion is low",
                "message": (
                    f"Only {site_visit_completion_rate}% of site visits "
                    "have been completed."
                ),
                "completion_rate":
                    site_visit_completion_rate
            })

        else:

            insights.append({
                "type": "positive",
                "category": "site_visits",
                "priority": "LOW",
                "title": "Site visits are progressing",
                "message": (
                    f"Site-visit completion rate is "
                    f"{site_visit_completion_rate}%."
                ),
                "completion_rate":
                    site_visit_completion_rate
            })

        if scheduled_site_visits > 0:

            insights.append({
                "type": "info",
                "category": "site_visits",
                "priority": "MEDIUM",
                "title": "Scheduled visits require attention",
                "message": (
                    f"{scheduled_site_visits} site visit(s) "
                    "are currently scheduled."
                ),
                "scheduled":
                    scheduled_site_visits
            })

    # ========================================================
    # OVERALL RECOMMENDATION
    # ========================================================

    high_priority_insights = [
        item
        for item in insights
        if item.get("priority") == "HIGH"
    ]

    if high_priority_insights:

        primary = high_priority_insights[0]

        overall_priority = "HIGH"

        overall_focus = (
            primary.get("title")
            or "Review sales performance."
        )

        overall_recommendation = (
            primary.get("message")
            or "Review the sales pipeline."
        )

    else:

        overall_priority = "MEDIUM"

        overall_focus = (
            "Continue monitoring sales performance."
        )

        overall_recommendation = (
            "No critical sales-performance issue "
            "was detected."
        )

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "overall_priority":
            overall_priority,

        "overall_focus":
            overall_focus,

        "overall_recommendation":
            overall_recommendation,

        "insight_count":
            len(insights),

        "high_priority_count":
            len(high_priority_insights),

        "insights":
            insights

    }
