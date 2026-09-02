from datetime import datetime

from google.genai import types

from app.models.lead import Lead
from app.models.property import Property
from app.models.site_visits import SiteVisit
from app.models.follow_up import FollowUp
from app.services.lead_scoring import update_lead_score


# ============================================================
# GET LEAD TOOL DECLARATION
# ============================================================

GET_LEAD_DECLARATION = types.FunctionDeclaration(
    name="get_lead",
    description=(
        "Retrieve the complete current information "
        "about a sales lead."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "lead_id": {
                "type": "INTEGER",
                "description": "ID of the lead."
            }
        },
        "required": ["lead_id"]
    }
)


# ============================================================
# UPDATE LEAD TOOL DECLARATION
# ============================================================

UPDATE_LEAD_DECLARATION = types.FunctionDeclaration(
    name="update_lead",
    description=(
        "Update known qualification information "
        "for a sales lead."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {

            "lead_id": {
                "type": "INTEGER",
                "description": "ID of the lead."
            },

            "budget": {
                "type": "STRING",
                "description": "Updated budget if explicitly provided."
            },

            "location": {
                "type": "STRING",
                "description": "Updated preferred location if explicitly provided."
            },

            "property_type": {
                "type": "STRING",
                "description": "Updated property type if explicitly provided."
            },

            "purpose": {
                "type": "STRING",
                "description": "Updated purchase purpose if explicitly provided."
            },

            "timeline": {
                "type": "STRING",
                "description": "Updated purchase timeline if explicitly provided."
            },

            "buying_intent": {
                "type": "STRING",
                "description": "Updated buying intent if explicitly provided."
            }
        },
        "required": ["lead_id"]
    }
)


# ============================================================
# NEXT BEST ACTION TOOL DECLARATION
# ============================================================

NEXT_BEST_ACTION_DECLARATION = types.FunctionDeclaration(
    name="next_best_action",
    description=(
        "Determine the next appropriate sales action "
        "for a lead."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {

            "lead_id": {
                "type": "INTEGER",
                "description": "ID of the lead."
            },

            "action": {
                "type": "STRING",
                "description": "Recommended next sales action."
            },

            "reason": {
                "type": "STRING",
                "description": "Reason for the recommended action."
            }
        },
        "required": [
            "lead_id",
            "action",
            "reason"
        ]
    }
)


# ============================================================
# SEARCH PROPERTIES TOOL DECLARATION
# ============================================================

SEARCH_PROPERTIES_DECLARATION = types.FunctionDeclaration(
    name="search_properties",
    description=(
        "Search the real estate property database for "
        "available properties matching a customer's "
        "location, property type, budget and bedroom "
        "requirements. max_price must be specified in "
        "lakhs. For example, 120 means ₹1.2 crore."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {

            "location": {
                "type": "STRING",
                "description": (
                    "Preferred location or city."
                )
            },

            "property_type": {
                "type": "STRING",
                "description": (
                    "Property type such as "
                    "2BHK apartment or 3BHK apartment."
                )
            },

            "max_price": {
                "type": "NUMBER",
                "description": (
                    "Maximum budget in lakhs. "
                    "Example: 120 means ₹1.2 crore."
                )
            },

            "min_bedrooms": {
                "type": "INTEGER",
                "description": (
                    "Minimum number of bedrooms."
                )
            }
        },
        "required": [
            "location",
            "property_type",
            "max_price"
        ]
    }
)


# ============================================================
# SCHEDULE SITE VISIT TOOL DECLARATION
# ============================================================

SCHEDULE_SITE_VISIT_DECLARATION = types.FunctionDeclaration(
    name="schedule_site_visit",
    description=(
        "Schedule a site visit for a lead at a specific "
        "property. Use this only when the customer has "
        "clearly requested a site visit and a specific "
        "future date and time are available."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {

            "lead_id": {
                "type": "INTEGER",
                "description": "ID of the lead."
            },

            "property_id": {
                "type": "INTEGER",
                "description": (
                    "ID of the property the customer "
                    "wants to visit."
                )
            },

            "visit_date": {
                "type": "STRING",
                "description": (
                    "Site visit date and time in ISO "
                    "format, for example "
                    "2026-09-05T17:00:00."
                )
            },

            "notes": {
                "type": "STRING",
                "description": (
                    "Optional notes about the visit."
                )
            }
        },
        "required": [
            "lead_id",
            "property_id",
            "visit_date"
        ]
    }
)


