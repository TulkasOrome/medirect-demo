"""Tests for InMemoryCaseRepository — get, save, seed operations."""

import pytest
from datetime import datetime

from models import Case, CaseStatus
from utils.in_memory_repo import InMemoryCaseRepository


class TestInMemoryCaseRepository:
    """InMemoryCaseRepository specification."""

    @pytest.fixture
    def repo(self):
        """Fresh repository instance per test."""
        return InMemoryCaseRepository()

    @pytest.fixture
    def sample_case(self):
        """A sample case for testing."""
        return Case(
            id="case-001",
            referrer_id="ref-100",
            status=CaseStatus.SUBMITTED,
            created_at=datetime(2026, 1, 15),
        )

    @pytest.mark.asyncio
    async def test_get_by_id_returns_none_when_empty(self, repo):
        """Empty repo should return None for any ID."""
        result = await repo.get_by_id("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_save_and_get_by_id(self, repo, sample_case):
        """Saved case should be retrievable by ID."""
        await repo.save(sample_case)
        result = await repo.get_by_id("case-001")

        assert result is not None
        assert result.id == "case-001"
        assert result.referrer_id == "ref-100"

    @pytest.mark.asyncio
    async def test_save_overwrites_existing(self, repo, sample_case):
        """Saving a case with the same ID should overwrite."""
        await repo.save(sample_case)

        updated = sample_case.model_copy(update={"status": CaseStatus.ASSIGNED})
        await repo.save(updated)

        result = await repo.get_by_id("case-001")
        assert result is not None
        assert result.status == CaseStatus.ASSIGNED

    @pytest.mark.asyncio
    async def test_seed_populates_store(self, repo):
        """seed() should make all provided cases retrievable."""
        cases = [
            Case(id="case-a", referrer_id="ref-a", status=CaseStatus.DRAFT),
            Case(id="case-b", referrer_id="ref-b", status=CaseStatus.SUBMITTED),
        ]
        repo.seed(cases)

        a = await repo.get_by_id("case-a")
        b = await repo.get_by_id("case-b")

        assert a is not None
        assert a.id == "case-a"
        assert b is not None
        assert b.id == "case-b"

    @pytest.mark.asyncio
    async def test_get_by_id_does_not_return_wrong_case(self, repo, sample_case):
        """get_by_id should not return a case with a different ID."""
        await repo.save(sample_case)
        result = await repo.get_by_id("case-999")
        assert result is None
