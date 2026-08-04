#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import readline from 'node:readline/promises';
import { buildPrompt } from './prompts.js';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(SCRIPT_DIR, '..', '..', '..', '..');
const PROFILE_DIR = path.join(PROJECT_ROOT, '.qwen-profile');
const STORAGE_FILE = path.join(PROFILE_DIR, 'storage-state.json');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'output');
const CHAT_URL = process.env.QWEN_CHAT_URL || 'https://chat.qwen.ai/';
const GEN_TIMEOUT = 10 * 60 * 1000; // 10 menit timeout
const DEFAULT_LOGO = path.join(PROJECT_ROOT, 'image.png');

let SELECTORS = {};
try {
  SELECTORS = JSON.parse(fs.readFileSync(path.join(SCRIPT_DIR, 'selectors.json'), 'utf8'));
} catch {
  console.warn('WARNING: selectors.json tidak ditemukan atau invalid, pakai default. Jalankan "detect" untuk regenerate.');
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

function askEnter(msg) {
  return rl.question(msg + '\nPress Enter to continue... ');
}

function pad(s, n) {
  return String(s).padEnd(n);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function findFirst(page, locatorList) {
  for (const sel of locatorList || []) {
    const loc = page.locator(sel);
    if ((await loc.count()) > 0) return loc;
  }
  return null;
}

function isChallengeText(text) {
  return /captcha|challenge|verify|verification|安全验证|验证码|滑块|human/i.test(text);
}

async function waitLoggedIn(page) {
  console.log('Menunggu login... kalau ada jendela verifikasi/captcha, selesaikan manual di browser.');
  const deadline = Date.now() + 10 * 60 * 1000;
  while (Date.now() < deadline) {
    const body = (await page.locator('body').innerText().catch(() => '')) || '';
    if (isChallengeText(body)) {
      console.log('>>> Terdeteksi challenge (captcha/verifikasi). Selesaikan manual di browser, lalu tunggu otomatis.');
    }
    const input = await findFirst(page, SELECTORS.chatInput);
    if (input && (await input.count()) > 0) {
      const editable = await input.isEditable().catch(() => false);
      if (editable) {
        console.log('Chat input terdeteksi — sudah login.');
        return true;
      }
    }
    await sleep(3000);
  }
  throw new Error('Timeout menunggu login (10 menit). Cek browser dan ulangi.');
}

async function openBrowser({ headless = false, loadState = true } = {}) {
  // Use regular launch() with temp profile to avoid persistent context hangs
  const tempProfile = path.join(PROFILE_DIR, `temp-${Date.now()}`);
  fs.mkdirSync(tempProfile, { recursive: true });
  const browser = await chromium.launch({
    headless,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: undefined,
  });

  // Load saved cookies if available
  if (loadState && fs.existsSync(STORAGE_FILE)) {
    try {
      const state = JSON.parse(fs.readFileSync(STORAGE_FILE, 'utf8'));
      if (state.cookies && state.cookies.length > 0) {
        await context.addCookies(state.cookies);
        console.log('Loaded saved session from', STORAGE_FILE);
      }
    } catch (e) {
      console.log('Failed to load storage state:', e.message);
    }
  }

  const page = await context.newPage();
  return { context, page, browser };
}

async function cmdLogin({ headless }) {
  const { context, page, browser } = await openBrowser({ headless, loadState: false });
  console.log('Buka', CHAT_URL, '— login manual di jendela browser.');
  await page.goto(CHAT_URL, { waitUntil: 'domcontentloaded' });
  await waitLoggedIn(page);
  fs.mkdirSync(path.dirname(STORAGE_FILE), { recursive: true });
  await context.storageState({ path: STORAGE_FILE });
  console.log('Login tersimpan ke', STORAGE_FILE);
  await context.close();
  await browser.close();
  process.exit(0);
}

async function cmdDetect({ headless, url }) {
  const { context, page } = await openBrowser({ headless });
  const target = url || CHAT_URL;
  console.log('Buka', target);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch((e) => console.warn('goto warn:', e.message));
  await page.waitForTimeout(8000);
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const shot = path.join(OUTPUT_DIR, 'debug-screenshot.png');
  await page.screenshot({ path: shot, fullPage: false }).catch(() => {});
  console.log('Screenshot: ' + shot);
  console.log('\nURL:', page.url());
  console.log('TITLE:', await page.title().catch(() => ''));
  console.log('\n=== VISIBLE BUTTONS ===');
  const buttons = await page.getByRole('button').all();
  const seen = new Set();
  for (const b of buttons.slice(0, 80)) {
    const text = (await b.innerText().catch(() => '')).trim().replace(/\s+/g, ' ').slice(0, 60);
    const aria = (await b.getAttribute('aria-label').catch(() => null)) || '';
    const t = text || aria;
    if (!t || seen.has(t)) continue;
    seen.add(t);
    console.log('button ' + pad(`text="${t}"`, 66) + pad('aria="' + aria + '"', 40) + 'title=' + ((await b.getAttribute('title').catch(() => null)) || ''));
  }
  console.log('\n=== INPUTS ===');
  const inputs = await page.locator('textarea, [contenteditable="true"], input[type="text"]').all();
  for (const i of inputs.slice(0, 20)) {
    const ph = (await i.getAttribute('placeholder').catch(() => null)) || '';
    const aria = (await i.getAttribute('aria-label').catch(() => null)) || '';
    console.log(pad('placeholder="' + ph + '"', 50) + 'aria="' + aria + '"');
  }
  console.log('\n=== VISIBLE IMAGES (terakhir 5) ===');
  const imgs = await page.locator('img').all();
  for (const img of imgs.slice(-5)) {
    const src = ((await img.getAttribute('src').catch(() => '')) || '').slice(0, 120);
    const w = await img.evaluate((el) => `${el.naturalWidth}x${el.naturalHeight}`).catch(() => '?');
    console.log(pad('src=' + src, 130) + 'size=' + w);
  }
  await context.close();
  process.exit(0);
}

async function clickDropdownOption(page, optionSelectors, label) {
  const opt = await findFirst(page, optionSelectors);
  if (!opt || (await opt.count()) === 0) {
    console.log(`FAIL: opsi "${label}" tidak ditemukan di dropdown. UI berubah? Jalankan "detect".`);
    return false;
  }
  const vis = opt.filter({ visible: true });
  if ((await vis.count()) === 0) {
    console.log(`FAIL: opsi "${label}" ada tapi tidak terlihat. UI berubah? Jalankan "detect".`);
    return false;
  }
  await vis.first().click();
  await page.waitForTimeout(800);
  return true;
}

async function enterImageMode(page) {
  // First close any "Choose a style" overlay if present
  await page.locator('button:has-text("Close")').first().click().catch(() => {});
  await page.waitForTimeout(500);

  // Check if "Create Image" is directly visible AS A BUTTON in the main UI
  // (not hidden inside overlay text)
  const createImageVisible = await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('button, [role="button"], a, div[onclick]'));
    for (const el of els) {
      if ((el.innerText || '').trim() === 'Create Image' && el.offsetParent !== null) {
        return true;
      }
    }
    return false;
  }).catch(() => false);

  if (createImageVisible) {
    // New UI: "Create Image" is directly visible as a clickable element
    console.log('New UI: "Create Image" button visible, clicking it...');
    await page.locator('button:has-text("Create Image"), [role="button"]:has-text("Create Image")').first().click();
    await page.waitForTimeout(1500);
  } else {
    // Old UI: click "Select Mode" dropdown and select "Create Image"
    const mode = await findFirst(page, SELECTORS.modeButton);
    if (!mode || (await mode.count()) === 0) {
      console.log('FAIL: tombol mode tidak ditemukan. UI berubah? Jalankan "detect" lalu update selectors.json.');
      return false;
    }
    await mode.first().click();
    await page.waitForTimeout(1500);
    if (!(await clickDropdownOption(page, SELECTORS.menuCreateImage, 'Create Image'))) return false;
  }

  // Select Qwen-Image 2.0 model (current default)
  const modelBtn = await findFirst(page, SELECTORS.imageModelButton);
  if (modelBtn && (await modelBtn.count()) > 0) {
    await modelBtn.first().click();
    await page.waitForTimeout(1000);
    if (!(await clickDropdownOption(page, SELECTORS.imageModelOption, 'Qwen-Image 2.0'))) {
      const currentModel = await page.evaluate(() => {
        return document.querySelector('[class*="model"] span')?.innerText || '';
      });
      console.log('Current model:', currentModel);
    }
  }

  // Select 1:1 aspect ratio
  const sizeBtn = await findFirst(page, SELECTORS.sizeSelector);
  if (sizeBtn && (await sizeBtn.count()) > 0) {
    await sizeBtn.first().click();
    await page.waitForTimeout(1000);
    if (!(await clickDropdownOption(page, SELECTORS.sizeOption1to1, '1:1'))) {
      const currentSize = await page.evaluate(() => {
        return document.querySelector('[class*="size"] span')?.innerText || '';
      });
      console.log('Current size:', currentSize);
    }
  }

  console.log('Mode Create Image aktif.');
  return true;
}

