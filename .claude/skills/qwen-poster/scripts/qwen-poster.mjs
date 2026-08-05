#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildPrompt } from './prompts.js';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(SCRIPT_DIR, '..', '..', '..', '..');
const PROFILE_DIR = path.join(PROJECT_ROOT, '.qwen-profile');
const STORAGE_FILE = path.join(PROFILE_DIR, 'storage-state.json');
const OUTPUT_DIR = path.join(PROJECT_ROOT, 'output');
const CHAT_URL = process.env.QWEN_CHAT_URL || 'https://chat.qwen.ai/';
const GEN_TIMEOUT = 10 * 60 * 1000;
const DEFAULT_LOGO = path.join(PROJECT_ROOT, 'image.png');
const CONFIG_FILE = path.join(SCRIPT_DIR, '..', 'config.json');

let SELECTORS = {};
try {
  SELECTORS = JSON.parse(fs.readFileSync(path.join(SCRIPT_DIR, 'selectors.json'), 'utf8'));
} catch {
  console.warn('WARNING: selectors.json tidak ditemukan atau invalid.');
}

function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  } catch {
    return {};
  }
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

async function openBrowser({ headless = false } = {}) {
  const browser = await chromium.launchPersistentContext(PROFILE_DIR, {
    headless,
    channel: 'chrome',
    viewport: { width: 1440, height: 900 },
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = browser.pages()[0] || await browser.newPage();
  console.log('Browser launched with persistent profile:', PROFILE_DIR);

  return { context: browser, page, browser };
}

async function autoLogin(page, browser, context) {
  const config = loadConfig();
  if (!config.email || !config.password) {
    throw new Error('Auto-login gagal: email/password belum diset di config.json');
  }

  console.log('Attempting auto-login dengan cred dari config...');

  // Click "Log in" button
  const loginBtn = await page.locator('button:has-text("Log in")').first();
  if (await loginBtn.count() === 0 || !await loginBtn.isVisible()) {
    console.log('Tidak ada tombol "Log in", mungkin sudah login.');
    return true;
  }

  await loginBtn.click();
  await sleep(2000);

  // Look for email input
  const emailInput = await page.locator('input[type="email"], input[placeholder*="email"], input[name="email"]').first();
  if (await emailInput.count() === 0) {
    // Try clicking "Sign in with email" or similar
    const emailSignIn = await page.locator('button:has-text("Email"), [class*="email"] button').first();
    if (await emailSignIn.count() > 0) {
      await emailSignIn.click();
      await sleep(1500);
    }
  }

  // Fill email
  await page.locator('input[type="email"], input[placeholder*="email"], input[name="email"]').first().fill(config.email);
  await sleep(1000);

  // Click Continue / Next
  const continueBtn = await page.locator('button:has-text("Continue"), button:has-text("Next")').first();
  if (await continueBtn.count() > 0) {
    await continueBtn.click();
    await sleep(2000);
  }

  // Fill password
  const passwordInput = await page.locator('input[type="password"]').first();
  if (await passwordInput.count() === 0) {
    throw new Error('Password input tidak ditemukan setelah email');
  }
  await passwordInput.fill(config.password);
  await sleep(1000);

  // Click Sign in / Log in
  const signInBtn = await page.locator('button:has-text("Sign in"), button:has-text("Log in")').first();
  await signInBtn.click();

  console.log('Credentials submitted. Menunggu login...');

  // Wait for login to complete (chat input becomes editable)
  const deadline = Date.now() + 5 * 60 * 1000;
  while (Date.now() < deadline) {
    await sleep(3000);

    const body = (await page.locator('body').innerText().catch(() => '')) || '';
    if (isChallengeText(body)) {
      console.log('>>> Terdeteksi challenge (captcha/verifikasi). Selesaikan manual.');
    }

    const input = await findFirst(page, SELECTORS.chatInput);
    if (input && (await input.count()) > 0) {
      const editable = await input.isEditable().catch(() => false);
      if (editable) {
        console.log('✓ Login berhasil!');
        await sleep(2000); // Wait for session to be saved
        return true;
      }
    }
  }

  throw new Error('Auto-login timeout (5 menit). Cek browser untuk challenge manual.');
}

async function ensureLoggedIn(page, browser, context) {
  console.log('Cek status login...');
  await page.goto(CHAT_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await sleep(3000);

  // Check if already logged in
  const loginBtn = await page.locator('button:has-text("Log in"), button:has-text("Sign in")').first();
  const hasLoginBtn = await loginBtn.count() > 0 && await loginBtn.isVisible().catch(() => false);

  if (!hasLoginBtn) {
    console.log('✓ Sudah login.');
    return true;
  }

  console.log('Belum login. Auto-login dengan cred dari config...');
  return await autoLogin(page, browser, context);
}

async function clickDropdownOption(page, optionSelectors, label) {
  const opt = await findFirst(page, optionSelectors);
  if (!opt || (await opt.count()) === 0) {
    console.log(`FAIL: opsi "${label}" tidak ditemukan di dropdown.`);
    return false;
  }
  const vis = opt.filter({ visible: true });
  if ((await vis.count()) === 0) {
    console.log(`FAIL: opsi "${label}" ada tapi tidak terlihat.`);
    return false;
  }
  await vis.first().click();
  await page.waitForTimeout(800);
  return true;
}

async function enterImageMode(page) {
  // Close any overlay
  await page.locator('button:has-text("Close")').first().click().catch(() => {});
  await page.waitForTimeout(500);

  // Click mode dropdown
  const mode = await findFirst(page, SELECTORS.modeButton);
  if (!mode || (await mode.count()) === 0) {
    console.log('FAIL: tombol mode tidak ditemukan.');
    return false;
  }
  await mode.first().click();
  await page.waitForTimeout(1500);

  // Click "Create Image"
  if (!(await clickDropdownOption(page, SELECTORS.menuCreateImage, 'Create Image'))) {
    return false;
  }

  await page.waitForTimeout(2000);

  // Select Qwen-Image 3.0 (fallback to 2.0)
  const modelSelector = await page.locator('[class*="image-model-selector-button"]').first();
  if (await modelSelector.count() > 0 && await modelSelector.isVisible()) {
    await modelSelector.click();
    await page.waitForTimeout(1000);

    const has30 = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('[class*="menu-item"]'))
        .some(el => el.offsetParent !== null && el.innerText.includes('3.0'));
    });
    if (has30) {
      await page.locator('[class*="menu-item"]:has-text("3.0")').first().click().catch(() => {});
    } else {
      await page.locator('[class*="menu-item"]:has-text("2.0")').first().click().catch(() => {});
    }
    await page.waitForTimeout(1000);
  }

  // Select 1:1 aspect ratio
  const sizeSelector = await page.locator('[class*="size-selector"]').first();
  if (await sizeSelector.count() > 0 && await sizeSelector.isVisible()) {
    await sizeSelector.click();
    await page.waitForTimeout(1500);

    const has1to1 = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('[class*="menu-item"]'))
        .some(el => el.offsetParent !== null && el.innerText.includes('1:1'));
    });
    if (has1to1) {
      await page.locator('[class*="menu-item"]:has-text("1:1")').first().click().catch(() => {});
    }
    await page.waitForTimeout(1000);
  }

  await page.waitForTimeout(1000);
  console.log('✓ Mode Create Image aktif.');
  return true;
}

