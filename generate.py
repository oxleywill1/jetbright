#!/usr/bin/env python3
"""
Static site generator — JetBright Pressure Washing
Edit CONFIG + SUBURBS, run `python3 generate.py`, push /docs to GitHub Pages.
"""
import os, html, json

# ============================================================
# CONFIG
# ============================================================
BIZ      = "JetBright Pressure Washing"
PHONE    = "0410 642 507"
SMS_A    = "sms:+61410642507"                 # opens messaging app pre-addressed
BASE_URL = "https://jetbright.homes"          # custom domain, no trailing slash
DOMAIN   = "jetbright.homes"                  # writes the CNAME file GitHub Pages needs
FORM_URL = "https://formspree.io/f/xaqrkrqb"  # JetBright form (separate from TipRun's)
OUT      = "docs"

# ============================================================
# SUBURBS — pressure-washing-specific notes & services per area
# ============================================================
SUBURBS = [
 # --- Sydney ---
 dict(n="Parramatta", c="Sydney", s="NSW", p="2150", note="Western Sydney heat bakes grime into concrete fast — Parramatta driveways and shopfronts come up like new after a proper hot-water blast.", jobs=["Driveway & concrete","Shopfront cleaning","House soft wash"]),
 dict(n="Bondi", c="Sydney", s="NSW", p="2026", note="Salt spray coats everything east of Bondi Road — we strip the salt film and green tinge off render, balconies and paths before it eats the paint.", jobs=["Salt & render wash","Balcony & paths","Roof cleaning"]),
 dict(n="Penrith", c="Sydney", s="NSW", p="2750", note="Big Penrith blocks mean long driveways and wide patios — dusty summers and muddy winters both end up ground into the concrete until we blast it out.", jobs=["Long driveways","Patio & pergola","Colorbond fence wash"]),
 dict(n="Blacktown", c="Sydney", s="NSW", p="2148", note="Blacktown's mix of older concrete drives and newer exposed-aggregate needs different pressures — we tune the machine to the surface so nothing gets etched.", jobs=["Exposed aggregate","Driveway cleaning","House wash"]),
 dict(n="Liverpool", c="Sydney", s="NSW", p="2170", note="New builds around Liverpool and Edmondson Park cop builder's dust and tyre marks from day one — a first proper wash makes the whole street notice.", jobs=["New-build first wash","Driveway cleaning","Render soft wash"]),
 dict(n="Chatswood", c="Sydney", s="NSW", p="2067", note="Shaded North Shore blocks grow moss and lichen like a hobby — Chatswood paths and south-facing walls need a treated soft wash, not just raw pressure.", jobs=["Moss & lichen treatment","Path cleaning","House soft wash"]),
 dict(n="Manly", c="Sydney", s="NSW", p="2095", note="Between salt air and morning damp, Manly decks and balustrades go grey-green fast — we bring them back and rinse the salt off glass and frames too.", jobs=["Deck restoration","Glass & balustrade","Salt wash-down"]),
 dict(n="Castle Hill", c="Sydney", s="NSW", p="2154", note="Hills District homes with big render facades and long paver drives — we soft wash the walls and pressure clean the pavers in one visit.", jobs=["Render soft wash","Paver cleaning","Gutter & eaves"]),
 dict(n="Bankstown", c="Sydney", s="NSW", p="2200", note="Bankstown landlords use us between tenants — driveways, paths and a full house wash lift a rental listing more than a coat of paint.", jobs=["Pre-listing wash","Driveway cleaning","Unit block common areas"]),
 dict(n="Sutherland", c="Sydney", s="NSW", p="2232", note="Gum trees over every Shire driveway means sap, leaf stains and bark tannins — stubborn marks that need heat and the right chemicals, which we carry.", jobs=["Sap & tannin stains","Driveway cleaning","Deck & outdoor area"]),
 dict(n="Ryde", c="Sydney", s="NSW", p="2112", note="Ryde's older brick homes come up beautifully — we wash decades of traffic film off brickwork without blowing out the mortar.", jobs=["Brick restoration wash","Path & steps","Roof cleaning"]),
 dict(n="Newtown", c="Sydney", s="NSW", p="2042", note="Terrace facades, tiled verandahs and graffiti — inner-west jobs are detail work, and we're careful around heritage paint and old mortar.", jobs=["Terrace facade wash","Graffiti removal","Tiled verandahs"]),
 # --- Melbourne ---
 dict(n="Richmond", c="Melbourne", s="VIC", p="3121", note="Richmond's brick cottages and factory conversions wear a century of Melbourne grime — a careful wash takes the buildings back decades.", jobs=["Brick & heritage wash","Warehouse floors","Graffiti removal"]),
 dict(n="St Kilda", c="Melbourne", s="VIC", p="3182", note="Sea air plus foot traffic makes St Kilda paths, art-deco facades and cafe strips slick and grey — we do early-morning commercial washes before opening.", jobs=["Cafe & shopfront","Facade soft wash","Footpath degrease"]),
 dict(n="Footscray", c="Melbourne", s="VIC", p="3011", note="Inner-west renovators call us for the finishing touch — washing render dust and boot marks off new surfaces, and reviving the old concrete they kept.", jobs=["Post-reno wash","Concrete revival","Fence & gate wash"]),
 dict(n="Brunswick", c="Melbourne", s="VIC", p="3056", note="Brunswick's shopfronts, roller doors and laneway walls collect grime and tags — we handle graffiti removal and scheduled storefront washes.", jobs=["Graffiti removal","Shopfront cleaning","Roller door wash"]),
 dict(n="Dandenong", c="Melbourne", s="VIC", p="3175", note="Factories and warehouses around Dandenong need forecourt degreasing, awning washes and line-marking prep — industrial work is our bread and butter here.", jobs=["Forecourt degrease","Warehouse washing","Awning & signage"]),
 dict(n="Frankston", c="Melbourne", s="VIC", p="3199", note="Bayside damp turns Frankston driveways and pool surrounds slippery green — we clean and treat so the slime stays gone longer.", jobs=["Pool surrounds","Driveway cleaning","Anti-slip treatment"]),
 dict(n="Box Hill", c="Melbourne", s="VIC", p="3128", note="Box Hill's older clinker-brick homes and mossy south sides scrub up brilliantly — soft wash for the walls, pressure for the paths.", jobs=["Clinker brick wash","Moss treatment","Path & steps"]),
 dict(n="Werribee", c="Melbourne", s="VIC", p="3030", note="New estates across Wyndham mean fresh concrete that shows every mark — we lift tyre scuffs, rust stains and builder's residue without etching.", jobs=["New concrete care","Tyre mark removal","House wash"]),
 dict(n="Preston", c="Melbourne", s="VIC", p="3072", note="Preston's mix of weatherboard and brick veneer both wash up well — we adjust from gentle soft wash to full pressure across a single property.", jobs=["Weatherboard soft wash","Driveway cleaning","Gutter & eaves"]),
 dict(n="Glen Waverley", c="Melbourne", s="VIC", p="3150", note="Pre-sale washes are the Glen Waverley specialty — agents tell us a bright driveway and clean facade adds real money at auction.", jobs=["Pre-auction wash","Driveway & paths","Render soft wash"]),
 dict(n="Craigieburn", c="Melbourne", s="VIC", p="3064", note="Craigieburn's new homes cop red dust and construction traffic — a seasonal wash keeps render, garage doors and driveways looking new-estate fresh.", jobs=["Render & garage door","Driveway cleaning","Fence wash"]),
 dict(n="Cranbourne", c="Melbourne", s="VIC", p="3977", note="Acreage properties around Cranbourne mean big sheds, long drives and machinery pads — we bring extra hose and a bigger water tank.", jobs=["Shed & machinery pads","Long driveways","House wash"]),
 # --- Brisbane ---
 dict(n="Fortitude Valley", c="Brisbane", s="QLD", p="4006", note="Valley venues and offices get gum, spills and Friday night's leftovers — we do pre-dawn washes so footpaths are spotless by opening.", jobs=["Venue & footpath","Gum removal","Graffiti removal"]),
 dict(n="Chermside", c="Brisbane", s="QLD", p="4032", note="Brisbane humidity feeds mould on every shaded Chermside wall — our soft wash kills it at the root instead of just pushing it around.", jobs=["Mould soft wash","Driveway cleaning","Roof cleaning"]),
 dict(n="Ipswich", c="Brisbane", s="QLD", p="4305", note="Ipswich Queenslanders with timber walls and iron rooves need low-pressure care — we wash a century-old home without lifting the paint.", jobs=["Queenslander soft wash","Roof cleaning","Under-house concrete"]),
 dict(n="Logan Central", c="Brisbane", s="QLD", p="4114", note="Logan rental turnovers move fast — a same-week driveway and house wash gets properties photographed and listed sooner.", jobs=["Rental turnover wash","Driveway cleaning","Path & patio"]),
 dict(n="Carindale", c="Brisbane", s="QLD", p="4152", note="Carindale's rendered family homes and pool areas wear storm-season mould fast — an annual soft wash keeps the render bright and the pavers safe.", jobs=["Render soft wash","Pool surrounds","Driveway cleaning"]),
 dict(n="Indooroopilly", c="Brisbane", s="QLD", p="4068", note="Steep western-suburbs blocks mean retaining walls, stairs and shaded paths — slippery in the wet until we clean and treat them.", jobs=["Retaining walls","Stairs & paths","Anti-slip treatment"]),
 dict(n="Redcliffe", c="Brisbane", s="QLD", p="4020", note="Peninsula salt air films over glass, render and driveways — a regular JetBright wash-down keeps Redcliffe homes bright against the sea air.", jobs=["Salt wash-down","Driveway cleaning","Glass & frames"]),
 dict(n="Springfield", c="Brisbane", s="QLD", p="4300", note="Springfield's newer estates show every tyre mark on pale concrete — we specialise in lifting marks without leaving wand stripes.", jobs=["Pale concrete care","Tyre mark removal","House wash"]),
 # --- Perth ---
 dict(n="Fremantle", c="Perth", s="WA", p="6160", note="Freo limestone and heritage brick need a gentle touch — we wash the port-town grime off without damaging soft old stone.", jobs=["Limestone care wash","Heritage brick","Graffiti removal"]),
 dict(n="Joondalup", c="Perth", s="WA", p="6027", note="Northern-corridor homes with big paved alfresco areas — Perth sun bakes in BBQ grease and red dust until we steam it out.", jobs=["Alfresco & paving","BBQ area degrease","Driveway cleaning"]),
 dict(n="Rockingham", c="Perth", s="WA", p="6168", note="Coastal Rockingham cops salt and sand year-round — we rinse the corrosion-feeding salt off render, glass and colorbond before it costs you.", jobs=["Salt wash-down","Colorbond & render","Driveway cleaning"]),
 dict(n="Midland", c="Perth", s="WA", p="6056", note="Workshops and older homes around Midland mean oil stains and decades-old concrete — heat plus degreaser gets results cold water never will.", jobs=["Oil stain removal","Workshop floors","House wash"]),
 dict(n="Cannington", c="Perth", s="WA", p="6107", note="Cannington commercial strips and warehouses book us for scheduled forecourt and awning washes — customers judge a business by its frontage.", jobs=["Commercial frontage","Forecourt degrease","Awning wash"]),
 dict(n="Scarborough", c="Perth", s="WA", p="6019", note="Beachfront apartments and Scarborough's coastal homes need regular salt rinses — balconies, glass and painted render especially.", jobs=["Balcony & glass","Salt wash-down","Common area wash"]),
 # --- Adelaide ---
 dict(n="Glenelg", c="Adelaide", s="SA", p="5045", note="Bay-side villas and apartment blocks wear salt film and gull mess — we keep Glenelg facades, paths and balconies holiday-bright.", jobs=["Facade wash","Balcony cleaning","Path & forecourt"]),
 dict(n="Norwood", c="Adelaide", s="SA", p="5067", note="Norwood bluestone and heritage brick need careful pressure — we lift the grime and leave the 150-year-old mortar exactly where it was.", jobs=["Bluestone care","Heritage brick wash","Verandah tiles"]),
 dict(n="Salisbury", c="Adelaide", s="SA", p="5108", note="Big northern-suburbs blocks with long drives and sheds — Salisbury jobs get the big machine, the water tank and the whole afternoon.", jobs=["Long driveways","Shed wash","House wash"]),
 dict(n="Marion", c="Adelaide", s="SA", p="5043", note="Pre-sale and rental washes keep us busy around Marion — agents book us because a clean drive photographs like a renovation.", jobs=["Pre-listing wash","Driveway cleaning","Path & patio"]),
 dict(n="Port Adelaide", c="Adelaide", s="SA", p="5015", note="The Port's warehouses, worker's cottages and salt air are a triple threat — we do industrial floors and heritage facades in the same week.", jobs=["Warehouse floors","Heritage facade","Salt wash-down"]),
 # --- Gold Coast ---
 dict(n="Southport", c="Gold Coast", s="QLD", p="4215", note="High-rise podiums, canal-front patios and body-corporate common areas — Southport strata work is our specialty, insurance paperwork included.", jobs=["Strata common areas","Canal-front patios","Driveway cleaning"]),
 dict(n="Surfers Paradise", c="Gold Coast", s="QLD", p="4217", note="Holiday buildings in Surfers need constant presentation — we wash entries, pool decks and balconies on schedules that dodge check-in times.", jobs=["Pool deck wash","Building entries","Balcony cleaning"]),
 dict(n="Robina", c="Gold Coast", s="QLD", p="4226", note="Robina's rendered homes and shaded south walls grow Gold Coast mould fast — an annual soft wash keeps it off for good.", jobs=["Render soft wash","Mould treatment","Driveway cleaning"]),
 # --- Canberra ---
 dict(n="Belconnen", c="Canberra", s="ACT", p="2617", note="Canberra frosts break down concrete sealer and feed winter moss — Belconnen drives and paths need a clean and re-treat come spring.", jobs=["Spring driveway clean","Moss treatment","House wash"]),
 dict(n="Woden", c="Canberra", s="ACT", p="2606", note="Established Woden Valley gardens drop leaf tannin stains all over paths and pergolas — stubborn marks we shift with heat and the right mix.", jobs=["Tannin stain removal","Pergola & paths","Gutter & eaves"]),
 # --- Hobart ---
 dict(n="Glenorchy", c="Hobart", s="TAS", p="7010", note="Hobart's cool damp grows moss and lichen faster than anywhere on the mainland — Glenorchy paths and rooves need treatment, not just blasting.", jobs=["Moss & lichen","Roof cleaning","Driveway cleaning"]),
 # --- Newcastle ---
 dict(n="Charlestown", c="Newcastle", s="NSW", p="2290", note="Lake Macquarie humidity plus coastal air means green driveways and salt-filmed windows — Charlestown homes book us yearly and it shows.", jobs=["Driveway cleaning","Salt wash-down","House soft wash"]),
]

