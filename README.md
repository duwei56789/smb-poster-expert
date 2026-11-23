# SMB Poster Expert

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](./.codebuddy-plugin/plugin.json)
[![Platform](https://img.shields.io/badge/platform-WorkBuddy-orange.svg)](https://www.workbuddy.cn)

A WorkBuddy expert pack that turns a small business's brand details into a **clear, ready-to-use poster content plan** — and, on request, renders it into a **print-ready PDF**.

Give it your brand info, campaign theme, target audience, key selling points and required size. It produces a structured copy hierarchy (headline / subhead / selling points / data anchors / CTA), layout and visual direction, an asset checklist and a risk review. When you need the final artwork, the bundled skill renders a print-grade PDF + PNG preview.

**中文文档**: [README.zh-CN.md](./README.zh-CN.md)

---

## Highlights

- **Structured intake** — collects the five core inputs in one pass, without repeatedly interrupting you.
- **Complete copy system** — headline, subheadline, selling points, data anchors and CTA, organized in a clear hierarchy.
- **Layout & visual guidance** — zoning, type scale, color palette, whitespace and hero-image direction.
- **Ready-to-print output** — HTML/CSS + Playwright rendering for commercial posters; a `posterly` workflow for academic posters.
- **Compliance checks** — flags image copyright, data accuracy and placeholder QR codes.

---

## At a glance

| Field | Value |
|---|---|
| Type | Agent (single AI expert) |
| Category | Marketing & Growth (`05-MarketingGrowth`) |
| Profession | Poster Content Strategist |
| Display name | SMB Poster Expert |
| Version | 1.0.2 |

---

## Input parameters

| Parameter | Required | Description |
|---|---|---|
| Brand info | Recommended | Brand name, slogan, industry, primary color, certifications |
| Campaign theme | **Required** | Promotion / grand opening / new product / brand campaign |
| Target audience | Recommended | Demographics, consumption scenario, region |
| Key messages | **Required** | 3–6 core selling points, numbers or offers |
| Poster size | **Required** | e.g. A4 / A3 / A2, roll-up banner, social-media portrait |

Optional: QR code destination, official logo / VI assets, physical store info.

---

## Output

1. **Plan overview** — positioning, hero-image direction, tone
2. **Copy hierarchy** — headline / subhead / selling points / data / CTA
3. **Layout advice** — zoning, type scale, color, whitespace
4. **Asset checklist** — images, QR code / logo to be supplied
5. **Final artwork** — on request: print-ready PDF + PNG preview
6. **Risk notes** — copyright, data accuracy, placeholder QR code

---

## Use cases

Promotional posters · store openings & anniversaries · product launches · brand collateral · recruitment material · social-media portrait images · roll-up banners · academic conference posters

---

## Example prompts

- *I need a promotional poster for a new product — help me draft a content plan.*
- *Design a store event poster based on my brand info and target audience.*
- *Render this poster plan into a print-ready A2 PDF.*

---

## Installation

### As a WorkBuddy expert (recommended)

1. Copy this folder into your local expert directory:

   ```
   C:\Users\<you>\.workbuddy\plugins\marketplaces\my-experts\plugins\smb-poster-expert\
   ```

2. Register it so it appears in **Expert Center → My Experts**:

   ```bash
   python3 scripts/register_expert.py <expert-dir>
   ```

3. Open WorkBuddy, go to the Expert Center, and start a conversation with **SMB Poster Expert**.

### From source

```bash
git clone https://github.com/duwei56789/smb-poster-expert.git
```

---

## Repository structure

```
smb-poster-expert/
├── .codebuddy-plugin/plugin.json        # manifest & display metadata
├── agents/smb-poster-expert.md          # expert definition (the "brain")
├── avatars/expert.png                   # avatar (512x512, <=500KB)
├── skills/poster-generation/
│   ├── SKILL.md                         # generation toolbox
│   ├── references/
│   │   ├── design-playbook.md           # colors, type scale, layout, size chart
│   │   └── posterly-guide.md            # academic poster workflow & gates
│   └── templates/
│       ├── build_skeleton.html          # commercial poster HTML skeleton
│       ├── build.py                     # inject hero image as base64
│       ├── render.py                    # Playwright renderer (PDF + PNG)
│       └── landscape_hero_neutral.html  # academic poster template
└── README.zh-CN.md                      # Chinese documentation
```

The bundled skill provides two rendering paths:

- **Path A — Commercial posters**: HTML/CSS layout + Playwright rendering. Full control over color, spacing and layout.
- **Path B — Academic posters**: the `posterly` workflow with hard layout gates (overflow, alignment, color checks).

---

## Rendering requirements

The final-artwork step needs a local rendering environment:

- Python 3.10+
- Playwright + Chromium
- `pdfinfo` (poppler) for final PDF verification

See `skills/poster-generation/SKILL.md` and `references/posterly-guide.md` for setup details and common pitfalls (base64 image embedding, watermark masking, gate tuning, pip mirror selection, etc.).

---

## Notes

- Never fabricate data, certifications or slogans — source them from the user or public information, and mark anything uncertain as *to be confirmed*.
- For commercial use, prefer official brand assets; mask watermarks on AI-generated images.
- The avatar can be replaced: PNG/JPG, 512×512 px, ≤500 KB.
- `posterly` is licensed under **AGPL-3.0**. Distributing a modified version as a SaaS / network service requires releasing the full source.