async function uploadLogo(page, logoPath) {
  if (!logoPath || !fs.existsSync(logoPath)) {
    console.log('Lewati upload logo (file tidak ada):', logoPath);
    return false;
  }

  console.log('Upload logo:', logoPath);

  // Click mode dropdown
  const mode = await page.locator('[aria-label="Select Mode"]').first();
  await mode.click().catch(() => {});
  await page.waitForTimeout(1000);

  // Click "Upload attachment"
  const uploadOpt = await page.locator('[role="menuitem"]:has-text("Upload attachment")').first();
  if (await uploadOpt.count() === 0) {
    console.log('Upload attachment option tidak ditemukan.');
    await page.keyboard.press('Escape').catch(() => {});
    return false;
  }

  await uploadOpt.click();
  await page.waitForTimeout(1500);

  // Upload via file input
  const fileInput = await page.locator('input[type="file"]#filesUpload').first();
  if (await fileInput.count() === 0) {
    console.log('File input tidak ditemukan.');
    return false;
  }

  try {
    await fileInput.setInputFiles(logoPath);
    await page.waitForTimeout(2000);
    console.log('✓ Logo berhasil diupload.');
    return true;
  } catch (e) {
    console.log('Upload gagal:', e.message);
    return false;
  }
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

async function waitForImageComplete(page) {
  console.log('Menunggu gambar selesai digenerate (max 10 menit)...');
  const deadline = Date.now() + GEN_TIMEOUT;
  const startTime = Date.now();

  while (Date.now() - startTime < GEN_TIMEOUT) {
    await sleep(2000);

    const result = await page.evaluate(() => {
      const skel = document.querySelectorAll('.qwen-media-skeleton').length;

      const generatedImgs = Array.from(document.querySelectorAll('img')).filter(img => {
        const src = img.getAttribute('src') || '';
        return src.includes('cdn.qwenlm.ai');
      });

      const newImgDetails = generatedImgs.map(img => ({
        src: img.getAttribute('src') || '',
        w: img.naturalWidth || img.offsetWidth || 0,
        h: img.naturalHeight || img.offsetHeight || 0,
      })).filter(d => d.w > 100 && d.h > 100);

      const errorMessages = Array.from(document.querySelectorAll('[class*="error"], [class*="message-notice"], [class*="toast"]'))
        .map(el => (el.innerText || '').trim())
        .filter(t => t.length > 10 && t.length < 200);

      return { skel, generatedImgs: newImgDetails.length, newImgDetails, errorMessages };
    });

    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    console.log(`  [${elapsed}s] skel=${result.skel} generatedImgs=${result.generatedImgs}`);

    const limitError = result.errorMessages.find(m =>
      /daily usage limit|rate limit|quota|too many requests|please wait/i.test(m)
    );
    if (limitError) {
      throw new Error(`Qwen API limit reached: ${limitError}`);
    }

    if (result.newImgDetails.length > 0) {
      const best = result.newImgDetails[result.newImgDetails.length - 1];
      await sleep(3000);
      console.log(`✓ Gambar selesai: ${best.w}x${best.h}`);
      return { img: best, src: best.src, size: `${best.w}x${best.h}` };
    }
  }

  throw new Error('Timeout menunggu gambar (10 menit).');
}

async function downloadImage(page, candidate, outPath) {
  const { img, src } = candidate;
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  console.log('Klik image untuk buka preview...');
  try {
    const escapedSrc = src.replace(/'/g, "\\'");
    const imgLocator = page.locator(`img[src*="${escapedSrc.slice(-60)}"]`).first();
    await imgLocator.click({ timeout: 10000 });
    await page.waitForTimeout(1500);

    const preview = await findFirst(page, SELECTORS.imagePreviewRoot);
    if (preview && (await preview.count()) > 0) {
      const downloadBtn = await findFirst(page, SELECTORS.downloadButton);
      if (downloadBtn && (await downloadBtn.count()) > 0) {
        const [download] = await Promise.all([
          page.waitForEvent('download', { timeout: 60000 }),
          downloadBtn.first().click(),
        ]);
        await download.saveAs(outPath);
        console.log('Tersimpan via download event:', outPath);
        return;
      }
    }
  } catch (e) {
    console.log('Klik image / preview gagal:', e.message);
  }

  // Fallback: fetch
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

  // Last resort
  try {
    const escapedSrc = src.replace(/'/g, "\\'");
    const imgLocator = page.locator(`img[src*="${escapedSrc.slice(-60)}"]`).first();
    await imgLocator.screenshot({ path: outPath });
    console.log('Screenshot tersimpan:', outPath);
  } catch (e) {
    console.log('Element screenshot gagal:', e.message);
  }
}

async function cmdDetect({ headless, url }) {
  const { context, page } = await openBrowser({ headless });
  const target = url || CHAT_URL;
  console.log('Buka', target);
  await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
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
    console.log(`button text="${t}" aria="${aria}"`);
  }

  console.log('\n=== INPUTS ===');
  const inputs = await page.locator('textarea, [contenteditable="true"], input[type="text"]').all();
  for (const i of inputs.slice(0, 20)) {
    const ph = (await i.getAttribute('placeholder').catch(() => null)) || '';
    const aria = (await i.getAttribute('aria-label').catch(() => null)) || '';
    console.log(`placeholder="${ph}" aria="${aria}"`);
  }

  await context.close();
  process.exit(0);
}

async function cmdGenerate(opts) {
  const { context, page, browser } = await openBrowser({ headless: opts.headless });

  // Step 1: Auto-login if needed
  await ensureLoggedIn(page, browser, context);

  // Step 2: Build prompt
  const prompt = opts.prompt || buildPrompt({ ...opts, promptOverride: opts.prompt });
  console.log('=== PROMPT KE QWEN ===\n' + prompt + '\n====================');

  // Step 3: Upload logo (BEFORE entering image mode)
  const config = loadConfig();
  const useLogo = opts.logo !== null && (opts.logo || config.useLogo === true);
  const logoPath = opts.logo ? path.resolve(opts.logo) : DEFAULT_LOGO;

  if (useLogo && fs.existsSync(logoPath)) {
    await uploadLogo(page, logoPath);
    await sleep(1000);
  } else {
    console.log('Lewati upload logo.');
  }

  // Step 4: Enter image mode
  const ok = await enterImageMode(page);
  if (!ok) {
    console.log('Gagal masuk mode Create Image.');
    await cmdDetect({ headless: true });
    process.exit(2);
  }

  // Step 5: Add logo reference to prompt if uploaded
  let fullPrompt = prompt;
  if (useLogo && fs.existsSync(logoPath)) {
    fullPrompt += '\n\n[Gunakan logo Venturo yang sudah di-upload sebagai referensi visual. Generate poster BARU yang kreatif dengan headline dan CTA, bukan hanya tampilkan logo.]';
  }

  // Step 6: Send prompt
  await sendPrompt(page, fullPrompt);
  console.log('Prompt terkirim. Menunggu gambar...');

  // Step 7: Wait for completion
  const found = await waitForImageComplete(page);

  // Step 8: Save image
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const ts = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14);
  const outPath = opts.out ? path.resolve(opts.out) : path.join(OUTPUT_DIR, `qwen-poster-${ts}.png`);

  await downloadImage(page, found, outPath);
  console.log(`✓ DONE: ${outPath} (${found.size}, ${fs.statSync(outPath).size} bytes)`);

  await context.close();
  process.exit(0);
}

function parseArgs(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--headless') opts.headless = true;
    else if (a === '--no-logo') opts.logo = null;
    else if (a === '--out') opts.out = argv[++i];
    else if (a === '--prompt') opts.prompt = argv[++i];
    else if (a === '--title') opts.title = argv[++i];
    else if (a === '--subtitle') opts.subtitle = argv[++i];
    else if (a === '--event') opts.event = argv[++i];
    else if (a === '--date') opts.date = argv[++i];
    else if (a === '--venue') opts.venue = argv[++i];
    else if (a === '--cta') opts.cta = argv[++i];
    else if (a === '--style') opts.style = argv[++i];
    else if (a === '--logo') opts.logo = argv[++i];
  }
  return opts;
}

const [cmd, ...rest] = process.argv.slice(2);
const opts = parseArgs(rest);

if (cmd === 'detect') {
  await cmdDetect(opts);
} else if (cmd === 'generate') {
  await cmdGenerate(opts);
} else {
  console.log(`
qwen-poster — otomasi chat.qwen.ai untuk generate poster promosi

USAGE:
  node qwen-poster.mjs generate [flags]    Generate poster via Qwen-Image (auto-login)
  node qwen-poster.mjs detect              Dump UI: button/input/image (debug selector)

GENERATE FLAGS:
  --title "..."      Judul utama poster
  --subtitle "..."   Subjudul
  --event "..."      Nama event/produk
  --date "..."       Tanggal
  --venue "..."      Lokasi/venue
  --cta "..."        Call to action
  --style "..."      Gaya visual
  --prompt "..."     Prompt bebas (override template)
  --out path.png     Lokasi output
  --logo path.png    Upload logo (override config useLogo)
  --no-logo          Skip logo upload
  --headless         Jalan tanpa jendela browser

CREDENTIALS:
  Disimpan di config.json. Script akan auto-login jika session expired.
`);
  process.exit(1);
}
