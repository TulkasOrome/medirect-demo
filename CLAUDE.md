# MEDirect Edge — Constitutional Context

## Before Writing Code
1. Read architecture/coding-standards.md — follow all standards
2. Read architecture/module-boundaries.md — respect import rules
3. Check contracts/ — honour all API contracts
4. Write tests FIRST that encode success conditions AND architectural constraints
5. Only then write implementation that passes your tests

## You MUST:
- Add type hints to all public functions
- Write docstrings on all public classes and functions
- Use dependency injection (constructor injection) for all services
- Keep functions under 50 lines
- Keep files under 300 lines
- Use domain exceptions from exceptions/ — never raise generic Exception
- Use async for all service methods that call external systems
- All models use Pydantic BaseModel

## You MUST NOT:
- Import from services/ in models/ (models are leaf nodes)
- Import from one service into another service directly
- Use global mutable state
- Hardcode API keys, connection strings, or secrets
- Return raw dicts from public functions (use Pydantic models)
- Modify any test file unless explicitly asked

## Module Boundaries (import direction)
- services/ → Can import: models/, schemas/, exceptions/, utils/
- models/   → Can import: nothing (leaf layer)
- schemas/  → Can import: models/ only
- tests/    → Can import: anything (test code)

## Error Handling
- All exceptions inherit from MEDirectError (in exceptions/base.py)
- Services raise domain exceptions, not generic Exception
- Never expose internal details in error messages

## Override Protocol
If a rule in this file conflicts with a specific, justified requirement:
1. The developer can instruct Claude Code to proceed anyway
2. Add a code comment: # OVERRIDE: [rule] — [reason] — [your name]
3. Note it in the PR description
4. The architectural tests in CI are the final authority — if they pass, you're fine