async function sendPrompt(page, prompt) {
  const input = await findFirst(page, SELECTORS.chatInput);
  if (!input || (await input.count()) === 0) throw new Error('Chat input tidak ditemukan.');
  await input.first().click();
  await input.first().fill(prompt);
  await page.waitForTimeout(500);
  const send = await findFirst(page, SELECTORS.sendButton);
  if (send && (await send.count()) > 0) {
    await send.filter({ visible: true }).first().click();
  } else {
    await input.first().press('Enter');
  }
}

async function ensureLoggedIn(page, browser) {
  // Check if user is logged in by looking for the "Log in" button
  const loginBtn = await page.locator('button:has-text("Log in"), button:has-text("Sign in")').first();
  if (loginBtn && (await loginBtn.count()) > 0 && await loginBtn.isVisible()) {
    console.log('Belum login. Membuka browser untuk login manual...');
    await browser.close();

    // Open headed browser for manual login
    const { context: loginCtx, page: loginPage, browser: loginBrowser } = await openBrowser({ headless: false });
    await loginPage.goto(CHAT_URL, { waitUntil: 'domcontentloaded' });

    console.log('Silakan login di browser. Menunggu...');
    await sleep(3000);

    // Wait for login to complete
    const deadline = Date.now() + 10 * 60 * 1000;
    while (Date.now() < deadline) {
      const lbtn = await loginPage.locator('button:has-text("Log in")').first();
      const btnCount = await lbtn.count().catch(() => 0);
      if (btnCount === 0 || !await lbtn.isVisible().catch(() => false)) {
        console.log('Login berhasil!');
        break;
      }
      await sleep(3000);
    }

    // Save session
    fs.mkdirSync(path.dirname(STORAGE_FILE), { recursive: true });
    await loginCtx.storageState({ path: STORAGE_FILE });
    console.log('Session tersimpan ke', STORAGE_FILE);
    await loginCtx.close();
    await loginBrowser.close();

    // Return a signal that login was needed (caller will re-open)
    return { needsReopen: true };
  }
  return { needsReopen: false };
}

