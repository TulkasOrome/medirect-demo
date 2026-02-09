"""In-memory case repository for development and testing."""

from typing import Optional

from models import Case


class InMemoryCaseRepository:
    """Dict-backed CaseRepository implementation.

    Satisfies the CaseRepository protocol defined in services.case_service.
    Useful for local development and integration tests without a real database.
    """

    def __init__(self) -> None:
        self._store: dict[str, Case] = {}

    async def get_by_id(self, case_id: str) -> Optional[Case]:
        """Retrieve a case by ID from the in-memory store.

        Args:
            case_id: The unique identifier of the case.

        Returns:
            The Case if found, otherwise None.
        """
        return self._store.get(case_id)

    async def save(self, case: Case) -> None:
        """Persist a case to the in-memory store.

        Args:
            case: The Case model to save.
        """
        self._store[case.id] = case

    def seed(self, cases: list[Case]) -> None:
        """Pre-populate the store with seed data.

        Args:
            cases: List of Case models to add to the store.
        """
        for case in cases:
            self._store[case.id] = case
