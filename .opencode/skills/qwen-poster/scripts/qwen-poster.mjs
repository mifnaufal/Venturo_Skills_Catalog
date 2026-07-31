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
const GEN_TIMEOUT = 5 * 60 * 1000;

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

async function openBrowser({ headless = false } = {}) {
  fs.mkdirSync(PROFILE_DIR, { recursive: true });
  const context = await chromium.launchPersistentContext(PROFILE_DIR, {
    headless,
    viewport: { width: 1440, height: 900 },
    userAgent: undefined,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const page = context.pages()[0] || (await context.newPage());
  return { context, page };
}

async function cmdLogin({ headless }) {
  const { context, page } = await openBrowser({ headless });
  console.log('Buka', CHAT_URL, '— login manual di jendela browser.');
  await page.goto(CHAT_URL, { waitUntil: 'domcontentloaded' });
  await waitLoggedIn(page);
  fs.mkdirSync(path.dirname(STORAGE_FILE), { recursive: true });
  await context.storageState({ path: STORAGE_FILE });
  console.log('Login tersimpan ke', STORAGE_FILE);
  await context.close();
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
  const think = await findFirst(page, SELECTORS.thinkingSelector);
  if (think && (await think.count()) > 0) {
    await think.first().click();
    await page.waitForTimeout(800);
    if (await clickDropdownOption(page, SELECTORS.thinkingOption, 'Thinking')) {
      console.log('Thinking mode dipilih.');
    }
  } else {
    console.log('NOTE: thinking selector tidak ditemukan — lanjut.');
  }

  const mode = await findFirst(page, SELECTORS.modeButton);
  if (!mode || (await mode.count()) === 0) {
    console.log('FAIL: tombol mode tidak ditemukan. UI berubah? Jalankan "detect" lalu update selectors.json.');
    return false;
  }
  await mode.first().click();
  await page.waitForTimeout(1000);
  if (!(await clickDropdownOption(page, SELECTORS.menuCreateImage, 'Create Image'))) return false;

  const modelBtn = await findFirst(page, SELECTORS.imageModelButton);
  if (!modelBtn || (await modelBtn.count()) === 0) {
    console.log('FAIL: tombol model tidak ditemukan. UI berubah? Jalankan "detect".');
    return false;
  }
  await modelBtn.first().click();
  await page.waitForTimeout(1000);
  if (!(await clickDropdownOption(page, SELECTORS.imageModelOption, 'Qwen-Image 3.0'))) return false;

  const sizeBtn = await findFirst(page, SELECTORS.sizeSelector);
  if (!sizeBtn || (await sizeBtn.count()) === 0) {
    console.log('FAIL: tombol ukuran tidak ditemukan. UI berubah? Jalankan "detect".');
    return false;
  }
  await sizeBtn.first().click();
  await page.waitForTimeout(1000);
  if (!(await clickDropdownOption(page, SELECTORS.sizeOption1to1, '1:1'))) return false;

  console.log('Mode Create Image aktif: Qwen-Image 3.0, 1:1.');
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

async function waitForImage(page) {
  console.log('Menunggu gambar selesai digenerate (max 5 menit)...');
  const deadline = Date.now() + GEN_TIMEOUT;
  let lastCount = 0;
  let stable = 0;
  while (Date.now() < deadline) {
    await sleep(3000);
    const imgs = await page.locator('img').all().catch(() => []);
    const candidates = [];
    for (const img of imgs.slice(-10)) {
      const src = (await img.getAttribute('src').catch(() => '')) || '';
      const size = await img.evaluate((el) => `${el.naturalWidth}x${el.naturalHeight}`).catch(() => '0x0');
      const [w, h] = size.split('x').map(Number);
      if (w > 100 && h > 100) candidates.push({ img, src, size });
    }
    if (candidates.length > 0 && candidates.length !== lastCount) {
      console.log(`Gambar terdeteksi: ${candidates.length} (${candidates[candidates.length - 1].size})`);
      lastCount = candidates.length;
      stable = 0;
    } else if (candidates.length > 0) {
      stable++;
    }
    const busy = await findFirst(page, SELECTORS.generatingIndicator);
    const busyCount = busy ? await busy.count().catch(() => 0) : 0;
    if (candidates.length > 0 && busyCount === 0 && stable >= 2) {
      await sleep(3000);
      return candidates[candidates.length - 1];
    }
  }
  throw new Error('Timeout menunggu gambar (5 menit). Mungkin generation gagal atau UI berubah. Jalankan "detect".');
}

async function saveImage(page, img, outPath) {
  const src = img.src;
  try {
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
  } catch {
    console.log('Blob fetch gagal, fallback: screenshot elemen.');
    await img.screenshot({ path: outPath });
  }
  console.log('Tersimpan:', outPath);
}

async function cmdGenerate(opts) {
  const { context, page } = await openBrowser({ headless: opts.headless });
  const prompt = opts.prompt || buildPrompt(opts);
  console.log('=== PROMPT KE QWEN ===\n' + prompt + '\n====================');
  await page.goto(CHAT_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  const logged = await findFirst(page, SELECTORS.chatInput);
  if (!logged || !(await logged.isEditable().catch(() => false))) {
    console.log('Belum login — buka jendela browser dan login manual.');
    await waitLoggedIn(page);
  }
  const ok = await enterImageMode(page);
  if (!ok) {
    await cmdDetect({ headless: true });
    process.exit(2);
  }
  await sendPrompt(page, prompt);
  const found = await waitForImage(page);
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const ts = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14);
  const outPath = opts.out ? path.resolve(opts.out) : path.join(OUTPUT_DIR, `qwen-poster-${ts}.png`);
  await saveImage(page, found, outPath);
  const size = found.size;
  console.log(`DONE: ${outPath} (${size}, ${fs.statSync(outPath).size} bytes)`);
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
    else if (a === '--venue') opts.venue = argv[++i];
    else if (a === '--cta') opts.cta = argv[++i];
    else if (a === '--style') opts.style = argv[++i];
    else if (a === '--ratio') opts.ratio = argv[++i];
    else if (a === '--url') opts.url = argv[++i];
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
  - Kalau UI chat.qwen.ai berubah: jalankan "detect", update selectors.json, ulangi.
  - Captcha/challenge: selesaikan manual di jendela browser, script menunggu otomatis.
  - Hanya jalankan SATU instance sekaligus (profile browser dipakai bersama).
`);
  process.exit(1);
}
