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
  python scripts/html_manipulator.py HTML_LESSONS/ --css-selector "blockquote" --remove-prop "font-style"
  python scripts/html_manipulator.py HTML_LESSONS/ --css-selector "blockquote" --set-prop "font-weight:600"
"""

import argparse
import re
import sys
from pathlib import Path

# ── Dependency guard ─────────────────────────────────────────────────────────


def _check_deps(need_cssutils: bool = False) -> None:
    try:
        from bs4 import BeautifulSoup  # noqa: F401
    except ImportError:
        sys.exit(
            "Missing dependency: pip install beautifulsoup4\n"
            "Install with: pip install beautifulsoup4"
        )

    if need_cssutils:
        try:
            import cssutils  # noqa: F401
        except ImportError:
            sys.exit(
                "Missing dependency: pip install cssutils\n"
                "Required for --css-selector / --remove-prop / --set-prop.\n"
                "Install with: pip install cssutils"
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

_LYRICS_CARD_CSS_MARKER = (
    "/* ── Lyrics card (audio + verse block) ──────────────────── */"
)

# ── CSS injected for Suno-prompt blocks (--fix-suno-prompts) ────────────────
#
# convert_md2html's stylesheet has:
#     pre:not(.codehilite pre) { direction: rtl; text-align: right; }
# which has specificity (0,1,2). A plain `pre[data-suno-prompt]` rule is only
# (0,1,1) and would lose to that base rule on specificity alone, regardless
# of source order — hence `!important` on the two properties that actually
# conflict (direction, text-align). line-height/font-family don't need it,
# since nothing else at this specificity sets them.

_SUNO_PROMPT_CSS = """
    /* ── Suno prompt LTR override ──────────────────── */
    pre[data-suno-prompt] {
      direction: ltr !important;
      text-align: left !important;
      line-height: 1.5;
      font-family: var(--font-mono);
    }