def slug(s): return s.lower().replace(" ", "-").replace("'", "")
for sb in SUBURBS: sb["slug"] = slug(sb["n"])
CITIES = []
for sb in SUBURBS:
    if sb["c"] not in CITIES: CITIES.append(sb["c"])

# ============================================================
# CSS — clean/water design: navy ink, jet aqua, bright white
# ============================================================
CSS = """
:root{
  --navy:#0b2239; --aqua:#00b4d8; --deep:#0077b6; --white:#ffffff;
  --mist:#eef6fa; --slate:#5b7185; --line:#d7e5ee; --grime:#3d4148;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{font-family:'Manrope',system-ui,sans-serif;background:var(--white);color:var(--navy);line-height:1.65;font-size:17px}
.display{font-family:'Outfit',system-ui,sans-serif;font-weight:800;letter-spacing:-.02em;line-height:1.02}
a{color:inherit}
.wrap{max-width:1100px;margin:0 auto;padding:0 24px}
a:focus-visible,button:focus-visible{outline:3px solid var(--aqua);outline-offset:2px}
/* clean-line divider: grime fading to clean */
.cleanline{height:8px;background:linear-gradient(90deg,var(--grime) 0%,var(--grime) 38%,var(--aqua) 50%,var(--mist) 62%,var(--white) 100%)}
/* header */
header{background:var(--white);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.nav{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;max-width:1100px;margin:0 auto;gap:16px}
.logo{font-family:'Outfit',sans-serif;font-weight:800;font-size:22px;text-decoration:none;letter-spacing:-.02em}
.logo em{color:var(--aqua);font-style:normal}
.nav-links{display:flex;gap:22px;list-style:none;font-size:15px;font-weight:600}
.nav-links a{text-decoration:none;color:var(--slate)}
.nav-links a:hover,.nav-links a:focus{color:var(--deep)}
.sms-btn{background:var(--navy);color:var(--white);font-weight:800;font-size:15px;text-decoration:none;padding:11px 20px;border-radius:999px;white-space:nowrap}
.sms-btn:hover,.sms-btn:focus{background:var(--deep)}
/* hero — diagonal grime-to-clean split */
.hero{position:relative;color:var(--white);padding:84px 0 76px;background:linear-gradient(112deg,var(--grime) 0%,#22303c 46%,var(--deep) 60%,var(--aqua) 100%);overflow:hidden}
.hero::after{content:"";position:absolute;top:-20%;bottom:-20%;left:52%;width:6px;background:var(--white);transform:rotate(22deg);opacity:.85}
.hero .wrap{position:relative;z-index:2}
.hero .eyebrow{color:var(--aqua);font-size:14px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;margin-bottom:18px}
.hero h1{font-size:clamp(42px,7.5vw,88px);color:var(--white)}
.hero h1 .hl{color:var(--aqua)}
.hero p.lede{max-width:540px;margin:24px 0 32px;font-size:19px;color:#dbe9f2}
.hero-ctas{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.btn-big{background:var(--aqua);color:var(--navy);font-family:'Outfit',sans-serif;font-weight:800;font-size:19px;text-decoration:none;padding:16px 30px;border-radius:999px}
.btn-big:hover,.btn-big:focus{background:var(--white)}
.btn-ghost{border:2px solid rgba(255,255,255,.5);color:var(--white);font-family:'Outfit',sans-serif;font-weight:800;font-size:19px;text-decoration:none;padding:14px 30px;border-radius:999px}
.btn-ghost:hover,.btn-ghost:focus{border-color:var(--aqua);color:var(--aqua)}
.hero-note{font-size:14px;color:#bcd4e4;margin-top:16px}
/* sections */
section{padding:76px 0}
.sec-label{display:inline-block;color:var(--deep);background:var(--mist);font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;padding:6px 14px;border-radius:999px;margin-bottom:16px}
h2.display{font-size:clamp(30px,4.5vw,50px);margin-bottom:16px}
.sub{color:var(--slate);max-width:640px;margin-bottom:36px}
/* services grid */
.svc{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}
.svc div{background:var(--mist);border:1px solid var(--line);border-radius:14px;padding:22px}
.svc h3{font-family:'Outfit',sans-serif;font-weight:800;font-size:18px;margin-bottom:6px}
.svc p{font-size:14px;color:var(--slate)}
/* before/after strip */
.ba{border-radius:14px;overflow:hidden;border:1px solid var(--line);display:grid;grid-template-columns:1fr 1fr}
.ba div{padding:26px;font-family:'Outfit',sans-serif;font-weight:800;letter-spacing:.06em;text-transform:uppercase;font-size:14px}
.ba .b{background:linear-gradient(100deg,var(--grime),#59606a);color:#c8cdd4}
.ba .a{background:linear-gradient(100deg,var(--mist),var(--white));color:var(--deep);text-align:right}
/* steps */
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:28px}
.step .tick{width:46px;height:46px;border-radius:50%;background:var(--aqua);color:var(--navy);font-family:'Outfit',sans-serif;font-weight:800;font-size:20px;display:flex;align-items:center;justify-content:center}
.step h3{font-family:'Outfit',sans-serif;font-weight:800;font-size:20px;margin:12px 0 8px}
.step p{color:var(--slate);font-size:15px}
/* areas */
.city-block{margin-bottom:34px}
.city-block h3{font-family:'Outfit',sans-serif;font-weight:800;font-size:21px;border-bottom:3px solid var(--aqua);display:inline-block;margin-bottom:14px}
.area-grid{display:flex;flex-wrap:wrap;gap:10px}
.area-grid a{background:var(--mist);border:1px solid var(--line);border-radius:999px;padding:8px 16px;font-size:15px;text-decoration:none;font-weight:600}
.area-grid a:hover,.area-grid a:focus{background:var(--aqua);border-color:var(--aqua);color:var(--navy)}
/* form */
.quote-form{border:1px solid var(--line);background:var(--mist);border-radius:16px;padding:30px;max-width:560px}
.ff{margin-bottom:18px}
.ff label{display:block;font-weight:800;font-size:13px;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;color:var(--deep)}
.ff input,.ff select{width:100%;border:1.5px solid var(--line);background:var(--white);border-radius:10px;padding:12px 14px;font:inherit;font-size:16px}
.ff input:focus,.ff select:focus{outline:none;border-color:var(--aqua)}
.ff select{cursor:pointer;appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--deep) 50%),linear-gradient(135deg,var(--deep) 50%,transparent 50%);background-position:calc(100% - 20px) 55%,calc(100% - 14px) 55%;background-size:6px 6px;background-repeat:no-repeat}
.ff .hint{font-size:13px;color:var(--slate);margin-top:5px}
.form-split{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
@media(max-width:820px){.form-split{grid-template-columns:1fr}}
.form-btn{background:var(--navy);color:var(--white);font-family:'Outfit',sans-serif;font-weight:800;font-size:18px;border:none;border-radius:999px;padding:15px 28px;width:100%;cursor:pointer}
.form-btn:hover,.form-btn:focus{background:var(--deep)}
/* faq */
.faq details{background:var(--white);border:1px solid var(--line);border-radius:12px;margin-bottom:10px}
.faq summary{padding:16px 20px;font-weight:700;cursor:pointer;list-style:none}
.faq summary::after{content:"+";float:right;font-family:'Outfit',sans-serif;font-weight:800;font-size:20px;color:var(--aqua)}
.faq details[open] summary::after{content:"–"}
.faq details p{padding:0 20px 18px;color:var(--slate)}
/* cta band */
.cta-band{background:linear-gradient(112deg,var(--navy),var(--deep));color:var(--white);text-align:center;padding:64px 24px}
.cta-band h2{font-size:clamp(30px,5vw,54px);color:var(--white);margin-bottom:10px}
.cta-band .hl{color:var(--aqua)}
.cta-band p{color:#bcd4e4;margin-bottom:28px}
/* footer */
footer{background:var(--navy);color:#8fa6b8;font-size:14px}
.foot{max-width:1100px;margin:0 auto;padding:36px 24px;display:flex;flex-wrap:wrap;gap:28px;justify-content:space-between}
.foot a{color:#cfe0ec;text-decoration:none}
.foot a:hover{color:var(--aqua)}
.foot-areas{max-width:1100px;margin:0 auto;padding:0 24px 36px;font-size:13px;line-height:2}
.foot-areas a{color:#7590a5;text-decoration:none;margin-right:14px}
.foot-areas a:hover{color:var(--aqua)}
/* suburb page */
.jobs-chips{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 0}
.jobs-chips span{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);color:var(--white);font-size:14px;padding:7px 16px;border-radius:999px;font-weight:700}
.two-col{display:grid;grid-template-columns:1.2fr .8fr;gap:48px}
@media(max-width:820px){.two-col{grid-template-columns:1fr}}
.side-card{border:1px solid var(--line);background:var(--mist);border-radius:16px;padding:26px;height:fit-content}
.side-card h3{font-family:'Outfit',sans-serif;font-weight:800;font-size:19px;margin-bottom:12px}
.side-card ul{list-style:none}
.side-card li{padding:7px 0;border-bottom:1px solid var(--line)}
.side-card li a{text-decoration:none;font-weight:600}
.side-card li a:hover{color:var(--deep);text-decoration:underline}
"""

