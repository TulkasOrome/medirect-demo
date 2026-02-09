"""API request/response schemas for MEDirect Edge."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models import Case, CaseAssignment, CaseStatus


class CaseResponse(BaseModel):
    """Response schema for a case resource."""

    id: str
    referrer_id: str
    expert_id: Optional[str]
    status: CaseStatus
    created_at: datetime

    @classmethod
    def from_model(cls, case: Case) -> "CaseResponse":
        """Convert a Case domain model to a CaseResponse schema.

        Args:
            case: The domain Case model.

        Returns:
            A CaseResponse instance.
        """
        return cls(
            id=case.id,
            referrer_id=case.referrer_id,
            expert_id=case.expert_id,
            status=case.status,
            created_at=case.created_at,
        )


class CaseAssignmentResponse(BaseModel):
    """Response schema for a case assignment result."""

    case_id: str
    expert_id: str
    assigned_at: datetime

    @classmethod
    def from_model(cls, assignment: CaseAssignment) -> "CaseAssignmentResponse":
        """Convert a CaseAssignment domain model to a response schema.

        Args:
            assignment: The domain CaseAssignment model.

        Returns:
            A CaseAssignmentResponse instance.
        """
        return cls(
            case_id=assignment.case_id,
            expert_id=assignment.expert_id,
            assigned_at=assignment.assigned_at,
        )


class AssignExpertRequest(BaseModel):
    """Request body for assigning an expert to a case."""

    expert_id: str


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    detail: str
