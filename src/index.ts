#!/usr/bin/env node
/**
 * Arabic Accents MCP Server
 *
 * Exposes Arabic accent knowledge as MCP resources.
 * Any MCP client (Cursor, Claude Desktop, etc.) can connect and use these resources.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync, existsSync, readdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Data directory - check multiple locations
function getDataDir(): string {
  // When running from npx, data might be in the package directory
  const locations = [
    join(__dirname, "..", "data"),      // dist/../data (development)
    join(__dirname, "data"),             // dist/data
    join(process.cwd(), "data"),         // current working directory
  ];

  for (const loc of locations) {
    if (existsSync(loc)) {
      return loc;
    }
  }

  return locations[0]; // Default to first option
}

const DATA_DIR = getDataDir();

interface AccentMeta {
  name: string;
  description: string;
}

interface Registry {
  [key: string]: AccentMeta;
}

// Load accent registry
function loadRegistry(): Registry {
  const registryPath = join(DATA_DIR, "accents.json");
  if (existsSync(registryPath)) {
    try {
      const content = readFileSync(registryPath, "utf-8");
      return JSON.parse(content);
    } catch {
      return {};
    }
  }
  return {};
}

// Get available accents from data/*.md files
function getAvailableAccents(): string[] {
  if (!existsSync(DATA_DIR)) {
    return [];
  }

  try {
    const files = readdirSync(DATA_DIR);
    return files
      .filter(f => f.endsWith(".md"))
      .map(f => f.replace(".md", ""));
  } catch {
    return [];
  }
}

// Load data at startup
const REGISTRY = loadRegistry();
const ACCENTS = getAvailableAccents();

// Create MCP server
const server = new McpServer({
  name: "Arabic Accents",
  version: "1.0.0",
});

// List all resources
server.resource(
  "list",
  "arabic-accents://list",
  async () => {
    if (ACCENTS.length === 0) {
      return {
        contents: [{
          uri: "arabic-accents://list",
          mimeType: "text/markdown",
          text: "No accents available. Run the ingest script to generate accent data.",
        }],
      };
    }

    const lines = ["# Available Arabic Accents\n"];
    for (const accentId of ACCENTS.sort()) {
      const meta = REGISTRY[accentId] || {};
      const name = meta.name || accentId.charAt(0).toUpperCase() + accentId.slice(1);
      const desc = meta.description || "";
      lines.push(`- **${name}** (\`${accentId}\`)`);
      if (desc) {
        lines.push(`  ${desc}`);
      }
    }
    lines.push(`\nTotal: ${ACCENTS.length} accent(s)`);
    lines.push("\nUse `arabic-accents://<accent_id>` to get the full content for an accent.");

    return {
      contents: [{
        uri: "arabic-accents://list",
        mimeType: "text/markdown",
        text: lines.join("\n"),
      }],
    };
  }
);

// Register a resource for each accent
for (const accentId of ACCENTS) {
  const meta = REGISTRY[accentId] || {};
  const name = meta.name || accentId.charAt(0).toUpperCase() + accentId.slice(1);

  server.resource(
    accentId,
    `arabic-accents://${accentId}`,
    async () => {
      const filePath = join(DATA_DIR, `${accentId}.md`);
      if (!existsSync(filePath)) {
        return {
          contents: [{
            uri: `arabic-accents://${accentId}`,
            mimeType: "text/plain",
            text: `Accent '${accentId}' not found.`,
          }],
        };
      }

      const content = readFileSync(filePath, "utf-8");
      return {
        contents: [{
          uri: `arabic-accents://${accentId}`,
          mimeType: "text/markdown",
          text: content,
        }],
      };
    }
  );
}

// Tool: Get accent content
server.tool(
  "get_accent_content",
  "Get the full content for a specific Arabic accent",
  {
    accent_id: z.string().describe("The accent identifier (e.g., 'emirati', 'levantine', 'levantine')"),
  },
  async ({ accent_id }) => {
    // Sanitize input to prevent path traversal
    const id = accent_id.toLowerCase().trim().replace(/[^a-z0-9-]/g, "");

    // Verify accent exists in known list
    if (!ACCENTS.includes(id)) {
      const available = ACCENTS.length > 0 ? ACCENTS.sort().join(", ") : "none";
      return {
        content: [{
          type: "text",
          text: `Accent '${id}' not found. Available accents: ${available}`,
        }],
      };
    }

    const filePath = join(DATA_DIR, `${id}.md`);

    if (!existsSync(filePath)) {
      const available = ACCENTS.length > 0 ? ACCENTS.sort().join(", ") : "none";
      return {
        content: [{
          type: "text",
          text: `Accent '${id}' not found. Available accents: ${available}`,
        }],
      };
    }

    const content = readFileSync(filePath, "utf-8");
    return {
      content: [{
        type: "text",
        text: content,
      }],
    };
  }
);

// Tool: List available accents
server.tool(
  "list_available_accents",
  "List all available Arabic accents in the library",
  {},
  async () => {
    if (ACCENTS.length === 0) {
      return {
        content: [{
          type: "text",
          text: "No accents available. The knowledge base may need to be ingested first.",
        }],
      };
    }

    const lines = ["Available Arabic Accents:"];
    for (const accentId of ACCENTS.sort()) {
      const meta = REGISTRY[accentId] || {};
      const name = meta.name || accentId.charAt(0).toUpperCase() + accentId.slice(1);
      lines.push(`  - ${accentId}: ${name}`);
    }

    return {
      content: [{
        type: "text",
        text: lines.join("\n"),
      }],
    };
  }
);

// Prompt: Translate to accent
server.prompt(
  "translate_to_accent",
  "Generate a prompt for translating content into a specific Arabic accent",
  {
    accent: z.string().describe("The target accent (e.g., 'emirati', 'levantine')"),
    content: z.string().optional().describe("Optional content to translate"),
  },
  async ({ accent, content }) => {
    const accentLower = accent.toLowerCase().trim();
    const meta = REGISTRY[accentLower] || {};
    const name = meta.name || accent.charAt(0).toUpperCase() + accent.slice(1) + " Arabic";

    const promptLines = [
      `You are a translator specializing in ${name}.`,
      `Use the vocabulary, phrases, and style from the ${name} accent library.`,
      "Translate the following content naturally, preserving meaning while using authentic dialect expressions.",
      "",
    ];

    if (content) {
      promptLines.push("Content to translate:");
      promptLines.push(content);
    } else {
      promptLines.push("Please provide the content you want translated.");
    }

    return {
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: promptLines.join("\n"),
        },
      }],
    };
  }
);

// Start the server
async function main() {
  console.error("Arabic Accents MCP Server");
  console.error(`  Accents loaded: ${ACCENTS.length}`);
  console.error(`  Data directory: ${DATA_DIR}`);

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
