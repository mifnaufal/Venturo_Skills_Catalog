export function buildPrompt({
  title,
  subtitle = '',
  event = '',
  date = '',
  venue = '',
  cta = '',
  style = '',
  ratio = '1:1',
}) {
  const parts = [];
  parts.push(`Design a promotional poster (aspect ratio ${ratio}) for ${event || 'a promotional campaign'}.`);
  parts.push(`MAIN TITLE as the dominant visual element: "${title}".`);
  if (subtitle) parts.push(`Subtitle: "${subtitle}".`);
  if (date) parts.push(`Date: ${date}.`);
  if (venue) parts.push(`Venue: ${venue}.`);
  if (cta) parts.push(`Call to action (clearly visible): "${cta}".`);
  if (style) parts.push(`Visual style: ${style}.`);
  parts.push(
    'Layout must be clean, readable, print-ready with strong typography hierarchy and balanced whitespace. All text in the poster must use exactly the provided wording — no invented words.'
  );
  return parts.join('\n');
}
