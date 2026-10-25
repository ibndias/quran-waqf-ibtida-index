"""Write the crawlable pages of the site from the index.

    python3 tools/build_site.py

The viewer (index.html) draws everything in the browser, which a search
engine may never run. This writes plain HTML that carries the marks as text:
one page per mushaf page (page/N/), one per surah (surah/N/), a sitemap and
robots.txt. Re-run it after the data changes; it rewrites the same bytes.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://quran-waqf-ibtida.netlify.app"
REPO = "https://github.com/ibndias/quran-waqf-ibtida-index"
PAGES = 604

with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
    VIEWER = f.read()
SURAH = json.loads(re.search(r"const SURAH = (\[.*?\]);", VIEWER).group(1))

with open(os.path.join(ROOT, "data", "waqf-ibtida.json"), encoding="utf-8") as f:
    DOC = json.load(f)
MARKS = DOC["marks"]

esc = html.escape


def ref(loc):
    return tuple(int(x) for x in loc.split(":"))


def page_text(n):
    with open(os.path.join(ROOT, "demo", "text", f"{n}.json"), encoding="utf-8") as f:
        lines = json.load(f)
    return [w for ln in sorted(lines, key=int) for w in lines[ln] if len(w) == 2]


def page_span(n):
    """First and last ayah on the page, as 2:6 and 2:16."""
    words = page_text(n)
    a, b = ref(words[0][0]), ref(words[-1][0])
    return a[:2], b[:2]


def span_label(a, b):
    if a[0] == b[0]:
        return f"{SURAH[a[0] - 1]} {a[0]}:{a[1]}–{b[1]}"
    return f"{SURAH[a[0] - 1]} {a[0]}:{a[1]} – {SURAH[b[0] - 1]} {b[0]}:{b[1]}"


SPANS = {n: page_span(n) for n in range(1, PAGES + 1)}
BY_PAGE = {}
for m in MARKS:
    BY_PAGE.setdefault(m["page"], []).append(m)
BY_SURAH = {}
for m in MARKS:
    BY_SURAH.setdefault(ref(m["restart"])[0], []).append(m)
SURAH_PAGES = {}
for n, (a, b) in SPANS.items():
    for s in range(a[0], b[0] + 1):
        SURAH_PAGES.setdefault(s, []).append(n)

KIND = {
    "repeat": ("Berhenti lalu ulang", "Stop, then repeat from MULAI"),
    "stop": ("Berhenti lalu lanjut", "Stop, then carry on"),
}


def issue_url(m):
    from urllib.parse import quote
    title = f"Correction: page {m['page']}, mark {m['id']} ({m['restart']} → {m['stop']})"
    body = f"**Mark id:** {m['id']}\n**Page:** {m['page']}\n**Restart → stop:** {m['restart']} → {m['stop']}\n\n**What the scan shows instead:**\n"
    return f"{REPO}/issues/new?title={quote(title)}&body={quote(body)}"


def arabic(m):
    words = m["text"].split(" ")
    if m["kind"] == "stop":
        return f'<span class="s">{esc(words[0])}</span> | <span class="r">{esc(words[-1])}</span>'
    out = []
    for i, w in enumerate(words):
        cls = "r" if i == 0 else "s" if i == len(words) - 1 else ""
        out.append(f'<span class="{cls}">{esc(w)}</span>' if cls else esc(w))
    return " ".join(out)


def mark_item(m, with_page=False):
    s, a, _ = ref(m["restart"])
    where = f'<a href="/page/{m["page"]}/">halaman {m["page"]}</a> · ' if with_page else ""
    id_, en = KIND[m["kind"]]
    return f"""<li class="mark" id="m{m['id']}">
  <p class="ar" lang="ar" dir="rtl">{arabic(m)}</p>
  <p class="row">{where}<strong>{s}:{a}</strong> · MULAI <code>{m['restart']}</code> → HENTI <code>{m['stop']}</code> · {id_} <span class="en">({en})</span></p>
  <p class="row"><a href="/#p={m['page']}&amp;m={m['id']}">Lihat di viewer</a> · <a href="{esc(issue_url(m))}" rel="nofollow">Laporkan koreksi</a></p>
</li>"""


CSS = "/assets/site.css"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
DISCLAIMER = """<p class="note"><b>Eksperimen.</b> Tanda ini dibaca dengan bantuan AI dari scan halaman yang bisa diakses publik di
<a href="https://quran.tampang.com/">quran.tampang.com</a>, lalu dicek. Belum tentu 100% benar; cocokkan dengan mushaf cetak.
<span class="en">Experimental: read with AI from public scans and checked, not guaranteed correct.</span></p>"""


def doc(path, title, description, body, ld, prev=None, nxt=None):
    url = SITE + path
    links = ""
    if prev:
        links += f'<link rel="prev" href="{SITE}{prev}">'
    if nxt:
        links += f'<link rel="next" href="{SITE}{nxt}">'
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">{links}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Waqaf Ibtida Index">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
{FONTS}
<link rel="stylesheet" href="{CSS}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="/">Waqaf Ibtida Index</a><span class="spacer"></span><a href="/surah/">Daftar surah</a><a href="{REPO}">GitHub</a></div></header>
<main class="wrap">
{body}
</main>
<footer class="wrap">Indeks tanda waqaf ibtida (HENTI / MULAI) untuk mushaf Madinah 604 halaman, riwayat Hafs.
Data: <a href="/data/waqf-ibtida.json">JSON</a> · <a href="/data/waqf-ibtida.csv">CSV</a> · <a href="{REPO}">GitHub</a>.
Sumber scan: <a href="https://quran.tampang.com/">quran.tampang.com</a>.</footer>
</body>
</html>
"""


