# Sound University — Project Context for Claude

> Share this file at the start of any new session.
> It gives Claude full context to help with bugs, features, and maintenance
> without needing to re-explain the project from scratch.

---

## 1. What This Project Is

**Sound University (جامعة الصوت)** is a GitHub Pages website that teaches
sound engineering concepts through Arabic classical poetry. Each lesson is a
poem — composed in a specific Arabic metre (بحر) — that encodes a technical
audio concept (frequency masking, dynamic range, transients, etc.). Students
generate the poems as songs in **Suno AI**, then compare the results to hear
the concept in practice.

**Live site:** `https://akbargherbal.github.io/su/`
**GitHub repo:** `https://github.com/akbargherbal/su`

---

## 2. Directory Structure

```
Sound_University_Website/          ← project root (also git root)
├── index.html                     ← homepage — GENERATED, do not hand-edit
├── Course_Philosophy.html         ← standalone overview page (generated or hand-authored)
├── README.md
├── .gitignore
│
├── HTML_LESSONS/                  ← lesson HTML files — GENERATED
│   ├── LESSON_1.html
│   ├── LESSON_2A.html
│   ├── LESSON_2B.html
│   ├── LESSON_3A.html
│   ├── LESSON_3B.html
│   ├── LESSON_4.html
│   ├── LESSON_5.html
│   ├── LESSON_06.html
│   └── LESSON_7.html
│
├── LESSONS/                       ← Markdown source files — hand-authored
│   ├── LESSON_1.md
│   └── ... (mirrors HTML_LESSONS)
│
└── scripts/                       ← Python tooling
    ├── convert_md2html.py         ← Markdown → HTML converter
    └── generate_homepage.py       ← Homepage generator
```

**Future sections** will follow the same pattern: a new `HTML_<SECTION>/`
folder at the root, mirrored by a source folder if applicable.

---

## 3. The Two Scripts

### `scripts/convert_md2html.py`

Converts `.md` lesson files into fully styled, self-contained HTML pages.
This is the **mature, primary script** — treat it conservatively. Any changes
must be backward-compatible and surgical.

**Typical invocation:**

```bash
python scripts/convert_md2html.py ./LESSONS -o ./HTML_LESSONS \
    --lang ar --prose --home-url ../index.html
```

**Key flags:**
| Flag | Purpose |
|---|---|
| `--lang ar` | Sets RTL layout, Arabic HTML attribute |
| `--prose` | Renders fenced code blocks as Amiri-font poetry cards instead of monospace |
| `--home-url ../index.html` | Injects a fixed `⌂` home button on every page |
| `--code-heavy` | Line numbers, wider column, language guessing (not used for lessons) |
| `-o DIR` | Output directory |
| `--prefix STR` | Filename prefix |
| `-q` | Quiet mode |

**How it works:**

1. Reads `.md` files, runs them through Python `markdown` + `pygments`
2. Extracts `<title>` from the first `# H1` in the source
3. Calls `_build_html()` which renders the full HTML template as one big
   f-string
4. Writes `<prefix><stem>.html` to the output directory

**What NOT to do with this script:**

- Do not restructure the f-string template — it uses `{{}}` escaping throughout
- Do not add positional arguments; always use keyword args when calling
  `convert_file()` or `_build_html()`
- Do not remove the `_check_deps()` guard at the top

---

### `scripts/generate_homepage.py`

Generates `index.html` at the project root. Designed to be re-run whenever
new lessons or sections are added.

**Invocation (from project root):**

```bash
python scripts/generate_homepage.py
```

**Key internals:**

`SITE` dict — global site metadata (title, tagline, GitHub URL) + interactive configuration for the banner teaser strip:

```python
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
        "default_text": "كل درس قصيدة — مكتوبة في بحرٍ عربي أصيل...",
        "link_label": "اقرأ المزيد ←",
        "link_url": "Course_Philosophy.html",
        "max_chars": 170,  # Limits character extraction to clean word-boundaries
    },
}
```

`get_teaser_text()` helper — Reads the file defined in `"link_url"`, cleans style/script blocks, finds the first substantive `<p>` tag (using a `> 100` character check to automatically bypass headings or subtitles), cleans inline HTML formatting, and cleanly truncates at space/word boundaries to your configured limit before adding `...`. Falls back gracefully to `"default_text"` if the target file does not exist.

