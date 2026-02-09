"""Domain models for MEDirect Edge. Pure data — no business logic."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class CaseStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Case(BaseModel):
    """A medicolegal case connecting a referrer to an expert."""

    id: str
    referrer_id: str
    expert_id: Optional[str] = None
    status: CaseStatus = CaseStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CaseAssignment(BaseModel):
    """Result of assigning an expert to a case."""

    case_id: str
    expert_id: str
    assigned_at: datetime = Field(default_factory=datetime.utcnow)