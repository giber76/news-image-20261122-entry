// Sunday 22 November 2026 — one front page, 38 stories.
// Node 22, standard library only. The entry is the entry.png drawn by
// draw.py in this repo; this program places that exact file at
// <output>/entry.png so the gate and the judge see the same bytes.
// The gate takes one whole PNG or JPEG of at most 1 MiB, 1024 by 1024.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The output directory is a mount point in the grader, so it is only ever
// created if missing — never removed, never emptied wholesale.
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));

console.log(`wrote ${join(outDir, 'entry.png')}`);
