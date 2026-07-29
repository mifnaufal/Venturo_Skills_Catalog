import * as fs from 'fs';
import * as path from 'path';

// Fallback tier data when config file is not available (use this for standalone testing)
const FALLBACK_TIER_DATA = {
  starter: {
    tier_label: 'STARTER',
    heading: 'Digital Presence',
    price_range: 'IDR 5-10 Juta',
    target_audience: 'Startup & UMKM',
    cta: 'Konsultasi Gratis'
  },
  growth: {
    tier_label: 'GROWTH',
    heading: 'Professional Growth',
    price_range: 'IDR 10-25 Juta',
    target_audience: 'Bisnis Menengah',
    cta: 'Mulai Sekarang'
  },
  enterprise: {
    tier_label: 'ENTERPRISE',
    heading: 'Enterprise Solutions',
    price_range: 'IDR 25 Juta+',
    target_audience: 'Perusahaan Besar',
    cta: 'Hubungi Kami'
  }
};

function parseYaml(yaml: string): Record<string, any> {
  const result: Record<string, any> = {};
  const lines = yaml.split('\n').filter(line => line.trim() && !line.startsWith('#'));
  let currentTier: string | null = null;
  for (const line of lines) {
    if (line.includes(':') && !line.startsWith('  ') && !line.trim().startsWith('-')) {
      const key = line.split(':')[0].trim();
      currentTier = key;
      result[currentTier] = {};
    } else if (currentTier && line.startsWith('  ')) {
      const propMatch = line.match(/^\s+(\w+):\s*(.+)$/);
      if (propMatch) {
        const [, prop, value] = propMatch;
        result[currentTier][prop] = value.trim().replace(/^["']|["']$/g, '');
      }
    }
  }
  return result;
}

const DATA_PATH = path.resolve(__dirname, '..', 'config', 'tier-copy.yaml');
let TIER_DATA: Record<string, any>;
try {
  const rawYaml = fs.readFileSync(DATA_PATH, 'utf8');
  TIER_DATA = parseYaml(rawYaml);
} catch (e) {
  const msg = e && typeof e === 'object' && 'message' in e ? (e as any).message : String(e);
  console.warn('Config file not found, using fallback data:', msg);
  TIER_DATA = FALLBACK_TIER_DATA;
}

interface TierStyle {
  bg: string;
  text: string;
  textMuted: string;
  accent: string;
  accentSoft: string;
  gradient: { from: string; to: string };
  ctaGradient: { from: string; to: string };
  ctaText: string;
  serif: string;
  qrColor: string;
}

const STYLES: Record<string, TierStyle> = {
  starter: {
    bg: '#FFFFFF',
    text: '#0F172A',
    textMuted: '#64748B',
    accent: '#006D79',
    accentSoft: '#009BAD',
    gradient: { from: '#006D79', to: '#FF6B6B' },
    ctaGradient: { from: '#0F172A', to: '#006D79' },
    ctaText: '#FFFFFF',
    serif: '#FF6B6B',
    qrColor: '#006D79',
  },
  growth: {
    bg: '#FFFFFF',
    text: '#0F172A',
    textMuted: '#64748B',
    accent: '#006D79',
    accentSoft: '#009BAD',
    gradient: { from: '#006D79', to: '#009BAD' },
    ctaGradient: { from: '#006D79', to: '#009BAD' },
    ctaText: '#FFFFFF',
    serif: '#009BAD',
    qrColor: '#006D79',
  },
  enterprise: {
    bg: '#0A1B1F',
    text: '#FFFFFF',
    textMuted: '#94A3B8',
    accent: '#009BAD',
    accentSoft: '#38BDF8',
    gradient: { from: '#009BAD', to: '#FF6B6B' },
    ctaGradient: { from: '#FF6B6B', to: '#EF4444' },
    ctaText: '#FFFFFF',
    serif: '#FF6B6B',
    qrColor: '#009BAD',
  },
};

export async function generateSVG(tier: string): Promise<string> {
  const data = TIER_DATA[tier] || TIER_DATA.starter || FALLBACK_TIER_DATA.starter;
  const s = STYLES[tier] || STYLES.starter;
  const isDark = tier === 'enterprise';

  // Split tagline for mixed typography (bold sans + italic serif)
  const taglineWords = data.heading.split(' ');
  const firstWord = taglineWords[0];
  const restWords = taglineWords.slice(1).join(' ');

  // --- Background Decorations (inspired by template structure) ---

  // Wave overlay - organic flowing curve at top (like template's hand illustration flow)
  const wave = isDark ?
    '<path d="M0,0 L700,150 L1024,80 L2048,0 L2048,-60 L0,-60 Z" fill="url(#waveGrad)" opacity="0.25"/>' :
    '<path d="M0,0 L700,150 L1024,80 L2048,0 L2048,-60 L0,-60 Z" fill="url(#waveGrad)" opacity="0.35"/>';

  // Subtle dot/grid pattern texture (textured paper look from template)
  const gridPattern = '<pattern id="gridPattern" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="1" height="1" fill="' + s.accent + '" opacity="0.04"/></pattern>';

  // QR code placeholder at left (template-style square element)
  const qrCode = '<g transform="translate(80,100)"><rect x="0" y="0" width="80" height="80" fill="none" stroke="' + s.qrColor + '" stroke-width="1.5"/><rect x="8" y="8" width="16" height="16" fill="' + s.qrColor + '"/><rect x="56" y="8" width="16" height="16" fill="' + s.qrColor + '"/><rect x="8" y="56" width="16" height="16" fill="' + s.qrColor + '"/><rect x="56" y="56" width="16" height="16" fill="' + s.qrColor + '"/></g>';

  // Accent circle in corner (decorative template element)
  const accentCircle = '<circle cx="1880" cy="120" r="80" fill="none" stroke="' + s.accent + '" stroke-width="1" opacity="0.2"/>';

  // Geometric wedge bottom-left (adds visual weight, template-inspired)
  const wedge = '<polygon points="0,2048 0,1840 220,1840" fill="' + s.ctaGradient.to + '" opacity="0.1"/>';

  // --- Content ---

  // Tagline rest span (italic serif for typographic contrast)
  const taglineRest = restWords ?
    '<tspan font-family="Playfair Display, Times New Roman, serif" font-size="75" font-weight="400" font-style="italic" dx="8" fill="' + s.serif + '">' + escapeXml(restWords) + '</tspan>' : '';

  return '<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="2048" viewBox="0 0 2048 2048">\n' +
    '  <defs>\n' +
    '    <linearGradient id="tierGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="' + s.gradient.from + '"/><stop offset="100%" stop-color="' + s.gradient.to + '"/></linearGradient>\n' +
    '    <linearGradient id="priceGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="' + s.gradient.from + '"/><stop offset="100%" stop-color="' + s.gradient.to + '"/></linearGradient>\n' +
    '    <linearGradient id="ctaGradient" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="' + s.ctaGradient.from + '"/><stop offset="100%" stop-color="' + s.ctaGradient.to + '"/></linearGradient>\n' +
    '    <linearGradient id="waveGrad" x1="0%" y1="0%"><stop offset="0%" stop-color="' + s.accentSoft + '" stop-opacity="0.2"/><stop offset="100%" stop-color="' + s.accent + '" stop-opacity="0.1"/></linearGradient>\n' +
    gridPattern + '\n' +
    '  </defs>\n\n' +
    '  <!-- Background layers (template-inspired decorations) -->\n' +
    '  <rect width="2048" height="2048" fill="' + s.bg + '"/>\n' +
    '  <rect width="2048" height="2048" fill="url(#gridPattern)" opacity="0.6"/>' +
    wave +
    accentCircle +
    wedge +
    qrCode + '\n\n' +
    '  <!-- Content area -- Focal Point Composition Framework -->\n' +
    '  <g font-family="Inter, system-ui, -apple-system, sans-serif" text-anchor="middle" fill="' + s.text + '">' +
    '    <!-- Top-left: Brand mark (Z-pattern anchor) -->\n' +
    '    <g transform="translate(80,80)"><text font-size="28" font-weight="700" letter-spacing="12" fill="' + s.textMuted + '">VENTURO</text></g>\n\n' +
    '    <!-- Top-right: Sticker/badge label (Z-pattern anchor) -->\n' +
    '    <g transform="translate(680,80)"><path d="M0,0 Q70,-20 140,0 L150,30 L130,60 Q70,40 10,60 L0,30 Z" fill="#FEFEFE" stroke="' + s.accent + '" stroke-width="1.5"/><text x="75" y="40" font-size="22" font-weight="800" fill="' + s.accent + '" text-anchor="middle">' + data.tier_label + '</text></g>\n\n' +
    '    <!-- Center: Main heading (focal point) -->\n' +
    '    <g transform="translate(1024,480)"><text font-size="210" font-weight="900" letter-spacing="-8" fill="url(#tierGrad)">PAKET ' + escapeXml(data.tier_label) + '</text></g>\n\n' +
    '    <!-- Divider rule under heading -->\n' +
    '    <g transform="translate(1024,600)"><line x1="-110" y1="0" x2="-35" y2="0" stroke="' + s.textMuted + '" stroke-width="1.5" opacity="0.4"/><circle cx="0" cy="0" r="4" fill="' + s.accent + '"/><line x1="35" y1="0" x2="110" y2="0" stroke="' + s.textMuted + '" stroke-width="1.5" opacity="0.4"/></g>\n\n' +
    '    <!-- Center: Tagline - mixed weight typography (bold + italic) -->\n' +
    '    <g transform="translate(1024,750)">' +
    '      <tspan font-size="75" font-weight="800" fill="' + s.text + '">' + escapeXml(firstWord) + '</tspan>' +
    taglineRest +
    '    </g>\n\n' +
    '    <!-- Center: Price information pill -->\n' +
    '    <g transform="translate(1024,930)">' +
    '      <rect x="-360" y="-30" width="720" height="60" rx="30" fill="none" stroke="url(#priceGrad)" stroke-width="2"/>' +
    '      <text y="10" font-size="50" font-weight="700" fill="url(#priceGrad)" text-anchor="middle">' + escapeXml(data.price_range) + '</text>' +
    '    </g>\n\n' +
    '    <!-- Center: Audience subtitle (italic) -->\n' +
    '    <g transform="translate(1024,1120)">' +
    '      <text font-family="Playfair Display, Times New Roman, serif" font-size="34" font-weight="400" font-style="italic" fill="' + s.textMuted + '">— ' + escapeXml(data.target_audience) + ' —</text>' +
    '    </g>\n\n' +
    '    <!-- Bottom: CTA button with arrow icon -->\n' +
    '    <g transform="translate(1024,1450)">' +
    '      <rect x="-230" y="-48" width="460" height="96" rx="48" fill="url(#ctaGradient)"/>' +
    '      <g transform="translate(-35,0)"><text y="14" font-size="46" font-weight="700" fill="' + s.ctaText + '" text-anchor="middle">' + escapeXml(data.cta) + '</text></g>' +
    '      <g transform="translate(135,18)" stroke="' + s.ctaText + '" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">' +
    '        <line x1="0" y1="0" x2="24" y2="0"/>' +
    '        <polyline points="15,-8 24,0 15,8"/>' +
    '      </g>' +
    '    </g>\n\n' +
    '    <!-- Footer separator & copyright -->\n' +
    '    <g transform="translate(1024,1880)">' +
    '      <line x1="-150" y1="-5" x2="150" y2="-5" stroke="' + s.textMuted + '" stroke-width="1" opacity="0.3"/>' +
    '      <text y="10" font-size="22" font-weight="600" letter-spacing="2" fill="' + s.textMuted + '" text-anchor="middle">&copy; venturo.id</text>' +
    '    </g>\n' +
    '  </g>\n</svg>';
}

function escapeXml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}