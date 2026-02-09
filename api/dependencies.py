"""Composition root — wires dependencies for FastAPI dependency injection."""

from functools import lru_cache

from models import Case, CaseStatus
from services.case_service import CaseService
from utils.in_memory_repo import InMemoryCaseRepository


@lru_cache(maxsize=1)
def _get_repo() -> InMemoryCaseRepository:
    """Create and seed a singleton in-memory repository.

    Returns:
        A seeded InMemoryCaseRepository instance.
    """
    repo = InMemoryCaseRepository()
    repo.seed([
        Case(
            id="case-001",
            referrer_id="ref-100",
            status=CaseStatus.SUBMITTED,
        ),
        Case(
            id="case-002",
            referrer_id="ref-200",
            status=CaseStatus.DRAFT,
        ),
    ])
    return repo


def get_case_service() -> CaseService:
    """Provide a CaseService instance for FastAPI Depends().

    Returns:
        A CaseService wired with the in-memory repository.
    """
    return CaseService(case_repo=_get_repo())
