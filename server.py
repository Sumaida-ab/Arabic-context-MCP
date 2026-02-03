#!/usr/bin/env python3
"""
Arabic Accents MCP Server

Exposes Arabic accent knowledge as MCP resources.
Any MCP client (Cursor, Claude Desktop, etc.) can connect and use these resources.

Usage:
  python server.py                           # stdio transport (default)
  python server.py --transport sse --port 8000  # SSE transport for remote clients
"""

import argparse
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Arabic Accents")

# Data directory (relative to this script)
DATA_DIR = Path(__file__).parent / "data"


def load_registry() -> dict:
    """Load accent registry (accent_id -> {name, description})."""
    registry_path = DATA_DIR / "accents.json"
    if registry_path.exists():
        try:
            return json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def get_available_accents() -> list[str]:
    """Get list of available accent IDs from data/*.md files."""
    if not DATA_DIR.exists():
        return []
    return [f.stem for f in DATA_DIR.glob("*.md")]


# Load registry at startup
REGISTRY = load_registry()
ACCENTS = get_available_accents()


@mcp.resource("arabic-accents://list")
def list_accents() -> str:
    """List all available Arabic accents."""
    if not ACCENTS:
        return "No accents available. Run `python ingest.py` to generate accent data."
    
    lines = ["# Available Arabic Accents\n"]
    for accent_id in sorted(ACCENTS):
        meta = REGISTRY.get(accent_id, {})
        name = meta.get("name", accent_id.title())
        desc = meta.get("description", "")
        lines.append(f"- **{name}** (`{accent_id}`)")
        if desc:
            lines.append(f"  {desc}")
    
    lines.append(f"\nTotal: {len(ACCENTS)} accent(s)")
    lines.append("\nUse `arabic-accents://<accent_id>` to get the full content for an accent.")
    return "\n".join(lines)


# Dynamically register a resource for each accent
for _accent_id in ACCENTS:
    # Capture accent_id in closure
    def make_resource(accent_id: str):
        @mcp.resource(f"arabic-accents://{accent_id}")
        def get_accent() -> str:
            """Get Arabic accent vocabulary and phrases."""
            file_path = DATA_DIR / f"{accent_id}.md"
            if not file_path.exists():
                return f"Accent '{accent_id}' not found."
            return file_path.read_text(encoding="utf-8")
        
        # Set proper name and description
        meta = REGISTRY.get(accent_id, {})
        get_accent.__name__ = f"get_{accent_id}"
        get_accent.__doc__ = meta.get("description", f"Vocabulary and phrases for {accent_id} Arabic")
        return get_accent
    
    make_resource(_accent_id)


@mcp.tool()
def get_accent_content(accent_id: str) -> str:
    """
    Get the full content for a specific Arabic accent.
    
    Args:
        accent_id: The accent identifier (e.g., 'emirati', 'levantine', 'khaleeji')
    
    Returns:
        Markdown content with vocabulary, phrases, and usage notes for the accent.
    """
    accent_id = accent_id.lower().strip()
    file_path = DATA_DIR / f"{accent_id}.md"
    
    if not file_path.exists():
        available = ", ".join(sorted(ACCENTS)) if ACCENTS else "none"
        return f"Accent '{accent_id}' not found. Available accents: {available}"
    
    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def list_available_accents() -> str:
    """
    List all available Arabic accents in the library.
    
    Returns:
        A list of available accent IDs with their names.
    """
    if not ACCENTS:
        return "No accents available. The knowledge base may need to be ingested first."
    
    lines = ["Available Arabic Accents:"]
    for accent_id in sorted(ACCENTS):
        meta = REGISTRY.get(accent_id, {})
        name = meta.get("name", accent_id.title())
        lines.append(f"  - {accent_id}: {name}")
    return "\n".join(lines)


@mcp.prompt()
def translate_to_accent(accent: str, content: str = "") -> str:
    """
    Generate a prompt for translating content into a specific Arabic accent.
    
    Args:
        accent: The target accent (e.g., 'emirati', 'levantine')
        content: Optional content to translate (leave empty to translate user's next message)
    """
    accent_lower = accent.lower().strip()
    meta = REGISTRY.get(accent_lower, {})
    name = meta.get("name", accent.title() + " Arabic")
    
    prompt_lines = [
        f"You are a translator specializing in {name}.",
        f"Use the vocabulary, phrases, and style from the {name} accent library.",
        "Translate the following content naturally, preserving meaning while using authentic dialect expressions.",
        "",
    ]
    
    if content:
        prompt_lines.append("Content to translate:")
        prompt_lines.append(content)
    else:
        prompt_lines.append("Please provide the content you want translated.")
    
    return "\n".join(prompt_lines)


def main():
    parser = argparse.ArgumentParser(description="Arabic Accents MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http"],
                        default="stdio", help="Transport type (default: stdio)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port for SSE/HTTP transport (default: 8000)")
    args = parser.parse_args()
    
    print(f"Arabic Accents MCP Server")
    print(f"  Accents loaded: {len(ACCENTS)}")
    print(f"  Transport: {args.transport}")
    
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "sse":
        mcp.run(transport="sse")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
