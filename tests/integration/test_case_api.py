"""Integration tests for case API endpoints via FastAPI TestClient."""

import pytest
from httpx import ASGITransport, AsyncClient

from main import create_app
from api.dependencies import _get_repo
from models import Case, CaseStatus


@pytest.fixture
def app():
    """Create a fresh app for each test, clearing the repo cache."""
    _get_repo.cache_clear()
    return create_app()


@pytest.fixture
async def client(app):
    """Async test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestGetCase:
    """GET /api/v1/cases/{case_id} endpoint tests."""

    @pytest.mark.asyncio
    async def test_get_existing_case_returns_200(self, client):
        """Seeded case should return 200 with case data."""
        response = await client.get("/api/v1/cases/case-001")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "case-001"
        assert data["referrer_id"] == "ref-100"
        assert data["status"] == "submitted"

    @pytest.mark.asyncio
    async def test_get_nonexistent_case_returns_404(self, client):
        """Missing case should return 404 with detail message."""
        response = await client.get("/api/v1/cases/no-such-case")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_case_response_matches_schema(self, client):
        """Response body should contain all expected fields."""
        response = await client.get("/api/v1/cases/case-001")
        data = response.json()

        assert "id" in data
        assert "referrer_id" in data
        assert "expert_id" in data
        assert "status" in data
        assert "created_at" in data


class TestAssignExpert:
    """POST /api/v1/cases/{case_id}/assign endpoint tests."""

    @pytest.mark.asyncio
    async def test_assign_expert_returns_200(self, client):
        """Assigning expert to submitted case should return 200."""
        response = await client.post(
            "/api/v1/cases/case-001/assign",
            json={"expert_id": "exp-200"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["case_id"] == "case-001"
        assert data["expert_id"] == "exp-200"
        assert "assigned_at" in data

    @pytest.mark.asyncio
    async def test_assign_expert_to_nonexistent_case_returns_404(self, client):
        """Assigning to a missing case should return 404."""
        response = await client.post(
            "/api/v1/cases/no-such-case/assign",
            json={"expert_id": "exp-200"},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_assign_expert_to_draft_case_returns_409(self, client):
        """Assigning to a draft case should return 409 Conflict."""
        response = await client.post(
            "/api/v1/cases/case-002/assign",
            json={"expert_id": "exp-200"},
        )

        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_assign_expert_twice_returns_409(self, client):
        """Assigning again after first assignment should return 409."""
        await client.post(
            "/api/v1/cases/case-001/assign",
            json={"expert_id": "exp-200"},
        )
        response = await client.post(
            "/api/v1/cases/case-001/assign",
            json={"expert_id": "exp-300"},
        )

        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_assign_expert_missing_body_returns_422(self, client):
        """Missing request body should return 422 validation error."""
        response = await client.post(
            "/api/v1/cases/case-001/assign",
            json={},
        )

        assert response.status_code == 422
