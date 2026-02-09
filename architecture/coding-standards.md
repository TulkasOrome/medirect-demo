# Coding Standards — Python

## General
- Python 3.11+
- Type hints on ALL public functions and methods
- Docstrings on all public classes and functions (Google style)
- Max function length: 50 lines
- Max file length: 300 lines
- No wildcard imports (from x import *)

## Naming
- Files: snake_case.py
- Classes: PascalCase
- Functions/methods: snake_case
- Constants: UPPER_SNAKE_CASE
- Private methods: _prefixed

## Dependencies
- Pydantic v2 for all data models
- httpx for async HTTP (never requests)
- pytest + pytest-asyncio for testing

## Patterns
- Constructor injection for all dependencies
- Domain exceptions (not generic Exception)
- Async by default for anything involving I/O
- Return Pydantic models from all public service methods