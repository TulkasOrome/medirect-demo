"""Tests for API schemas — serialization and from_model converters."""

from datetime import datetime

from models import Case, CaseAssignment, CaseStatus
from schemas import (
    AssignExpertRequest,
    CaseAssignmentResponse,
    CaseResponse,
    ErrorResponse,
)


class TestCaseResponse:
    """CaseResponse schema specification."""

    def test_from_model_converts_all_fields(self):
        """from_model should map every Case field to CaseResponse."""
        case = Case(
            id="case-001",
            referrer_id="ref-100",
            expert_id="exp-200",
            status=CaseStatus.ASSIGNED,
            created_at=datetime(2026, 1, 15),
        )
        response = CaseResponse.from_model(case)

        assert response.id == "case-001"
        assert response.referrer_id == "ref-100"
        assert response.expert_id == "exp-200"
        assert response.status == CaseStatus.ASSIGNED
        assert response.created_at == datetime(2026, 1, 15)

    def test_from_model_handles_none_expert(self):
        """from_model should preserve None expert_id."""
        case = Case(
            id="case-002",
            referrer_id="ref-200",
            status=CaseStatus.DRAFT,
            created_at=datetime(2026, 2, 1),
        )
        response = CaseResponse.from_model(case)

        assert response.expert_id is None

    def test_serialization_round_trip(self):
        """CaseResponse should serialize to dict and back."""
        case = Case(
            id="case-001",
            referrer_id="ref-100",
            status=CaseStatus.SUBMITTED,
            created_at=datetime(2026, 1, 15),
        )
        response = CaseResponse.from_model(case)
        data = response.model_dump()

        assert data["id"] == "case-001"
        assert data["status"] == CaseStatus.SUBMITTED

        restored = CaseResponse.model_validate(data)
        assert restored == response


class TestCaseAssignmentResponse:
    """CaseAssignmentResponse schema specification."""

    def test_from_model_converts_all_fields(self):
        """from_model should map every CaseAssignment field."""
        assignment = CaseAssignment(
            case_id="case-001",
            expert_id="exp-200",
            assigned_at=datetime(2026, 1, 15, 10, 30),
        )
        response = CaseAssignmentResponse.from_model(assignment)

        assert response.case_id == "case-001"
        assert response.expert_id == "exp-200"
        assert response.assigned_at == datetime(2026, 1, 15, 10, 30)


class TestAssignExpertRequest:
    """AssignExpertRequest schema specification."""

    def test_parses_expert_id(self):
        """Should parse a request body with expert_id."""
        request = AssignExpertRequest(expert_id="exp-300")
        assert request.expert_id == "exp-300"


class TestErrorResponse:
    """ErrorResponse schema specification."""

    def test_serializes_detail(self):
        """Should serialize the detail field."""
        error = ErrorResponse(detail="Something went wrong")
        assert error.model_dump() == {"detail": "Something went wrong"}
