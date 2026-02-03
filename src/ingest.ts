#!/usr/bin/env node
/**
 * Ingest Arabic accent knowledge from PDFs and JSON into markdown files.
 *
 * Sources:
 *   - knowledge/*.pdf → extract text, output to data/<name>.md
 *   - knowledge/contributions/<id>/ → accent.json + PDFs or content.md
 *
 * Usage:
 *   npx arabic-accents-mcp ingest
 *   node dist/ingest.js
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from "fs";
import { join, dirname, basename } from "path";
import { fileURLToPath } from "url";
// @ts-ignore - pdf-parse doesn't have great types
import pdf from "pdf-parse";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Directories
const ROOT_DIR = join(__dirname, "..");
const KNOWLEDGE_DIR = process.argv[2] || join(ROOT_DIR, "knowledge");
const DATA_DIR = join(ROOT_DIR, "data");
const CONTRIBUTIONS_DIR = join(KNOWLEDGE_DIR, "contributions");

interface AccentMeta {
  name: string;
  description: string;
}

interface Registry {
  [key: string]: AccentMeta;
}

// Extract text from PDF
async function extractPdfText(pdfPath: string): Promise<string> {
  try {
    const buffer = readFileSync(pdfPath);
    const data = await pdf(buffer);
    return data.text || "";
  } catch (error) {
    console.error(`  [ERROR] Failed to read ${basename(pdfPath)}: ${error}`);
    return "";
  }
}

// Convert PDF text to markdown
function pdfToMarkdown(text: string, name: string): string {
  return [
    `# ${name} Arabic\n`,
    `Content extracted from ${name} reference material.\n`,
    "---\n",
    text,
  ].join("\n");
}

// Process a contribution folder
async function processContribution(
  contribDir: string
): Promise<{ accentId: string; content: string; meta: AccentMeta } | null> {
  const accentJsonPath = join(contribDir, "accent.json");
  const contentMdPath = join(contribDir, "content.md");
  const dirName = basename(contribDir);

  if (!existsSync(accentJsonPath)) {
    console.log(`  [SKIP] ${dirName}: no accent.json`);
    return null;
  }

  let meta: AccentMeta;
  try {
    meta = JSON.parse(readFileSync(accentJsonPath, "utf-8"));
  } catch (error) {
    console.error(`  [ERROR] ${dirName}/accent.json: ${error}`);
    return null;
  }

  const name = meta.name || dirName;
  const description = meta.description || "";
  const accentId = dirName.toLowerCase();

  // Option 1: content.md exists
  if (existsSync(contentMdPath)) {
    const content = readFileSync(contentMdPath, "utf-8");
    return { accentId, content, meta: { name, description } };
  }

  // Option 2: PDFs in folder
  const pdfs = readdirSync(contribDir).filter(f => f.endsWith(".pdf"));
  if (pdfs.length > 0) {
    const textParts: string[] = [];
    for (const pdfFile of pdfs) {
      console.log(`    Extracting ${pdfFile}...`);
      const text = await extractPdfText(join(contribDir, pdfFile));
      if (text) {
        textParts.push(text);
      }
    }
    if (textParts.length > 0) {
      const combined = textParts.join("\n\n---\n\n");
      const md = `# ${name}\n\n${description}\n\n---\n\n${combined}`;
      return { accentId, content: md, meta: { name, description } };
    }
  }

  console.log(`  [SKIP] ${dirName}: no content.md or PDFs`);
  return null;
}

async function main() {
  console.log("Arabic Accents Ingestion Script\n");

  // Ensure data directory exists
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }

  const accents: Map<string, string> = new Map();
  const registry: Registry = {};

  // 1. Process PDFs in knowledge/
  console.log(`Processing PDFs in ${KNOWLEDGE_DIR}...`);
  if (existsSync(KNOWLEDGE_DIR)) {
    const files = readdirSync(KNOWLEDGE_DIR).filter(f => f.endsWith(".pdf"));
    for (const file of files) {
      console.log(`  ${file}`);
      const text = await extractPdfText(join(KNOWLEDGE_DIR, file));
      if (text) {
        const accentId = basename(file, ".pdf")
          .toLowerCase()
          .replace(/\s+/g, "-")
          .replace(/_/g, "-");
        const name = basename(file, ".pdf")
          .replace(/-/g, " ")
          .replace(/_/g, " ")
          .replace(/\b\w/g, c => c.toUpperCase());

        accents.set(accentId, pdfToMarkdown(text, name));
        registry[accentId] = {
          name: `${name} Arabic`,
          description: `Content from ${file}`,
        };
      }
    }
  }

  // 2. Process contributions
  if (existsSync(CONTRIBUTIONS_DIR)) {
    console.log(`\nProcessing contributions in ${CONTRIBUTIONS_DIR}...`);
    const dirs = readdirSync(CONTRIBUTIONS_DIR).filter(d => {
      const fullPath = join(CONTRIBUTIONS_DIR, d);
      return statSync(fullPath).isDirectory() && !d.startsWith(".");
    });

    for (const dir of dirs) {
      console.log(`  ${dir}/`);
      const result = await processContribution(join(CONTRIBUTIONS_DIR, dir));
      if (result) {
        const existing = accents.get(result.accentId);
        if (existing) {
          accents.set(result.accentId, existing + "\n\n---\n\n" + result.content);
        } else {
          accents.set(result.accentId, result.content);
          registry[result.accentId] = result.meta;
        }
      }
    }
  }

  // 3. Write output files
  console.log(`\nWriting ${accents.size} accent file(s) to ${DATA_DIR}...`);
  for (const [accentId, content] of accents) {
    const outPath = join(DATA_DIR, `${accentId}.md`);
    writeFileSync(outPath, content, "utf-8");
    console.log(`  ${accentId}.md`);
  }

  // 4. Write registry
  const registryPath = join(DATA_DIR, "accents.json");
  writeFileSync(registryPath, JSON.stringify(registry, null, 2), "utf-8");
  console.log(`  accents.json (registry)`);

  console.log(`\nDone. ${accents.size} accent(s) ready.`);
}

main().catch(console.error);
