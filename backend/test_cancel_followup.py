from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.models.lead import Lead
from app.models.follow_up import FollowUp

db = SessionLocal()

try:
    lead = db.query(Lead).filter(Lead.id == 13).first()

    follow_up = FollowUp(
        lead_id=lead.id,
        follow_up_date=datetime.now() + timedelta(hours=4),
        status="pending",
        message="Temporary cancellation API test",
        notes="Cancel API test"
    )

    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)

    print("CANCEL TEST FOLLOW-UP CREATED")
    print("ID:", follow_up.id)
    print("LEAD:", follow_up.lead_id)
    print("DATE:", follow_up.follow_up_date)
    print("STATUS:", follow_up.status)

finally:
    db.close()