async function uploadAttachment(page, filePath) {
  // Mode dropdown harus dibuka dulu untuk mencari opsi Upload attachment
  const mode = await findFirst(page, SELECTORS.modeButton);
  if (!mode || (await mode.count()) === 0) {
    console.log('FAIL: tombol mode tidak ditemukan. UI berubah? Jalankan "detect".');
    return false;
  }
  await mode.first().click();
  await page.waitForTimeout(800);

  const uploadOpt = await findFirst(page, SELECTORS.uploadAttachment);
  if (!uploadOpt || (await uploadOpt.count()) === 0) {
    console.log('FAIL: opsi "Upload attachment" tidak ditemukan di dropdown. UI berubah? Jalankan "detect".');
    await page.keyboard.press('Escape').catch(() => {});
    return false;
  }
  await uploadOpt.first().click();
  await page.waitForTimeout(800);

  const fileInput = await findFirst(page, SELECTORS.fileInput);
  if (fileInput && (await fileInput.count()) > 0) {
    try {
      await fileInput.first().setInputFiles(filePath);
      await page.waitForTimeout(1500);
      console.log('Logo berhasil diupload (setInputFiles):', filePath);
      return true;
    } catch (e) {
      console.log('setInputFiles gagal, coba fileChooser:', e.message);
    }
  }

  try {
    const [chooser] = await Promise.all([
      page.waitForEvent('filechooser', { timeout: 5000 }),
      mode.first().click(),
    ]);
    await chooser.setFiles(filePath);
    await page.waitForTimeout(1500);
    console.log('Logo berhasil diupload (fileChooser):', filePath);
    return true;
  } catch (e) {
    console.log('Upload gagal:', e.message);
    return false;
  }
}

