#!/usr/bin/env python3
"""
sync.py — Sound University build & deploy automation
-----------------------------------------------------
Usage:
    python sync.py                          # run default routine (local)
    python sync.py full                     # run named routine
    python sync.py full --message "fix X"  # override commit message
    python sync.py --list                   # list all routines
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# ── tomllib: stdlib in 3.11+, fall back to third-party 'tomli' ────
try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # pip install tomli
    except ModuleNotFoundError:
        sys.exit(
            "[ERROR] Python < 3.11 detected and 'tomli' is not installed.\n"
            "        Fix: pip install tomli   (or upgrade to Python 3.11+)"
        )

# ── Paths ──────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.resolve()
CONFIG_FILE = ROOT / "sync.toml"

# ── Defaults ───────────────────────────────────────────────────────
DEFAULT_ROUTINE = "local"
DEFAULT_MESSAGE = "Update website"


# ── ANSI colours ───────────────────────────────────────────────────
# Enabled only when writing to a real terminal (not piped/redirected).
# On Windows, enables VT processing so colours work in cmd / PowerShell.
def _enable_ansi_windows():
    if sys.platform == "win32":
        import ctypes

        kernel = ctypes.windll.kernel32
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)


_enable_ansi_windows()

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"


def c(text: str, *codes: str) -> str:
    """Wrap text in ANSI codes only when stdout is a TTY."""
    if sys.stdout.isatty():
        return "".join(codes) + str(text) + RESET
    return str(text)


# ── Config loading ─────────────────────────────────────────────────
def load_config() -> dict:
    if not CONFIG_FILE.exists():
        sys.exit(
            f"[ERROR] Config file not found: {CONFIG_FILE}\n"
            f"        Expected 'sync.toml' next to 'sync.py'."
        )
    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


# ── --list ─────────────────────────────────────────────────────────
def list_routines(config: dict) -> None:
    routines = config.get("routines", {})
    steps_registry = config.get("steps", {})
    default = config.get("settings", {}).get("default_routine", DEFAULT_ROUTINE)

    print(c(f"\n{'━' * 52}", CYAN))
    print(c("  Available routines", BOLD, CYAN))
    print(c(f"{'━' * 52}", CYAN))

    for name, routine in routines.items():
        tag = c(" [default]", YELLOW) if name == default else ""
        desc = routine.get("description", "")
        print(f"\n  {c(name, BOLD, CYAN)}{tag}")
        if desc:
            print(f"  {c(desc, DIM)}")
        for step_name in routine.get("steps", []):
            label = steps_registry.get(step_name, {}).get("label", step_name)
            print(f"    {c('·', DIM)} {c(step_name, YELLOW)}  {c(label, DIM)}")

    print(c(f"\n{'━' * 52}\n", CYAN))


# ── Single step runner ─────────────────────────────────────────────
def build_cmd(cmd: str, shell: str) -> str | list:
    """
    Wrap cmd for the requested shell.

    shell = "powershell"  →  loads $PROFILE so profile functions
                              (e.g. convert_md2html) are available.
    shell = "default"     →  cmd.exe on Windows, /bin/sh elsewhere.
    """
    if shell == "powershell":
        # Source the profile first so user-defined functions are available.
        # Single-quote the inner command to avoid escaping hell.
        escaped = cmd.replace("'", "''")  # escape any single-quotes in cmd
        return f'powershell -NoLogo -Command ". $PROFILE; {escaped}"'
    return cmd


def run_step(cmd: str, shell: str = "default") -> subprocess.CompletedProcess:
    """
    Run a shell command from the project root.
    Returns the CompletedProcess; caller decides what to do with it.
    """
    # Force UTF-8 I/O for all child processes.
    # Critical on Windows (default is cp1252) for Arabic content and
    # any script that prints Unicode characters (arrows, symbols, etc.)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"  # Python 3.7+ UTF-8 mode

    full_cmd = build_cmd(cmd, shell)
    return subprocess.run(
        full_cmd,
        shell=True,
        cwd=ROOT,  # always run from project root
        text=True,
        encoding="utf-8",  # sync.py itself reads stdout/stderr as UTF-8
        capture_output=True,
        env=env,
    )


# ── Routine runner ─────────────────────────────────────────────────
def run_routine(config: dict, routine_name: str, message: str) -> None:
    routines = config.get("routines", {})
    steps_registry = config.get("steps", {})

    if routine_name not in routines:
        available = ", ".join(routines.keys())
        sys.exit(
            f"[ERROR] Routine '{routine_name}' not found.\n"
            f"        Available: {available}"
        )

    routine = routines[routine_name]
    step_names = routine.get("steps", [])
    total = len(step_names)
    desc = routine.get("description", "")

    # ── Header ────────────────────────────────────────────────────
    print(c(f"\n{'━' * 52}", CYAN))
    print(f"  {c('Routine :', BOLD)} {c(routine_name, CYAN, BOLD)}")
    if desc:
        print(f"  {c('Info    :', BOLD)} {desc}")
    print(f"  {c('Steps   :', BOLD)} {total}")
    print(c(f"{'━' * 52}", CYAN))

    # ── Execute steps in order ────────────────────────────────────
    for i, step_name in enumerate(step_names, start=1):

        if step_name not in steps_registry:
            _abort(
                i,
                total,
                step_name,
                f"Step '{step_name}' is listed in routine '{routine_name}' "
                f"but is not defined in [steps].\n"
                f"  → Check sync.toml for a typo.",
            )

        step = steps_registry[step_name]
        label = step.get("label", step_name)
        cmd = step.get("cmd", "").replace("{message}", message)
        shell = step.get("shell", "default")

        if not cmd:
            _abort(
                i,
                total,
                step_name,
                f"Step '{step_name}' has no 'cmd' defined in sync.toml.",
            )

        # Step banner
        shell_tag = f"  {c('[powershell]', YELLOW)}" if shell == "powershell" else ""
        print(f"\n{c(f'[{i}/{total}]', YELLOW, BOLD)} {label}{shell_tag}")
        print(f"  {c('$', DIM)} {c(cmd, DIM)}")

        result = run_step(cmd, shell)

        # Print stdout even on success (some CLIs report progress there)
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                print(f"  {line}")

        if result.returncode != 0:
            # Print stderr
            if result.stderr.strip():
                print(c(f"\n  ── stderr {'─' * 38}", RED))
                for line in result.stderr.strip().splitlines():
                    print(c(f"  {line}", RED))

            _abort(
                i, total, step_name, f"Exit code {result.returncode}. See stderr above."
            )

        print(c(f"  ✓ OK", GREEN, BOLD))

    # ── Footer ────────────────────────────────────────────────────
    print(c(f"\n{'━' * 52}", GREEN))
    print(c(f"  ✓ All {total} steps completed successfully.", GREEN, BOLD))
    print(c(f"{'━' * 52}\n", GREEN))


def _abort(step_num: int, total: int, step_name: str, reason: str) -> None:
    """Print a clear failure summary and exit with code 1."""
    print(c(f"\n{'━' * 52}", RED))
    print(c(f"  ✗ FAILED at step {step_num}/{total}: {step_name}", RED, BOLD))
    print(c(f"  {reason}", RED))
    print(c(f"  Fix the issue above, then re-run.", RED))
    print(c(f"{'━' * 52}\n", RED))
    sys.exit(1)


# ── CLI ────────────────────────────────────────────────────────────
def main() -> None:
    config = load_config()
    settings = config.get("settings", {})
    default_routine = settings.get("default_routine", DEFAULT_ROUTINE)
    default_message = settings.get("default_message", DEFAULT_MESSAGE)

    parser = argparse.ArgumentParser(
        prog="sync.py",
        description="Sound University — build & deploy automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python sync.py                        # run default routine\n"
            "  python sync.py full                   # full rebuild + push\n"
            "  python sync.py lessons                # lessons only\n"
            "  python sync.py full --message 'fix'  # custom commit message\n"
            "  python sync.py --list                 # show all routines\n"
        ),
    )
    parser.add_argument(
        "routine",
        nargs="?",
        default=default_routine,
        help=f"Name of the routine to run (default: '{default_routine}')",
    )
    parser.add_argument(
        "--message",
        "-m",
        default=default_message,
        help=f'Git commit message (default: "{default_message}")',
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all available routines and exit",
    )

    args = parser.parse_args()

    if args.list:
        list_routines(config)
        return

    run_routine(config, args.routine, args.message)


if __name__ == "__main__":
    main()
