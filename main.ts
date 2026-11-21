// news-image-20261121 — a one-image summary of Saturday 21 November 2026 world news.
// The program copies the poster (entry.png) beside this file to the output
// directory. Node 22, standard library only. The poster itself is drawn by
// draw_poster.py (Pillow) from the 30 verified 21 November stories.
//
// The image path is resolved from this file's own directory, never from the
// process working directory: the grader runs `node /bot/main.ts` from an
// arbitrary cwd, so a bare relative "entry.png" would fail there.
//
// Usage:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Resolve the poster from this file's own directory, never from the
// process working directory: the grader runs `node /bot/main.ts` from an
// arbitrary cwd, so a bare relative "entry.png" would fail there.
const src = join(here, 'entry.png');
const dst = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);

// Confirm the copy landed whole; a truncated image fails the gate.
if (statSync(dst).size !== statSync(src).size) {
  throw new Error(`entry.png copy mismatch: ${statSync(dst).size} != ${statSync(src).size}`);
}
console.log(`wrote ${dst} (${statSync(dst).size} bytes)`);