async function waitForImageComplete(page) {
  console.log('Menunggu gambar selesai digenerate (max 10 menit)...');
  const deadline = Date.now() + GEN_TIMEOUT;

  // Capture the attachment src (the logo preview) - this should be excluded
  const attachmentSrc = await page.evaluate(() => {
    const allImgs = document.querySelectorAll('img');
    for (const img of allImgs) {
      if (img.alt?.includes('image.png') || img.className.includes('vision-item')) {
        return img.getAttribute('src') || '';
      }
    }
    return '';
  }).catch(() => '');
  console.log(`Attachment src: ${attachmentSrc.slice(0, 60)}`);

  // Capture initial set of qwen-image srcs (these are pre-existing before generation)
  const initialSrcs = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img.ant-image-img.qwen-image'))
      .map(img => img.getAttribute('src') || '')
      .filter(s => s.length > 0);
  }).catch(() => []);
  console.log(`Initial qwen-image srcs: ${initialSrcs.length}`);

  // Combine - we'll exclude both the attachment and any pre-existing qwen images
  const excludeSrcs = [...initialSrcs, attachmentSrc].filter(Boolean);
  console.log(`Exclusion list: ${excludeSrcs.length} srcs`);

  // Just poll for new images with cdn.qwenlm.ai (generated) src
  // Skeleton check is unreliable - skip it and just wait for new image
  const startTime = Date.now();

  while (Date.now() - startTime < GEN_TIMEOUT) {
    await sleep(2000);

    const result = await page.evaluate((excludeList) => {
      const skel = document.querySelectorAll('.qwen-media-skeleton').length;

      // Find ANY image with cdn.qwenlm.ai (these are generated, not attachments)
      const generatedImgs = Array.from(document.querySelectorAll('img')).filter(img => {
        const src = img.getAttribute('src') || '';
        return src.includes('cdn.qwenlm.ai');
      });

      const newImgDetails = generatedImgs.map(img => ({
        src: img.getAttribute('src') || '',
        w: img.naturalWidth || img.offsetWidth || 0,
        h: img.naturalHeight || img.offsetHeight || 0,
      })).filter(d => d.w > 100 && d.h > 100);

      return { skel, generatedImgs: newImgDetails.length, newImgDetails };
    }, excludeSrcs);

    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    console.log(`  [${elapsed}s] skel=${result.skel} generatedImgs=${result.generatedImgs}`);

    if (result.newImgDetails.length > 0) {
      const best = result.newImgDetails[result.newImgDetails.length - 1];
      await sleep(3000);
      console.log(`✓ Gambar selesai digenerate: ${best.w}x${best.h} src=${best.src.slice(0, 60)}`);
      return { img: best, src: best.src, size: `${best.w}x${best.h}` };
    }
  }

  throw new Error('Timeout menunggu gambar (10 menit).');
}

