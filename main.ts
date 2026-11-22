// Sunday 22 November 2026 — one front page, 39 stories (v4, late edition).
// Node 22, standard library only. draw.py paints entry.png in this repo;
// this program drops that exact file into <output>/entry.png so the gate
// and the judge both see the same bytes. The gate wants a single whole
// PNG or JPEG, at most 1 MiB and at most 1024 by 1024 pixels.
//
// When run outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const dest = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// In the grader /output is a mount point: create it when it is missing,
// never remove it and never empty it wholesale.
mkdirSync(dest, { recursive: true });
copyFileSync(join(root, "entry.png"), join(dest, "entry.png"));

console.log(`wrote ${join(dest, "entry.png")}`);
