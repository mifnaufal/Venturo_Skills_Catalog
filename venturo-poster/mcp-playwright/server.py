#!/usr/bin/env python3
"""
Venturo Poster — Playwright MCP Server
"""

import logging
import re
import sys
import asyncio
from pathlib import Path
from typing import Optional

from playwright.async_api import (
    async_playwright,
    Browser,
    Page,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeout,
)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Venturo Poster — Playwright")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("venturo-poster")

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PLUGIN_ROOT / "assets" / "image_1c155d.png"
OUTPUT_DIR = PLUGIN_ROOT / "output"

VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800
LONG_TIMEOUT_MS = 30_000
GENERATION_TIMEOUT_MS = 180_000
PAUSE_SHORT_MS = 300
PAUSE_MEDIUM_MS = 1_000
PAUSE_LONG_MS = 5_000

DREAMINA_LOGIN_URL = (
    "https://dreamina.capcut.com/ai-tool/"
    "home?need_login=true&type=image&workspace=0"
)
DREAMINA_IMAGE_URL = "https://dreamina.capcut.com/ai-tool/image"

SIGN_IN_SELECTORS = [
    "button:has-text('Sign in')",
    "button:has-text('Log in')",
    "button:has-text('Login')",
    "button:has-text('Masuk')",
    "button:has-text('Sign In')",
    "a:has-text('Sign in')",
    "a:has-text('Log in')",
    "span:has-text('Sign in')",
    "div[class*='login'] button",
    "div[class*='sign-in'] button",
    "div[class*='signin'] button",
]

EMAIL_SELECTORS = [
    "input[type='email']",
    "input[name='email']",
    "input[name='account']",
    "input[placeholder*='email']",
    "input[placeholder*='Email']",
    "input[placeholder*='account']",
    "input[autocomplete='username']",
    "input[autocomplete='email']",
]

PASSWORD_SELECTORS = [
    "input[type='password']",
    "input[name='password']",
    "input[placeholder*='password']",
    "input[placeholder*='Password']",
    "input[placeholder*='Kata Sandi']",
    "input[autocomplete='current-password']",
]

SUBMIT_SELECTORS = [
    "button[type='submit']",
    "button:has-text('Sign in')",
    "button:has-text('Log in')",
    "button:has-text('Login')",
    "button:has-text('Masuk')",
    "button:has-text('Continue')",
    "button:has-text('Lanjutkan')",
    "button:has-text('Submit')",
    "button[class*='submit']",
    "button[class*='login']",
    "button[class*='sign-in']",
]

UPLOAD_SELECTORS = [
    "input[type='file']",
    "div[class*='upload'] input",
    "div[class*='reference'] input",
    "div[class*='image-input'] input",
    "button[class*='upload']",
    "div[class*='img-input']",
    "div[role='button']:has-text('upload')",
    "div[aria-label*='upload']",
]

PROMPT_SELECTORS = [
    "textarea",
    "[contenteditable='true']",
    ".ql-editor",
    "div[class*='prompt'] div[contenteditable]",
    "div[class*='input'] textarea",
    "div[class*='editor'] div[contenteditable]",
]

GENERATE_SELECTORS = [
    "button:has-text('Generate')",
    "button:has-text('Buat')",
    "button:has-text('Create')",
    "button[class*='generate']",
    "button[class*='submit']",
    "div[class*='generate'] button",
]

_playwright_instance = None
_browser: Optional[Browser] = None
_page: Optional[Page] = None


def _assert_browser():
    if not _browser or not _browser.is_connected():
        raise RuntimeError("Browser not started. Call browser_start() first.")


def _assert_page():
    _assert_browser()
    if not _page:
        raise RuntimeError("No active page. Call browser_navigate() first.")


async def _find_visible(selectors):
    _assert_page()
    for sel in selectors:
        try:
            el = await _page.query_selector(sel)
            if el and await el.is_visible():
                return el
        except PlaywrightError:
            continue
    return None


async def _find_any(selectors):
    _assert_page()
    for sel in selectors:
        try:
            el = await _page.query_selector(sel)
            if el:
                return el
        except PlaywrightError:
            continue
    return None


async def _find_file_input():
    _assert_page()
    for sel in [
        "input[type='file']",
        "input[accept*='image']",
        "input[accept*='png']",
    ]:
        try:
            el = await _page.query_selector(sel)
            if el:
                return el
        except PlaywrightError:
            continue
    return None


@mcp.tool()
async def browser_start(headless: bool = False) -> str:
    global _playwright_instance, _browser, _page
    if _browser and _browser.is_connected():
        return "Browser already running."
    try:
        p = await async_playwright().start()
        _playwright_instance = p
        _browser = await p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        _page = await _browser.new_page()
        await _page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
        logger.info("Browser started")
        return f"Browser started. Viewport: {VIEWPORT_WIDTH}x{VIEWPORT_HEIGHT}"
    except PlaywrightError as exc:
        return f"Error: {exc}"


@mcp.tool()
async def browser_stop() -> str:
    global _playwright_instance, _browser, _page
    try:
        if _page: await _page.close()
        if _browser: await _browser.close()
        if _playwright_instance: await _playwright_instance.stop()
    except PlaywrightError:
        pass
    _page = None
    _browser = None
    _playwright_instance = None
    return "Browser stopped."


@mcp.tool()
async def browser_navigate(url: str) -> str:
    _assert_browser()
    try:
        await _page.goto(url, wait_until="domcontentloaded")
        return f"Navigated to {url}"
    except PlaywrightError as exc:
        return f"Error navigating to {url}: {exc}"


