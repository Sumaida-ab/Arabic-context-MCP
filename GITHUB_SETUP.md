# Pushing this project to GitHub

Follow these steps to create the GitHub repo and push this project.

## 1. Create the repository on GitHub

1. Go to [github.com](https://github.com) and sign in.
2. Click **New repository** (or the **+** menu → New repository).
3. Set:
   - **Repository name**: e.g. `arabic-accents-mcp`
   - **Description**: e.g. "MCP server that exposes Arabic accent libraries for AI agents (Cursor, Claude Desktop, etc.)"
   - **Public**
   - **Do not** check "Add a README" (this project already has one).
4. Click **Create repository**.

## 2. Push from your machine

In a terminal, from this project folder (`MCP`), run:

```bash
git init
git add .
git commit -m "Initial commit: open-source project structure for Arabic Accents MCP"
git branch -M main
git remote add origin https://github.com/Sumaida-ab/Arabic-context-MCP.git
git push -u origin main
```

If you use SSH:

```bash
git remote add origin git@github.com:Sumaida-ab/Arabic-context-MCP.git
```

## 3. After the first push

- Update **README.md** and **CONTRIBUTING.md**: replace `YOUR_USERNAME/arabic-accents-mcp` with your real repo URL.
- Optionally add a **description** and **topics** (e.g. `mcp`, `arabic`, `translation`) on the repo page.
- Optional: submit the server to the [MCP Registry](https://modelcontextprotocol.io/registry) so others can discover it.
