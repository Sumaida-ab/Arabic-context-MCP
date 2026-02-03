<div align="center">

# Contributing to Arabic Accents MCP Server

[![العربية](https://img.shields.io/badge/العربية-green?style=flat-square)](CONTRIBUTING.ar.md)

</div>

Thanks for your interest in contributing! This project welcomes **Arabic language content contributions** from the community.

## What We Accept

✅ **New Arabic accents/dialects** — vocabulary, phrases, usage notes
✅ **Improvements to existing accents** — corrections, additions, examples
✅ **Bug reports** — issues with the server or data

## What We Don't Accept

❌ Code changes (server, build scripts, etc.)
❌ Changes to core `knowledge/` files
❌ Non-Arabic language content

> **Note:** Code contributions are handled by maintainers only. If you have a feature idea, open an issue to discuss it first.

---

## Adding a New Accent

All accent contributions go in `knowledge/contributions/`. Here's how:

### Step 1: Fork and create your folder

```
knowledge/contributions/<accent_id>/
```

Use lowercase, no spaces (e.g. `sudanese`, `moroccan`, `khaleeji`, `iraqi`)

### Step 2: Add `accent.json`

```json
{
  "name": "Your Accent Name",
  "description": "Brief description of this dialect"
}
```

### Step 3: Add your content

Choose one format:

**Option A: Markdown** (preferred)
Create `content.md` with vocabulary and phrases:

```markdown
# Sudanese Arabic

## Vocabulary

### شنو (shinu)
**Meaning:** What
**Example:** شنو اسمك؟ (What is your name?)

### تمام (tamam)
**Meaning:** Okay / Good
**Example:** كل شي تمام (Everything is fine)

## Common Phrases

| Phrase | Meaning | Usage |
|--------|---------|-------|
| كيفك | How are you | Informal greeting |
```

**Option B: PDFs**
Add `.pdf` files containing vocabulary, phrases, and usage notes.

### Step 4: Open a pull request

- Title: `Add [Accent Name] Arabic`
- Description: Brief overview of what's included

---

## Content Guidelines

Good contributions include:

- **Vocabulary**: Words with meanings and transliterations
- **Phrases**: Common expressions with context
- **Examples**: Sample sentences showing usage
- **Context**: Formal vs informal, regional variations

### Format requirements

- Arabic text must be UTF-8 encoded
- Include transliterations (Latin letters) when possible
- Provide English translations for all content

---

## Improving Existing Accents

To add content to an existing accent:

1. Find the accent folder in `knowledge/contributions/`
2. Edit `content.md` or add new PDF files
3. Open a pull request with your additions

---

## Bug Reports

Found an issue? Open a [GitHub issue](https://github.com/Sumaida-ab/Arabic-context-MCP/issues) with:

- What happened
- What you expected
- Steps to reproduce (if applicable)

---

## Questions?

Open an issue or start a discussion. We're happy to help!