# ============================================================
# Building blocks
# ============================================================
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">'

def head(title, desc, canonical, css_path, extra_schema=""):
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
{FONTS}
<link rel="stylesheet" href="{css_path}style.css">
{extra_schema}
</head>
<body>"""

def header_nav(root=""):
    return f"""<header>
<nav class="nav" aria-label="Main">
  <a class="logo" href="{root}index.html">Jet<em>Bright</em></a>
  <ul class="nav-links">
    <li><a href="{root}index.html#services">Services</a></li>
    <li><a href="{root}index.html#quote">Get a quote</a></li>
    <li><a href="{root}locations/index.html">Service areas</a></li>
  </ul>
  <a class="sms-btn" href="{SMS_A}">Text a photo: {PHONE}</a>
</nav>
</header>
<div class="cleanline" aria-hidden="true"></div>"""

def quote_form(suburb=None):
    sub_val = f' value="{suburb}"' if suburb else ' placeholder="e.g. Frankston"'
    return f"""<form class="quote-form" action="{FORM_URL}" method="POST">
  <div class="ff"><label for="qf-name">Your name</label><input id="qf-name" type="text" name="name" required autocomplete="name"></div>
  <div class="ff"><label for="qf-phone">Mobile number</label><input id="qf-phone" type="tel" name="phone" required autocomplete="tel"><p class="hint">We'll text you back to grab a photo and send your quote.</p></div>
  <div class="ff"><label for="qf-suburb">Suburb</label><input id="qf-suburb" type="text" name="suburb" required{sub_val}></div>
  <div class="ff"><label for="qf-surface">What needs washing?</label>
    <select id="qf-surface" name="surface" required>
      <option value="" disabled selected>Choose one…</option>
      <option>Driveway or concrete</option>
      <option>House walls (render/brick/weatherboard)</option>
      <option>Roof</option>
      <option>Deck, fence or pergola</option>
      <option>Paths, patio or pool surrounds</option>
      <option>Shopfront or commercial</option>
      <option>Graffiti removal</option>
      <option>A few different areas</option>
    </select></div>
  <div class="ff"><label for="qf-size">Roughly how big is the area?</label>
    <select id="qf-size" name="area_size" required>
      <option value="" disabled selected>Choose one…</option>
      <option>Small — single car space or one wall</option>
      <option>Medium — standard driveway or a few walls</option>
      <option>Large — long driveway or whole house</option>
      <option>Very large — acreage or commercial site</option>
      <option>Not sure</option>
    </select></div>
  <div class="ff"><label for="qf-state">How bad is it?</label>
    <select id="qf-state" name="condition" required>
      <option value="" disabled selected>Choose one…</option>
      <option>Light — general dust and dirt</option>
      <option>Moderate — visible grime or green patches</option>
      <option>Heavy — thick moss, mould or black stains</option>
      <option>Oil, rust or specific stains</option>
    </select></div>
  <button type="submit" class="form-btn">Get my quote</button>
  <p class="hint" style="margin-top:12px">Fastest way? Text a photo straight to <a href="{SMS_A}"><strong>{PHONE}</strong></a> and we'll reply with a fixed price.</p>
