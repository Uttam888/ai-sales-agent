from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.database import Base


class Conversation(Base):

    __tablename__ = "conversations"


    # ========================================================
    # ID
    # ========================================================

    id: Mapped[int] = mapped_column(

        primary_key=True,

        index=True
    )


    # ========================================================
    # LEAD ID
    # ========================================================

    lead_id: Mapped[int] = mapped_column(

        ForeignKey(
            "leads.id"
        ),

        nullable=False,

        index=True
    )


    # ========================================================
    # ROLE
    # ========================================================

    role: Mapped[str] = mapped_column(

        String(20),

        nullable=False
    )


    # ========================================================
    # MESSAGE
    # ========================================================

    message: Mapped[str] = mapped_column(

        Text,

        nullable=False
    )


    # ========================================================
    # CREATED AT
    # ========================================================

    created_at: Mapped[datetime] = mapped_column(

        DateTime,

        default=datetime.utcnow,

        nullable=False
    )