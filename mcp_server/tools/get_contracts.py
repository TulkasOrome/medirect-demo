"""Returns OpenAPI contracts for a given service domain."""

from pathlib import Path


def get_contracts(project_root: Path, domain: str) -> str:
    """Load and return the OpenAPI contract for a domain.

    Args:
        project_root: Absolute path to project root.
        domain: Service domain name (e.g. 'case', 'report').

    Returns:
        The contract YAML content, or an error message.
    """
    contracts_dir = project_root / "contracts"
    contract_file = contracts_dir / f"{domain}.yaml"

    if contract_file.exists():
        content = contract_file.read_text()
        return f"Contract for '{domain}':\n\n{content}"

    available = [f.stem for f in contracts_dir.glob("*.yaml")]
    if available:
        return (
            f"No contract found for '{domain}'. "
            f"Available contracts: {', '.join(available)}"
        )
    return f"No contracts found in {contracts_dir}."