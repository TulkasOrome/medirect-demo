"""
Constitutional Agent — MCP Server for MEDirect Edge.

Claude Code spawns this as a child process on session start.
Exposes tools for architectural validation, contract retrieval,
and module boundary checks.

No separate infrastructure — runs locally, dies when session ends.
"""

from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from mcp_server.tools.validate_architecture import validate_architecture
from mcp_server.tools.get_contracts import get_contracts
from mcp_server.tools.get_module_boundaries import get_module_boundaries

PROJECT_ROOT = Path(__file__).parent.parent

server = Server("constitution")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Register tools that Claude Code can call."""
    return [
        Tool(
            name="validate_architecture",
            description=(
                "Validates a Python file path and its imports against module boundary rules. "
                "Call this BEFORE writing or modifying any Python file."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path relative to project root, e.g. 'services/case_service.py'"
                    },
                    "imports": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of import paths, e.g. ['models.case', 'services.other']"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="get_contracts",
            description="Returns the OpenAPI contract for a given service domain.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Service domain name, e.g. 'case', 'report'"
                    }
                },
                "required": ["domain"]
            }
        ),
        Tool(
            name="get_module_boundaries",
            description="Returns import rules and constraints for a given module directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "module": {
                        "type": "string",
                        "description": "Module name, e.g. 'services', 'models', 'schemas'"
                    }
                },
                "required": ["module"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to implementations."""
    if name == "validate_architecture":
        result = validate_architecture(
            project_root=PROJECT_ROOT,
            file_path=arguments["file_path"],
            imports=arguments.get("imports", [])
        )
    elif name == "get_contracts":
        result = get_contracts(
            project_root=PROJECT_ROOT,
            domain=arguments["domain"]
        )
    elif name == "get_module_boundaries":
        result = get_module_boundaries(module=arguments["module"])
    else:
        result = f"Unknown tool: {name}"

    return [TextContent(type="text", text=result)]


async def main():
    """Entry point — Claude Code connects via stdio."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())