# ============================================================
# CANCEL SITE VISIT TOOL DECLARATION
# ============================================================

CANCEL_SITE_VISIT_DECLARATION = types.FunctionDeclaration(
    name="cancel_site_visit",
    description=(
        "Cancel a scheduled site visit for the current sales lead. "
        "Use this only when the customer explicitly asks to cancel "
        "a site visit. If multiple scheduled visits exist, provide "
        "the property and/or visit date and time to identify the visit."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "lead_id": {"type": "INTEGER", "description": "ID of the lead."},
            "property_title": {"type": "STRING", "description": "Optional property title identifying the visit."},
            "visit_date": {"type": "STRING", "description": "Optional site visit date and time in ISO format, for example 2026-09-05T17:00:00."},
            "notes": {"type": "STRING", "description": "Optional reason or internal note for the cancellation."}
        },
        "required": ["lead_id"]
    }
)


# ============================================================
# CREATE FOLLOW-UP TOOL DECLARATION
# ============================================================

CREATE_FOLLOW_UP_DECLARATION = types.FunctionDeclaration(
    name="create_follow_up",
    description=(
        "Create a follow-up task for a sales lead. "
        "Use this when a lead needs to be contacted "
        "again at a specific future date and time."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {

            "lead_id": {
                "type": "INTEGER",
                "description": "ID of the lead."
            },

            "follow_up_date": {
                "type": "STRING",
                "description": (
                    "Follow-up date and time in ISO format, "
                    "for example 2026-09-10T10:00:00."
                )
            },

            "message": {
                "type": "STRING",
                "description": (
                    "Message that should be used when "
                    "following up with the lead."
                )
            },

            "notes": {
                "type": "STRING",
                "description": (
                    "Optional internal notes about "
                    "the follow-up."
                )
            }
        },
        "required": [
            "lead_id",
            "follow_up_date",
            "message"
        ]
    }
)


# ============================================================
# GET PENDING FOLLOW-UPS TOOL DECLARATION
# ============================================================

GET_PENDING_FOLLOW_UPS_DECLARATION = types.FunctionDeclaration(
    name="get_pending_follow_ups",
    description=(
        "Retrieve pending follow-up tasks for a sales lead."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {

            "lead_id": {
                "type": "INTEGER",
                "description": "ID of the lead."
            }
        },
        "required": ["lead_id"]
    }
)


# ============================================================
# GET LEAD
# ============================================================

