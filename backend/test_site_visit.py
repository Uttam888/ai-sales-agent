from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.models.lead import Lead
from app.models.property import Property
from app.models.site_visits import SiteVisit

db = SessionLocal()

try:
    lead = db.query(Lead).filter(Lead.id == 13).first()
    prop = db.query(Property).filter(Property.id == 3).first()

    visit = SiteVisit(
        lead_id=lead.id,
        property_id=prop.id,
        visit_date=datetime.now() + timedelta(hours=2),
        status="scheduled",
        notes="Lifecycle API test"
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

    print("TEST VISIT CREATED")
    print("ID:", visit.id)
    print("LEAD:", visit.lead_id)
    print("PROPERTY:", visit.property_id)
    print("DATE:", visit.visit_date)
    print("STATUS:", visit.status)

finally:
    db.close()
