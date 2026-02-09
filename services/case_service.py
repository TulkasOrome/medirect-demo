"""Case service — orchestrates case operations via injected repository."""

from typing import Protocol

from models import Case, CaseAssignment, CaseStatus
from exceptions import NotFoundError, InvalidStateError


class CaseRepository(Protocol):
    """Interface that any case repository implementation must satisfy."""

    async def get_by_id(self, case_id: str) -> Case | None: ...

    async def save(self, case: Case) -> None: ...


class CaseService:
    """Manages case lifecycle operations.

    Uses constructor injection for the repository dependency,
    keeping the service decoupled from any specific persistence layer.
    """

    def __init__(self, case_repo: CaseRepository) -> None:
        self._case_repo = case_repo

    async def get_case(self, case_id: str) -> Case:
        """Retrieve a case by its ID.

        Args:
            case_id: Unique identifier of the case.

        Returns:
            The matching Case model.

        Raises:
            NotFoundError: If no case exists with the given ID.
        """
        case = await self._case_repo.get_by_id(case_id)
        if case is None:
            raise NotFoundError(f"Case '{case_id}' not found")
        return case

    async def assign_expert(self, case_id: str, expert_id: str) -> CaseAssignment:
        """Assign an expert to a case.

        The case must be in SUBMITTED status. Cases in DRAFT or COMPLETED
        status cannot be assigned.

        Args:
            case_id: Unique identifier of the case.
            expert_id: Unique identifier of the expert to assign.

        Returns:
            A CaseAssignment confirming the assignment.

        Raises:
            NotFoundError: If no case exists with the given ID.
            InvalidStateError: If the case is not in SUBMITTED status.
        """
        case = await self.get_case(case_id)

        if case.status != CaseStatus.SUBMITTED:
            raise InvalidStateError(
                f"Case '{case_id}' is in '{case.status.value}' status "
                f"and cannot be assigned"
            )

        case.status = CaseStatus.ASSIGNED
        case.expert_id = expert_id
        await self._case_repo.save(case)

        return CaseAssignment(case_id=case.id, expert_id=expert_id)
