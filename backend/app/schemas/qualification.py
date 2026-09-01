from typing import Optional

from pydantic import BaseModel, Field


class QualificationResult(BaseModel):
    budget: Optional[str] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    purpose: Optional[str] = None
    timeline: Optional[str] = None
    buying_intent: Optional[str] = None
    missing_information: list[str] = Field(default_factory=list)