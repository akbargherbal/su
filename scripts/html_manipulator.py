#!/usr/bin/env python3
"""
html_manipulator.py — Post-processing tool for Sound University HTML files.

Run AFTER convert_md2html.py. Operations are applied in sequence.

Usage:
  python scripts/html_manipulator.py HTML_MUSIC/LESSON_2A.html --move-audio
  python scripts/html_manipulator.py HTML_MUSIC/ --move-audio
  python scripts/html_manipulator.py HTML_MUSIC/ --move-audio --dry-run
  python scripts/html_manipulator.py HTML_MUSIC/ --remove-tag "div.some-class"
  python scripts/html_manipulator.py HTML_LESSONS/ --fix-suno-prompts
"""

import argparse
import re
import sys
from pathlib import Path

# ── Dependency guard ─────────────────────────────────────────────────────────

def _check_deps() -> None:
    try:
        from bs4 import BeautifulSoup  # noqa: F401
    except ImportError:
        sys.exit(
            "Missing dependency: pip install beautifulsoup4\n"
            "Install with: pip install beautifulsoup4"
        )

# ── CSS injected when a lyrics-card is created ───────────────────────────────

_LYRICS_CARD_CSS = """
    /* ── Lyrics card (audio + verse block) ──────────────────── */
    .lyrics-card {
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      margin: 2rem 0;
    }
    .lyrics-card audio {
      display: block;
      width: 100%;
      background: var(--surface2);
      padding: 0.75rem 1rem;
      margin: 0;
      border-bottom: 1px solid var(--border);
    }
    .lyrics-card pre {
      margin: 0 !important;
      border-radius: 0 !important;
      border-top: none;
    }
"""

_LYRICS_CARD_CSS_MARKER = "/* ── Lyrics card (audio + verse block) ──────────────────── */"

# ── Operations ───────────────────────────────────────────────────────────────

def op_move_audio(soup) -> int:
    """
    Globally pairs the lesson's "perfect audio" block with the lesson's
    designated "lyrics block", grouping them in a <div class="lyrics-card">.

    How it pairs:
      1. Finds the designated lyrics <pre> block (must start with '///***///').
      2. Finds the "perfect audio" tag (must have data-embed="lyrics").
      3. Moves the audio inside a card container wrapping the lyrics pre block.
      4. Cleans up any orphaned empty parent <p> tag that held the audio.

    Returns: 1 if pairing succeeded, 0 otherwise.
    """
    # 1. Find the unique lyrics block starting with ///***///
    lyrics_pre = None
    for pre in soup.find_all("pre"):
        code = pre.find("code")
        text = code.get_text() if code else pre.get_text()
        if text.strip().startswith("///***///"):
            lyrics_pre = pre
            break

    if not lyrics_pre:
        print("    [move-audio] Skipping: No lyrics block starting with '///***///' found in this file.")
        return 0

    # 2. Find the perfect audio marked for embedding
    perfect_audio = soup.find("audio", attrs={"data-embed": "lyrics"})
    if not perfect_audio:
        print("    [move-audio] Skipping: No <audio data-embed=\"lyrics\"> tag found in this file.")
        return 0

    # 3. Safely extract audio and decompose its empty parent wrapper if it is a <p>
    audio_parent = perfect_audio.parent
    perfect_audio.extract()

    if audio_parent and audio_parent.name == "p":
        # Check if the <p> wrapper is now functionally empty (only whitespace/breaks remain)
        has_text = bool(audio_parent.get_text(strip=True))
        has_tags = bool(audio_parent.find_all(lambda tag: tag.name != "br"))
        if not has_text and not has_tags:
            audio_parent.decompose()

    # 4. Build the wrapper card container
    card = soup.new_tag("div", attrs={"class": "lyrics-card"})

    # Insert container right where the lyrics block is
    lyrics_pre.insert_before(card)

    # Move both elements inside the container (audio on top, lyrics on bottom)
    card.append(perfect_audio)
    lyrics_pre.extract()
    card.append(lyrics_pre)

    # 5. Inject CSS styles
    _inject_css(soup, _LYRICS_CARD_CSS_MARKER, _LYRICS_CARD_CSS)

    return 1


def op_remove_tag(soup, selector: str) -> int:
    """
    Remove every element that matches a CSS selector.

    Example selectors:
        "h1#_1"          — the duplicate H1 convert_md2html injects
        "div.some-class" — any div with that class
        "p:empty"        — empty paragraphs

    Returns: number of elements removed.
    """
    removed = 0
    for el in soup.select(selector):
        el.decompose()
        removed += 1
    return removed


