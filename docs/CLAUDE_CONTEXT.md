# Sound University — Claude Context

> Paste this file at the start of any new session. It is the single source of truth.
> Update it whenever scripts, structure, or conventions change.

---

## 1. Project Overview

**Sound University (جامعة الصوت)** is a GitHub Pages site that teaches sound engineering
through Arabic classical poetry. Each lesson is a poem composed in a specific Arabic metre
(بحر) encoding a technical audio concept (frequency masking, dynamic range, transients, etc.).
Students generate the poems as songs in **Suno AI** and compare results to hear the concept
in practice.

- **Live site:** `https://akbargherbal.github.io/su/`
- **Repo:** `https://github.com/akbargherbal/su`
- **Pages config:** `main` branch, `/` (root) — `index.html` is the entry point

---

## 2. Directory Structure

```
Sound_University_Website/           ← project root / git root
├── index.html                      ← GENERATED — do not hand-edit
├── Course_Philosophy.html          ← standalone page (lives at root, not inside any scanned folder)
├── README.md
├── sync.py                         ← build automation entry point (do not hand-edit)
├── sync.toml                       ← build automation config (edit this to add steps/routines)
│
├── HTML_LESSONS/                   ← GENERATED lesson pages
│   ├── LESSON_1.html … LESSON_7.html
│
├── HTML_MUSIC/                     ← GENERATED music-gallery pages
│   └── LESSON_2A.html
│
├── HTML_REFERENCE/                 ← reference pages
│   └── GLOSSARY.html
│
├── TOOLS/                          ← standalone HTML tool apps (NOT converted from Markdown)
│   ├── Tone.js                     ← dependency for arabic-poetry-drum-machine.html
│   ├── arabic-poetry-drum-machine.html
│   ├── arabic-poetic-meters-and-iqaat-guide.html
│   └── suno-prompt-generator-arabic-iqaat.html
│
├── LESSONS/                        ← hand-authored Markdown source (mirrors HTML_LESSONS)
├── MUSIC/                          ← hand-authored Markdown source (mirrors HTML_MUSIC)
│
├── audio/
│   ├── lessons/
│   │   ├── L1/   Epic_Cinematic.mp3
│   │   └── L2A/  BALANCED_01.mp3, P1_thin_hollow_01.mp3,
│   │             P2_muddy_smeared_01.mp3, P3_Harsh_Sibilance_01.mp3
│   └── music/
│       └── lesson_02/
│
└── scripts/
    ├── generate_homepage.py
    └── html_manipulator.py
```

---

## 3. Tools & Scripts

### 3a. `convert_md2html` — PowerShell profile function (not a system executable)

Defined in `$PROFILE` as:
```powershell
function convert_md2html {
    python C:\Users\DELL\Jupyter_Notebooks\Useful_Functions_and_Utilities\convert_md2html.py $args
}
```

Converts `.md` files to fully styled, self-contained HTML using the project's design language.
Because it is a profile function (not a PATH executable), any script invoking it must run
via PowerShell with the profile loaded — see `sync.py` / `sync.toml` for how this is handled.

**Invocation examples:**

```bash
# Lessons (RTL, prose/poetry cards, home button)
convert_md2html ./LESSONS -o ./HTML_LESSONS --lang ar --prose --home-url ../index.html

# Standalone root page (e.g. Course Philosophy)
convert_md2html ./PHILOSOPHY -o . --lang ar --prose --home-url ./index.html

# Music section
convert_md2html ./MUSIC -o ./HTML_MUSIC --lang ar --prose --home-url ../index.html
```

**Key flags:**

| Flag | Effect |
|---|---|
| `--lang ar` | RTL layout, Arabic `lang` attribute |
| `--prose` / `--no-code` | Plain fenced blocks → Amiri-font poetry cards instead of monospace |
| `--home-url URL` | Injects a fixed `⌂` home button on every page |
| `--code-heavy` | Line numbers, language guessing, wider column |
| `-o DIR` | Output directory (created if absent) |
| `--prefix STR` | String prepended to every output filename |
| `-r` | Recurse into subdirectories |
| `-q` | Quiet mode |

**How it works internally:**
1. Reads `.md`, runs through Python `markdown` + `pygments`
2. Extracts `<title>` from the first `# H1`
3. Renders the full HTML as one f-string template (`_build_html()`)
4. Writes `<prefix><stem>.html` to the output directory

---

### 3b. `scripts/generate_homepage.py`

Generates `index.html` at the project root. No third-party dependencies.
`ROOT = Path(__file__).parent.parent` — works correctly from any working directory.

**Invocation:**
```bash
python scripts/generate_homepage.py
```

**Key internals:**