</form>"""

def steps():
    return f"""<div class="steps">
  <div class="step"><div class="tick">1</div><h3>Snap a photo</h3><p>Driveway, wall, roof, deck — one photo from your phone shows us everything we need.</p></div>
  <div class="step"><div class="tick">2</div><h3>Text it or send the form</h3><p>Text it to {PHONE} or upload it here. Either way, we text back a fixed quote — fast.</p></div>
  <div class="step"><div class="tick">3</div><h3>We blast it clean</h3><p>We turn up with our own water, hot-wash gear and the right pressure for your surface.</p></div>
</div>"""

SERVICES = [
 ("Driveways & concrete","Oil, tyre marks, moss and years of grime — hot water and surface cleaners leave concrete stripe-free."),
 ("House soft washing","Low pressure, right chemicals. Kills mould at the root on render, weatherboard and brick without damage."),
 ("Roof cleaning","Moss, lichen and black streaks removed gently — your roof looks new without losing a tile."),
 ("Decks, fences & pergolas","Timber and composite brought back from grey, ready to re-oil or just enjoy."),
 ("Paths, patios & pool surrounds","Slippery green gone, with anti-slip treatments that keep it gone."),
 ("Commercial & shopfronts","Footpaths, awnings, forecourts and graffiti — scheduled or one-off, before your doors open."),
]
def services():
    cells = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t,d in SERVICES)
    return f'<div class="svc">{cells}</div>'

def footer_block(root=""):
    links = " ".join(f'<a href="{root}locations/{s["slug"]}.html">{s["n"]}</a>' for s in SUBURBS)
    return f"""<div class="cta-band">
  <h2 class="display">One photo. <span class="hl">One quote.</span></h2>
  <p>Text a photo of the job and we'll reply with a fixed price — free quotes, 7 days.</p>
  <a class="btn-big" href="{SMS_A}">Text a photo to {PHONE}</a>
