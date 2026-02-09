"""
Case Service Specification — Developer-Written Tests

These tests define the complete specification for the CaseService.
Claude Code will write the implementation that makes every test pass.

Architecture:
- CaseService depends on CaseRepository via constructor injection
- It does NOT directly access any database
- All methods are async
- Errors are domain exceptions from exceptions/
- Returns Pydantic models, never raw dicts
"""

import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from models import Case, CaseStatus, CaseAssignment
from exceptions import NotFoundError, InvalidStateError


class TestCaseService:
    """Specification for CaseService."""

    # --- FIXTURES ---

    @pytest.fixture
    def mock_repo(self):
        """CaseRepository mock — defines the interface the service depends on."""
        repo = AsyncMock()
        repo.get_by_id.return_value = Case(
            id="case-001",
            referrer_id="ref-100",
            expert_id=None,
            status=CaseStatus.SUBMITTED,
            created_at=datetime(2026, 1, 15),
        )
        repo.save.return_value = None
        return repo

    @pytest.fixture
    def service(self, mock_repo):
        """Service constructed with injected dependencies — no global state."""
        from services.case_service import CaseService
        return CaseService(case_repo=mock_repo)

    # --- SUCCESS CONDITIONS ---

    @pytest.mark.asyncio
    async def test_get_case_returns_case_model(self, service):
        """Getting an existing case returns a Case model instance."""
        result = await service.get_case("case-001")
        assert isinstance(result, Case)
        assert result.id == "case-001"
        assert result.referrer_id == "ref-100"

    @pytest.mark.asyncio
    async def test_get_case_calls_repo_with_correct_id(self, service, mock_repo):
        """Service delegates to repository with the exact ID provided."""
        await service.get_case("case-001")
        mock_repo.get_by_id.assert_called_once_with("case-001")

    @pytest.mark.asyncio
    async def test_assign_expert_returns_assignment(self, service):
        """Assigning an expert to a submitted case returns a CaseAssignment."""
        result = await service.assign_expert(case_id="case-001", expert_id="exp-200")
        assert isinstance(result, CaseAssignment)
        assert result.case_id == "case-001"
        assert result.expert_id == "exp-200"

    @pytest.mark.asyncio
    async def test_assign_expert_updates_case_status(self, service, mock_repo):
        """After assignment, case status must be ASSIGNED and expert_id set."""
        await service.assign_expert(case_id="case-001", expert_id="exp-200")
        mock_repo.save.assert_called_once()

        saved_case = mock_repo.save.call_args[0][0]
        assert saved_case.status == CaseStatus.ASSIGNED
        assert saved_case.expert_id == "exp-200"

    # --- ERROR CONDITIONS ---

    @pytest.mark.asyncio
    async def test_get_nonexistent_case_raises_not_found(self, service, mock_repo):
        """Missing case must raise NotFoundError, not generic Exception."""
        mock_repo.get_by_id.return_value = None
        with pytest.raises(NotFoundError) as exc:
            await service.get_case("case-999")
        assert "case-999" in str(exc.value)

    @pytest.mark.asyncio
    async def test_assign_expert_to_completed_case_raises_invalid_state(
        self, service, mock_repo
    ):
        """Cannot assign an expert to a case that's already completed."""
        mock_repo.get_by_id.return_value = Case(
            id="case-001",
            referrer_id="ref-100",
            expert_id="exp-100",
            status=CaseStatus.COMPLETED,
            created_at=datetime(2026, 1, 15),
        )
        with pytest.raises(InvalidStateError):
            await service.assign_expert(case_id="case-001", expert_id="exp-200")

    @pytest.mark.asyncio
    async def test_assign_expert_to_draft_case_raises_invalid_state(
        self, service, mock_repo
    ):
        """Cannot assign an expert to a draft case — must be submitted first."""
        mock_repo.get_by_id.return_value = Case(
            id="case-001",
            referrer_id="ref-100",
            status=CaseStatus.DRAFT,
            created_at=datetime(2026, 1, 15),
        )
        with pytest.raises(InvalidStateError):
            await service.assign_expert(case_id="case-001", expert_id="exp-200")

    # --- ARCHITECTURAL CONSTRAINTS ---

    def test_service_does_not_import_database(self):
        """CaseService must not have any direct database imports."""
        import importlib
        spec = importlib.util.find_spec("services.case_service")
        assert spec is not None, "services/case_service.py must exist"
        with open(spec.origin) as f:
            content = f.read().lower()
        assert "sqlalchemy" not in content, "Service imports SQLAlchemy directly"
        assert "import db" not in content, "Service imports database module"

    def test_service_does_not_import_fastapi(self):
        """CaseService must be framework-agnostic — no FastAPI imports."""
        import importlib
        spec = importlib.util.find_spec("services.case_service")
        with open(spec.origin) as f:
            content = f.read()
        assert "fastapi" not in content.lower(), "Service imports FastAPI"
        assert "HTTPException" not in content, "Service raises HTTP exceptions"

    def test_service_does_not_import_other_services(self):
        """CaseService must not import other services directly."""
        import importlib
        spec = importlib.util.find_spec("services.case_service")
        with open(spec.origin) as f:
            content = f.read()
        lines_with_service_imports = [
            line for line in content.splitlines()
            if "from services." in line and "case_service" not in line
        ]
        assert len(lines_with_service_imports) == 0, \
            "Service imports another service — use contracts instead"