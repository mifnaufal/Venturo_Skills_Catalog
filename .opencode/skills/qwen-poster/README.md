# Qwen Poster Generator

Auto-generate promotional posters via Qwen Chat (chat.qwen.ai).

## Quick Start

```bash
# Generate a poster (headless)
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs generate \
  --headless \
  --prompt "Design a premium modern Indonesian service-package poster for AC repair services. Colors: teal #006D79 and green #10B981."

# Manual login (if needed)
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs login

# Debug UI (dump visible elements)
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs detect
```

## Flow

1. **Login Detection**: Check top-right corner for "NAUFAL IDN" (or similar)
   - If "Log in" button visible → not logged in
   - If user avatar/name visible → logged in

2. **Enter Image Mode**: Click Select Mode → Create Image

3. **Model Selection**: Click model selector → Qwen-Image 3.0 (fallback to 2.0)

4. **Aspect Ratio**: Click size selector → 1:1

5. **Send Prompt**: Fill textarea and press Enter

6. **Wait for Generation**: Poll for `cdn.qwenlm.ai` images (not attachment previews)

7. **Download**: Auto-download generated image

8. **Limit Detection**: If rate limit hit, exit with clear error message

## Config

`.claude/skills/qwen-poster/config.json`:
```json
{
  "email": "naufalidn2009@gmail.com",
  "password": "NaufalHd12!",
  "useLogo": false,
  "model": "Qwen-Image 3.0",
  "aspectRatio": "1:1"
}
```

## Requirements

- Node.js v24+
- Playwright `^1.62.1` (installed)
- Persistent Chrome profile at `.qwen-profile/`

## Known Limitations

- **Daily usage limit**: Qwen free tier has limits. If hit, wait ~15-24h or use different account.
- **No logo by default**: Logo upload causes generation hangs. Enable via `useLogo: true` in config.

## File Structure

```
.claude/skills/qwen-poster/
├── config.json          # Account + settings
├── README.md            # This file
├── scripts/
│   ├── qwen-poster.mjs  # Main script
│   └── prompts.js       # Prompt templates
└── SKILL.md             # Original skill spec
```