</div>
<footer>
  <div class="foot">
    <div><strong style="color:#fff">{BIZ}</strong><br>Driveways, homes, rooves &amp; commercial — washed right, Australia-wide.<br>7 days &middot; Free photo quotes</div>
    <div><a href="{SMS_A}">Text: {PHONE}</a><br><a href="{root}locations/index.html">All service areas</a></div>
  </div>
  <div class="foot-areas"><strong style="color:#cfe0ec">Service areas:</strong><br>{links}</div>
  <div style="text-align:center;padding:0 24px 28px;color:#5b7185">&copy; 2026 {BIZ}.</div>
</footer>
</body></html>"""

def faq_html(pairs):
    out = '<div class="faq">'
    for q,a in pairs:
        out += f"<details><summary>{q}</summary><p>{a}</p></details>"
    return out + "</div>"

def faq_schema(pairs):
    data = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pairs]}
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'

def biz_schema(area=None):
    d = {"@context":"https://schema.org","@type":"LocalBusiness","name":BIZ,
         "telephone":PHONE,"url":BASE_URL,
         "openingHours":"Mo-Su 07:00-18:00",
         "description":"Pressure washing and soft washing — driveways, house washes, rooves, decks and commercial. Text a photo for a fast fixed quote."}
    if area: d["areaServed"] = {"@type":"City","name":f"{area['n']}, {area['s']}"}
    else: d["areaServed"] = {"@type":"Country","name":"Australia"}
    return f'<script type="application/ld+json">{json.dumps(d)}</script>'

# ============================================================
# PAGES
# ============================================================
os.makedirs(f"{OUT}/locations", exist_ok=True)
with open(f"{OUT}/style.css","w") as f: f.write(CSS)

home_faq = [
 ("How do photo quotes work?", f"Take a photo of the surface — driveway, wall, deck, whatever needs washing — and text it to {PHONE} or upload it in the form. We can see the size, surface type and how dirty it is, so we text back a fixed quote without needing a site visit."),
 ("What's the difference between pressure washing and soft washing?","Pressure washing uses high-pressure water for hard surfaces like concrete and pavers. Soft washing uses low pressure with cleaning solutions for delicate surfaces — render, painted walls, rooves — killing mould and algae at the root without damage. We do both and choose the right one for each surface."),
 ("Do you bring your own water?","Yes — our units carry water, so restrictions or no outdoor tap are no problem. If your tap is handy we'll use it, but we never rely on it."),
 ("Will pressure washing damage my surfaces?","Not when it's done right. Wrong pressure on soft brick, render or timber causes real damage — that's why we match pressure, temperature and chemicals to every surface, and soft wash anything delicate."),
 ("How long does a job take?","Most driveways take 1–2 hours; a full house soft wash is usually half a day. Your photo quote comes with a time estimate."),
]
title = f"Pressure Washing Australia | Text a Photo, Get a Quote | {BIZ}"
desc  = f"Driveway cleaning, house soft washing, roof & deck washing across 50+ Australian suburbs. Text a photo of the job to {PHONE} for a fast fixed quote."
page = head(title, desc, f"{BASE_URL}/", "", biz_schema()+faq_schema(home_faq))
page += header_nav()
page += f"""
<div class="hero"><div class="wrap">
  <p class="eyebrow">Photo quotes by text &middot; 7 days &middot; We bring the water</p>
  <h1 class="display">Grime.<br><span class="hl">Blasted.</span></h1>
  <p class="lede">Driveways, house washes, rooves, decks and shopfronts — washed by people who know which surfaces need pressure and which need care.</p>
  <div class="hero-ctas"><a class="btn-big" href="{SMS_A}">Text a photo to {PHONE}</a><a class="btn-ghost" href="#quote">Or upload it here</a></div>
  <p class="hero-note">Snap it on your phone → text it → get a fixed price back. No site visit needed.</p>