def get_lead(
    db,
    lead_id: int
):

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )

    if not lead:

        return {
            "success": False,
            "error": (
                f"Lead {lead_id} was not found."
            )
        }

    return {

        "success": True,

        "lead": {

            "id": lead.id,

            "name": lead.name,

            "email": lead.email,

            "phone": lead.phone,

            "budget": lead.budget,

            "location": lead.location,

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
    }


# ============================================================
# UPDATE LEAD
# ============================================================

def update_lead(
    db,
    lead_id: int,
    budget=None,
    location=None,
    property_type=None,
    purpose=None,
    timeline=None,
    buying_intent=None
):

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )

    if not lead:

        return {
            "success": False,
            "error": (
                f"Lead {lead_id} was not found."
            )
        }


    if budget is not None:
        lead.budget = budget

    if location is not None:
        lead.location = location

    if property_type is not None:
        lead.property_type = property_type

    if purpose is not None:
        lead.purpose = purpose

    if timeline is not None:
        lead.timeline = timeline

    if buying_intent is not None:
        lead.buying_intent = buying_intent


    db.commit()

    db.refresh(lead)


    return {

        "success": True,

        "message":
            "Lead updated successfully.",

        "lead": {

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
    }


# ============================================================
# NEXT BEST ACTION
# ============================================================

def next_best_action(
    db,
    lead_id: int,
    action: str = "",
    reason: str = ""
):

    # --------------------------------------------------------
    # CHECK LEAD
    # --------------------------------------------------------

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )

    if not lead:

        return {
            "success": False,
            "error": (
                f"Lead {lead_id} was not found."
            )
        }

    now = datetime.now()

    # --------------------------------------------------------
    # CHECK FOLLOW-UPS
    # --------------------------------------------------------

    follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.lead_id == lead_id
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
            follow_up.status or ""
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

    # --------------------------------------------------------
    # CHECK SITE VISITS
    # --------------------------------------------------------

    site_visits = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.lead_id == lead_id
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
            visit.status or ""
        ).strip().lower() == "scheduled"
    ]

    completed_visits = [
        visit
        for visit in site_visits
        if (
            visit.status or ""
        ).strip().lower() == "completed"
    ]

    cancelled_visits = [
        visit
        for visit in site_visits
        if (
            visit.status or ""
        ).strip().lower() == "cancelled"
    ]

    missed_visits = [
        visit
        for visit in scheduled_visits
        if (
            visit.visit_date
            and visit.visit_date < now
        )
    ]

    # --------------------------------------------------------
    # LEAD STATE
    # --------------------------------------------------------

    status = (
        lead.qualification_status or ""
    ).strip().lower()

    stage = (
        lead.pipeline_stage or ""
    ).strip().upper()

    intent = (
        lead.buying_intent or ""
    ).strip().lower()

    score = lead.lead_score or 0

    # ========================================================
    # DETERMINE NEXT BEST ACTION
    # ========================================================

    if overdue_follow_ups:

        recommended_action = (
            "complete_overdue_follow_up"
        )

        recommended_reason = (
            "A follow-up for this lead is overdue. "
            "The next sales action is to complete "
            "the overdue follow-up immediately."
        )

    elif missed_visits:

        recommended_action = (
            "contact_and_reschedule_site_visit"
        )

        recommended_reason = (
            "A scheduled site visit has passed "
            "without being marked completed or "
            "cancelled. The next sales action is "
            "to contact the customer, verify the "
            "visit status, and reschedule if needed."
        )

    elif (
        cancelled_visits
        and not scheduled_visits
    ):

        recommended_action = (
            "reschedule_site_visit"
        )

        recommended_reason = (
            "A previous site visit was cancelled "
            "and there is no replacement visit "
            "currently scheduled. The next sales "
            "action is to contact the customer and "
            "reschedule the visit."
        )

    elif scheduled_visits:

        recommended_action = (
            "prepare_for_site_visit"
        )

        recommended_reason = (
            "The lead has a scheduled site visit. "
            "The next sales action is to confirm "
            "the visit and prepare the customer "
            "with the relevant property details."
        )

    elif completed_visits:

        recommended_action = (
            "follow_up_after_site_visit"
        )

        recommended_reason = (
            "The lead has completed a site visit. "
            "The next sales action is to follow up "
            "with the customer, collect feedback, "
            "and identify remaining objections."
        )

    elif (
        stage == "NEGOTIATION"
        or status == "negotiation"
    ):

        recommended_action = (
            "discuss_negotiation"
        )

        recommended_reason = (
            "The lead is in the negotiation stage. "
            "The next sales action is to discuss "
            "pricing, terms, objections, and the "
            "path toward closing."
        )

    elif (
        stage == "PROPERTY_INTEREST"
        or status == "property_interest"
    ):

        recommended_action = (
            "schedule_site_visit"
        )

        recommended_reason = (
            "The lead has shown property interest "
            "but does not currently have a scheduled "
            "site visit. The next sales action is "
            "to encourage a site visit."
        )

    elif (
        stage == "QUALIFIED"
        or status == "qualified"
    ):

        recommended_action = (
            "recommend_properties"
        )

        recommended_reason = (
            "The lead is qualified. The next sales "
            "action is to recommend suitable "
            "properties based on the customer's "
            "requirements."
        )

    elif (
        intent == "high"
        or score >= 70
    ):

        recommended_action = (
            "contact_high_intent_lead"
        )

        recommended_reason = (
            "The lead has strong buying signals. "
            "The next sales action is to contact "
            "the lead promptly and move them toward "
            "property selection or a site visit."
        )

    elif (
        stage == "CONTACTED"
        or status == "contacted"
    ):

        recommended_action = (
            "qualify_lead"
        )

        recommended_reason = (
            "The lead has been contacted but needs "
            "further qualification. Confirm budget, "
            "location, property type, purpose, "
            "timeline, and buying intent."
        )

    else:

        recommended_action = (
            "contact_lead"
        )

        recommended_reason = (
            "The lead does not currently have a "
            "stronger sales action recorded. "
            "The next step is to contact the lead "
            "and understand their requirements."
        )

    return {

        "success": True,

        "lead_id":
            lead_id,

        "action":
            recommended_action,

        "reason":
            recommended_reason,

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
                len(pending_follow_ups),

            "overdue_follow_ups":
                len(overdue_follow_ups),

            "scheduled_site_visits":
                len(scheduled_visits),

            "completed_site_visits":
                len(completed_visits),

            "cancelled_site_visits":
                len(cancelled_visits),

            "missed_site_visits":
                len(missed_visits)

        }

    }