async function downloadImage(page, candidate, outPath) {
  const { img, src } = candidate;
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  // Try Playwright's expect-style locator click using the src URL
  // The `img` object we get is plain metadata from page.evaluate, not a Locator
  // So we click by locator with selector matching src
  console.log('Klik image hasil generate untuk buka preview...');
  try {
    // Build a selector that finds the img with this exact src
    const escapedSrc = src.replace(/'/g, "\\'");
    const imgLocator = page.locator(`img[src*="${escapedSrc.slice(-60)}"]`).first();
    await imgLocator.click({ timeout: 10000 });
    await page.waitForTimeout(1500);

    // Tunggu preview root muncul
    const preview = await findFirst(page, SELECTORS.imagePreviewRoot);
    if (preview && (await preview.count()) > 0) {
      console.log('Preview terbuka.');

      // Step 2: klik tombol Download di dalam preview
      const downloadBtn = await findFirst(page, SELECTORS.downloadButton);
      if (downloadBtn && (await downloadBtn.count()) > 0) {
        console.log('Klik tombol Download di preview...');
        const [download] = await Promise.all([
          page.waitForEvent('download', { timeout: 60000 }),
          downloadBtn.first().click(),
        ]);
        await download.saveAs(outPath);
        console.log('Tersimpan via download event:', outPath);
        return;
      }
    } else {
      console.log('Preview tidak muncul setelah klik image.');
    }
  } catch (e) {
    console.log('Klik image / preview gagal:', e.message);
  }

  // Fallback: fetch via evaluate (works for http/https blob URLs)
  try {
    console.log('Fallback: fetch src langsung...');
    const b64 = await page.evaluate(async (s) => {
      const r = await fetch(s);
      if (!r.ok) throw new Error('fetch ' + r.status);
      const buf = await r.arrayBuffer();
      const bytes = new Uint8Array(buf);
      let bin = '';
      const CH = 0x8000;
      for (let i = 0; i < bytes.length; i += CH) {
        bin += String.fromCharCode.apply(null, bytes.subarray(i, i + CH));
      }
      return btoa(bin);
    }, src);
    fs.writeFileSync(outPath, Buffer.from(b64, 'base64'));
    console.log('Tersimpan via fetch:', outPath);
    return;
  } catch (e) {
    console.log('Fetch gagal:', e.message);
  }

  // Last resort: element screenshot
  try {
    const escapedSrc = src.replace(/'/g, "\\'");
    const imgLocator = page.locator(`img[src*="${escapedSrc.slice(-60)}"]`).first();
    await imgLocator.screenshot({ path: outPath });
    console.log('Screenshot tersimpan (last resort):', outPath);
  } catch (e) {
    console.log('Element screenshot gagal:', e.message);
  }
}

async function cmdGenerate(opts) {
  const { context, page, browser } = await openBrowser({ headless: opts.headless });
  const prompt = opts.prompt || buildPrompt({ ...opts, promptOverride: opts.prompt });
  console.log('=== PROMPT KE QWEN ===\n' + prompt + '\n====================');

  await page.goto(CHAT_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });

  // Check login - if not logged in, save session and exit for user to retry
  try {
    const loginBtn = await page.locator('button:has-text("Log in")').first();
    const loginVisible = await loginBtn.isVisible().catch(() => false);
    if (loginVisible) {
      console.log('Not logged in. Please login first by running:');
      console.log('  node scripts/login-manual.mjs');
      await browser.close();
      process.exit(0);
    }
  } catch (e) {
    // Ignore errors, assume logged in
  }
  
  // Enter image mode
  const ok = await enterImageMode(page);
  if (!ok) {
    console.log('Gagal masuk mode Create Image. Jalankan "detect" untuk debug.');
    await cmdDetect({ headless: true });
    process.exit(2);
  }

  // Upload Venturo logo - skip if --no-logo, use default logo otherwise
  if (opts.logo === null) {
    console.log('Lewati upload logo (--no-logo)');
  } else if (opts.logo) {
    console.log('Upload logo:', path.resolve(opts.logo));
    const uploaded = await uploadAttachment(page, path.resolve(opts.logo));
    if (!uploaded) {
      console.log('Upload logo gagal, lanjut tanpa logo');
    }
  } else if (fs.existsSync(DEFAULT_LOGO)) {
    console.log('Upload logo (default Venturo):', DEFAULT_LOGO);
    const uploaded = await uploadAttachment(page, DEFAULT_LOGO);
    if (!uploaded) {
      console.log('Upload logo gagal, lanjut tanpa logo');
    }
  } else {
    console.log('Lewati upload logo (file tidak ditemukan):', DEFAULT_LOGO);
  }

  // Build prompt with explicit instruction about the uploaded image
  const fullPrompt = prompt + '\n\n[Gunakan logo Venturo yang sudah di-upload sebagai referensi visual pojok kiri atas. Generate poster BARU yang kreatif dengan headline dan CTA, bukan hanya tampilkan logo.]';
  await sendPrompt(page, fullPrompt);
  console.log('Prompt terkirim. Menunggu gambar selesai digenerate...');

  // WAIT for image to complete
  const found = await waitForImageComplete(page);

  // Save image
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const ts = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14);
  const outPath = opts.out ? path.resolve(opts.out) : path.join(OUTPUT_DIR, `qwen-poster-${ts}.png`);
  
  await downloadImage(page, found, outPath);
  const size = found.size;
  console.log(`DONE: ${outPath} (${size}, ${fs.statSync(outPath).size} bytes)`);
  
  // Close browser after successful save
  await context.close();
  process.exit(0);
}

const RECORD_INIT = () => {
  if (window.__qrec) return;
  window.__qrec = { buf: [], active: localStorage.getItem('__qrec_active') === '1' };
  document.addEventListener(
    'click',
    (e) => {
      if (!window.__qrec.active) return;
      const chain = [];
      let el = e.target;
      for (let i = 0; i < 5 && el && el !== document.documentElement; i++) {
        const t = el.tagName || '';
        if (!t) break;
        const r = el.getBoundingClientRect();
        chain.push({
          tag: t.toLowerCase(),
          text: ((el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60)),
          aria: el.getAttribute('aria-label') || '',
          title: el.getAttribute('title') || '',
          role: el.getAttribute('role') || '',
          type: el.getAttribute('type') || '',
          placeholder: el.getAttribute('placeholder') || '',
          checked: el.checked || '',
          class: (el.className || '').toString().slice(0, 80),
          box: `${Math.round(r.width)}x${Math.round(r.height)}`,
        });
        el = el.parentElement;
      }
      window.__qrec.buf.push({ t: Date.now(), url: location.href, chain });
    },
    true
  );
};