def crumbs(*items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + path}
            for i, (name, path) in enumerate(items)
        ],
    }


def write(path, text):
    full = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def page_html(n):
    a, b = SPANS[n]
    span = span_label(a, b)
    marks = BY_PAGE.get(n, [])
    title = f"Waqaf ibtida halaman {n}: {span} · HENTI MULAI"
    desc = (f"Tanda waqaf ibtida (HENTI / MULAI) di mushaf halaman {n}, {span}: {len(marks)} tanda, per kata, "
            f"dengan scan halaman untuk dicek. Waqf ibtida marks for page {n}.")
    pager = "".join([
        f'<a href="/page/{n - 1}/">← Halaman {n - 1}</a>' if n > 1 else "<span></span>",
        f'<a href="/page/{n + 1}/">Halaman {n + 1} →</a>' if n < PAGES else "<span></span>",
    ])
    surahs = " · ".join(f'<a href="/surah/{s}/">{s}. {esc(SURAH[s - 1])}</a>' for s in range(a[0], b[0] + 1))
    items = "\n".join(mark_item(m) for m in marks) or '<li class="empty">Halaman ini tidak punya tanda HENTI / MULAI.</li>'
    body = f"""<nav class="crumbs"><a href="/">Beranda</a> › {surahs} › Halaman {n}</nav>
<h1>Waqaf ibtida halaman {n} <span class="sub">{esc(span)}</span></h1>
{DISCLAIMER}
<p><a class="cta" href="/#p={n}">Buka di viewer (teks + scan berdampingan)</a></p>
<h2>{len(marks)} tanda di halaman ini</h2>
<ol class="marks">{items}</ol>
<h2>Scan halaman {n}</h2>
<p><img class="scan" src="/pages/{n:03d}.webp" alt="Scan mushaf halaman {n}, {esc(span)}, dengan tanda HENTI dan MULAI" loading="lazy" width="807" height="1200"></p>
<nav class="pager">{pager}</nav>"""
    ld = [crumbs(("Waqaf Ibtida Index", "/"), (f"Halaman {n}", f"/page/{n}/")),
          {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc,
           "url": f"{SITE}/page/{n}/", "isPartOf": {"@id": SITE + "/#dataset"}, "inLanguage": ["id", "ar"]}]
    return doc(f"/page/{n}/", title, desc, body, ld,
               prev=f"/page/{n - 1}/" if n > 1 else None, nxt=f"/page/{n + 1}/" if n < PAGES else None)


def surah_html(s):
    name = SURAH[s - 1]
    marks = BY_SURAH.get(s, [])
    pages = SURAH_PAGES.get(s, [])
    title = f"Waqaf ibtida Surah {name} ({s}) · tanda HENTI MULAI"
    desc = (f"Semua tanda waqaf ibtida (HENTI / MULAI) di Surah {name}: {len(marks)} tanda per ayat dan kata, "
            f"halaman {pages[0]}–{pages[-1]} mushaf Madinah. Waqf ibtida marks in Surah {name}.")
    items = "\n".join(mark_item(m, with_page=True) for m in marks) or '<li class="empty">Surah ini tidak punya tanda HENTI / MULAI di sumber ini.</li>'
    page_links = " ".join(f'<a href="/page/{p}/">{p}</a>' for p in pages)
    body = f"""<nav class="crumbs"><a href="/">Beranda</a> › <a href="/surah/">Surah</a> › {s}. {esc(name)}</nav>
<h1>Waqaf ibtida Surah {esc(name)} <span class="sub">surah ke-{s}</span></h1>
{DISCLAIMER}
<p>Halaman: {page_links}</p>
<h2>{len(marks)} tanda</h2>
<ol class="marks">{items}</ol>
<nav class="pager">{f'<a href="/surah/{s - 1}/">← {esc(SURAH[s - 2])}</a>' if s > 1 else '<span></span>'}{f'<a href="/surah/{s + 1}/">{esc(SURAH[s])} →</a>' if s < 114 else '<span></span>'}</nav>"""
    ld = [crumbs(("Waqaf Ibtida Index", "/"), ("Surah", "/surah/"), (name, f"/surah/{s}/")),
          {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc,
           "url": f"{SITE}/surah/{s}/", "isPartOf": {"@id": SITE + "/#dataset"}, "inLanguage": ["id", "ar"]}]
    return doc(f"/surah/{s}/", title, desc, body, ld)


def surah_list_html():
    rows = "\n".join(
        f'<li><a href="/surah/{s}/">{s}. {esc(SURAH[s - 1])}</a> <span class="count">{len(BY_SURAH.get(s, []))} tanda</span></li>'
        for s in range(1, 115))
    title = "Daftar surah · Waqaf ibtida HENTI MULAI"
    desc = "Tanda waqaf ibtida (HENTI / MULAI) per surah, 114 surah mushaf Madinah. Waqf ibtida marks by surah."
    body = f"""<nav class="crumbs"><a href="/">Beranda</a> › Surah</nav>
<h1>Waqaf ibtida per surah</h1>
{DISCLAIMER}
<ol class="surahs">{rows}</ol>"""
    return doc("/surah/", title, desc, body, [crumbs(("Waqaf Ibtida Index", "/"), ("Surah", "/surah/"))])


def sitemap():
    urls = ["/", "/surah/"] + [f"/surah/{s}/" for s in range(1, 115)] + [f"/page/{n}/" for n in range(1, PAGES + 1)]
    body = "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


for n in range(1, PAGES + 1):
    write(f"/page/{n}/", page_html(n))
for s in range(1, 115):
    write(f"/surah/{s}/", surah_html(s))
write("/surah/", surah_list_html())
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap())
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print(f"{PAGES} pages, 114 surahs, sitemap")