`SECTIONS` list — the single source of truth for what appears on the homepage.
Each entry:

```python
{
    "id":          "lessons",        # HTML anchor id
    "icon":        "📖",
    "title_ar":    "الدروس",
    "title_en":    "Lessons",
    "dir":         "HTML_LESSONS",   # folder to scan (relative to project root)
    "ext":         ".html",
    "coming_soon": False,            # True → placeholder card, dir ignored
    "description": "...",
}
```

`LESSON_META` dict — overrides for specific lesson files (display number,
badge label). Keyed by uppercase stem e.g. `"LESSON_3A"`.

**To add a new section:**

1. Create the folder (e.g. `HTML_MUSIC/`)
2. Drop HTML files into it
3. Add an entry to `SECTIONS` (or flip `coming_soon: False` on an existing one)
4. Run `python scripts/generate_homepage.py`
5. Commit and push

`ROOT` is set to `Path(__file__).parent.parent` (one level up from `scripts/`)
so the script works correctly from any working directory.

---

## 4. Design System

Both scripts share the same design language. **Never deviate from these
tokens** when adding CSS to either script.

### Colour palette

```css
--bg: #0f1117; /* page background */
--surface: #161b27; /* card / sidebar background */
--surface2: #1e2535; /* hover state, code blocks */
--border: #2a3348; /* default borders */
--accent: #e8c87d; /* warm gold — primary accent */
--accent2: #6eb5ff; /* sky blue — links, inline code */
--text: #d4dce8; /* body text */
--text-muted: #7a8aa0; /* secondary text */
--text-strong: #eef2f8; /* headings, strong */
```

### Typography

```css
--font-body: "DM Sans", sans-serif;
--font-head: "Fraunces", Georgia, serif; /* headings, display */
--font-mono: "JetBrains Mono", monospace; /* code, meta labels */
--font-prose: "Amiri", Georgia, serif; /* Arabic poetry blocks */
```

### Layout conventions

- Lessons: `max-width: 860px` (prose), `1100px` (code-heavy)
- Homepage: `max-width: 1100px`
- Sidebar width: `260px` (lessons only), fixed, RTL-aware
- Standard gap: `2rem`
- Border radius: `10px` cards, `50%` icon buttons

### Hero Teaser Card (Interactive)

- Clickable banner card styled under `#hero` in the homepage.
- Displays a `badge` label on the right side, dynamic truncated `text` matching the Amiri font, and an action link on the left.
- Interactive hover lifts the card container slightly (`translateY(-2px)`), transitions container backgrounds (`var(--surface2)`), changes text color to `var(--text-strong)`, and slides the action arrow on the left.
- Mobile Layout (screen widths < 768px): flex layout drops and wraps columns vertically.

### Fixed UI elements on lesson pages

- **Progress bar** — top of page, gold→blue gradient, 3px
- **Sidebar TOC** — fixed right (RTL), auto-built from headings by JS
- **`⌂` home button** — fixed, same corner as `↑`, bottom offset `5.5rem`
- **`↑` back-to-top** — fixed, appears after 300px scroll, bottom `2rem`
- **Copy buttons** — injected by JS onto every code/prose block

### RTL handling

The lesson converter is RTL-aware throughout. All directional CSS properties
(padding, margin, border, position sides) use Python ternary expressions
inside the f-string:

```python
{'right' if rtl else 'left'}
{'left'  if rtl else 'right'}
```

The homepage is Arabic (`dir="rtl"`) but uses fixed CSS since it's
homepage-only.

---

## 5. Deployment Workflow

```bash
# 1. Author / edit a lesson in LESSONS/ or standalone pages (e.g. PHILOSOPHY/)
# 2. Regenerate HTML lessons
python scripts/convert_md2html.py ./LESSONS -o ./HTML_LESSONS \
    --lang ar --prose --home-url ../index.html

# 3. Compile standalone root pages (like Course Philosophy) to root directory
python scripts/convert_md2html.py ./PHILOSOPHY -o . --lang ar --prose --home-url ./index.html

# 4. Regenerate homepage (which will dynamically read root philosophy paragraphs)
python scripts/generate_homepage.py

# 5. Commit and push — GitHub Pages redeploys automatically
git add .
git commit -m "update website"
git push
```

