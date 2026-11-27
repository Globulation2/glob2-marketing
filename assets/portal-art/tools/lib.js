const {chromium} = require('playwright');
const snap = page => page.evaluate(() => glob2Diagnostics.snapshot());
async function waitFor(page, pred, ms = 120000) {
  const t = Date.now();
  while (Date.now() - t < ms) {
    const s = await page.evaluate(() => typeof glob2Diagnostics !== 'undefined' ? glob2Diagnostics.snapshot() : null).catch(() => null);
    if (s && pred(s)) return s;
    await page.waitForTimeout(250);
  }
  throw new Error('timeout');
}
async function click(page, key) {
  const s = await waitFor(page, s => s.controls && s.controls[key] && s.controls[key].enabled !== false, 30000);
  const b = s.controls[key]; const v = (b.visible && b.visible.w > 4) ? b.visible : b;
  const vp = await page.evaluate(() => ({w: innerWidth, h: innerHeight}));
  const x = (v.x + v.w / 2) * vp.w / b.surface.w, y = (v.y + v.h / 2) * vp.h / b.surface.h;
  await page.mouse.click(x, y, {delay: 80});
  await page.waitForTimeout(400);
}
async function open(opts = {}) {
  const browser = await chromium.launch({headless: true, args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist']});
  const page = await browser.newPage({viewport: opts.viewport || {width: 1280, height: 720}, deviceScaleFactor: opts.dpr || 1});
  await page.goto('http://127.0.0.1:8791/');
  await waitFor(page, s => s.controls && Object.keys(s.controls).length > 0);
  return {browser, page};
}
module.exports = {snap, waitFor, click, open};
