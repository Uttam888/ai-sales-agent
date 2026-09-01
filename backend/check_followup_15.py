from app.db.database import SessionLocal
from app.models.lead import Lead
from app.models.property import Property
from app.models.follow_up import FollowUp
from app.models.communication import CommunicationHistory
from app.models.site_visits import SiteVisit

from datetime import datetime

db = SessionLocal()

f = db.query(FollowUp).filter(FollowUp.id == 15).first()

print("FOLLOW-UP ID :", f.id if f else None)
print("STATUS       :", f.status if f else None)
print("DATE         :", f.follow_up_date if f else None)
print("PYTHON NOW   :", datetime.now())
print("IS DUE       :", f.follow_up_date <= datetime.now() if f else None)

db.close()
