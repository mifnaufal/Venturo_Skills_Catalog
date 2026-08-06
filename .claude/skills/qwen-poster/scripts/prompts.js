export function buildPrompt({
  title,
  subtitle = '',
  event = '',
  date = '',
  venue = '',
  cta = '',
  style = '',
  ratio = '1:1',
  promptOverride = '',
}) {
  // If explicit prompt override provided, use it
  if (promptOverride) return promptOverride;

  const parts = [];
  parts.push(`Design a BOLD, ENERGETIC, high-impact Indonesian service-package poster for Venturo, a custom software development company. Square ${ratio}.`);
  parts.push(`This is a SHOW-STOPPING poster, NOT a corporate flyer, NOT a brochure, NOT a boring template. It should make people STOP SCROLLING.`);
  parts.push(``);
  parts.push(`🚫 STRICTLY FORBIDDEN:`);
  parts.push(`- NO QR codes, barcodes, or matrix patterns`);
  parts.push(`- NO generic corporate stock photos`);
  parts.push(`- NO flat boring symmetric layouts`);
  parts.push(`- NO centered-everything compositions`);
  parts.push(``);
  parts.push(`=== CONTENT (exact text, no invented wording) ===`);
  parts.push(`- Brand: "VENTURO" (premium treatment — gradient text, 3D effect, or bold pill badge)`);
  parts.push(`- Headline: "${title}" — MASSIVE, takes 25-35% of canvas`);
  if (subtitle) parts.push(`- Tagline: "${subtitle}" — smaller italic display text`);
  if (event) parts.push(`- Event/brand: "${event}"`);
  if (cta) parts.push(`- CTA button: "${cta}"`);
  parts.push(``);
  parts.push(`=== TYPOGRAPHY (use distinct font mix for impact) ===`);
  parts.push(`- HEADLINE: ultra-condensed BLACK sans-serif (Anton, Bebas Neue, Oswald Black, or Tungsten Bold style) — uppercase, all caps, MASSIVE size 100-180pt equivalent, very tight letter-spacing`);
  parts.push(`- Focal word in headline: italic + outlined OR filled with vibrant accent color OR in a contrasting pill badge with shadow`);
  parts.push(`- SUBTITLE: italic display serif (Playfair Display Italic, Cormorant Italic, or DM Serif Display Italic style) — elegant contrast against bold headline`);
  parts.push(`- BODY TEXT: clean geometric sans (Inter, Manrope, or Space Grotesk) — 14-18pt equivalent`);
  parts.push(`- CTA: Space Grotesk Bold or Manrope ExtraBold — uppercase, letter-spacing 0.08-0.12em, in pill-shaped button`);
  parts.push(`- STATS/NUMBERS: HUGE display numbers (3-5x body size) with tiny labels — e.g. "Rp 15-35 JT" in giant bold, "Budget" in tiny uppercase`);
  parts.push(`- KEY RULE: mix 1 condensed display + 1 italic serif + 1 clean sans = visual tension and interest`);
  parts.push(``);
  parts.push(`=== LAYOUT (asymmetric, dynamic, NOT the boring left-text-right-phone template) ===`);
  parts.push(`- ASYMMETRIC composition with diagonal energy (think 15-25° rotation on key elements)`);
  parts.push(`- Use a large BOLD BACKGROUND SHAPE — a giant blob, circle, or diagonal slash in vibrant teal/cyan that covers 40-60% of canvas`);
  parts.push(`- Split composition: text block on one side overlapping with phone mockup on the other`);
  parts.push(`- Headline can be slightly rotated (-3° to -8°) for dynamism`);
  parts.push(`- OVERLAPPING elements: text overlaps phone, phone overlaps CTA, shapes overlap everything`);
  parts.push(`- Use bold NEGATIVE SPACE — let one big element breathe, not crowded`);
  parts.push(`- Visual flow: eye should zigzag, not just scan top-to-bottom`);
  parts.push(``);
  parts.push(`=== COLOR PALETTE (VIBRANT, not muted) ===`);
  parts.push(`- PRIMARY: Deep Teal #006D79 (40%+ of canvas)`);
  parts.push(`- SECONDARY: Bright Cyan #00D4FF or Light Teal #009BAD`);
  parts.push(`- ACCENT 1: Vibrant Green #10B981 (use for highlights, badges, checkmarks, focal words)`);
  parts.push(`- ACCENT 2 (pick one for punch): Electric Yellow #FFD93D OR Hot Coral #FF6B6B OR Vibrant Magenta #EC4899`);
  parts.push(`- Background: GRADIENT (teal-to-cyan-to-white) OR clean white with bold color blocks OR deep teal with light foreground`);
  parts.push(`- Text: dark navy #0F172A on light bg, OR pure white on dark gradient bg`);
  parts.push(`- HIGH CONTRAST — no muddy muted colors, all colors should POP`);
  parts.push(``);
  parts.push(`=== VISUAL ELEMENTS (make it KECE) ===`);
  parts.push(`- Smartphone mockup TILTED 15-20° angle (not straight), with realistic shadow, showing app UI`);
  parts.push(`- Floating geometric shapes around the phone: circles, triangles, blob shapes, half-moons in accent colors with soft drop shadows`);
  parts.push(`- SPARKLE/star decorations (4-point stars, sparkles, asterisks) scattered around — 8-12 of them, in white or accent color`);
  parts.push(`- Bold pill-shaped badges with hard shadow (offset 4-6px) for CTA and key info`);
  parts.push(`- 3D DEPTH: drop shadows on all major elements, gradient on shapes, highlight on edges`);
  parts.push(`- Halftone dot pattern or gradient mesh on background (NOT grid — grid is boring)`);
  parts.push(`- Decorative line elements: swooshes, arrows, thick underlines, curved lines`);
  parts.push(`- Icon set: bold flat icons (lightning bolt, checkmark, rocket, arrow) in accent color`);
  parts.push(`- Optional: small 3D-style spheres or geometric solids floating in background`);
  parts.push(``);
  parts.push(`=== DETAILS & FINISHING ===`);
  parts.push(`- Smartphone showing realistic app interface with at least 3 visible UI elements (cards, buttons, lists)`);
  parts.push(`- Stats in HUGE numbers — "Rp 15-35 JT", "4-6 MINGGU", "3 ORANG" — these should be HERO elements`);
  parts.push(`- Subtle film grain or noise texture overlay (2-3%) for premium feel`);
  parts.push(`- Soft glow on key elements (headline, CTA, focal word)`);
  parts.push(`- Outer corner accent marks (like crop marks or registration marks) for editorial design feel`);
  parts.push(``);
  parts.push(`=== MOOD & REFERENCE ===`);
  parts.push(`- Reference style: Behance top-tier tech agency posters, Stripe Sessions, Gojek/Tokopedia promotional posters, Apple product launch keynotes`);
  parts.push(`- Mood: bold, energetic, futuristic, Indonesian tech-startup, Gen-Z friendly but premium`);
  parts.push(`- Aesthetic: Y2K-meets-modern, with playful elements (sparkles, stars) + serious typography`);
  parts.push(`- Should look like a poster from a high-end design agency, not a Word template`);
  parts.push(`- "WOW" factor — viewer should want to share it, not just glance and scroll past`);
  parts.push(``);
  parts.push(`=== FINAL RULES ===`);
  parts.push(`- High quality, print-ready, would look amazing on Instagram feed`);
  parts.push(`- All text must be readable and prominent`);
  parts.push(`- No invented text — only use exactly what's provided in CONTENT section`);
  parts.push(`- Absolutely NO QR codes or QR-code-like patterns`);

  return parts.join('\n');
}
