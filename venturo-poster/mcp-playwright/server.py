#!/usr/bin/env python3
"""
Venturo Poster — Playwright MCP Server

Exposes browser automation tools for Dreamina AI image generation.
Used by Antigravity AI agent via MCP protocol (stdio transport).

Tools:
  Low-level browser:  browser_start, browser_stop, browser_navigate,
                      browser_click, browser_fill, browser_upload_file,
                      browser_screenshot, browser_wait, browser_wait_for_url,
                      browser_evaluate

  Mid-level Dreamina: dreamina_login, dreamina_upload_reference,
                      dreamina_fill_prompt, dreamina_click_generate

Usage:
  python server.py
"""

import logging
import re
import sys
import time
from pathlib import Path
from typing import Optional

from playwright.sync_api import (
    sync_playwright,
    Browser,
    Page,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeout,
)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Venturo Poster — Playwright")

# =============================================================================
# Logging
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("venturo-poster")

# =============================================================================
# Paths
# =============================================================================

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PLUGIN_ROOT / "assets" / "image_1c155d.png"
OUTPUT_DIR = PLUGIN_ROOT / "output"

# =============================================================================
# Constants
# =============================================================================

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

# =============================================================================
# Selectors
# =============================================================================

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

# =============================================================================
# Global Browser State
# =============================================================================

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


def _find_visible(selectors):
    _assert_page()
    for sel in selectors:
        try:
            el = _page.query_selector(sel)
            if el and el.is_visible():
                return el
        except PlaywrightError:
            continue
    return None


def _find_any(selectors):
    _assert_page()
    for sel in selectors:
        try:
            el = _page.query_selector(sel)
            if el:
                return el
        except PlaywrightError:
            continue
    return None


def _find_file_input():
    _assert_page()
    for sel in [
        "input[type='file']",
        "input[accept*='image']",
        "input[accept*='png']",
    ]:
        try:
            el = _page.query_selector(sel)
            if el:
                return el
        except PlaywrightError:
            continue
    return None


# =============================================================================
# Low-Level Browser Tools
# =============================================================================


@mcp.tool()
def browser_start(headless: bool = False) -> str:
    """Launch Chromium browser. Must be called first."""
    global _playwright_instance, _browser, _page

    if _browser and _browser.is_connected():
        return "Browser already running."

    try:
        _playwright_instance = sync_playwright().start()
        _browser = _playwright_instance.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        _page = _browser.new_page()
        _page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
        logger.info("Browser started (headless=%s)", headless)
        return f"Browser started. Viewport: {VIEWPORT_WIDTH}x{VIEWPORT_HEIGHT}"
    except PlaywrightError as exc:
        logger.error("Failed to start browser: %s", exc)
        return f"Error: {exc}"


@mcp.tool()
def browser_stop() -> str:
    """Close browser and release resources."""
    global _playwright_instance, _browser, _page

    try:
        if _page:
            _page.close()
        if _browser:
            _browser.close()
        if _playwright_instance:
            _playwright_instance.stop()
    except PlaywrightError as exc:
        logger.warning("Error during browser shutdown: %s", exc)

    _page = None
    _browser = None
    _playwright_instance = None
    logger.info("Browser stopped.")
    return "Browser stopped."


@mcp.tool()
def browser_navigate(url: str) -> str:
    """Navigate to a URL."""
    _assert_browser()
    try:
        _page.goto(url, wait_until="domcontentloaded")
        logger.info("Navigated to: %s", url)
        return f"Navigated to {url}"
    except PlaywrightError as exc:
        logger.error("Navigation failed: %s", exc)
        return f"Error navigating to {url}: {exc}"


@mcp.tool()
def browser_click(selector: str) -> str:
    """Click the first visible element matching the CSS selector."""
    _assert_page()
    try:
        el = _find_visible([selector])
        if not el:
            el = _find_any([selector])
        if not el:
            return f"Element not found: {selector}"
        el.click()
        time.sleep(PAUSE_SHORT_MS / 1000)
        return f"Clicked: {selector}"
    except PlaywrightError as exc:
        return f"Error clicking {selector}: {exc}"