async function cmdRecord() {
  const { context, page } = await openBrowser({ headless: false });
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const logFile = path.join(OUTPUT_DIR, 'click-record.jsonl');
  fs.writeFileSync(logFile, '');
  await context.addInitScript(RECORD_INIT);
  console.log('Buka', CHAT_URL, '— login manual di jendela browser. Rekaman DIKUNCI sampai login terdeteksi.');
  await page.goto(CHAT_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await waitLoggedIn(page);
  await page.evaluate(() => {
    localStorage.setItem('__qrec_active', '1');
    window.__qrec.active = true;
  });
  console.log('>>> LOGIN DETEKSI. REKAMAN DIMULAI. Tulis klik ke: ' + logFile);
  console.log('>>> Lakukan flow: + → Create image → Qwen-Image 3.0 → 1:1. Tekan Ctrl+C saat selesai.');
  const w = fs.createWriteStream(logFile, { flags: 'a' });
  let emptyStreak = 0;
  while (true) {
    const items = await page.evaluate(() => {
      const b = window.__qrec.buf;
      window.__qrec.buf = [];
      return b;
    }).catch(() => []);
    for (const it of items) {
      w.write(JSON.stringify(it) + '\n');
      console.log('CLICK ' + JSON.stringify(it).slice(0, 220));
      emptyStreak = 0;
    }
    if (items.length === 0) emptyStreak++;
    if (emptyStreak > 600) break;
    await sleep(1000);
  }
  w.end();
  console.log('Rekaman selesai: ' + logFile);
  await context.close();
  process.exit(0);
}

function parseArgs(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--headless') opts.headless = true;
    else if (a === '--out') opts.out = argv[++i];
    else if (a === '--prompt') opts.prompt = argv[++i];
    else if (a === '--title') opts.title = argv[++i];
    else if (a === '--subtitle') opts.subtitle = argv[++i];
    else if (a === '--event') opts.event = argv[++i];
    else if (a === '--date') opts.date = argv[++i];
    else if (a === '--price-from') opts.priceFrom = argv[++i];
    else if (a === '--price-to') opts.priceTo = argv[++i];
    else if (a === '--cta') opts.cta = argv[++i];
    else if (a === '--font') opts.font = argv[++i];
    else if (a === '--accent-color') opts.accentColor = argv[++i];
    else if (a === '--style') opts.style = argv[++i];
    else if (a === '--aspect-ratio') opts.aspectRatio = argv[++i];
    else if (a === '--logo') opts.logo = argv[++i];
    else if (a === '--no-logo') opts.logo = null;
  }
  return opts;
}

const [cmd, ...rest] = process.argv.slice(2);
const opts = parseArgs(rest);

if (cmd === 'login') {
  await cmdLogin(opts);
} else if (cmd === 'detect') {
  await cmdDetect(opts);
} else if (cmd === 'record') {
  await cmdRecord();
} else if (cmd === 'generate') {
  await cmdGenerate(opts);
} else {
  console.log(`
qwen-poster — otomasi chat.qwen.ai untuk generate poster promosi (Playwright)

USAGE:
  node qwen-poster.mjs login               Login manual sekali (storage state tersimpan)
  node qwen-poster.mjs detect              Dump UI: button/input/image yang terlihat (debug selector)
  node qwen-poster.mjs record              Rekam klik user SETELAH login (untuk update selector)
  node qwen-poster.mjs generate [flags]    Generate poster via Qwen-Image

GENERATE FLAGS:
  --title "..."      Judul utama poster (wajib)
  --subtitle "..."   Subjudul
  --event "..."      Nama event/produk
  --date "..."       Tanggal acara
  --venue "..."      Lokasi/venue
  --cta "..."        Call to action
  --style "..."      Gaya visual (warna, mood, font)
  --ratio 1:1        Rasio (default 1:1)
  --prompt "..."     Prompt bebas (override template)
  --out path.png     Lokasi output (default: output/qwen-poster-<ts>.png)
  --headless         Jalan tanpa jendela browser (anti-bot lebih mudah kena)

CATATAN:
  - Script akan MENUNGGU hingga gambar selesai digenerate sebelum download.
  - Kalau UI chat.qwen.ai berubah: jalankan "detect", update selectors.json, ulangi.
  - Captcha/challenge: selesaikan manual di jendela browser, script menunggu otomatis.
  - Hanya jalankan SATU instance sekaligus (profile browser dipakai bersama).
`);
  process.exit(1);
}
