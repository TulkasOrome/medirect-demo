"""
Architectural Boundary Tests — run on every CI push.
Enforces system-level rules across ALL code.
"""

from pathlib import Path
import ast


class TestModuleBoundaries:
    """Verify import rules are respected across the entire codebase."""

    def test_models_do_not_import_services(self):
        """models/ must never import from services/."""
        models_dir = Path("models")
        if not models_dir.exists():
            return
        for py_file in models_dir.rglob("*.py"):
            content = py_file.read_text()
            assert "from services" not in content, \
                f"{py_file} imports from services/ — models are leaf nodes"
            assert "import services" not in content, \
                f"{py_file} imports services — models are leaf nodes"

    def test_no_generic_exception_in_services(self):
        """Services must raise domain exceptions, not bare Exception."""
        services_dir = Path("services")
        if not services_dir.exists():
            return
        for py_file in services_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            content = py_file.read_text()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Raise) and node.exc:
                    if isinstance(node.exc, ast.Call):
                        if isinstance(node.exc.func, ast.Name):
                            assert node.exc.func.id != "Exception", \
                                f"{py_file} raises generic Exception — use domain exceptions"

    def test_all_public_functions_have_type_hints(self):
        """All public functions in services/ must have return type annotations."""
        services_dir = Path("services")
        if not services_dir.exists():
            return
        for py_file in services_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            content = py_file.read_text()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not node.name.startswith("_"):
                        assert node.returns is not None, \
                            f"{py_file}:{node.name}() missing return type hint"