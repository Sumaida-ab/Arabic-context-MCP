<div align="center">

# Arabic Accents MCP Server

[![العربية](https://img.shields.io/badge/العربية-green?style=flat-square)](README.ar.md)

</div>

An open-source [MCP](https://modelcontextprotocol.io) (Model Context Protocol) server that exposes a library of Arabic accents and vocabulary. Use it with any MCP-capable AI agent (Cursor, Claude Desktop, and others) to get context for translating or adapting content into Emirati, Levantine, Gulf, or other Arabic varieties.

## What it does

- **Resources**: Exposes accent guides (vocabulary, phrases, usage notes) as MCP resources. Your AI agent can pull in the right accent context when you ask for translations (e.g. "translate this into Emirati Arabic").
- **Pre-built knowledge base**: Comes with Arabic accent data ready to use out of the box.
- **Any client**: Works with Cursor, Claude Desktop, MCP Inspector, or any app that speaks MCP.

## Quick Start (No Installation Required)

Just add this to your MCP client config — no cloning, no setup:

### Cursor

Edit `~/.cursor/mcp.json` (macOS/Linux) or `%USERPROFILE%\.cursor\mcp.json` (Windows):

```json
{
  "mcpServers": {
    "arabic-accents": {
      "command": "npx",
      "args": ["-y", "arabic-accents-mcp"]
    }
  }
}
```

Restart Cursor. Done.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "arabic-accents": {
      "command": "npx",
      "args": ["-y", "arabic-accents-mcp"]
    }
  }
}
```

Restart Claude Desktop. Done.

## Usage

Once connected, ask your AI assistant:

- "What Arabic accents are available?"
- "Show me the Emirati Arabic vocabulary"
- "Translate 'Hello, how are you?' into Emirati Arabic"
- "Convert this formal Arabic text to casual Gulf dialect"

The AI will use the accent library for authentic dialect expressions.

### Available Resources

| Resource | Description |
|----------|-------------|
| `arabic-accents://list` | List all available accents |
| `arabic-accents://emirati` | Emirati Arabic vocabulary and phrases |
| `arabic-accents://arabic-language` | Arabic language examples and structure |

### Available Tools

| Tool | Description |
|------|-------------|
| `get_accent_content` | Get full content for a specific accent |
| `list_available_accents` | List all available accents |

## Requirements

- Node.js 18+ (only if running locally)
- For `npx` usage: Node.js must be installed, but no other setup needed

## Local Development

If you want to contribute or modify the server:

```bash
# Clone the repo
git clone https://github.com/Sumaida-ab/Arabic-context-MCP.git
cd Arabic-context-MCP

# Install dependencies
npm install

# Build
npm run build

# Run the server
npm start

# Ingest new PDFs (if adding accents)
npm run ingest
```

## Project Structure

| Path | Purpose |
|------|---------|
| `src/` | TypeScript source code |
| `dist/` | Compiled JavaScript (generated) |
| `data/` | Pre-built accent content (markdown) |
| `knowledge/` | Source PDFs (maintainers only) |
| `knowledge/contributions/` | Community-contributed accents |

## Contributing a New Accent

Want to add an Arabic accent or dialect? See our [Contributing Guide](CONTRIBUTING.en.md).

## Sources and Citations

The knowledge base includes content from the following sources:

### Emirati Arabic

- **Title:** لهجتنا المحلية (Our Local Dialect) — Second Edition
- **Author:** عائشة جمعة الرميثي (Aisha Juma Al Rumaithi)
- **Publisher:** الاتحاد النسائي العام (General Women's Union), UAE
- **ISBN:** 978-9948-22-843-1
- **Contributors:**
  - Cover Design: روضة سالم السويدي (Rawda Salem Al Suwaidi)
  - First Edition Review: لولوة عيسى الحميدي (Lulwa Issa Al Humaidi)
  - Linguistic Review: الأستاذ رائد الحلاحلة (Prof. Raed Al Halalah)

### Arabic Language Examples

- **File:** Arabic-Source.pdf
- **Content:** Examples of Arabic words, phrases, and how the Arabic language works

---

All content is used for educational and linguistic reference purposes. If you are a rights holder and have concerns, please open an issue.

## License

MIT — see [LICENSE](../LICENSE).

## Contributing

Contributions are welcome. See [CONTRIBUTING.en.md](CONTRIBUTING.en.md) for full guidelines.
