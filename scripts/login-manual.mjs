#!/usr/bin/env node
// Manual login helper — opens headed browser, waits for user to login,
// then saves session to .qwen-profile/storage-state.json
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const STORAGE = '.qwen-profile/storage-state.json';
const URL = 'https://chat.qwen.ai/';

(async () => {
  console.log('Membuka browser...');
  const browser = await chromium.launch({
    headless: false,
    channel: 'chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  console.log('Browser terbuka di https://chat.qwen.ai/');
  console.log('');
  console.log('=================================================');
  console.log('  SILAKAN LOGIN DI BROWSER YANG TERBUKA');
  console.log('  (Google / GitHub / Email / apapun yg lo mau)');
  console.log('=================================================');
  console.log('');
  console.log('Script ini akan otomatis detect kalo lo udah login...');

  let loggedIn = false;
  const startTime = Date.now();
  const TIMEOUT = 10 * 60 * 1000; // 10 minutes

  while (Date.now() - startTime < TIMEOUT) {
    await page.waitForTimeout(3000);

    // Check if logged in
    const loginBtn = await page.locator('button:has-text("Log in")').count().catch(() => 0);
    const signUpBtn = await page.locator('button:has-text("Sign up")').count().catch(() => 0);
    const signInBtn = await page.locator('button:has-text("Sign in")').count().catch(() => 0);
    const loginVisible = loginBtn > 0 || signUpBtn > 0 || signInBtn > 0;

    // Also check for user avatar/profile indicator
    const hasAvatar = await page.locator('img[alt*="avatar"], [class*="avatar"] img, button[class*="user"]').count();
    const hasNewChat = await page.locator('button:has-text("New Chat")').count();
    const isLoggedIn = !loginVisible || hasAvatar > 0 || hasNewChat > 0;

    if (isLoggedIn && Date.now() - startTime > 10000) {  // Wait at least 10s
      loggedIn = true;
      break;
    }

    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    process.stdout.write(`\r[${elapsed}s] Menunggu login... (loginVisible=${loginVisible}, avatar=${hasAvatar})`);
  }
  console.log('');

  if (!loggedIn) {
    console.log('Timeout. Login belum selesai.');
    await browser.close();
    process.exit(1);
  }

  // Save session
  fs.mkdirSync(path.dirname(STORAGE), { recursive: true });
  await context.storageState({ path: STORAGE });
  console.log(`✓ Login berhasil! Session tersimpan ke ${STORAGE}`);
  console.log('');
  console.log('Sekarang lo bisa jalanin command generate, contoh:');
  console.log('  node .claude/skills/qwen-poster/scripts/qwen-poster.mjs generate \\');
  console.log('    --headless --title "PAKET STARTER" --prompt "..."');

  // Keep browser open for a moment so user can verify
  console.log('');
  console.log('Browser bakal tutup dalam 5 detik...');
  await page.waitForTimeout(5000);

  await browser.close();
  process.exit(0);
})().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
