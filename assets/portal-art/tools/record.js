// Record one take of the lite build's own canvas at real speed:
// node record.js SAVE OUT.webm W H FX FY ZOOMCLICKS SECONDS [SETTLE_MS]
// The canvas is captured with canvas.captureStream(60) + MediaRecorder (no cursor: the
// canvas never contains one). Each frame is what the game drew; nothing is sped up.
const fs = require('fs');
const {snap} = require('./lib');
const {session} = require('./session');
(async () => {
  const [save, out, W, H, fx, fy, zc, secs, settle] = process.argv.slice(2);
  const w = Number(W), h = Number(H);
  const {browser, page} = await session(save, {width: w, height: h});
  for (let i = 0; i < Number(zc); i++) { await page.mouse.click(w - 112, h - 17); await page.waitForTimeout(300); }
  await page.mouse.click(w - 165 + 130 * Number(fx), 8 + 130 * Number(fy));
  await page.mouse.move(w / 2, 5); // pointer parked on the top bar; the canvas has no cursor anyway
  await page.waitForTimeout(Number(settle || 3000));
  const before = await snap(page);
  const b64 = await page.evaluate(async ({ms, codecs}) => {
    const canvas = document.getElementById('canvas');
    const stream = canvas.captureStream(60);
    const type = codecs.find(t => MediaRecorder.isTypeSupported(t));
    const rec = new MediaRecorder(stream, {mimeType: type, videoBitsPerSecond: 120000000});
    const chunks = [];
    rec.ondataavailable = e => chunks.push(e.data);
    const done = new Promise(r => rec.onstop = r);
    rec.start(1000);
    await new Promise(r => setTimeout(r, ms));
    rec.stop(); await done;
    const buf = await new Blob(chunks).arrayBuffer();
    let s = ''; const u = new Uint8Array(buf);
    for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000));
    return btoa(s);
  }, {ms: Number(secs) * 1000, codecs: process.env.CODECS ? JSON.parse(process.env.CODECS) : ['video/webm;codecs=vp9', 'video/webm;codecs=vp8']});
  const after = await snap(page);
  fs.writeFileSync(out, Buffer.from(b64, 'base64'));
  const meta = {codec: process.env.CODECS || 'vp9', save, viewport: [w, h], minimap_point: [Number(fx), Number(fy)], zoom_clicks: Number(zc), seconds: Number(secs),
    tick_start: before.tick, tick_end: after.tick, frames_start: before.frames, frames_end: after.frames, renderer: after.renderer,
    edition: await page.evaluate(() => globalThis.Glob2Edition.name), version: after.version};
  fs.writeFileSync(out.replace(/\.webm$/, '.json'), JSON.stringify(meta, null, 1));
  await page.screenshot({path: out.replace(/\.webm$/, '-end.png')});
  console.log(JSON.stringify(meta));
  await browser.close();
})();
