# JetBright Pressure Washing — Static Site

Same engine as TipRun, completely different business. 56 files: homepage,
50 suburb pages, locations index, 404, sitemap, robots.

## Before you publish
1. Formspree endpoint is already set (xaqrkrqb) — separate form from TipRun so
   the two lead streams stay in separate inboxes/dashboards.
   No file uploads: the form collects name, phone, suburb, surface, size and
   condition. You text the customer for a photo, then quote.
2. Edit generate.py CONFIG: BASE_URL (your new domain), DOMAIN (for CNAME).
3. Run: python3 generate.py
4. New GitHub repo (separate from TipRun) -> upload docs/, generate.py, README.md
   -> Settings -> Pages -> branch main, folder /docs -> add custom domain.
5. DNS at your registrar: same 4 GitHub A records as before + CNAME www -> YOURUSERNAME.github.io
6. Google Search Console: verify the new domain, submit sitemap.xml.

## SMS links
All "Text a photo" buttons use sms:+61410642507 — on mobile they open the
messaging app pre-addressed to you. On desktop they may do nothing (normal).