# ============================================================
# SEARCH PROPERTIES
# ============================================================

def search_properties(
    db,
    location: str,
    property_type: str,
    max_price: float,
    min_bedrooms: int | None = None
):

    query = (
        db.query(Property)
        .filter(
            Property.available.is_(True)
        )
    )


    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    if location:

        query = query.filter(
            Property.location.ilike(
                f"%{location}%"
            )
        )


    # --------------------------------------------------------
    # PROPERTY TYPE
    # --------------------------------------------------------

    if property_type:

        query = query.filter(
            Property.property_type.ilike(
                f"%{property_type}%"
            )
        )


    # --------------------------------------------------------
    # BEDROOMS
    # --------------------------------------------------------

    if min_bedrooms is not None:

        query = query.filter(
            Property.bedrooms >= min_bedrooms
        )


    properties = (
        query
        .order_by(
            Property.id.asc()
        )
        .all()
    )


    matching_properties = []


    # --------------------------------------------------------
    # PRICE CONVERSION
    # --------------------------------------------------------

    for property_item in properties:

        price_text = (
            property_item.price
            .lower()
            .replace(",", "")
            .replace("₹", "")
            .strip()
        )


        price_value = None


        # ----------------------------------------------------
        # CRORE
        # ----------------------------------------------------

        if "crore" in price_text:

            try:

                number = float(
                    price_text
                    .replace(
                        "crore",
                        ""
                    )
                    .strip()
                )

                price_value = (
                    number * 100
                )

            except ValueError:

                continue


        # ----------------------------------------------------
        # LAKH
        # ----------------------------------------------------

        elif "lakh" in price_text:

            try:

                number = float(
                    price_text
                    .replace(
                        "lakh",
                        ""
                    )
                    .strip()
                )

                price_value = number

            except ValueError:

                continue


        # ----------------------------------------------------
        # UNKNOWN PRICE FORMAT
        # ----------------------------------------------------

        if price_value is None:

            continue


        # ----------------------------------------------------
        # BUDGET CHECK
        # ----------------------------------------------------

        if price_value > max_price:

            continue


        # ----------------------------------------------------
        # ADD PROPERTY
        # ----------------------------------------------------

        matching_properties.append({

            "id":
                property_item.id,

            "title":
                property_item.title,

            "location":
                property_item.location,

            "property_type":
                property_item.property_type,

            "price":
                property_item.price,

            "bedrooms":
                property_item.bedrooms,

            "bathrooms":
                property_item.bathrooms,

            "area_sqft":
                property_item.area_sqft,

            "description":
                property_item.description,

            "amenities":
                property_item.amenities,

            "available":
                property_item.available
        })


    # --------------------------------------------------------
    # LIMIT RESULTS
    # --------------------------------------------------------

    matching_properties = (
        matching_properties[:5]
    )


    return {

        "success": True,

        "count":
            len(matching_properties),

        "properties":
            matching_properties
    }


# ============================================================
# SCHEDULE SITE VISIT
# ============================================================

