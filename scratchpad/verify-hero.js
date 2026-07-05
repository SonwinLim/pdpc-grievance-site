// Verify the new hero hook section renders correctly
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  const errors = [];
  page.on('pageerror', (err) => errors.push('JS error: ' + err.message));
  page.on('requestfailed', (req) => errors.push('Request failed: ' + req.url() + ' — ' + req.failure().errorText));

  await page.goto('http://localhost:8099/index.html', { waitUntil: 'networkidle0', timeout: 30000 });

  // Check the hook section
  const hookInfo = await page.evaluate(() => {
    const hook = document.getElementById('hook');
    if (!hook) return { found: false };
    const img = hook.querySelector('.hook__diagram-img');
    const figcaption = hook.querySelector('.hook__diagram-caption');
    const eyebrow = hook.querySelector('.eyebrow');
    const h1 = hook.querySelector('h1');
    const iron = hook.querySelector('.hook__irony');
    const open = hook.querySelector('.hook__open');
    const btn = hook.querySelector('.btn');
    return {
      found: true,
      eyebrowText: eyebrow ? eyebrow.textContent.trim() : null,
      h1Text: h1 ? h1.textContent.trim().slice(0, 80) + '...' : null,
      h1Hidden: h1 ? getComputedStyle(h1).position === 'absolute' : null,
      imgSrc: img ? img.getAttribute('src') : null,
      imgNaturalWidth: img ? img.naturalWidth : null,
      imgNaturalHeight: img ? img.naturalHeight : null,
      imgRenderedWidth: img ? img.getBoundingClientRect().width : null,
      figcaptionText: figcaption ? figcaption.textContent.trim() : null,
      ironPresent: !!iron,
      openPresent: !!open,
      btnHref: btn ? btn.getAttribute('href') : null,
    };
  });

  // Take screenshots
  await page.screenshot({ path: 'scratchpad/hook-desktop.png', clip: await page.evaluate(() => {
    const r = document.getElementById('hook').getBoundingClientRect();
    return { x: 0, y: r.top, width: 1280, height: Math.min(r.height, 1200) };
  })});

  // Mobile screenshot
  await page.setViewport({ width: 390, height: 844 });
  await page.reload({ waitUntil: 'networkidle0' });
  await page.screenshot({ path: 'scratchpad/hook-mobile.png', clip: await page.evaluate(() => {
    const r = document.getElementById('hook').getBoundingClientRect();
    return { x: 0, y: r.top, width: 390, height: Math.min(r.height, 1600) };
  })});

  await browser.close();

  console.log('=== Hook section verification ===');
  console.log(JSON.stringify(hookInfo, null, 2));
  console.log('=== Errors ===');
  console.log(errors.length === 0 ? 'NONE' : errors.join('\n'));
})();