@mcp.tool()
async def browser_click(selector: str) -> str:
    _assert_page()
    try:
        el = await _find_visible([selector])
        if not el: el = await _find_any([selector])
        if not el: return f"Element not found: {selector}"
        await el.click()
        await asyncio.sleep(PAUSE_SHORT_MS / 1000)
        return f"Clicked: {selector}"
    except PlaywrightError as exc:
        return f"Error clicking {selector}: {exc}"


@mcp.tool()
async def browser_fill(selector: str, text: str) -> str:
    _assert_page()
    try:
        el = await _find_visible([selector])
        if not el: el = await _find_any([selector])
        if not el: return f"Element not found: {selector}"
        await el.click()
        await asyncio.sleep(PAUSE_SHORT_MS / 1000)
        await el.fill(text)
        return f"Filled: {selector} ({len(text)} chars)"
    except PlaywrightError as exc:
        return f"Error filling {selector}: {exc}"


@mcp.tool()
async def browser_upload_file(file_path: str) -> str:
    _assert_page()
    resolved = Path(file_path)
    if not resolved.exists(): return f"File not found: {file_path}"
    try:
        file_input = await _find_file_input()
        if not file_input: return "No file input found on page."
        await file_input.set_input_files(str(resolved))
        return f"Uploaded: {resolved.name}"
    except PlaywrightError as exc:
        return f"Error uploading file: {exc}"


@mcp.tool()
async def browser_screenshot(output_path: str) -> str:
    _assert_page()
    resolved = Path(output_path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    try:
        await _page.screenshot(path=str(resolved), full_page=True)
        return f"Screenshot saved: {resolved}"
    except PlaywrightError as exc:
        return f"Error taking screenshot: {exc}"


@mcp.tool()
async def browser_wait(duration_ms: int) -> str:
    _assert_page()
    try:
        await _page.wait_for_timeout(duration_ms)
        return f"Waited {duration_ms}ms"
    except PlaywrightError as exc:
        return f"Error during wait: {exc}"


@mcp.tool()
async def browser_wait_for_url(pattern: str, timeout_ms: int = LONG_TIMEOUT_MS) -> str:
    _assert_page()
    try:
        await _page.wait_for_url(re.compile(pattern), timeout=timeout_ms)
        return f"URL matched pattern: {pattern}"
    except (PlaywrightTimeout, PlaywrightError) as exc:
        return f"Error: {exc}"


@mcp.tool()
async def browser_evaluate(script: str) -> str:
    _assert_page()
    try:
        result = await _page.evaluate(script)
        return str(result)
    except PlaywrightError as exc:
        return f"Error evaluating JS: {exc}"


@mcp.tool()
async def dreamina_login(email: str, password: str) -> str:
    _assert_page()
    try:
        await _page.goto(DREAMINA_LOGIN_URL, wait_until="domcontentloaded")
    except PlaywrightError as exc:
        return f"Error navigating to login page: {exc}"
    await asyncio.sleep(PAUSE_LONG_MS / 1000)

    email_el = await _find_visible(EMAIL_SELECTORS)
    if not email_el: email_el = await _find_any(EMAIL_SELECTORS)
    password_el = await _find_visible(PASSWORD_SELECTORS)
    if not password_el: password_el = await _find_any(PASSWORD_SELECTORS)

    if not email_el or not password_el:
        return "Login form not found."

    try:
        await email_el.click()
        await asyncio.sleep(PAUSE_SHORT_MS / 1000)
        await email_el.fill(email)
        await password_el.click()
        await asyncio.sleep(PAUSE_SHORT_MS / 1000)
        await password_el.fill(password)
    except PlaywrightError:
        pass

    submit_el = await _find_visible(SUBMIT_SELECTORS)
    if not submit_el: submit_el = await _find_any(SUBMIT_SELECTORS)

    if submit_el:
        try:
            await submit_el.click()
        except PlaywrightError:
            pass
    else:
        return "Submit button not found."

    await asyncio.sleep(PAUSE_LONG_MS / 1000)
    for _ in range(5):
        current = _page.url
        if "/ai-tool/" in current or "dreamina" in current.lower():
            return f"Login successful. Current URL: {current}"
        await asyncio.sleep(1)
    return "Login submitted but could not verify success."


@mcp.tool()
async def dreamina_upload_reference() -> str:
    _assert_page()
    if not LOGO_PATH.exists(): return f"Logo not found at {LOGO_PATH}."
    for sel in UPLOAD_SELECTORS:
        try:
            el = await _page.query_selector(sel)
            if not el: continue
            tag = await el.evaluate("el => el.tagName.toLowerCase()")
            if tag == "input":
                await el.set_input_files(str(LOGO_PATH))
                return f"Logo uploaded via: {sel}"
            else:
                await el.click()
                await asyncio.sleep(PAUSE_MEDIUM_MS / 1000)
                file_input = await _find_file_input()
                if file_input:
                    await file_input.set_input_files(str(LOGO_PATH))
                    return f"Logo uploaded via: {sel}"
        except PlaywrightError:
            continue
    return "Could not auto-upload logo."


@mcp.tool()
async def dreamina_fill_prompt(prompt: str) -> str:
    _assert_page()
    for sel in PROMPT_SELECTORS:
        try:
            el = await _page.query_selector(sel)
            if not el: continue
            await el.click()
            await asyncio.sleep(PAUSE_SHORT_MS / 1000)
            await el.fill(prompt)
            return f"Prompt filled via: {sel}"
        except PlaywrightError:
            continue
    return "Could not auto-fill prompt."


@mcp.tool()
async def dreamina_click_generate() -> str:
    _assert_page()
    for sel in GENERATE_SELECTORS:
        try:
            el = await _page.query_selector(sel)
            if el:
                await el.click()
                return f"Generate clicked via: {sel}"
        except PlaywrightError:
            continue
    return "Could not auto-click Generate."

if __name__ == "__main__":
    mcp.run(transport="stdio")
