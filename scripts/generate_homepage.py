#!/usr/bin/env python3
"""
generate_homepage.py
====================
Generates ``index.html`` for Sound University (GitHub Pages).

Place this file at the **project root** (same level as HTML_LESSONS/).
Run:
    python generate_homepage.py

The script will:
  1. Auto-scan configured section directories for HTML files.
  2. Extract <title> and an optional <meta name="description"> from each file.
  3. Render a fully styled homepage that matches the lesson design language.
  4. Write ``index.html`` to the project root.

── Adding a new section ────────────────────────────────────────────────────────
Edit SECTIONS below.  Each entry is a dict:

    {
        "id":       "unique-id",          # used for anchor & CSS
        "icon":     "🎵",                 # emoji shown in header
        "title_ar": "Arabic label",       # large heading
        "title_en": "English subtitle",   # small subtitle
        "dir":      "HTML_MUSIC",         # folder to scan (relative to script)
        "ext":      ".html",              # file extension to match
        "coming_soon": False,             # True → shows a placeholder card
        "description": "Optional blurb", # shown under the section header
    }

Set ``coming_soon=True`` and omit ``dir`` for sections that don't exist yet.
────────────────────────────────────────────────────────────────────────────────
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# ── Project root (wherever this script lives) ──────────────────────────────
ROOT = Path(__file__).parent.parent


# ═══════════════════════════════════════════════════════════════════════════
#  CONFIGURE YOUR SECTIONS HERE
# ═══════════════════════════════════════════════════════════════════════════
SITE = {
    "title_ar": "جامعة الصوت",
    "title_en": "Sound University",
    "tagline_ar": "حيث تلتقي الشعرية العربية بهندسة الصوت الحديثة",
    "tagline_en": "Where Arabic poetry meets modern sound engineering",
    "github_url": "https://github.com/akbargherbal/su",
    "lang": "ar",
    "dir": "rtl",
    "hero_teaser": {
        "badge": "الفلسفة",
        "default_text": "كل درس قصيدة — مكتوبة في بحرٍ عربي أصيل، تحمل في موسيقاها مفهوماً صوتياً دقيقاً. الأذن تتعلم ما لا تستطيع الكلمات وحدها تعليمه.",
        "link_label": "اقرأ المزيد ←",
        "link_url": "Course_Philosophy.html",
        "max_chars": 280,  # ← Control how many characters to display here!
    },
}

SECTIONS = [
    {
        "id": "lessons",
        "icon": "📖",
        "title_ar": "الدروس",
        "title_en": "Lessons",
        "dir": "HTML_LESSONS",
        "ext": ".html",
        "coming_soon": False,
        "description": "دروس هندسة الصوت مُقدَّمة شعرياً — كل درس قصيدة وتجربة سمعية.",
    },
    {
        "id": "music",
        "icon": "🎵",
        "title_ar": "معرض الأغاني",
        "title_en": "Music Gallery",
        "dir": "HTML_MUSIC",  # create this folder when ready
        "ext": ".html",
        "coming_soon": False,
        "description": "استمع إلى الأغاني التي أنتجها الطلاب باستخدام سونو — مزيج بين الفصحى والإنتاج الحديث.",
    },
    {
        "id": "exercises",
        "icon": "🎛️",
        "title_ar": "التمارين التفاعلية",
        "title_en": "Interactive Exercises",
        "dir": "HTML_EXERCISES",  # create this folder when ready
        "ext": ".html",
        "coming_soon": True,
        "description": "تمارين عملية لتطبيق مفاهيم المزيج والتردد والديناميكية.",
    },
    {
        "id": "reference",
        "icon": "📚",
        "title_ar": "المرجع السريع",
        "title_en": "Quick Reference",
        "dir": "HTML_REFERENCE",  # create this folder when ready
        "ext": ".html",
        "coming_soon": False,
        "description": "جداول ومصطلحات تقنية للرجوع إليها بسرعة أثناء الإنتاج.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
#  LESSON METADATA OVERRIDES
#  Map filename stem → custom display info.
#  If a file is not listed here, the script extracts its <title> automatically.
# ═══════════════════════════════════════════════════════════════════════════
LESSON_META: dict[str, dict] = {
    "LESSON_1": {"number": "01", "badge": "مقدمة"},
    "LESSON_2A": {"number": "02A"},
    "LESSON_2B": {"number": "02B"},
    "LESSON_3A": {"number": "03A"},
    "LESSON_3B": {"number": "03B"},
    "LESSON_4": {"number": "04"},
    "LESSON_5": {"number": "05"},
    "LESSON_06": {"number": "06"},
    "LESSON_7": {"number": "07"},
}


# ── Helpers ────────────────────────────────────────────────────────────────


def extract_meta(html_path: Path) -> dict:
    """Pull <title> and <meta name=description> from an HTML file."""
    try:
        text = html_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {"title": html_path.stem, "description": ""}

    title_m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    title = title_m.group(1).strip() if title_m else html_path.stem

    desc_m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        text,
        re.S | re.I,
    )
    description = desc_m.group(1).strip() if desc_m else ""

    return {"title": title, "description": description}


def sort_key(path: Path) -> tuple:
    """Sort lesson files numerically: LESSON_1, LESSON_2A, … LESSON_06, …"""
    m = re.search(r"(\d+)([A-Za-z]*)", path.stem)
    if m:
        return (int(m.group(1)), m.group(2).upper())
    return (9999, path.stem)


def scan_section(section: dict) -> list[dict]:
    """Return a list of page dicts for a section directory."""
    if section.get("coming_soon"):
        return []

    folder = ROOT / section["dir"]
    ext = section.get("ext", ".html")

    if not folder.is_dir():
        print(f"  [warn] Directory not found: {folder}  → skipping", file=sys.stderr)
        return []

    files = sorted(folder.glob(f"*{ext}"), key=sort_key)
    pages = []
    for f in files:
        meta = extract_meta(f)
        stem = f.stem.upper()
        override = LESSON_META.get(stem, {})
        rel_path = f.relative_to(ROOT).as_posix()
        pages.append(
            {
                "href": rel_path,
                "title": meta["title"],
                "description": meta["description"],
                "stem": stem,
                "number": override.get("number", ""),
                "badge": override.get("badge", ""),
            }
        )
    return pages


def get_teaser_text() -> str:
    """Read Course_Philosophy.html and dynamically parse a preview paragraph."""
    target_file = ROOT / SITE["hero_teaser"]["link_url"]
    if target_file.is_file():
        try:
            content = target_file.read_text(encoding="utf-8", errors="replace")

            # Strip styles and scripts to prevent false matches
            content = re.sub(r"<script.*?>.*?</script>", "", content, flags=re.S | re.I)
            content = re.sub(r"<style.*?>.*?</style>", "", content, flags=re.S | re.I)

            # Find all <p>...</p> blocks
            paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", content, re.S | re.I)
            for p in paragraphs:
                # Remove inner HTML formatting (strong, span, links, etc.)
                cleaned = re.sub(r"<[^>]+>", "", p).strip()

                # We skip short header subtitles by requiring > 100 characters.
                # This ensures we match actual explanatory prose paragraphs.
                if (
                    len(cleaned) > 100
                    and "Built with" not in cleaned
                    and "Generated" not in cleaned
                    and "topnav" not in p
                ):
                    # Unescape common HTML entities
                    cleaned = (
                        cleaned.replace("&nbsp;", " ")
                        .replace("&amp;", "&")
                        .replace("&quot;", '"')
                    )

                    # Clean word-boundary truncation using configured limit
                    max_len = SITE["hero_teaser"].get("max_chars", 170)
                    if len(cleaned) > max_len:
                        space_idx = cleaned.rfind(" ", 0, max_len - 3)
                        if space_idx > 80:
                            cleaned = cleaned[:space_idx].strip() + "..."
                        else:
                            cleaned = cleaned[: max_len - 3].strip() + "..."
                    return cleaned
        except Exception as e:
            print(
                f"  [warn] Error parsing teaser from philosophy: {e}", file=sys.stderr
            )

    return SITE["hero_teaser"]["default_text"]


# ── Card HTML builders ─────────────────────────────────────────────────────


def lesson_card(page: dict) -> str:
    number_html = (
        f'<span class="card-number">{page["number"]}</span>' if page["number"] else ""
    )
    badge_html = (
        f'<span class="card-badge">{page["badge"]}</span>' if page["badge"] else ""
    )
    desc_html = (
        f'<p class="card-desc">{page["description"]}</p>' if page["description"] else ""
    )
    return f"""
        <a class="lesson-card" href="{page['href']}">
          <div class="card-top">
            {number_html}
            {badge_html}
          </div>
          <h3 class="card-title">{page['title']}</h3>
          {desc_html}
          <span class="card-arrow">←</span>
        </a>"""


def coming_soon_card(section: dict) -> str:
    return f"""
        <div class="lesson-card coming-soon">
          <div class="card-top">
            <span class="card-number">—</span>
          </div>
          <h3 class="card-title">قريباً · Coming Soon</h3>
          <p class="card-desc">{section.get('description', '')}</p>
        </div>"""


def section_block(section: dict, pages: list[dict]) -> str:
    cards_html = ""
    if section.get("coming_soon") or not pages:
        cards_html = coming_soon_card(section)
    else:
        cards_html = "\n".join(lesson_card(p) for p in pages)

    desc_html = (
        f'<p class="section-desc">{section["description"]}</p>'
        if section.get("description")
        else ""
    )

    return f"""
  <!-- ── {section['title_en']} ──────────────────────────────────── -->
  <section id="{section['id']}" class="site-section">
    <div class="section-header">
      <span class="section-icon">{section['icon']}</span>
      <div>
        <h2 class="section-title">{section['title_ar']}</h2>
        <span class="section-subtitle">{section['title_en']}</span>
      </div>
    </div>
    {desc_html}
    <div class="cards-grid">
      {cards_html}
    </div>
  </section>
