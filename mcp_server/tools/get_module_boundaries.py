"""Returns import rules for a given module."""

BOUNDARIES: dict[str, dict] = {
    "services": {
        "can_import": ["models", "schemas", "exceptions", "utils"],
        "cannot_import": ["services (other)", "api"],
        "notes": (
            "Services must be independently testable. Use constructor injection "
            "for all dependencies. Never import one service into another — use contracts."
        ),
    },
    "models": {
        "can_import": ["(nothing — leaf layer)"],
        "cannot_import": ["services", "schemas", "api", "utils"],
        "notes": (
            "Models are pure Pydantic data classes. No business logic. "
            "No dependencies. These are the foundation everything else builds on."
        ),
    },
    "schemas": {
        "can_import": ["models"],
        "cannot_import": ["services", "api"],
        "notes": "Schemas define API request/response shapes. They may reference models for shared types.",
    },
    "exceptions": {
        "can_import": ["(nothing — leaf layer)"],
        "cannot_import": ["everything"],
        "notes": "All exceptions inherit from MEDirectError. Domain-specific, never generic.",
    },
    "tests": {
        "can_import": ["anything"],
        "cannot_import": [],
        "notes": "Test code has no import restrictions.",
    },
}


def get_module_boundaries(module: str) -> str:
    """Return import rules for a module.

    Args:
        module: Module name (e.g. 'services', 'models').

    Returns:
        Human-readable boundary rules.
    """
    rules = BOUNDARIES.get(module)
    if not rules:
        available = ", ".join(BOUNDARIES.keys())
        return f"Unknown module '{module}'. Available: {available}"

    lines = [
        f"Module boundaries for '{module}/':",
        "",
        f"  Can import from: {', '.join(rules['can_import'])}",
        f"  Cannot import from: {', '.join(rules['cannot_import'])}",
        "",
        f"  Notes: {rules['notes']}",
    ]
    return "\n".join(lines)