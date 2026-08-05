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
  parts.push(`Design a professional modern tech promotional poster for Venturo, a custom software development company. Square ${ratio}.`);
  parts.push(`This is a SERVICE PACKAGE POSTER for Venturo, NOT a QR code, NOT a business card, NOT a logo.`);
  parts.push(``);
  parts.push(`🚫 STRICTLY FORBIDDEN - DO NOT INCLUDE:`);
  parts.push(`- NO QR codes of any kind`);
  parts.push(`- NO barcodes`);
  parts.push(`- NO matrix patterns`);
  parts.push(`- NO square pixelated codes`);
  parts.push(`- NO geometric grid patterns that resemble QR codes`);
  parts.push(``);
  parts.push(`CONTENT:`);
  parts.push(`- Brand: "VENTURO" (displayed prominently)`);
  parts.push(`- Headline (dominant, uppercase, large bold font): "${title}"`);
  if (subtitle) parts.push(`- Tagline/subtitle: "${subtitle}"`);
  if (event) parts.push(`- Brand/event name: "${event}"`);
  if (cta) parts.push(`- CTA button text: "${cta}"`);
  parts.push(``);
  parts.push(`DESIGN STYLE (modern tech promo aesthetics):`);
  parts.push(`- Clean, modern layout with bold typography`);
  parts.push(`- Smartphone/phone mockup on the right side showing app interface`);
  parts.push(`- Subtle dot grid pattern background (NOT QR-code-like)`);
  parts.push(`- Diagonal or curved accent shapes for depth`);
  parts.push(`- Floating badges/elements around the phone with rounded corners`);
  parts.push(`- Visual hierarchy: large headline > supporting text > details`);
  parts.push(`- Professional spacing with adequate white space`);
  parts.push(``);
  parts.push(`COLOR PALETTE (Venturo brand colors):`);
  parts.push(`- Primary: Teal/Deep Blue (#006D79 or similar)`);
  parts.push(`- Secondary: Light Teal/Cyan (#009BAD or similar)`);
  parts.push(`- Accent: Green (#10B981 or similar)`);
  parts.push(`- Background: White or very light gray`);
  parts.push(`- Text: Dark navy or black for contrast`);
  parts.push(``);
  parts.push(`LAYOUT STRUCTURE:`);
  parts.push(`- Left side: Text content (headline, tagline, description, features)`);
  parts.push(`- Right side: Phone mockup with floating badges`);
  parts.push(`- Bottom: CTA button or info bar`);
  parts.push(``);
  parts.push(`DETAILS:`);
  parts.push(`- Phone mockup should look realistic with proper shadow`);
  parts.push(`- Feature list with icons/checkmarks`);
  parts.push(`- Stats/metrics displayed prominently (budget, timeline, team size)`);
  parts.push(`- Professional, corporate yet modern feel`);
  parts.push(``);
  parts.push(`DESIGN REQUIREMENTS:`);
  parts.push(`- Professional marketing poster with bold typography`);
  parts.push(`- Clear visual hierarchy: headline > tagline > details > CTA`);
  parts.push(`- Use modern Indonesian business aesthetic`);
  parts.push(`- Include decorative elements (gradients, geometric shapes, subtle patterns)`);
  parts.push(`- Background should be clean and professional`);
  parts.push(`- Text must be readable and prominent`);
  parts.push(`- Output should look like a real promotional flyer/poster`);
  parts.push(`- High quality, print-ready appearance`);
  parts.push(`- Absolutely NO QR codes or QR-code-like patterns`);

  return parts.join('\n');
}
