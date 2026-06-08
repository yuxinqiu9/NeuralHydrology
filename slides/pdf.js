const puppeteer = require('puppeteer-core');
const http = require('http');
const path = require('path');
const fs = require('fs');

const DEFAULT_CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const CHROME_PATH = process.env.CHROME_PATH || DEFAULT_CHROME_PATH;

function startServer(htmlDir) {
  const server = http.createServer((req, res) => {
    const filePath = path.join(htmlDir, req.url.split('?')[0]);
    try {
      const content = fs.readFileSync(filePath);
      const mime = {
        '.html': 'text/html', '.css': 'text/css',
        '.js': 'application/javascript', '.png': 'image/png',
        '.svg': 'image/svg+xml', '.jpg': 'image/jpeg',
      };
      res.writeHead(200, { 'Content-Type': mime[path.extname(filePath)] || 'text/plain' });
      res.end(content);
    } catch { res.writeHead(404); res.end(); }
  });
  return new Promise(r => server.listen(0, '127.0.0.1', () => r(server)));
}

(async () => {
  const outPath = path.resolve('output/slides.pdf');
  const htmlPath = path.resolve('output/slides.html');

  if (!fs.existsSync(htmlPath)) {
    console.error('ERROR: output/slides.html not found. Render HTML first with Quarto.');
    process.exit(1);
  }

  if (!fs.existsSync(CHROME_PATH)) {
    console.error(`ERROR: Chrome executable not found at: ${CHROME_PATH}`);
    console.error('Set CHROME_PATH to your Chrome executable path and retry.');
    process.exit(1);
  }

  if (fs.existsSync(outPath)) {
    try { fs.unlinkSync(outPath); } catch {
      console.error('ERROR: slides.pdf is open in another program. Close it and try again.');
      process.exit(1);
    }
  }

  const server = await startServer(path.resolve('output'));
  const port = server.address().port;

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    args: ['--no-sandbox'],
    headless: true,
  });

  try {
    const page = await browser.newPage();
    // Exact slide dimensions
    await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });

    // Load presentation normally (not print mode)
    await page.goto(`http://127.0.0.1:${port}/slides.html`, {
      waitUntil: 'networkidle0', timeout: 30000,
    });
    await page.waitForSelector('.reveal.ready', { timeout: 15000 });
    await new Promise(r => setTimeout(r, 1000));

    // Make all fragments visible and hide UI chrome + custom nav/footer overlays
    await page.evaluate(() => {
      const s = document.createElement('style');
      s.textContent = `
        .fragment { visibility: visible !important; opacity: 1 !important; }
        .controls, .progress, .slide-number,
        .slide-menu-button, button.slide-menu-button { display: none !important; }
      `;
      document.head.appendChild(s);
    });

    // Count top-level slides (horizontal)
    const slideCount = await page.evaluate(() =>
      document.querySelectorAll('.reveal .slides > section').length
    );
    console.log(`Capturing ${slideCount} slides...`);

    // Screenshot each slide
    const shots = [];
    for (let i = 0; i < slideCount; i++) {
      await page.evaluate((idx) => window.Reveal.slide(idx, 0), i);
      await new Promise(r => setTimeout(r, 400));
      const img = await page.screenshot({ type: 'png' });
      shots.push(img.toString('base64'));
      process.stdout.write(`\r  slide ${i + 1}/${slideCount}`);
    }
    console.log('\nBuilding PDF...');

    // Assemble a single HTML page with all slides, each on its own print page
    const html = `<!DOCTYPE html><html><head><style>
      @page { size: 1280px 720px; margin: 0; }
      body { margin: 0; padding: 0; }
      .s { position: relative; width: 1280px; height: 720px; page-break-after: always; overflow: hidden; }
      .s:last-child { page-break-after: avoid; }
      img { display: block; width: 1280px; height: 720px; }
      .pn {
        position: absolute; bottom: 18px; right: 24px;
        font-family: Arial, sans-serif; font-size: 18px;
        color: #555; background: rgba(255,255,255,0.6);
        padding: 2px 6px; border-radius: 3px;
      }
    </style></head><body>
      ${shots.map((b64, i) => `<div class="s">
        <img src="data:image/png;base64,${b64}">
        ${i > 0 ? `<div class="pn">${i + 1}</div>` : ''}
      </div>`).join('')}
    </body></html>`;

    await page.setContent(html, { waitUntil: 'load' });
    await page.pdf({
      path: outPath,
      width: '1280px',
      height: '720px',
      printBackground: true,
      preferCSSPageSize: true,
    });

    console.log('PDF saved: output/slides.pdf');
  } finally {
    await browser.close();
    server.close();
  }
})();
