import asyncio
import os

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# ROUTERS
# ============================================================

from app.api.leads import (
    router as leads_router
)

from app.api.chat import (
    router as chat_router
)

from app.api.follow_ups import (
    router as follow_ups_router
)

from app.api.site_visits import (
    router as site_visits_router
)

from app.api.dashboard import (
    router as dashboard_router
)

from app.api.properties import (
    router as properties_router
)

from app.api.activity import (
    router as activity_router
)

from app.api.voice import (
    router as voice_router
)


# ============================================================
# DATABASE
# ============================================================

from app.db.database import (
    Base,
    engine,
    SessionLocal
)


# ============================================================
# MODELS
#
# Importing the models here ensures SQLAlchemy knows about
# every model before create_all() runs.
# ============================================================

from app.models.lead import Lead

from app.models.conversation import (
    Conversation
)

from app.models.property import (
    Property
)

from app.models.follow_up import (
    FollowUp
)

from app.models.site_visits import (
    SiteVisit
)

from app.models.communication import (
    CommunicationHistory
)

from app.models.sales_action_outcome import (
    SalesActionOutcome
)


# ============================================================
# SERVICES
# ============================================================

from app.services.follow_up_service import (
    process_due_follow_ups
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

# Local development origins
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


# Optional production frontend URL.
#
# In production, set:
#
# FRONTEND_URL=https://your-frontend-domain.com
#
# Multiple origins can also be supplied as a comma-separated
# value if required.
#
frontend_url = os.getenv(
    "FRONTEND_URL"
)


if frontend_url:
    production_origins = [
        origin.strip()
        for origin in frontend_url.split(",")
        if origin.strip()
    ]

    allowed_origins.extend(
        production_origins
    )


# Remove duplicates while preserving order
allowed_origins = list(
    dict.fromkeys(
        allowed_origins
    )
)


# ============================================================
# AUTOMATIC FOLLOW-UP WORKER
# ============================================================

async def follow_up_worker():

    print(
        "[FOLLOW-UP WORKER] Started."
    )

    while True:

        db = SessionLocal()

        try:

            print(
                "[FOLLOW-UP WORKER] "
                "Checking for due follow-ups..."
            )

            result = process_due_follow_ups(
                db
            )

            processed = result.get(
                "processed",
                0
            )

            print(
                f"[FOLLOW-UP WORKER] "
                f"Due follow-ups found: "
                f"{processed}"
            )

            if processed > 0:

                print(
                    f"[FOLLOW-UP WORKER] "
                    f"Processed "
                    f"{processed} "
                    f"follow-up(s)."
                )

        except Exception as e:

            db.rollback()

            print(
                "[FOLLOW-UP WORKER] ERROR:",
                type(e).__name__,
                str(e)
            )

        finally:

            db.close()

        await asyncio.sleep(
            60
        )


# ============================================================
# FASTAPI LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    worker_task = asyncio.create_task(
        follow_up_worker()
    )

    try:

        yield

    finally:

        print(
            "[FOLLOW-UP WORKER] "
            "Stopping..."
        )

        worker_task.cancel()

        try:

            await worker_task

        except asyncio.CancelledError:

            pass

        print(
            "[FOLLOW-UP WORKER] "
            "Stopped."
        )


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title="AI Sales Agent",

    description=(
        "AI-powered lead qualification "
        "and sales automation platform"
    ),

    version="1.0.0",

    lifespan=lifespan
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=allowed_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# DATABASE TABLES
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    leads_router
)

app.include_router(
    chat_router
)

app.include_router(
    follow_ups_router
)

app.include_router(
    site_visits_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    properties_router
)

app.include_router(
    activity_router
)

app.include_router(
    voice_router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "message":
            "AI Sales Agent API is running",

        "status":
            "online"

    }