</div></div>
<section id="services"><div class="wrap">
  <span class="sec-label">What we wash</span>
  <h2 class="display">Every surface, the right way</h2>
  <p class="sub">High pressure where it helps, soft washing where it matters — matched to your surface so nothing gets damaged.</p>
  {services()}
  <div class="ba" style="margin-top:28px" aria-hidden="true"><div class="b">Before — grime, moss, oil, salt</div><div class="a">After — JetBright clean</div></div>
</div></section>
<section id="quote" style="background:var(--mist)"><div class="wrap">
  <div class="form-split">
    <div>
      <span class="sec-label" style="background:var(--white)">Photo quote</span>
      <h2 class="display">One photo gets you a price</h2>
      <p class="sub">A phone snap shows us the surface, the size and the grime — that's a quote, no site visit needed. Text it or upload it, and we'll text you back a fixed price.</p>
      <a class="btn-big" href="{SMS_A}" style="background:var(--navy);color:var(--white)">Text a photo to {PHONE}</a>
    </div>
    {quote_form()}
  </div>
</div></section>
<section><div class="wrap">
  <span class="sec-label">How it works</span>
  <h2 class="display">Three steps to spotless</h2>
  {steps()}
</div></section>
<section style="background:var(--mist)"><div class="wrap">
  <span class="sec-label">Service areas</span>
  <h2 class="display">Where we wash</h2>
  <p class="sub">Local crews in every major city. Find your suburb:</p>"""
for city in CITIES:
    subs = [s for s in SUBURBS if s["c"]==city]
    links = "".join(f'<a href="locations/{s["slug"]}.html">{s["n"]}</a>' for s in subs)
    page += f'<div class="city-block"><h3>{city}</h3><div class="area-grid">{links}</div></div>'
page += f"""</div></section>
<section><div class="wrap">
  <span class="sec-label">Questions</span>
  <h2 class="display">Before you text</h2>
  {faq_html(home_faq)}