`SITE` dict — global metadata + hero teaser strip config:
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
        "default_text": "...",           # fallback if Course_Philosophy.html absent
        "link_label": "اقرأ المزيد ←",
        "link_url": "Course_Philosophy.html",
        "max_chars": 280,               # truncation limit, word-boundary aware
    },
}
```

`get_teaser_text()` — reads `Course_Philosophy.html`, strips `<style>`/`<script>`,
finds the first `<p>` with `> 100` chars (skips headings/subtitles), cleans inline HTML,
truncates at word boundary. Falls back to `default_text` on any failure.

`SECTIONS` list — single source of truth for homepage sections:
```python
{ "id", "icon", "title_ar", "title_en", "dir", "ext", "coming_soon", "description" }
```

`LESSON_META` dict — display overrides keyed by uppercase stem (e.g. `"LESSON_3A"`):
```python
{ "number": "03A", "badge": "مقدمة" }   # badge is optional
```
Lesson cards auto-extract `<title>` from each HTML file; `LESSON_META` only overrides
`number` and `badge`. Card sort order: numeric then alpha suffix (`LESSON_2A` < `LESSON_2B`,
`LESSON_06` sorts as 6).

**To add a new lesson:** add a `LESSON_META` entry for its stem → regenerate.

**To add a new section:**
1. Create `HTML_<ID>/` folder and populate with HTML files
2. Add or flip `coming_soon: False` on the matching `SECTIONS` entry
3. Run `python scripts/generate_homepage.py`

---

### 3c. `scripts/html_manipulator.py`

Post-processing DOM tool (BeautifulSoup). Run **after** `convert_md2html`.
Operations are applied in sequence. Requires: `pip install beautifulsoup4`

**Invocation:**
```bash
# Single file in-place
python scripts/html_manipulator.py HTML_MUSIC/LESSON_2A.html --move-audio

# Whole directory in-place
python scripts/html_manipulator.py HTML_MUSIC/ --move-audio

# Dry run (no writes)
python scripts/html_manipulator.py HTML_MUSIC/ --move-audio --dry-run

# Write to separate output folder
python scripts/html_manipulator.py HTML_MUSIC/ --move-audio -o HTML_MUSIC/out/

# Remove elements by CSS selector
python scripts/html_manipulator.py HTML_MUSIC/ --remove-tag "h1#_1"
```

**Operations:**

`--move-audio`
Pairs the lesson's designated "perfect audio" with its "lyrics block" and wraps both
in a `.lyrics-card` container (audio on top, verse below). Injects card CSS idempotently.

- **Lyrics block:** a `<pre>` whose text starts with `///***///`
- **Perfect audio:** `<audio data-embed="lyrics">`
- Search is global (not sibling-based) — intervening prose/headings in the Markdown are fine
- Cleans up any orphaned empty `<p>` wrapper the audio was extracted from

`--remove-tag "SELECTOR"`
Removes all elements matching a CSS selector. Repeatable flag.
Common use: `"h1#_1"` removes the duplicate H1 `convert_md2html` injects.

**Lyrics card CSS** (injected once, idempotent via marker comment):
```css
.lyrics-card { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; margin: 2rem 0; }
.lyrics-card audio { display: block; width: 100%; background: var(--surface2); padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); }
.lyrics-card pre { margin: 0 !important; border-radius: 0 !important; border-top: none; }
```

---

### 3d. `sync.py` + `sync.toml` — Build automation

Single entry point for all build and deploy workflows. `sync.py` reads `sync.toml` at
runtime — **never edit `sync.py` directly**. All configuration lives in `sync.toml`.

Requires Python 3.11+ (uses `tomllib` from stdlib). On older Python: `pip install tomli`.

**Invocation:**
```bash
python sync.py                          # default routine: 'local' (full rebuild, no push)
python sync.py full                     # full rebuild + git commit + push
python sync.py lessons                  # lessons only (convert + post-process)
python sync.py music                    # music only (convert + post-process)
python sync.py push                     # git commit + push only, no rebuild
python sync.py full --message "..."     # override the default commit message
python sync.py --list                   # print all available routines and their steps
```

**Built-in routines:**

| Routine | Steps | Pushes? |
|---|---|---|
| `local` *(default)* | convert lessons + music → post-process both → homepage | No |
| `full` | same as `local` + git commit + push | Yes |
| `lessons` | convert lessons → post-process lessons | No |
| `music` | convert music → post-process music | No |
| `push` | git commit + push only | Yes |

**`sync.toml` structure:**

```toml
[settings]
default_routine = "local"
default_message = "Update website"

[steps.my_step]
label = "Human-readable label shown in logs"
cmd   = "the shell command to run"
shell = "powershell"   # optional — only needed for PowerShell profile functions

[routines.my_routine]
description = "Shown in --list output"
steps = ["step_one", "step_two"]
```

**To add a new step:** add a `[steps.name]` block with `label` and `cmd`.
**To add a new routine:** add a `[routines.name]` block with a `steps` list referencing step names.
**PowerShell profile functions** (e.g. `convert_md2html`) require `shell = "powershell"` on their
step — this makes `sync.py` source `$PROFILE` before running the command.

**Implementation notes:**
- All commands run from the project root regardless of where `sync.py` is invoked
- `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` are injected into every subprocess environment
  (required on Windows to handle Arabic text and Unicode symbols in child script output)
