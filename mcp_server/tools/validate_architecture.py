"""
Validates file placement and imports against module boundary rules.

Checks that:
- Files are placed in valid module directories
- Imports respect the one-way dependency flow
- Cross-service imports are blocked (use contracts instead)
"""

from pathlib import Path

LAYER_RULES: dict[str, dict[str, str]] = {
    "services": {
        "models": "ALLOW",
        "schemas": "ALLOW",
        "exceptions": "ALLOW",
        "utils": "ALLOW",
        "services": "BLOCK",
        "api": "BLOCK",
    },
    "models": {
        "models": "ALLOW",
        "exceptions": "ALLOW",
        "services": "BLOCK",
        "schemas": "BLOCK",
        "api": "BLOCK",
        "utils": "BLOCK",
    },
    "schemas": {
        "models": "ALLOW",
        "schemas": "ALLOW",
        "exceptions": "ALLOW",
        "services": "BLOCK",
        "api": "BLOCK",
    },
    "exceptions": {
        "exceptions": "ALLOW",
        "services": "BLOCK",
        "models": "BLOCK",
        "schemas": "BLOCK",
        "api": "BLOCK",
    },
}


def get_layer(path: str) -> str:
    """Determine which architectural layer a file belongs to."""
    parts = Path(path).parts
    if not parts:
        return "unknown"
    first = parts[0]
    if first in ("services", "models", "schemas", "exceptions", "utils", "api", "tests"):
        return first
    return "unknown"


def validate_architecture(
    project_root: Path,
    file_path: str,
    imports: list[str] | None = None,
) -> str:
    """Validate a file against architectural rules.

    Args:
        project_root: Absolute path to project root.
        file_path: Relative path of the file being checked.
        imports: List of import module paths found in the file.

    Returns:
        Human-readable validation result.
    """
    findings: list[str] = []
    source_layer = get_layer(file_path)

    if source_layer == "unknown":
        findings.append(
            f"WARNING: {file_path} is not in a recognised module directory. "
            f"Expected: services/, models/, schemas/, exceptions/, utils/, api/"
        )

    if source_layer == "tests":
        return "PASS — Test files have no import restrictions."

    for imp in (imports or []):
        target_layer = get_layer(imp.replace(".", "/"))
        rules = LAYER_RULES.get(source_layer, {})
        verdict = rules.get(target_layer)

        if verdict == "BLOCK":
            findings.append(
                f"BLOCK: {file_path} ({source_layer}) imports '{imp}' ({target_layer}) "
                f"— violates module boundary. "
                f"{'Use API contracts instead of direct cross-service imports.' if target_layer == 'services' else 'This dependency direction is not allowed.'}"
            )
        elif verdict is None and target_layer != "unknown":
            findings.append(
                f"WARN: {file_path} ({source_layer}) imports '{imp}' ({target_layer}) "
                f"— no explicit rule found. Verify this is intentional."
            )

    # File length check
    full_path = project_root / file_path
    if full_path.exists():
        lines = full_path.read_text().splitlines()
        if len(lines) > 300:
            findings.append(
                f"WARN: {file_path} is {len(lines)} lines (max 300). Consider splitting."
            )

    if not findings:
        return "PASS — No architectural violations found."

    return "\n".join(findings)