def schedule_site_visit(
    db,
    lead_id: int,
    property_id: int,
    visit_date: str,
    notes: str | None = None
):

    # --------------------------------------------------------
    # CHECK LEAD
    # --------------------------------------------------------

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )


    if not lead:

        return {

            "success": False,

            "error": (
                f"Lead {lead_id} was not found."
            )
        }


    # --------------------------------------------------------
    # CHECK PROPERTY
    # --------------------------------------------------------

    property_item = (
        db.query(Property)
        .filter(
            Property.id == property_id
        )
        .first()
    )


    if not property_item:

        return {

            "success": False,

            "error": (
                f"Property {property_id} "
                "was not found."
            )
        }


    # --------------------------------------------------------
    # CHECK PROPERTY AVAILABILITY
    # --------------------------------------------------------

    if not property_item.available:

        return {

            "success": False,

            "error": (
                "This property is currently "
                "not available."
            )
        }


    # --------------------------------------------------------
    # PARSE DATE
    # --------------------------------------------------------

    try:

        parsed_visit_date = (
            datetime.fromisoformat(
                visit_date
            )
        )

    except ValueError:

        return {

            "success": False,

            "error": (
                "Invalid date format. "
                "Please use "
                "YYYY-MM-DDTHH:MM:SS."
            )
        }


    # --------------------------------------------------------
    # PREVENT PAST APPOINTMENTS
    # --------------------------------------------------------

    if parsed_visit_date <= datetime.now():

        return {

            "success": False,

            "error": (
                "The site visit must be "
                "scheduled for a future "
                "date and time."
            )
        }


    # --------------------------------------------------------
    # CHECK DUPLICATE
    # --------------------------------------------------------

    existing_visit = (
        db.query(SiteVisit)
        .filter(
            SiteVisit.lead_id == lead_id,

            SiteVisit.property_id ==
                property_id,

            SiteVisit.visit_date ==
                parsed_visit_date,

            SiteVisit.status ==
                "scheduled"
        )
        .first()
    )


    if existing_visit:

        return {

            "success": False,

            "error": (
                "A site visit for this "
                "property is already "
                "scheduled at this time."
            ),

            "visit_id":
                existing_visit.id
        }


    # --------------------------------------------------------
    # CREATE VISIT
    # --------------------------------------------------------

    new_visit = SiteVisit(

        lead_id=lead_id,

        property_id=property_id,

        visit_date=parsed_visit_date,

        status="scheduled",

        notes=notes
    )


    db.add(
        new_visit
    )


    # --------------------------------------------------------
    # UPDATE LEAD PIPELINE
    # --------------------------------------------------------

    lead.qualification_status = (
        "site_visit"
    )

    # Recalculate the lead score after the site visit
    # so the behavioral signal is reflected immediately.
    update_lead_score(
        db=db,
        lead=lead
    )


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()


    db.refresh(
        new_visit
    )

    db.refresh(
        lead
    )


    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "success": True,

        "message": (
            "Site visit scheduled successfully."
        ),

        "visit": {

            "id":
                new_visit.id,

            "lead_id":
                new_visit.lead_id,

            "property_id":
                new_visit.property_id,

            "property_title":
                property_item.title,

            "location":
                property_item.location,

            "property_type":
                property_item.property_type,

            "price":
                property_item.price,

            "visit_date":
                new_visit.visit_date.isoformat(),

            "status":
                new_visit.status,

            "notes":
                new_visit.notes
        },

        "lead": {

            "id":
                lead.id,

            "pipeline_stage":
                lead.pipeline_stage,

            "qualification_status":
                lead.qualification_status
        }
    }


# ============================================================
# CANCEL SITE VISIT
# ============================================================

