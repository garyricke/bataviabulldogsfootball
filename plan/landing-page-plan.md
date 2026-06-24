# Batavia Bulldogs Football — Brand Guide + Landing Page Plan

_Approved 2026-06-12. Stack: static HTML/CSS/JS. Scope: full long-scroll landing page. Imagery: placeholders (Cloudinary-ready)._

## Brand foundation (authentic identity)
- **School colors:** Crimson `#A6192E` + Gold `#C9A227` (NOT the navy from the Squarespace mockup — that's a template default).
- **Nickname:** Bulldogs / "Battlin' Bulldogs". Conference: DuKane.
- **Tradition:** State Champions 2013 (6A) & 2017 (7A); 2024 7A Runner-Up; playoff history back to 1991.
- **Motto:** "For Your Team, For Your Town."

## Research synthesis
- **Squarespace mockup:** polished marketing flow — hero → credibility → schedule+tickets → past video → coaches → resources → sponsors → youth → contact.
- **Live bps101 site:** deep data hub (history, all-staters 1994+, stats, livestream, social) but a wall of Google links; dated, poor mobile hierarchy.
- **Best practice:** action hero, scannable schedule, audience segmentation (players/parents/fans/recruits), mobile-first (60%+), easy ticketing, storytelling/championships, accessibility.
- **Strategy:** marry the polished flow with the deep archive — surface credibility + key actions, tuck the archive behind clean labeled entry points.

## Deliverables
- `brand-guide.html` — living brand system (colors, type, logo, voice, components).
- `index.html` — long-scroll landing page.
- `styles.css` — shared tokens + component kit.
- `/assets` — SVG logo placeholder; Cloudinary-ready image slots.

## Landing page sections
1. Sticky nav + persistent Buy Tickets
2. Hero (action, motto, credibility strip, CTAs)
3. Season schedule (rows, results, ticket/Hudl links)
4. Quick-action band (Watch Live / Stats / Roster / Camps)
5. The Program + coaches
6. Tradition & History timeline
7. Youth Football pipeline
8. Sponsors grid + become-a-sponsor
9. Footer (social, contact, links)

## Build order
brand-guide.html → styles.css → index.html → responsive/a11y pass.