@mcp.tool()
def browser_fill(selector: str, text: str) -> str:
    """Fill an input field or contenteditable element with text."""
    _assert_page()
    try:
        el = _find_visible([selector])
        if not el:
            el = _find_any([selector])
        if not el:
            return f"Element not found: {selector}"
        el.click()
        time.sleep(PAUSE_SHORT_MS / 1000)
        el.fill(text)
        return f"Filled: {selector} ({len(text)} chars)"
    except PlaywrightError as exc:
        return f"Error filling {selector}: {exc}"


@mcp.tool()
def browser_upload_file(file_path: str) -> str:
    """Upload a file via the first file input found."""
    _assert_page()
    resolved = Path(file_path)
    if not resolved.exists():
        return f"File not found: {file_path}"

    try:
        file_input = _find_file_input()
        if not file_input:
            return "No file input found on page."
        file_input.set_input_files(str(resolved))
        logger.info("File uploaded: %s", resolved.name)
        return f"Uploaded: {resolved.name}"
    except PlaywrightError as exc:
        return f"Error uploading file: {exc}"


@mcp.tool()
def browser_screenshot(output_path: str) -> str:
    """Take a full-page screenshot and save to file."""
    _assert_page()
    resolved = Path(output_path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    try:
        _page.screenshot(path=str(resolved), full_page=True)
        logger.info("Screenshot saved: %s", resolved)
        return f"Screenshot saved: {resolved}"
    except PlaywrightError as exc:
        return f"Error taking screenshot: {exc}"


@mcp.tool()
def browser_wait(duration_ms: int) -> str:
    """Wait for a specified duration in milliseconds."""
    _assert_page()
    try:
        _page.wait_for_timeout(duration_ms)
        return f"Waited {duration_ms}ms"
    except PlaywrightError as exc:
        return f"Error during wait: {exc}"


@mcp.tool()
def browser_wait_for_url(pattern: str, timeout_ms: int = LONG_TIMEOUT_MS) -> str:
    """Wait until the page URL matches the regex pattern."""
    _assert_page()
    try:
        _page.wait_for_url(re.compile(pattern), timeout=timeout_ms)
        return f"URL matched pattern: {pattern}"
    except PlaywrightTimeout:
        return f"Timeout waiting for URL pattern: {pattern} (>{timeout_ms}ms)"
    except PlaywrightError as exc:
        return f"Error waiting for URL: {exc}"


@mcp.tool()
def browser_evaluate(script: str) -> str:
    """Execute JavaScript in the page context and return the result."""
    _assert_page()
    try:
        result = _page.evaluate(script)
        logger.info("JS evaluated: %.80s", script)
        return str(result)
    except PlaywrightError as exc:
        return f"Error evaluating JS: {exc}"


# =============================================================================
# Mid-Level Dreamina Tools
# =============================================================================


@mcp.tool()
def dreamina_login(email: str, password: str) -> str:
    """
    Log in to Dreamina using email credentials.
    Navigates to the login page, fills email & password, and submits.
    Returns success/failure status.
    """
    _assert_page()

    try:
        _page.goto(DREAMINA_LOGIN_URL, wait_until="domcontentloaded")
    except PlaywrightError as exc:
        return f"Error navigating to login page: {exc}"

    time.sleep(PAUSE_LONG_MS / 1000)

    email_el = _find_visible(EMAIL_SELECTORS)
    if not email_el:
        email_el = _find_any(EMAIL_SELECTORS)

    password_el = _find_visible(PASSWORD_SELECTORS)
    if not password_el:
        password_el = _find_any(PASSWORD_SELECTORS)

    if not email_el or not password_el:
        return "Login form not found. Could not locate email or password fields."

    try:
        email_el.click()
        time.sleep(PAUSE_SHORT_MS / 1000)
        email_el.fill(email)
        logger.info("Email field filled")
    except PlaywrightError as exc:
        logger.warning("Failed to fill email: %s", exc)

    try:
        password_el.click()
        time.sleep(PAUSE_SHORT_MS / 1000)
        password_el.fill(password)
        logger.info("Password field filled")
    except PlaywrightError as exc:
        logger.warning("Failed to fill password: %s", exc)

    submit_el = _find_visible(SUBMIT_SELECTORS)
    if not submit_el:
        submit_el = _find_any(SUBMIT_SELECTORS)

    if submit_el:
        try:
            submit_el.click()
            logger.info("Submit button clicked")
        except PlaywrightError as exc:
            logger.warning("Failed to click submit: %s", exc)
    else:
        return "Login form found but submit button could not be located."

    time.sleep(PAUSE_LONG_MS / 1000)

    for attempt in range(5):
        current = _page.url
        if "/ai-tool/" in current or "dreamina" in current.lower():
            logger.info("Login successful. URL: %s", current)
            return f"Login successful. Current URL: {current}"
        time.sleep(1)

    return (
        "Login submitted but could not verify success. "
        "The page may require additional verification (OTP/CAPTCHA)."
    )


@mcp.tool()
def dreamina_upload_reference() -> str:
    """
    Upload the Venturo logo as a reference image to Dreamina.
    Uses multi-selector fallback strategy.
    Returns success/failure status.
    """
    _assert_page()

    if not LOGO_PATH.exists():
        return f"Logo not found at {LOGO_PATH}. Upload manually."

    for sel in UPLOAD_SELECTORS:
        try:
            el = _page.query_selector(sel)
            if not el:
                continue
            tag = el.evaluate("el => el.tagName.toLowerCase()")
            if tag == "input":
                el.set_input_files(str(LOGO_PATH))
                logger.info("Logo uploaded via: %s", sel)
                return f"Logo uploaded successfully via: {sel}"
            else:
                el.click()
                time.sleep(PAUSE_MEDIUM_MS / 1000)
                file_input = _find_file_input()
                if file_input:
                    file_input.set_input_files(str(LOGO_PATH))
                    logger.info("Logo uploaded after clicking: %s", sel)
                    return f"Logo uploaded successfully via: {sel}"
        except PlaywrightError:
            continue

    return (
        "Could not auto-upload logo. "
        f"Please upload manually: {LOGO_PATH}"
    )


@mcp.tool()
def dreamina_fill_prompt(prompt: str) -> str:
    """
    Fill the Dreamina prompt text area with the given prompt.
    Uses multi-selector fallback strategy.
    Returns success/failure status.
    """
    _assert_page()

    for sel in PROMPT_SELECTORS:
        try:
            el = _page.query_selector(sel)
            if not el:
                continue
            el.click()
            time.sleep(PAUSE_SHORT_MS / 1000)
            el.fill(prompt)
            logger.info("Prompt filled via: %s (%d chars)", sel, len(prompt))
            return f"Prompt filled via: {sel}"
        except PlaywrightError:
            continue

    return "Could not auto-fill prompt. Please paste manually."


@mcp.tool()
def dreamina_click_generate() -> str:
    """
    Click the Generate button in Dreamina.
    Uses multi-selector fallback strategy.
    Returns success/failure status.
    """
    _assert_page()

    for sel in GENERATE_SELECTORS:
        try:
            el = _page.query_selector(sel)
            if el:
                el.click()
                logger.info("Generate clicked via: %s", sel)
                return f"Generate clicked via: {sel}"
        except PlaywrightError:
            continue

    return "Could not auto-click Generate. Please click manually."


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    logger.info("Starting Venturo Poster MCP server...")
    mcp.run(transport="stdio")