</div></section>"""
page += footer_block()
with open(f"{OUT}/index.html","w") as f: f.write(page)

# ---- Locations index ----
title = f"Service Areas | Pressure Washing in 50+ Australian Suburbs | {BIZ}"
desc = f"Find pressure washing in your suburb — driveways, house washes, rooves & decks. Text a photo to {PHONE} for a fast fixed quote."
page = head(title, desc, f"{BASE_URL}/locations/", "../", biz_schema())
page += header_nav("../")
page += """<section><div class="wrap">
  <span class="sec-label">Service areas</span>
  <h2 class="display">Pick your suburb</h2>
  <p class="sub">Every area below gets photo quotes by text, local crews and surface-matched washing.</p>"""
for city in CITIES:
    subs = [s for s in SUBURBS if s["c"]==city]
    links = "".join(f'<a href="{s["slug"]}.html">{s["n"]} {s["p"]}</a>' for s in subs)
    page += f'<div class="city-block"><h3>{city}</h3><div class="area-grid">{links}</div></div>'
page += "</div></section>"
page += footer_block("../")
with open(f"{OUT}/locations/index.html","w") as f: f.write(page)

# ---- Suburb pages ----
for sb in SUBURBS:
    same_city = [s for s in SUBURBS if s["c"]==sb["c"] and s["n"]!=sb["n"]][:6]
    if len(same_city) < 3:
        same_city += [s for s in SUBURBS if s["s"]==sb["s"] and s["n"]!=sb["n"] and s not in same_city][:3]
    sfaq = [
     (f"How much does pressure washing cost in {sb['n']}?", f"Every {sb['n']} job is priced from your photo — surface, size and grime level. Text a snap to {PHONE} or upload it in the form and we'll text back a fixed quote, usually the same day. No site visit needed."),
     (f"What do you clean in {sb['n']}?", f"{sb['jobs'][0]}, {sb['jobs'][1].lower()}, {sb['jobs'][2].lower()} — plus driveways, house soft washing, rooves, decks, fences and commercial frontages across {sb['n']} and nearby {sb['s']} suburbs."),
     ("Do I need to be home?","Usually not. If we can reach the surfaces and there's clear access, most jobs are done while you're at work — you come home to the before-and-after."),
     ("Do you bring your own water?","Yes, our units carry water — handy for water restrictions, units without outdoor taps, or commercial sites."),
    ]
    jl = ", ".join(sb["jobs"][:-1]).lower() + " and " + sb["jobs"][-1].lower()
    title = f"Pressure Washing {sb['n']} {sb['s']} {sb['p']} | Photo Quotes by Text | {BIZ}"
    desc = f"Pressure washing in {sb['n']} {sb['p']} — {sb['jobs'][0].lower()}, {sb['jobs'][1].lower()} & more. Text a photo to {PHONE} for a fast fixed quote."
    canonical = f"{BASE_URL}/locations/{sb['slug']}.html"
    page = head(title, desc, canonical, "../", biz_schema(sb)+faq_schema(sfaq))
    page += header_nav("../")
    chips = "".join(f"<span>{j}</span>" for j in sb["jobs"])
    nearby = "".join(f'<li><a href="{s["slug"]}.html">Pressure washing {s["n"]}</a></li>' for s in same_city)
    page += f"""