def cancel_site_visit(
    db, lead_id: int, property_title: str | None = None,
    visit_date: str | None = None, notes: str | None = None
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return {"success": False, "error": f"Lead {lead_id} was not found."}

    query = (db.query(SiteVisit, Property)
        .join(Property, SiteVisit.property_id == Property.id)
        .filter(SiteVisit.lead_id == lead_id, SiteVisit.status == "scheduled"))

    if property_title:
        query = query.filter(Property.title.ilike(f"%{property_title.strip()}%"))

    if visit_date:
        try:
            parsed_visit_date = datetime.fromisoformat(visit_date)
        except ValueError:
            return {"success": False, "error": "Invalid visit date format. Please use YYYY-MM-DDTHH:MM:SS."}
        query = query.filter(SiteVisit.visit_date == parsed_visit_date)

    matches = query.order_by(SiteVisit.visit_date.asc(), SiteVisit.id.asc()).all()
    if not matches:
        return {"success": False, "error": "No scheduled site visit matching the provided details was found for this lead."}
    if len(matches) > 1:
        return {"success": False, "error": "Multiple scheduled site visits were found. Please specify the property or visit date and time.", "count": len(matches)}

    site_visit, property_item = matches[0]
    site_visit.status = "cancelled"
    if notes and notes.strip():
        cancellation_note = f"Cancellation: {notes.strip()}"
        if site_visit.notes and site_visit.notes.strip():
            site_visit.notes = f"{site_visit.notes.strip()} | {cancellation_note}"
        else:
            site_visit.notes = cancellation_note

    update_lead_score(db=db, lead=lead)
    db.commit(); db.refresh(site_visit); db.refresh(lead)

    return {"success": True, "message": "Site visit cancelled successfully.",
        "visit": {"id": site_visit.id, "lead_id": site_visit.lead_id,
        "property_id": site_visit.property_id, "property_title": property_item.title,
        "location": property_item.location, "property_type": property_item.property_type,
        "price": property_item.price, "visit_date": site_visit.visit_date.isoformat(),
        "status": site_visit.status, "notes": site_visit.notes},
        "lead": {"id": lead.id, "pipeline_stage": lead.pipeline_stage,
        "qualification_status": lead.qualification_status}}


# ============================================================
# CREATE FOLLOW-UP
# ============================================================

def create_follow_up(
    db,
    lead_id: int,
    follow_up_date: str,
    message: str,
    notes: str | None = None
):

    # --------------------------------------------------------
    # CHECK LEAD
    # --------------------------------------------------------

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )


    if not lead:

        return {

            "success": False,

            "error": (
                f"Lead {lead_id} was not found."
            )
        }


    # --------------------------------------------------------
    # VALIDATE MESSAGE
    # --------------------------------------------------------

    if not message or not message.strip():

        return {

            "success": False,

            "error": (
                "Follow-up message "
                "cannot be empty."
            )
        }


    # --------------------------------------------------------
    # PARSE DATE
    # --------------------------------------------------------

    try:

        parsed_follow_up_date = (
            datetime.fromisoformat(
                follow_up_date
            )
        )

    except ValueError:

        return {

            "success": False,

            "error": (
                "Invalid follow-up date "
                "format. Please use "
                "YYYY-MM-DDTHH:MM:SS."
            )
        }


    # --------------------------------------------------------
    # PREVENT PAST FOLLOW-UP
    # --------------------------------------------------------

    if parsed_follow_up_date <= datetime.now():

        return {

            "success": False,

            "error": (
                "The follow-up must be "
                "scheduled for a future "
                "date and time."
            )
        }


    # --------------------------------------------------------
    # CHECK DUPLICATE FOLLOW-UP
    # --------------------------------------------------------

    existing_follow_up = (
        db.query(FollowUp)
        .filter(

            FollowUp.lead_id ==
                lead_id,

            FollowUp.follow_up_date ==
                parsed_follow_up_date,

            FollowUp.status ==
                "pending"
        )
        .first()
    )


    if existing_follow_up:

        return {

            "success": False,

            "error": (
                "A pending follow-up "
                "is already scheduled "
                "for this date and time."
            ),

            "follow_up_id":
                existing_follow_up.id
        }


    # --------------------------------------------------------
    # CREATE FOLLOW-UP
    # --------------------------------------------------------

    new_follow_up = FollowUp(

        lead_id=lead_id,

        follow_up_date=
            parsed_follow_up_date,

        status="pending",

        message=message.strip(),

        notes=notes
    )


    db.add(
        new_follow_up
    )

    db.commit()

    db.refresh(
        new_follow_up
    )


    return {

        "success": True,

        "message": (
            "Follow-up scheduled successfully."
        ),

        "follow_up": {

            "id":
                new_follow_up.id,

            "lead_id":
                new_follow_up.lead_id,

            "follow_up_date":
                new_follow_up
                .follow_up_date
                .isoformat(),

            "status":
                new_follow_up.status,

            "message":
                new_follow_up.message,

            "notes":
                new_follow_up.notes
        }
    }


# ============================================================
# GET PENDING FOLLOW-UPS
# ============================================================

def get_pending_follow_ups(
    db,
    lead_id: int
):

    # --------------------------------------------------------
    # CHECK LEAD
    # --------------------------------------------------------

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )


    if not lead:

        return {

            "success": False,

            "error": (
                f"Lead {lead_id} was not found."
            )
        }


    # --------------------------------------------------------
    # FETCH PENDING FOLLOW-UPS
    # --------------------------------------------------------

    follow_ups = (
        db.query(FollowUp)
        .filter(

            FollowUp.lead_id ==
                lead_id,

            FollowUp.status ==
                "pending"
        )
        .order_by(
            FollowUp.follow_up_date.asc()
        )
        .all()
    )


    # --------------------------------------------------------
    # FORMAT RESULTS
    # --------------------------------------------------------

    results = []


    for follow_up in follow_ups:

        results.append({

            "id":
                follow_up.id,

            "lead_id":
                follow_up.lead_id,

            "follow_up_date":
                follow_up
                .follow_up_date
                .isoformat(),

            "status":
                follow_up.status,

            "message":
                follow_up.message,

            "notes":
                follow_up.notes
        })


    return {

        "success": True,

        "count":
            len(results),

        "follow_ups":
            results
    }