def op_fix_suno_prompts(soup) -> int:
    """
    Find all <pre><code> blocks that contain the SUNO_PROMPT marker,
    set dir="ltr" on the <pre> element, and strip the marker line from
    the code content.

    Why this is needed:
      Pages are generated with --lang ar, so all content inherits RTL
      direction. Suno prompts are English and must render LTR. The
      SUNO_PROMPT marker line is a build-time signal only — it is removed
      from the final HTML so readers never see it.

    Returns: number of blocks fixed.
    """
    from bs4 import NavigableString

    count = 0
    for pre in soup.find_all("pre"):
        code = pre.find("code")
        if not code:
            continue
        if "SUNO_PROMPT" not in code.get_text():
            continue

        # 1. Force left-to-right direction on the container.
        #    Safe to set even if already present — idempotent.
        pre["dir"] = "ltr"

        # 2. Strip the marker line (and its trailing newline) from the
        #    code content.  We handle two cases:
        #
        #    a) .string is not None  → the <code> has a single text node
        #       (no syntax-highlight spans).  Direct replacement is safe.
        #
        #    b) .string is None      → multiple child nodes (e.g. the
        #       converter added span elements for syntax colouring).
        #       Walk NavigableString children and patch the one that
        #       contains the marker.
        if code.string is not None:
            cleaned = re.sub(r"SUNO_PROMPT\n?", "", str(code.string), count=1)
            code.string.replace_with(cleaned)
        else:
            for node in list(code.contents):
                if isinstance(node, NavigableString) and "SUNO_PROMPT" in node:
                    cleaned = re.sub(r"SUNO_PROMPT\n?", "", str(node), count=1)
                    node.replace_with(cleaned)

        count += 1

    return count


# ── CSS injection helper ─────────────────────────────────────────────────────

def _inject_css(soup, marker: str, css: str) -> None:
    """Append css into the first <style> tag, once (idempotent via marker)."""
    style_tag = soup.find("style")
    if style_tag is None:
        return
    current = style_tag.string or ""
    if marker in current:
        return  # Already injected — idempotent
    style_tag.string = current + css


# ── File-level processing ────────────────────────────────────────────────────

def process_file(
    path: Path,
    ops: list,
    dry_run: bool = False,
    output_dir: "Path | None" = None,
) -> bool:
    """
    Apply a list of (function, kwargs) operations to one HTML file.
    Returns True if any changes were made.
    """
    from bs4 import BeautifulSoup

    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    total_changes = 0
    for op_fn, kwargs in ops:
        count = op_fn(soup, **kwargs)
        if count:
            label = op_fn.__name__.replace("op_", "").replace("_", "-")
            print(f"    [{label}] {count} change(s)")
            total_changes += count

    if total_changes == 0:
        print(f"    (no changes)")
        return False

    if dry_run:
        print(f"    [dry-run] would write → {path if output_dir is None else output_dir / path.name}")
        return True

    dest = (output_dir / path.name) if output_dir else path
    dest.write_text(str(soup), encoding="utf-8")
    print(f"    written → {dest}")
    return True


# ── CLI ──────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="html_manipulator.py",
        description="Post-process Sound University HTML files after convert_md2html.py.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/html_manipulator.py HTML_MUSIC/ --move-audio
  python scripts/html_manipulator.py HTML_MUSIC/LESSON_2A.html --move-audio
  python scripts/html_manipulator.py HTML_MUSIC/ --move-audio --dry-run
  python scripts/html_manipulator.py HTML_MUSIC/ --remove-tag "h1#_1"
  python scripts/html_manipulator.py HTML_MUSIC/ --move-audio -o HTML_MUSIC/out/
  python scripts/html_manipulator.py HTML_LESSONS/ --fix-suno-prompts
  python scripts/html_manipulator.py HTML_LESSONS/ --move-audio --fix-suno-prompts
""",
    )
    p.add_argument("files", nargs="+", help="HTML file(s) or directory paths to process")
    p.add_argument(
        "--move-audio",
        action="store_true",
        help='Move <audio data-embed="lyrics"> into an adjacent lyrics card',
    )
    p.add_argument(
        "--fix-suno-prompts",
        action="store_true",
        help=(
            "Find <pre><code> blocks containing the SUNO_PROMPT marker, "
            "set dir=ltr on the <pre>, and remove the marker line from the code"
        ),
    )
    p.add_argument(
        "--remove-tag",
        metavar="SELECTOR",
        action="append",
        default=[],
        help="Remove all elements matching CSS selector (repeatable)",
    )
    p.add_argument(
        "-o", "--output-dir",
        metavar="DIR",
        help="Write to DIR instead of modifying files in place",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without writing any files",
    )
    return p


def main() -> None:
    _check_deps()
    parser = build_parser()
    args = parser.parse_args()

    # Build ordered operation list
    ops: list = []
    if args.move_audio:
        ops.append((op_move_audio, {}))
    if args.fix_suno_prompts:
        ops.append((op_fix_suno_prompts, {}))
    for selector in args.remove_tag:
        ops.append((op_remove_tag, {"selector": selector}))

    if not ops:
        parser.error(
            "No operations specified. Add --move-audio, --fix-suno-prompts, --remove-tag SELECTOR, etc."
        )

    output_dir = Path(args.output_dir) if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Parse and expand directory inputs into direct file paths
    resolved_files = []
    for arg in args.files:
        path = Path(arg)
        if not path.exists():
            print(f"  ERROR: path '{arg}' does not exist — skipping")
            continue
        
        if path.is_dir():
            # Find all HTML files inside this folder (sorted alphabetically)
            html_files = sorted(path.glob("*.html"))
            if not html_files:
                print(f"  WARNING: No .html files found in directory '{arg}'")
            resolved_files.extend(html_files)
        else:
            resolved_files.append(path)

    if not resolved_files:
        print("No files available to process.")
        sys.exit(0)

    changed_count = 0
    for f in resolved_files:
        print(f"\n  {f}")
        if process_file(f, ops, dry_run=args.dry_run, output_dir=output_dir):
            changed_count += 1

    print(f"\n  Done — {changed_count}/{len(resolved_files)} file(s) modified.")


if __name__ == "__main__":
    main()