<div class="hero" style="padding:60px 0"><div class="wrap">
  <p class="eyebrow">{sb['c']} &middot; {sb['s']} {sb['p']} &middot; Photo quotes by text</p>
  <h1 class="display" style="font-size:clamp(36px,6vw,70px)">Pressure washing<br><span class="hl">{sb['n']}</span></h1>
  <p class="lede">{sb['note']}</p>
  <div class="jobs-chips">{chips}</div>
  <div class="hero-ctas" style="margin-top:30px"><a class="btn-big" href="{SMS_A}">Text a photo to {PHONE}</a></div>
</div></div>
<section><div class="wrap"><div class="two-col">
  <div>
    <span class="sec-label">{sb['n']} jobs</span>
    <h2 class="display" style="font-size:clamp(26px,3.5vw,40px)">What we wash in {sb['n']}</h2>
    <p>Our {sb['c']} crew handles {jl} across {sb['n']} and the surrounding {sb['s']} suburbs — alongside the full JetBright list: driveways and concrete, house soft washing, roof cleaning, decks and fences, paths and pool surrounds, and commercial frontages.</p>
    <p style="margin-top:14px">Every quote starts with a photo. Snap the surface on your phone, text it to {PHONE} or upload it below, and we'll text you back a fixed price — usually the same day. We bring our own water and match the pressure to your surface, so delicate render and old brick get soft washed while concrete gets the full blast.</p>
    <h2 class="display" style="font-size:clamp(24px,3vw,34px);margin-top:44px">Get a photo quote in {sb['n']}</h2>
    <p class="sub" style="margin-bottom:22px">One photo, one fixed price, texted back fast:</p>
    {quote_form(sb['n'])}
  </div>
  <aside class="side-card">
    <h3>Nearby areas we wash</h3>
    <ul>{nearby}<li><a href="index.html">All service areas →</a></li></ul>
  </aside>
</div></div></section>
<section style="background:var(--mist)"><div class="wrap">
  <span class="sec-label">Questions</span>
  <h2 class="display" style="font-size:clamp(24px,3vw,36px)">Pressure washing in {sb['n']} — FAQs</h2>
  {faq_html(sfaq)}
</div></section>"""
    page += footer_block("../")
    with open(f"{OUT}/locations/{sb['slug']}.html","w") as f: f.write(page)

# ---- 404 ----
page = head(f"Page not found | {BIZ}", "This page got washed away. Head back to the homepage.", f"{BASE_URL}/404.html", "")
page += header_nav()
page += f"""<section style="text-align:center;padding:110px 24px"><h1 class="display" style="font-size:clamp(40px,7vw,80px)">This page got<br><span style="color:var(--aqua)">washed away.</span></h1><p style="margin:20px 0 30px;color:var(--slate)">Squeaky clean — and gone.</p><a class="btn-big" href="index.html">Back to homepage</a></section>"""
page += footer_block()
with open(f"{OUT}/404.html","w") as f: f.write(page)

# ---- sitemap, robots, CNAME ----
urls = [f"{BASE_URL}/", f"{BASE_URL}/locations/"] + [f"{BASE_URL}/locations/{s['slug']}.html" for s in SUBURBS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls: sm += f"  <url><loc>{u}</loc><changefreq>monthly</changefreq></url>\n"
sm += "</urlset>\n"
with open(f"{OUT}/sitemap.xml","w") as f: f.write(sm)
with open(f"{OUT}/robots.txt","w") as f: f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
if DOMAIN:
    with open(f"{OUT}/CNAME","w") as f: f.write(DOMAIN + "\n")

print(f"Built {len(SUBURBS)} suburb pages + homepage, locations index, 404, sitemap, robots into /{OUT}")
