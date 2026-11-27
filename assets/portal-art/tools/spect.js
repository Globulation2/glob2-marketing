// Spectator look: node spect.js SAVE OUT.png ZOOM_PLUS ZOOM_MINUS FX FY
const {snap} = require('./lib');
const {session} = require('./session');
(async () => {
  const [save, out, zp, zm, fx, fy] = process.argv.slice(2);
  const W = Number(process.env.VW || 2122), H = Number(process.env.VH || 1200);
  const {browser, page} = await session(save, {width: W, height: H});
  for (let i = 0; i < Number(zm); i++) { await page.mouse.click(W - 183, H - 17); await page.waitForTimeout(250); }
  for (let i = 0; i < Number(zp); i++) { await page.mouse.click(W - 112, H - 17); await page.waitForTimeout(250); }
  if (fx) await page.mouse.click(W - 165 + 130 * Number(fx), 8 + 130 * Number(fy));
  await page.waitForTimeout(Number(process.env.WAIT || 2000));
  await page.screenshot({path: out});
  const s = await snap(page); console.log(s.screen, s.tick, Object.keys(s.controls).filter(k => /spect|areas|fog/.test(k)).join(' '));
  await browser.close();
})();
