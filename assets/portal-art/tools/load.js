// Load a save (a real player seat) into the lite build through its own Load game menu.
const fs = require('fs'), path = require('path');
const {snap, waitFor, click, open} = require('./lib');
async function loadSave(page, file) {
  const name = path.basename(file);
  const bytes = [...fs.readFileSync(file)];
  await page.evaluate(async ({name, bytes}) => {
    FS.writeFile('/home/web_user/.glob2/games/' + name, new Uint8Array(bytes));
    await new Promise(r => FS.syncfs(false, r));
  }, {name, bytes});
  let s = await snap(page);
  if (s.controls['intro/menu']) await click(page, 'intro/menu');
  await waitFor(page, s => String(s.screen).includes('MainMenu'));
  await click(page, 'menu/2');
  s = await waitFor(page, s => Object.keys(s.controls).some(k => k.startsWith('files/')));
  const row = Object.entries(s.controls).find(([k, v]) => k.startsWith('files/') && v.label.includes(name.replace('.game.gz', '')));
  if (!row) throw new Error('save not listed: ' + Object.entries(s.controls).filter(([k]) => k.startsWith('files/')).map(([k, v]) => v.label).join(','));
  await click(page, row[0]);
  await click(page, 'ok');
  await waitFor(page, s => s.tick > 0, 180000);
}
module.exports = {loadSave};
if (require.main === module) (async () => {
  const {browser, page} = await open({viewport: {width: 1280, height: 720}});
  console.log(await page.evaluate(() => Object.keys(glob2Diagnostics).join(',')));
  await loadSave(page, process.argv[2]);
  await page.waitForTimeout(3000);
  const s = await snap(page); console.log(s.screen, s.tick, s.hud ? JSON.stringify(s.hud).slice(0, 800) : '', Object.keys(s.controls).slice(0, 60).join(' '));
  await page.screenshot({path: process.argv[3]});
  await browser.close();
})();
