# Module Boundaries — Import Direction Rules

## Dependency Graph

```
tests/  ──→  (anything)
api/    ──→  services/, schemas/, models/, exceptions/, utils/, config
services/ ──→  models/, schemas/, exceptions/, utils/
schemas/  ──→  models/
models/   ──→  (nothing — leaf layer)
exceptions/ ──→ (nothing — leaf layer)
utils/    ──→  models/, exceptions/
```

## Rules

1. **models/** is a leaf module. It may not import from any other project module.
2. **exceptions/** is a leaf module. It may not import from any other project module.
3. **schemas/** may only import from **models/**.
4. **utils/** may import from **models/** and **exceptions/** only.
5. **services/** may import from **models/**, **schemas/**, **exceptions/**, and **utils/**.
6. **api/** may import from **services/**, **schemas/**, **models/**, **exceptions/**, **utils/**, and **config**.
7. **tests/** may import from anything (test code is unrestricted).
8. No service may import from another service directly — use contracts/protocols instead.

## Rationale

- Keeps the domain model independent of frameworks and infrastructure.
- Services depend only on abstractions (protocols), not concrete implementations.
- The API layer is the only place that touches FastAPI — services remain framework-agnostic.
