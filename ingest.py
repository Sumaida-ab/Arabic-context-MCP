#!/usr/bin/env python3
"""
Ingest Arabic accent knowledge from PDFs and JSON into markdown files.

Sources:
  - knowledge/*.pdf          → extract text, output to data/<name>.md
  - knowledge/contributions/<id>/ → accent.json + PDFs or content.md
  - data/dialects/*.json     → curated JSON vocabulary → data/<dialect>.md

Usage:
  python ingest.py
  python ingest.py --knowledge-dir path/to/pdfs
"""

import argparse
import json
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    if PdfReader is None:
        print(f"  [WARN] pypdf not installed, skipping {pdf_path.name}")
        return ""
    try:
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n\n".join(text_parts)
    except Exception as e:
        print(f"  [ERROR] Failed to read {pdf_path.name}: {e}")
        return ""


def json_to_markdown(data: dict) -> str:
    """Convert curated JSON vocabulary to markdown."""
    dialect = data.get("dialect", "Unknown")
    terms = data.get("terms", [])
    
    lines = [f"# {dialect} Arabic\n"]
    lines.append(f"Vocabulary and phrases for {dialect} dialect.\n")
    lines.append("## Vocabulary\n")
    
    for term in terms:
        word = term.get("word", "").strip()
        meaning = term.get("meaning", "").strip()
        context = term.get("context", "").strip()
        
        if not word:
            continue
        
        lines.append(f"### {word}\n")
        if meaning:
            # Clean up meaning (remove excessive newlines)
            meaning_clean = re.sub(r'\n{3,}', '\n\n', meaning)
            lines.append(f"**Meaning:** {meaning_clean}\n")
        if context and context != meaning:
            context_clean = re.sub(r'\n{3,}', '\n\n', context)
            lines.append(f"**Example:** {context_clean}\n")
        lines.append("")
    
    return "\n".join(lines)


def pdf_to_markdown(text: str, name: str) -> str:
    """Wrap extracted PDF text in markdown structure."""
    lines = [f"# {name} Arabic\n"]
    lines.append(f"Content extracted from {name} reference material.\n")
    lines.append("---\n")
    lines.append(text)
    return "\n".join(lines)


def process_contribution(contrib_dir: Path) -> tuple[str, str] | None:
    """Process a contribution folder (accent.json + PDFs or content.md)."""
    accent_json = contrib_dir / "accent.json"
    content_md = contrib_dir / "content.md"
    
    if not accent_json.exists():
        print(f"  [SKIP] {contrib_dir.name}: no accent.json")
        return None
    
    try:
        meta = json.loads(accent_json.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [ERROR] {contrib_dir.name}/accent.json: {e}")
        return None
    
    name = meta.get("name", contrib_dir.name)
    description = meta.get("description", "")
    accent_id = contrib_dir.name.lower()
    
    # Option 1: content.md exists
    if content_md.exists():
        content = content_md.read_text(encoding="utf-8")
        return accent_id, content
    
    # Option 2: PDFs in folder
    pdfs = list(contrib_dir.glob("*.pdf"))
    if pdfs:
        text_parts = []
        for pdf in pdfs:
            print(f"    Extracting {pdf.name}...")
            text = extract_pdf_text(pdf)
            if text:
                text_parts.append(text)
        if text_parts:
            combined = "\n\n---\n\n".join(text_parts)
            md = f"# {name}\n\n{description}\n\n---\n\n{combined}"
            return accent_id, md
    
    print(f"  [SKIP] {contrib_dir.name}: no content.md or PDFs")
    return None


def main():
    parser = argparse.ArgumentParser(description="Ingest Arabic accent knowledge")
    parser.add_argument("--knowledge-dir", type=Path, default=Path("knowledge"),
                        help="Directory containing PDFs (default: knowledge/)")
    parser.add_argument("--data-dir", type=Path, default=Path("data"),
                        help="Output directory for markdown files (default: data/)")
    args = parser.parse_args()
    
    knowledge_dir = args.knowledge_dir.resolve()
    data_dir = args.data_dir.resolve()
    dialects_dir = data_dir / "dialects"
    contributions_dir = knowledge_dir / "contributions"
    
    data_dir.mkdir(exist_ok=True)
    
    accents: dict[str, str] = {}  # accent_id -> markdown content
    registry: dict[str, dict] = {}  # accent_id -> {name, description}
    
    # 1. Process PDFs in knowledge/
    print(f"Processing PDFs in {knowledge_dir}...")
    for pdf in knowledge_dir.glob("*.pdf"):
        print(f"  {pdf.name}")
        text = extract_pdf_text(pdf)
        if text:
            accent_id = pdf.stem.lower().replace(" ", "-").replace("_", "-")
            # Try to make a nicer name
            name = pdf.stem.replace("-", " ").replace("_", " ").title()
            accents[accent_id] = pdf_to_markdown(text, name)
            registry[accent_id] = {"name": f"{name} Arabic", "description": f"Content from {pdf.name}"}
    
    # 2. Process curated JSON in data/dialects/
    if dialects_dir.exists():
        print(f"Processing curated JSON in {dialects_dir}...")
        for json_file in dialects_dir.glob("*.json"):
            print(f"  {json_file.name}")
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                dialect = data.get("dialect", json_file.stem)
                accent_id = dialect.lower().replace(" ", "-")
                md = json_to_markdown(data)
                
                # Merge if accent already exists
                if accent_id in accents:
                    accents[accent_id] += f"\n\n---\n\n{md}"
                else:
                    accents[accent_id] = md
                    registry[accent_id] = {"name": f"{dialect} Arabic", "description": f"Vocabulary for {dialect} dialect"}
            except Exception as e:
                print(f"  [ERROR] {json_file.name}: {e}")
    
    # 3. Process contributions
    if contributions_dir.exists():
        print(f"Processing contributions in {contributions_dir}...")
        for contrib in contributions_dir.iterdir():
            if contrib.is_dir() and not contrib.name.startswith("."):
                print(f"  {contrib.name}/")
                result = process_contribution(contrib)
                if result:
                    accent_id, content = result
                    if accent_id in accents:
                        accents[accent_id] += f"\n\n---\n\n{content}"
                    else:
                        accents[accent_id] = content
                        # Try to get name from accent.json
                        try:
                            meta = json.loads((contrib / "accent.json").read_text(encoding="utf-8"))
                            registry[accent_id] = {"name": meta.get("name", accent_id), "description": meta.get("description", "")}
                        except:
                            registry[accent_id] = {"name": accent_id.title(), "description": ""}
    
    # 4. Write output files
    print(f"\nWriting {len(accents)} accent file(s) to {data_dir}...")
    for accent_id, content in accents.items():
        out_path = data_dir / f"{accent_id}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"  {out_path.name}")
    
    # 5. Write registry
    registry_path = data_dir / "accents.json"
    registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  {registry_path.name} (registry)")
    
    print(f"\nDone. {len(accents)} accent(s) ready.")


if __name__ == "__main__":
    main()
