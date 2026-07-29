# Venturo Skill Project

This project contains context data for generating Venturo Service Package posters.

## How to Use the Poster Skill

After opening this folder in Claude Code or OpenCode, you can use the **venturo-poster** skill directly with trigger phrases like:

- `design venturo poster starter` → Generate Starter package poster
- `create venturo growth package poster` → Generate Growth package poster  
- `design venturo enterprise poster` → Generate Enterprise package poster

The skill follows the poster-design workflow (Z-pattern layout, 2048×2048 HD canvas) with venturo-specific content from `packages_context.md`.

## Data File

- `packages_context.md` — Contains tier descriptions, team structures, timelines, budget ranges, and color palette reference for all three packages.

## Dependencies

- Uses the installed `poster-design` skill as foundation
- Color palette referenced: Primary Teal `#006D79`, CTA Green `#10B981`, CTA Gold `#F59E0B`

## Notes

All posters are rendered at 2048��2048px square with Device Scale Factor 2 (output 4096×4096px). Layout follows Z-Pattern: Logo (top-left) → Tier Name (top-right) → Content (left-center) → CTA Button (bottom-right).
