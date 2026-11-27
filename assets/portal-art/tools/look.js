// Look at one minimap point at a given number of zoom-in clicks: node look.js SAVE OUT.png FX FY ZOOMCLICKS [WAITMS]
const {session} = require('./session');
(async () => {
  const [save, out, fx, fy, zc, wait] = process.argv.slice(2);
  const W = Number(process.env.VW || 2122), H = Number(process.env.VH || 1138);
  const {browser, page} = await session(save, {width: W, height: H});
  for (let i = 0; i < Number(zc); i++) { await page.mouse.click(W - 112, H - 17); await page.waitForTimeout(300); }
  await page.mouse.click(W - 165 + 130 * Number(fx), 8 + 130 * Number(fy));
  await page.waitForTimeout(Number(wait || 2000));
  await page.screenshot({path: out});
  await browser.close();
})();
