"""Case API routes matching contracts/case.yaml."""

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_case_service
from exceptions import NotFoundError, InvalidStateError
from schemas import AssignExpertRequest, CaseAssignmentResponse, CaseResponse
from services.case_service import CaseService

router = APIRouter(prefix="/api/v1", tags=["cases"])


@router.get("/cases/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: str,
    service: CaseService = Depends(get_case_service),
) -> CaseResponse:
    """Retrieve a case by its ID.

    Args:
        case_id: Unique identifier of the case.
        service: Injected CaseService.

    Returns:
        The case data.
    """
    try:
        case = await service.get_case(case_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message)
    return CaseResponse.from_model(case)


@router.post("/cases/{case_id}/assign", response_model=CaseAssignmentResponse)
async def assign_expert(
    case_id: str,
    body: AssignExpertRequest,
    service: CaseService = Depends(get_case_service),
) -> CaseAssignmentResponse:
    """Assign an expert to a case.

    Args:
        case_id: Unique identifier of the case.
        body: Request body containing the expert_id.
        service: Injected CaseService.

    Returns:
        The assignment result.
    """
    try:
        assignment = await service.assign_expert(case_id, body.expert_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message)
    except InvalidStateError as exc:
        raise HTTPException(status_code=409, detail=exc.message)
    return CaseAssignmentResponse.from_model(assignment)
