"""Preview or activate optional local environment and status-line settings."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shlex
import shutil
import sys
import tomllib

from shared_setup import atomic_write

ROOT = Path(__file__).resolve().parents[1]
STATUS_ITEMS = ["model-with-reasoning", "context-remaining", "current-dir", "git-branch"]


def add_defaults(text, section, defaults):
    """Insert only missing keys; reject unusual layouts instead of rewriting them."""
    before = tomllib.loads(text)
    existing = before
    for part in section.split("."):
        existing = existing.get(part, {})
        if not isinstance(existing, dict):
            raise ValueError(f"Expected a table at {section}")
    missing = {k: v for k, v in defaults.items() if k not in existing}
    if not missing:
        return text
    addition = "".join(f"{k} = {json.dumps(v)}\n" for k, v in missing.items())
    header = re.search(r"(?m)^\[" + re.escape(section) + r"\][ \t]*(?:#[^\n]*)?\n", text)
    if header:
        result = text[:header.end()] + addition + text[header.end():]
    else:
        result = text.rstrip() + f"\n\n[{section}]\n" + addition
    try:
        after = tomllib.loads(result)
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"Cannot safely extend {section}; use a regular TOML table") from error
    expected = deepcopy(before)
    current = expected
    for part in section.split("."):
        current = current.setdefault(part, {})
    current.update(missing)
    if after != expected:
        raise ValueError("TOML edit changed unrelated configuration")
    return result


def validate_path(path, home):
    for candidate in (path, *path.parents):
        if candidate == home:
            break
        if candidate.is_symlink():
            raise ValueError(f"Refusing symlinked configuration or parent: {candidate}")


def setup(repo=ROOT, home=None, apply=False):
    home = (home or Path.home()).absolute()
    repo = repo.resolve()
    env = json.loads((repo / "agent-env.json").read_text())
    uv = shutil.which("uv")
    if uv is None:
        raise ValueError("uv must be installed before status-line activation")
    claude = home / ".claude/settings.json"
    codex = home / ".codex/config.toml"
    for path in (claude, codex):
        validate_path(path, home)
    originals = {p: p.read_bytes() if p.exists() else None for p in (claude, codex)}
    settings = json.loads(originals[claude] or b"{}")
    if not isinstance(settings, dict) or not isinstance(settings.get("env", {}), dict):
        raise ValueError("Claude settings and env must be objects")
    settings.setdefault("env", {})
    for key, value in env.items():
        settings["env"].setdefault(key, value)
    status = {"type": "command", "command": shlex.join([
        uv, "run", "--quiet", "--offline", "--no-project", "--python", sys.executable,
        str(repo / "scripts/statusline.py")])}
    if "statusLine" in settings and settings["statusLine"] != status:
        print("Existing Claude status line preserved; Funfigs bar not activated")
    else:
        settings["statusLine"] = status
    text = (originals[codex] or b"").decode()
    text = add_defaults(text, "shell_environment_policy.set", env)
    text = add_defaults(text, "tui", {"status_line": STATUS_ITEMS})
    writes = {claude: (json.dumps(settings, indent=2) + "\n").encode(), codex: text.encode()}
    writes = {p: d for p, d in writes.items() if originals[p] != d}
    for path in writes:
        print(f"Update: {path} (existing values preserved)")
    if not writes:
        print("Client settings already current")
    if not apply or not writes:
        return
    backup = home / ".local/state/funfigs/backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    validate_path(backup, home)
    backup.mkdir(parents=True, mode=0o700)
    for path in writes:
        if originals[path] is not None:
            atomic_write(backup / path.relative_to(home), originals[path])
    for path in writes:
        current = path.read_bytes() if path.exists() else None
        if current != originals[path]:
            raise ValueError("Configuration changed during preview; rerun before installing")
    for path, data in writes.items():
        atomic_write(path, data)
    print(f"Backups: {backup}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "install"])
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args()
    setup(home=args.home.expanduser(), apply=args.action == "install")