"""


# ── Navigation items ───────────────────────────────────────────────────────


def nav_links(sections: list[dict]) -> str:
    items = "".join(
        f'<a href="#{s["id"]}" class="nav-link">' f'{s["icon"]} {s["title_ar"]}</a>'
        for s in sections
    )
    return items


# ── Full page template ─────────────────────────────────────────────────────


def render_page(
    sections_html: str, nav_html: str, page_count: int, teaser_text: str
) -> str:
    now = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html>
<html lang="{SITE['lang']}" dir="{SITE['dir']}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{SITE['title_ar']} — {SITE['title_en']}</title>
  <meta name="description" content="{SITE['tagline_ar']}" />

  <!-- Fonts (matching lesson design) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&family=JetBrains+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&family=Amiri:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet" />

  <style>
    /* ── Reset ──────────────────────────────────────────────────── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg:          #0f1117;
      --surface:     #161b27;
      --surface2:    #1e2535;
      --surface3:    #232c3d;
      --border:      #2a3348;
      --border2:     #3a4a64;
      --accent:      #e8c87d;
      --accent2:     #6eb5ff;
      --accent3:     #a78bfa;
      --text:        #d4dce8;
      --text-muted:  #7a8aa0;
      --text-strong: #eef2f8;

      --font-body:   'DM Sans', sans-serif;
      --font-head:   'Fraunces', Georgia, serif;
      --font-mono:   'JetBrains Mono', monospace;
      --font-prose:  'Amiri', Georgia, serif;

      --content-max: 1100px;
      --gap:         2rem;
      --radius:      10px;
    }}

    html {{ scroll-behavior: smooth; }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      font-size: clamp(15px, 1.05vw, 17px);
      line-height: 1.75;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
    }}

    /* ── Progress bar ───────────────────────────────────────────── */
    #progress {{
      position: fixed; top: 0; left: 0; right: 0;
      height: 3px; width: 0%;
      background: linear-gradient(90deg, var(--accent), var(--accent2));
      z-index: 1000;
      transition: width 0.1s linear;
    }}

    /* ── Top nav ────────────────────────────────────────────────── */
    #topnav {{
      position: sticky; top: 0;
      background: rgba(15, 17, 23, 0.92);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      z-index: 200;
      padding: 0 var(--gap);
    }}
    .nav-inner {{
      max-width: var(--content-max);
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      height: 56px;
    }}
    .nav-brand {{
      font-family: var(--font-head);
      font-size: 1.15rem;
      font-weight: 600;
      color: var(--accent);
      text-decoration: none;
      white-space: nowrap;
      letter-spacing: -0.01em;
    }}
    .nav-links {{
      display: flex;
      gap: 0.25rem;
      overflow-x: auto;
      scrollbar-width: none;
    }}
    .nav-links::-webkit-scrollbar {{ display: none; }}
    .nav-link {{
      font-size: 0.82rem;
      color: var(--text-muted);
      text-decoration: none;
      padding: 0.3rem 0.7rem;
      border-radius: 6px;
      white-space: nowrap;
      transition: background 0.15s, color 0.15s;
    }}
    .nav-link:hover {{
      background: var(--surface2);
      color: var(--text-strong);
    }}
    .nav-github {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--text-muted);
      text-decoration: none;
      border: 1px solid var(--border);
      padding: 0.3rem 0.8rem;
      border-radius: 6px;
      white-space: nowrap;
      transition: border-color 0.15s, color 0.15s;
      flex-shrink: 0;
    }}
    .nav-github:hover {{ border-color: var(--accent); color: var(--accent); }}

    /* ── Hero ───────────────────────────────────────────────────── */
    #hero {{
      position: relative;
      overflow: hidden;
      padding: 7rem var(--gap) 4.5rem;
      text-align: right;
      border-bottom: 1px solid var(--border);
    }}
    /* Decorative grid background */
    #hero::before {{
      content: '';
      position: absolute; inset: 0;
      background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
      background-size: 48px 48px;
      opacity: 0.18;
      pointer-events: none;
    }}
    /* Radial glow */
    #hero::after {{
      content: '';
      position: absolute;
      top: -20%; right: -10%;
      width: 600px; height: 600px;
      background: radial-gradient(circle, rgba(232,200,125,0.07) 0%, transparent 65%);
      pointer-events: none;
    }}
    .hero-inner {{
      position: relative;
      max-width: var(--content-max);
      margin: 0 auto;
    }}
    .hero-eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 1.25rem;
    }}
    .hero-title {{
      font-family: var(--font-prose);
      font-size: clamp(2.8rem, 6vw, 5.5rem);
      font-weight: 700;
      color: var(--text-strong);
      line-height: 1.05;
      letter-spacing: -0.02em;
    }}
    .hero-title-en {{
      display: block;
      font-family: var(--font-head);
      font-size: clamp(1.1rem, 2vw, 1.6rem);
      font-weight: 300;
      font-style: italic;
      color: var(--text-muted);
      letter-spacing: 0.02em;
      margin-top: 0.4rem;
    }}
    .hero-tagline {{
      margin-top: 1.5rem;
      font-family: var(--font-prose);
      font-size: clamp(1rem, 1.5vw, 1.25rem);
      color: var(--text-muted);
      max-width: 560px;
      line-height: 1.9;
    }}
    .hero-meta {{
      margin-top: 2rem;
      display: flex;
      gap: 2rem;
      flex-wrap: wrap;
    }}
    .hero-stat {{
      display: flex;
      flex-direction: column;
      gap: 0.1rem;
    }}
    .hero-stat-num {{
      font-family: var(--font-head);
      font-size: 2rem;
      font-weight: 600;
      color: var(--accent);
      line-height: 1;
    }}
    .hero-stat-label {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-muted);
    }}

    /* ── Hero Teaser Strip ──────────────────────────────────────── */
    .hero-teaser {{
      position: relative;
      z-index: 10;
      margin-top: 3.5rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.25rem 1.75rem;
      display: flex;
      align-items: center;
      gap: 1.5rem;
      text-align: right;
      text-decoration: none;
      color: inherit;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s, background-color 0.2s;
      cursor: pointer;
    }}
    .hero-teaser:hover {{
      transform: translateY(-2px);
      border-color: var(--border2);
      background: var(--surface2);
    }}
    .hero-teaser-badge {{
      font-family: var(--font-mono);
      font-size: 0.68rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
      background: rgba(232, 200, 125, 0.08);
      border: 1px solid rgba(232, 200, 125, 0.2);
      padding: 0.25rem 0.65rem;
      border-radius: 4px;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .hero-teaser-text {{
      font-family: var(--font-prose);
      font-size: 1.05rem;
      color: var(--text-muted);
      line-height: 1.6;
      flex: 1;
      margin: 0;
      transition: color 0.2s;
    }}
    .hero-teaser:hover .hero-teaser-text {{
      color: var(--text-strong);
    }}
    .hero-teaser-link {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--accent2);
      text-decoration: none;
      white-space: nowrap;
      flex-shrink: 0;
      transition: color 0.15s, transform 0.15s;
    }}
    .hero-teaser:hover .hero-teaser-link {{
      color: var(--accent);
      transform: translateX(-4px);
    }}

    /* ── Main content ───────────────────────────────────────────── */
    #content {{
      max-width: var(--content-max);
      margin: 0 auto;
      padding: 3rem var(--gap) 6rem;
    }}

    /* ── Section ────────────────────────────────────────────────── */
    .site-section {{
      margin-bottom: 4.5rem;
      scroll-margin-top: 4rem;
    }}
    .section-header {{
      display: flex;
      align-items: flex-start;
      gap: 1rem;
      margin-bottom: 0.6rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border);
      position: relative;
    }}
    .section-header::after {{
      content: '';
      position: absolute;
      bottom: -1px; right: 0;
      width: 60px; height: 2px;
      background: var(--accent);
    }}
    .section-icon {{
      font-size: 1.8rem;
      line-height: 1;
      margin-top: 0.1rem;
      flex-shrink: 0;
    }}
    .section-title {{
      font-family: var(--font-head);
      font-size: clamp(1.4rem, 2.2vw, 1.9rem);
      font-weight: 600;
      color: var(--text-strong);
      line-height: 1.1;
    }}
    .section-subtitle {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-muted);
    }}
    .section-desc {{
      margin-bottom: 1.5rem;
      color: var(--text-muted);
      font-family: var(--font-prose);
      font-size: 1.02rem;
      line-height: 1.85;
    }}

    /* ── Cards grid ─────────────────────────────────────────────── */
    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }}

    /* ── Lesson card ────────────────────────────────────────────── */
    .lesson-card {{
      display: flex;
      flex-direction: column;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.4rem 1.5rem;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.2s, background 0.2s, transform 0.15s;
      position: relative;
      overflow: hidden;
    }}
    .lesson-card::before {{
      content: '';
      position: absolute;
      top: 0; right: 0;
      width: 3px; height: 100%;
      background: var(--accent);
      transform: scaleY(0);
      transform-origin: bottom;
      transition: transform 0.2s ease;
    }}
    .lesson-card:hover {{
      border-color: var(--border2);
      background: var(--surface2);
      transform: translateY(-2px);
    }}
    .lesson-card:hover::before {{
      transform: scaleY(1);
    }}
    .lesson-card.coming-soon {{
      opacity: 0.45;
      cursor: default;
      border-style: dashed;
    }}
    .lesson-card.coming-soon:hover {{
      transform: none;
      border-color: var(--border);
      background: var(--surface);
    }}
    .lesson-card.coming-soon::before {{ display: none; }}

    .card-top {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.6rem;
    }}
    .card-number {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      letter-spacing: 0.1em;
      color: var(--accent);
      background: rgba(232,200,125,0.1);
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      border: 1px solid rgba(232,200,125,0.2);
    }}
    .card-badge {{
      font-family: var(--font-mono);
      font-size: 0.65rem;
      letter-spacing: 0.08em;
      color: var(--accent2);
      background: rgba(110,181,255,0.08);
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      border: 1px solid rgba(110,181,255,0.2);
    }}
    .card-title {{
      font-family: var(--font-prose);
      font-size: clamp(0.95rem, 1.2vw, 1.08rem);
      font-weight: 400;
      color: var(--text-strong);
      line-height: 1.4;
      flex: 1;
      margin-bottom: 0.5rem;
    }}
    .card-desc {{
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 0.8rem;
    }}
    .card-arrow {{
      font-size: 1rem;
      color: var(--text-muted);
      margin-top: auto;
      transition: color 0.2s, transform 0.2s;
      align-self: flex-start;
    }}
    .lesson-card:hover .card-arrow {{
      color: var(--accent);
      transform: translateX(-4px);
    }}

    /* ── Footer ─────────────────────────────────────────────────── */
    #footer {{
      border-top: 1px solid var(--border);
      padding: 2.5rem var(--gap);
      text-align: center;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-muted);
      letter-spacing: 0.06em;
    }}
    #footer a {{ color: var(--accent); text-decoration: none; }}
    #footer a:hover {{ text-decoration: underline; }}

    /* ── Back to top ────────────────────────────────────────────── */
    #back-top {{
      position: fixed;
      bottom: 1.5rem;
      left: 1.5rem;
      width: 40px; height: 40px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 1rem;
      opacity: 0; pointer-events: none;
      transition: opacity 0.2s, border-color 0.2s, color 0.2s;
    }}
    #back-top.visible {{ opacity: 1; pointer-events: auto; }}
    #back-top:hover {{ border-color: var(--accent); color: var(--accent); }}

    /* ── Responsive ─────────────────────────────────────────────── */
    @media (max-width: 768px) {{
      .hero-teaser {{
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 1.25rem;
      }}
      .hero-teaser-link {{
        align-self: flex-start;
      }}
    }}
    @media (max-width: 640px) {{
      .nav-links {{ display: none; }}
      .cards-grid {{ grid-template-columns: 1fr; }}
      #hero {{ padding: 4rem var(--gap) 3.5rem; }}
    }}
  </style>
</head>
<body>

<div id="progress"></div>

<!-- Top Navigation -->
<nav id="topnav" aria-label="Site navigation">
  <div class="nav-inner">
    <a href="#" class="nav-brand">{SITE['title_ar']}</a>
    <div class="nav-links">
      {nav_html}
    </div>
    <a href="{SITE['github_url']}" class="nav-github" target="_blank" rel="noopener">
      GitHub ↗
    </a>
  </div>
</nav>

<!-- Hero -->
<header id="hero">
  <div class="hero-inner">
    <p class="hero-eyebrow">Sound Engineering · Arabic Poetry · Suno AI</p>
    <h1 class="hero-title">
      {SITE['title_ar']}
      <span class="hero-title-en">{SITE['title_en']}</span>
    </h1>
    <p class="hero-tagline">{SITE['tagline_ar']}</p>
    <div class="hero-meta">
      <div class="hero-stat">
        <span class="hero-stat-num">{page_count}</span>
        <span class="hero-stat-label">درس · Lessons</span>
      </div>
      <div class="hero-stat">
        <span class="hero-stat-num">{len(SECTIONS)}</span>
        <span class="hero-stat-label">أقسام · Sections</span>
      </div>
      <div class="hero-stat">
        <span class="hero-stat-num">∞</span>
        <span class="hero-stat-label">إمكانيات · Possibilities</span>
      </div>
    </div>
    
    <!-- Hero Teaser Strip (Option A — Fully Clickable Card) -->
    <a href="{SITE['hero_teaser']['link_url']}" class="hero-teaser">
      <span class="hero-teaser-badge">{SITE['hero_teaser']['badge']}</span>
      <p class="hero-teaser-text">{teaser_text}</p>
      <span class="hero-teaser-link">
        {SITE['hero_teaser']['link_label']}
      </span>
    </a>
  </div>
</header>

<!-- Sections -->
<main id="content">
{sections_html}
</main>

<!-- Footer -->
<footer id="footer">
  <p>
    {SITE['title_ar']} &mdash; {SITE['title_en']} &nbsp;·&nbsp;
    Built with Python &amp; hosted on <a href="{SITE['github_url']}" target="_blank" rel="noopener">GitHub Pages</a>
    &nbsp;·&nbsp; Generated {now}
  </p>
</footer>

<a id="back-top" href="#" aria-label="Back to top">↑</a>

<script>
(function () {{
  // Progress bar
  const bar = document.getElementById('progress');
  window.addEventListener('scroll', () => {{
    const h = document.documentElement;
    bar.style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight) * 100) + '%';
  }}, {{ passive: true }});

  // Back-to-top
  const btt = document.getElementById('back-top');
  window.addEventListener('scroll', () => {{
    btt.classList.toggle('visible', window.scrollY > 400);
  }}, {{ passive: true }});
  btt.addEventListener('click', e => {{
    e.preventDefault();
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }});
}})();
</script>

</body>
</html>
"""


# ── Main ───────────────────────────────────────────────────────────────────


def main() -> None:
    print(f"Sound University — Homepage Generator")
    print(f"Project root: {ROOT}\n")

    all_sections_html = ""
    total_pages = 0

    for section in SECTIONS:
        pages = scan_section(section)
        count = len(pages)
        status = "coming soon" if section.get("coming_soon") else f"{count} file(s)"
        print(
            f"  [{section['id']:12s}]  {section['dir'] if not section.get('coming_soon') else '—':20s}  {status}"
        )
        total_pages += count
        all_sections_html += section_block(section, pages)

    # Dynamic Parser triggers here to fetch philosophy snippet
    teaser_text = get_teaser_text()

    nav_html = nav_links(SECTIONS)
    html = render_page(all_sections_html, nav_html, total_pages, teaser_text)

    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")

    print(f"\n✅  Written → {out}")
    print(f"   Total lesson pages discovered: {total_pages}")
    print(f"\nTip: push to GitHub and enable Pages on the main branch root.")


if __name__ == "__main__":
    main()
