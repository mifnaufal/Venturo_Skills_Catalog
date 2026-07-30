---
name: venturo-poster
description: >
  Generate Venturo Service Package posters (Starter, Growth, Enterprise)
  using the project's brand context from packages_context.md. Delegates the
  actual design/render to the global canvas-design skill, producing a
  premium visual philosophy expressed as PNG/PDF output sized 2048x2048.
  Trigger phrases: "design venturo poster", "create venturo package poster",
  "venturo starter poster", "venturo growth poster", "venturo enterprise poster",
  "buatkan poster paket venturo".
license: MIT
---

# Venturo Service Package Poster

Generate a single premium poster for one Venturo tier. Brand context lives in
`packages_context.md` at the project root; actual design and rendering are
performed by the `canvas-design` skill (installed globally), which produces a
museum-quality design philosophy expressed as a PNG or PDF file.

## When to use

User asks for a Venturo service package poster, specifies a tier
(Starter / Growth / Enterprise), or accepts the default.

## Workflow

1. Locate the project root and read `packages_context.md` (the path is
   project-relative).
2. Confirm the tier with the user if ambiguous. Default: **Starter**.
3. Extract from `packages_context.md`:
   - For the chosen tier: "Ideal untuk", "Budget Proyek", "Dedicated Team",
     "Timeline" rows
   - The full "Color Palette Reference" table (Primary Teal `#006D79`,
     Primary Light `#009BAD`, Dark BG `#0A1B1F`, CTA Green `#10B981`, etc.)
4. Compose a single free-text instruction containing:
   - Tier content fields above (verbatim where possible)
   - Brand color palette (hex codes) — these are anchor tones, not the
     whole composition
   - Canvas: square, 2048 x 2048 PNG
   - Style direction: clean modern teal-themed Indonesian service
     package poster, Z-pattern layout, CTA "Konsultasi Gratis" in
     `#10B981` (or "Hubungi Kami" in `#F59E0B` for Enterprise)
   - Tier-specific headline: "PAKET STARTER" / "PAKET GROWTH" /
     "PAKET ENTERPRISE"
5. Invoke the `canvas-design` skill via the Skill tool, passing the
   composed instruction verbatim. Do not paraphrase the package facts.
6. The `canvas-design` skill handles philosophy creation + canvas render.
   Output is a .md (philosophy) + .png or .pdf (poster) in the working
   directory.
7. If the user asks for a second tier, repeat the workflow; do not
   batch tiers in a single `canvas-design` call.

## Notes

- This skill does NOT render the poster itself. All rendering is
  delegated to `canvas-design`.
- If `packages_context.md` is missing, refuse and point the user to
  the file before continuing.
- If the `canvas-design` skill is not installed globally, instruct
  the user to install it before retrying.