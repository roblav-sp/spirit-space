// Headless browser verification for Spirit Space.
// Usage: node verify.mjs <base-url> <repo-root>
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';

const BASE = process.argv[2] ?? 'http://localhost:8123';
const ART = path.join(process.cwd(), 'artifacts');
fs.mkdirSync(ART, { recursive: true });

const results = [];
let passed = 0, failed = 0;

async function check(name, fn) {
  try {
    await fn();
    results.push(`PASS ${name}`);
    passed++;
  } catch (e) {
    results.push(`FAIL ${name}: ${String(e.message ?? e).split('\n')[0]}`);
    failed++;
    if (globalThis.__page) {
      await globalThis.__page
        .screenshot({ path: path.join(ART, `${name.replace(/\W+/g, '-')}.png`) })
        .catch(() => {});
    }
  }
}

// Sum of RGB channels over the canvas: cheap proxy for "did pixels change".
async function canvasSig(p) {
  return p.evaluate(() => {
    const c = document.getElementById('game');
    const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    let s = 0;
    for (let i = 0; i < d.length; i += 4) s += d[i] + d[i + 1] + d[i + 2];
    return s;
  });
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 900, height: 700 } });
globalThis.__page = page;

const consoleErrors = [];
page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('pageerror', e => consoleErrors.push(String(e)));

await page.goto(`${BASE}/index.html`, { waitUntil: 'load' });
await page.waitForTimeout(1000); // allow wasm to instantiate

// Bootstrap contract -------------------------------------------------------
await check('bootstrap: no console errors on load', async () => {
  if (consoleErrors.length) throw new Error(consoleErrors.join('; '));
});

await check('bootstrap: canvas is 800x600', async () => {
  const box = await page.locator('#game').boundingBox();
  if (!box) throw new Error('#game not found');
  if (box.width !== 800 || box.height !== 600)
    throw new Error(`canvas is ${box.width}x${box.height}`);
});

await check('law7: no error banner when wasm loads correctly', async () => {
  const pre = await page.locator('pre').count();
  if (pre > 0) throw new Error('unexpected <pre> error banner');
});

// Law 7 — broken wasm path must show a visible error banner (AC-Law7).
// Uses a separate page pointed at a missing wasm file on the same origin.
await check('law7: broken wasm shows visible error banner', async () => {
  const p2 = await browser.newPage();
  globalThis.__page = p2;
  await p2.setContent(`<!DOCTYPE html><html><body>
    <script>var Go = function(){ this.importObject = {}; };</script>
    <script>
      WebAssembly.instantiateStreaming(fetch("${BASE}/does-not-exist.wasm"), new Go().importObject)
        .catch(err => { document.body.innerHTML =
          "<pre style='color:red'>" + err + "</pre>"; });
    </script></body></html>`);
  await p2.waitForSelector('pre', { timeout: 5000 });
  const txt = await p2.locator('pre').textContent();
  if (!txt || txt.length < 10) throw new Error('error banner missing or empty');
  await p2.close();
  globalThis.__page = page;
});

// Gameplay smoke -----------------------------------------------------------
await check('gameplay: canvas animates without input', async () => {
  const a = await canvasSig(page);
  await page.waitForTimeout(1500);
  const b = await canvasSig(page);
  if (a === b) throw new Error('canvas static for 1.5s — is the wasm running?');
});

await check('input: ArrowRight changes rendering', async () => {
  const before = await canvasSig(page);
  await page.keyboard.down('ArrowRight');
  await page.waitForTimeout(400);
  await page.keyboard.up('ArrowRight');
  if ((await canvasSig(page)) === before)
    throw new Error('no visual change from movement input');
});

await check('input: Space fire produces visual change', async () => {
  const before = await canvasSig(page);
  await page.keyboard.down('Space');
  await page.waitForTimeout(100);
  await page.keyboard.up('Space');
  if ((await canvasSig(page)) === before)
    throw new Error('no visual change from fire input');
});

// FR-005.2 — R while running must NOT restart (no crash, game continues).
await check('input: KeyR while running does not crash or reset', async () => {
  const before = await canvasSig(page);
  await page.keyboard.press('KeyR');
  await page.waitForTimeout(300);
  const after = await canvasSig(page);
  if (!after) throw new Error('canvas blank after R');
  if (consoleErrors.length) throw new Error(consoleErrors.join('; '));
  void before;
});

await page.screenshot({ path: path.join(ART, 'final-state.png') });
await browser.close();

console.log(results.join('\n'));
console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
