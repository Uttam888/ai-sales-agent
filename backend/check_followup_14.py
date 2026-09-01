from sqlalchemy import text
from app.db.database import engine

with engine.connect() as db:
    rows = db.execute(
        text("""
            SELECT
                id,
                follow_up_id,
                lead_id,
                channel,
                direction,
                status,
                sent_at,
                created_at
            FROM communication_history
            WHERE follow_up_id = 14
        """)
    ).fetchall()

print("COMMUNICATIONS FOR FOLLOW-UP #14:")

for row in rows:
    print(row)