GitHub Pages is configured to serve from **`main` branch, `/` (root)**.
`index.html` at the root is the entry point.

---

## 6. Conventions & Decisions Log

| Decision                                             | Rationale                                                                                                                                                                                 |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LESSONS/` excluded from `.gitignore`                | Source `.md` files are not needed on the public site; only `HTML_LESSONS/` is served                                                                                                      |
| `generate_homepage.py` lives in `scripts/`, not root | Keeps root clean; `ROOT = Path(__file__).parent.parent` compensates                                                                                                                       |
| `--home-url` is a CLI flag, not hardcoded            | Keeps `convert_md2html.py` generic; the flag is omitted when not deploying to a sub-site                                                                                                  |
| `coming_soon: True` sections show placeholder cards  | Signals roadmap without dead links; flip to `False` when the folder is ready                                                                                                              |
| Home `⌂` button stacks above `↑` button              | Same corner, same design, no new screen real estate consumed                                                                                                                              |
| Homepage card titles extracted from `<title>` tag    | Single source of truth — no separate metadata file to maintain                                                                                                                            |
| Lesson sort order: numeric then alpha suffix         | `LESSON_2A` before `LESSON_2B`, `LESSON_06` sorts correctly as 6                                                                                                                          |
| Standalone page location (`Course_Philosophy.html`)  | Placed directly in root folder rather than inside scanned folders (`HTML_LESSONS`, `HTML_REFERENCE`) so it can be linked directly without automatically appearing as a section grid card. |
| Dynamic Teaser prose threshold (`> 100` chars)       | Setting character matching threshold to `> 100` automatically filters out short metadata/subtitle headings, ensuring we extract genuine, rich body content.                               |
| Dynamic word-boundary truncation                     | To preserve readability, the text is cut cleanly at word/space boundaries before `max_chars`, avoiding truncated words in the middle of characters before appending `...`.                |

---

## 7. Planned / Coming-Soon Sections

Defined in `SECTIONS` with `coming_soon: True`. Activate by:

1. Creating the matching `HTML_<ID>/` folder
2. Setting `coming_soon: False`
3. Running `generate_homepage.py`

| Section id  | Folder            | Purpose                                               |
| ----------- | ----------------- | ----------------------------------------------------- |
| `music`     | `HTML_MUSIC/`     | Student Suno-generated songs, embeds or audio players |
| `exercises` | `HTML_EXERCISES/` | Interactive exercises for mix/frequency concepts      |
| `reference` | `HTML_REFERENCE/` | Quick-reference tables, terminology glossary          |

---

## 8. Dependencies

```bash
pip install markdown pygments
```

Both are checked at import time by `convert_md2html.py` with a clear error
message if missing. `generate_homepage.py` has no third-party dependencies.

---

## 9. How to Brief Claude in a New Session

Paste this file and say what you need. Example openers:

> "Here's the context doc. I want to add an audio player to the music section."

> "Here's the context doc. `generate_homepage.py` is crashing with KeyError on
> a new section I added — here's the traceback."

> "Here's the context doc. Add a `--subtitle` flag to `convert_md2html.py`
> that renders a subtitle line under the doc title."

Claude will read this document and have enough context to help without
needing to re-examine every file.

---

# 1. Author / edit a lesson in LESSONS/ or standalone pages (e.g. PHILOSOPHY/)

# 2. Regenerate HTML lessons

python scripts/convert_md2html.py ./LESSONS -o ./HTML_LESSONS \\
--lang ar --prose --home-url ../index.html

# 3. Compile standalone root pages (like Course Philosophy) to root directory

python scripts/convert_md2html.py ./PHILOSOPHY -o . --lang ar --prose --home-url ./index.html

# 4. Regenerate student work pages (same command, different folders)

python scripts/convert_md2html.py ./MUSIC -o ./HTML_MUSIC \\
--lang ar --prose --home-url ../index.html

# 5. Drop mp3 files into audio/lessons/ or audio/music/ as appropriate

# 6. Regenerate homepage

python scripts/generate_homepage.py

# 7. Commit and push — GitHub Pages redeploys automatically

```
git add .
git commit -m "update website"
git push
```

GitHub Pages is configured to serve from **`main` branch, `/` (root)**.
`index.html` at the root is the entry point.'''
