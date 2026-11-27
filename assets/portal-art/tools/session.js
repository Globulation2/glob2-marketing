// One lite session: clean profile, clouds off (Settings), load a seat save, bars off (key I).
const {snap, waitFor, click, open} = require('./lib');
const {loadSave} = require('./load');
async function session(save, viewport) {
  let {browser, page} = await open({viewport});
  await page.evaluate(async () => {
    let text = '';
    try { text = new TextDecoder().decode(FS.readFile('/home/web_user/.glob2/preferences.txt')); } catch (e) {}
    text = text.split('\n').filter(l => l && !/^(clouds|cloudShadows|graphicsDetailAdaptive)=/.test(l)).join('\n') + '\ngraphicsDetailAdaptive=0\nclouds=0\ncloudShadows=0\n';
    FS.writeFile('/home/web_user/.glob2/preferences.txt', text);
    await new Promise(r => FS.syncfs(false, r));
  });
  await page.reload();
  await waitFor(page, s => s.controls && Object.keys(s.controls).length > 0);
  await loadSave(page, save);
  await page.waitForTimeout(1500);
  await page.locator('#canvas').press('i');
  await page.waitForTimeout(300);
  return {browser, page};
}
// Minimap: the square at the top of the 200-px right panel.
async function minimap(page) {
  const s = await snap(page);
  const mm = Object.entries(s.controls).find(([k]) => /minimap/i.test(k));
  return mm ? mm[1] : null;
}
module.exports = {session, minimap};