"""

_SUNO_PROMPT_CSS_MARKER = "/* ── Suno prompt LTR override ──────────────────── */"

# ── CSS overrides ─────────────────────────────────────────────────────────
#
# Each entry overrides a single CSS rule emitted by convert_md2html.
# Workflow: open the page, find the rule in DevTools, toggle/edit
# properties until it looks right, then copy the *entire resulting
# declaration block* (everything between { and }) into `css` below.
#
# `op_modify_css_rule` replaces the whole declaration block for `selector`
# with `css` — properties not listed here are dropped, not just left alone.
# If `selector` isn't found in the stylesheet, the entry is skipped with
# a warning (so a typo here won't silently do nothing forever).
#
# Add as many entries as you like; --apply-css-overrides applies all of
# them, in order, to every <style> tag in each file.

CSS_OVERRIDES = [
    {
        "selector": "blockquote",
        "css": """
            border-right: 3px solid var(--accent);
            margin: 1.5rem 0;
            padding: 1rem 1.5rem;
            background: var(--surface2);
            border-radius: 0 8px 8px 0;
            color: var(--text-muted);
        """,
    },
    {
        "selector": 'pre[data-suno-prompt="true"] button',
        "css": """
    position: absolute;
    top: 0.5rem;
    right: 0.75rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.72rem;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    z-index: 2;
        """,
    },
    # {
    #     "selector": "blockquote p",
    #     "css": """
    #         margin: 0;
    #     """,
    # },
]

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
        print(
            "    [move-audio] Skipping: No lyrics block starting with '///***///' found in this file."
        )
        return 0

    # 2. Find the perfect audio marked for embedding
    perfect_audio = soup.find("audio", attrs={"data-embed": "lyrics"})
    if not perfect_audio:
        print(
            '    [move-audio] Skipping: No <audio data-embed="lyrics"> tag found in this file.'
        )
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
    mark them for LTR rendering, and strip the marker line from the
    code content.

    Why two elements need touching:

      <code dir="ltr">
        The dir attribute goes on <code> so the text content itself
        renders left-to-right (this is a bidi/text-shaping concern,
        not CSS, so it can't be handled via the stylesheet).

      <pre data-suno-prompt>
        convert_md2html's stylesheet has a rule:
            pre:not(.codehilite pre) { direction: rtl; text-align: right; }
        Setting just dir="ltr" on <code> isn't enough to flip layout,
        since that stylesheet rule wins on specificity. Rather than an
        inline style, we tag the element with a data attribute and let
        the injected `_SUNO_PROMPT_CSS` rule (added via `_inject_css`)
        override direction/text-align via !important. This is idempotent —
        re-setting the same attribute is a no-op.

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

        # 1. Set dir="ltr" on the <code> element (bidi text shaping).
        code["dir"] = "ltr"

        # 2. Tag the <pre> so the injected stylesheet rule can target it.
        pre["data-suno-prompt"] = "true"

        # 3. Strip the SUNO_PROMPT marker line (+ its trailing newline) from
        #    the code content.  Two cases:
        #
        #    a) code.string is not None → single text node (plain code block,
        #       no syntax-highlight spans).  Replace directly.
        #
        #    b) code.string is None → multiple child nodes (syntax-highlighted
        #       spans).  Walk NavigableString children and patch the one that
        #       carries the marker.
        if code.string is not None:
            cleaned = re.sub(r"SUNO_PROMPT\n?", "", str(code.string), count=1)
            code.string.replace_with(cleaned)
        else:
            for node in list(code.contents):
                if isinstance(node, NavigableString) and "SUNO_PROMPT" in node:
                    cleaned = re.sub(r"SUNO_PROMPT\n?", "", str(node), count=1)
                    node.replace_with(cleaned)

        count += 1

    if count:
        _inject_css(soup, _SUNO_PROMPT_CSS_MARKER, _SUNO_PROMPT_CSS)

    return count


def op_modify_css_rule(
    soup,
    selector: str,
    remove: "list[str] | None" = None,
    set: "dict[str, str] | None" = None,
    replace_with: "str | None" = None,
) -> int:
    """
    Find a CSS rule by selector inside the <style> tag(s) and modify it
    in place — either surgically (remove/set individual properties) or
    wholesale (replace the entire declaration block with `replace_with`).

    This edits convert_md2html's generated stylesheet directly via a real
    CSSOM (cssutils), rather than appending override rules or touching
    individual elements with inline styles.

    `replace_with` mode (used by --apply-css-overrides / CSS_OVERRIDES):
        The entire `rule.style` is replaced with the given declaration
        block — properties not present in `replace_with` are dropped,
        not merely left alone. This matches a "copy the final state from
        DevTools" workflow: edit the rule until it looks right, copy
        everything between `{` and `}`, paste it as `replace_with`.

    `remove` / `set` mode (surgical, used by --css-selector etc.):
        Only the listed properties are touched; everything else in the
        rule is left as-is.

    `replace_with` takes precedence if both are given.

    Searches every <style> tag in the document and applies the change to
    every matching rule found (in case convert_md2html ever emits more
    than one <style> block or repeats a selector). If `selector` is not
    found in any <style> tag, and we have a `replace_with` block, it appends
    it as a new rule to the first <style> tag.

    Idempotent: re-running with the same `replace_with`/`set`/`remove`
    produces an equivalent rule, though the stylesheet is re-serialized
    each time (whitespace/formatting may shift).

    Returns: number of rules changed (0 or more, depending on how many
    <style> tags contain a matching selector).
    """
    import cssutils
    import logging

    cssutils.log.setLevel(logging.CRITICAL)  # silence cssutils warnings

    changed = 0
    found_anywhere = False

    for style_tag in soup.find_all("style"):
        css_text = style_tag.string or ""
        if not css_text.strip():
            continue

        sheet = cssutils.parseString(css_text)
        found_in_sheet = False

        for rule in sheet:
            if rule.type != rule.STYLE_RULE:
                continue
            if rule.selectorText != selector:
                continue

            found_in_sheet = True
            found_anywhere = True

            if replace_with is not None:
                rule.style.cssText = replace_with
                changed += 1
                continue

            for prop in remove or []:
                if rule.style.getProperty(prop):
                    rule.style.removeProperty(prop)

            for prop, value in (set or {}).items():
                rule.style.setProperty(prop, value)

            changed += 1

        if found_in_sheet:
            style_tag.string = sheet.cssText.decode("utf-8")

    if not found_anywhere:
        if replace_with is not None:
            # If the rule wasn't found but we have a wholesale replacement,
            # append it as a new rule to the first <style> tag.
            style_tag = soup.find("style")
            if style_tag:
                current = style_tag.string or ""
                style_tag.string = (
                    current
                    + f"\n/* ── Added via CSS override (idempotent) ── */\n{selector} {{\n{replace_with}\n}}\n"
                )
                changed += 1
            else:
                print(
                    f"    [modify-css-rule] WARNING: No <style> tag found to append '{selector}'"
                )
        else:
            print(
                f"    [modify-css-rule] WARNING: selector '{selector}' not found in any <style> tag"
            )

    return changed


def op_apply_css_overrides(soup, overrides: "list[dict]") -> int:
    """
    Apply each entry in `overrides` (a list of {"selector", "css"} dicts,
    see CSS_OVERRIDES at the top of this file) via op_modify_css_rule's
    whole-block `replace_with` mode.

    Returns: total number of rules changed across all overrides.
    """
    total = 0
    for entry in overrides:
        total += op_modify_css_rule(
            soup, selector=entry["selector"], replace_with=entry["css"]
        )
    return total


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
        print(
            f"    [dry-run] would write → {path if output_dir is None else output_dir / path.name}"
        )
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

  # Apply all configured CSS_OVERRIDES (edit the list at the top of this script)
  python scripts/html_manipulator.py HTML_LESSONS/ --apply-css-overrides

  # Remove a CSS property from a rule (e.g. de-italicize blockquotes)
  python scripts/html_manipulator.py HTML_LESSONS/ --css-selector "blockquote" --remove-prop "font-style"

  # Set/override a CSS property on a rule
  python scripts/html_manipulator.py HTML_LESSONS/ --css-selector "blockquote" --set-prop "font-weight:600"

  # Both at once, on the same selector
  python scripts/html_manipulator.py HTML_LESSONS/ --css-selector "blockquote" \\
      --remove-prop "font-style" --set-prop "font-weight:600"
""",
    )
    p.add_argument(
        "files", nargs="+", help="HTML file(s) or directory paths to process"
    )
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
        "--apply-css-overrides",
        action="store_true",
        help=(
            "Apply every entry in the CSS_OVERRIDES list (defined near the top "
            "of this script) — replaces each selector's full declaration block "
            "with the configured 'css' text"
        ),
    )
    p.add_argument(
        "--css-selector",
        metavar="SELECTOR",
        help=(
            "CSS selector of the rule to modify in the <style> tag "
            "(use with --remove-prop / --set-prop)"
        ),
    )
    p.add_argument(
        "--remove-prop",
        metavar="PROP",
        action="append",
        default=[],
        help="CSS property to remove from the rule matched by --css-selector (repeatable)",
    )
    p.add_argument(
        "--set-prop",
        metavar="PROP:VALUE",
        action="append",
        default=[],
        help=(
            "CSS property:value to set on the rule matched by --css-selector "
            "(repeatable, format 'prop:value')"
        ),
    )
    p.add_argument(
        "-o",
        "--output-dir",
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
    parser = build_parser()
    args = parser.parse_args()

    needs_css_edit = bool(
        args.css_selector
        or args.remove_prop
        or args.set_prop
        or args.apply_css_overrides
    )
    _check_deps(need_cssutils=needs_css_edit)

    # Build ordered operation list
    ops: list = []
    if args.move_audio:
        ops.append((op_move_audio, {}))
    if args.fix_suno_prompts:
        ops.append((op_fix_suno_prompts, {}))
    for selector in args.remove_tag:
        ops.append((op_remove_tag, {"selector": selector}))

    if args.apply_css_overrides:
        if not CSS_OVERRIDES:
            parser.error(
                "--apply-css-overrides was given but CSS_OVERRIDES is empty — "
                "add entries near the top of this script"
            )
        ops.append((op_apply_css_overrides, {"overrides": CSS_OVERRIDES}))

    if args.remove_prop or args.set_prop:
        if not args.css_selector:
            parser.error("--remove-prop / --set-prop require --css-selector")

    if args.css_selector:
        if not (args.remove_prop or args.set_prop):
            parser.error(
                "--css-selector requires at least one of --remove-prop / --set-prop"
            )

        set_props = {}
        for item in args.set_prop:
            if ":" not in item:
                parser.error(
                    f"--set-prop must be in 'prop:value' format, got: '{item}'"
                )
            prop, _, value = item.partition(":")
            set_props[prop.strip()] = value.strip()

        ops.append(
            (
                op_modify_css_rule,
                {
                    "selector": args.css_selector,
                    "remove": args.remove_prop,
                    "set": set_props,
                },
            )
        )

    if not ops:
        parser.error(
            "No operations specified. Add --move-audio, --fix-suno-prompts, "
            "--remove-tag SELECTOR, --css-selector + --remove-prop/--set-prop, etc."
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