- `{message}` in a `cmd` string is replaced at runtime with the commit message
- Failure stops the run immediately with full stderr output and the step name

---

## 4. Design System

All CSS must use these tokens. Never introduce new colours or fonts.

### Colour palette (CSS variables)
```css
--bg:          #0f1117;   /* page background */
--surface:     #161b27;   /* card / sidebar background */
--surface2:    #1e2535;   /* hover state, code blocks */
--surface3:    #232c3d;   /* deeper surface */
--border:      #2a3348;   /* default borders */
--border2:     #3a4a64;   /* stronger borders */
--accent:      #e8c87d;   /* warm gold — primary accent */
--accent2:     #6eb5ff;   /* sky blue — links, inline code */
--accent3:     #a78bfa;   /* violet — tertiary accent */
--text:        #d4dce8;   /* body text */
--text-muted:  #7a8aa0;   /* secondary text */
--text-strong: #eef2f8;   /* headings / emphasis */
```

### Typography
```css
--font-body:   'DM Sans', sans-serif;
--font-head:   'Fraunces', Georgia, serif;
--font-mono:   'JetBrains Mono', monospace;
--font-prose:  'Amiri', Georgia, serif;    /* poetry cards, RTL */
```

### Layout
```css
--content-max: 1100px;
--gap:         2rem;
--radius:      10px;
```

### RTL handling (in `convert_md2html` f-string templates)
Directional CSS properties use Python ternaries:
```python
{'right' if rtl else 'left'}
{'left'  if rtl else 'right'}
```
The homepage uses fixed RTL CSS (no ternaries) since it's always Arabic.

---

## 5. Current Sections State

| Section id | Folder            | `coming_soon` | Status                           |
|------------|-------------------|---------------|----------------------------------|
| `lessons`  | `HTML_LESSONS/`   | `False`       | Live — 9 lessons                 |
| `music`    | `HTML_MUSIC/`     | `False`       | Live — LESSON_2A.html present    |
| `tools`    | `TOOLS/`          | `False`       | Live — 3 tools + Tone.js         |
| `reference`| `HTML_REFERENCE/` | `False`       | Live — GLOSSARY.html present     |

---

## 6. Deployment Workflow

**Standard workflow — use `sync.py`:**

```bash
# Edit source Markdown in LESSONS/, MUSIC/, or PHILOSOPHY/, then:

python sync.py        # full local rebuild (no push) — verify in browser first
python sync.py full   # rebuild + commit + push to GitHub
```

**Manual steps (for operations not yet in sync.toml):**

```bash
# Standalone root pages (e.g. Course Philosophy) — run manually, not in sync.py
convert_md2html ./PHILOSOPHY -o . --lang ar --prose --home-url ./index.html
```

GitHub Pages redeploys automatically on push to `main`.

---

## 7. Key Conventions

| Convention | Rationale |
|---|---|
| `index.html` is GENERATED | Never hand-edit; always regenerate via `generate_homepage.py` or `sync.py` |
| `sync.py` is GENERATED | Never hand-edit; all config lives in `sync.toml` |
| `Course_Philosophy.html` lives at root | Not inside any scanned folder — prevents it appearing as a section card |
| `convert_md2html` is a PowerShell profile function | Not a PATH executable — steps invoking it need `shell = "powershell"` in `sync.toml` |
| `--home-url` is a CLI flag, not hardcoded | Keeps `convert_md2html` generic across different deploy contexts |
| `HTML_` prefix = Markdown-converted output | `HTML_LESSONS/`, `HTML_MUSIC/` contain generated HTML. `TOOLS/` has no `HTML_` prefix because files are native HTML, not converted from Markdown |
| `TOOLS/` filenames use hyphens | URL-friendly; consistent across all three tool files |
| Lyrics block marker: `///***///` | Prefix on the `<pre>` code block; visible in Markdown, reliably locatable by the manipulator |
| Perfect audio marker: `data-embed="lyrics"` | Differentiates the canonical song from secondary/illustrative audio tags |
| `--move-audio` uses global search | Allows prose/headings between the audio tag and the lyrics block in Markdown |
| CSS injection is idempotent | `_inject_css()` checks for a marker comment before injecting — safe to re-run |
| `LESSON_META` keyed by uppercase stem | e.g. `"LESSON_3A"` — must match `f.stem.upper()` from the scanned filename |
| Lesson sort: numeric then alpha suffix | `LESSON_2A` < `LESSON_2B`; `LESSON_06` sorts as 6, not 60 |
| Teaser prose threshold `> 100` chars | Automatically skips short headings/subtitles when extracting philosophy preview |
| `ROOT = Path(__file__).parent.parent` | `generate_homepage.py` lives in `scripts/`; this resolves to project root regardless of working directory |
| UTF-8 enforced in subprocesses | `sync.py` sets `PYTHONIOENCODING=utf-8` + `PYTHONUTF8=1` for all child processes — required on Windows for Arabic text |

---

## 8. To Do

> Remove items once completed.
