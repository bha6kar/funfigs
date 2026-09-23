"""Preview and install our portable Claude preferences with recoverable backups."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def merge(existing, incoming):
    result = dict(existing)
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        elif isinstance(value, list) and isinstance(result.get(key), list):
            result[key] = result[key] + [v for v in value if v not in result[key]]
        else:
            result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "install"])
    parser.add_argument("--target", type=Path, default=Path.home() / ".claude")
    parser.add_argument("--include-rules", action="store_true",
                        help="Explicitly replace CLAUDE.md with our exported snapshot")
    parser.add_argument("--engineering", action="store_true",
                        help="Install engineering agreements and the Funfigs engineering skill")
    parser.add_argument("--all-skills", action="store_true",
                        help="Install all bundled personal skills and engineering agreements")
    args = parser.parse_args()
    if args.include_rules and not (ROOT / "funfigs-claude-template.md").is_file():
        parser.error("--include-rules requires a local-only funfigs-claude-template.md snapshot")
    target = args.target.expanduser().absolute()
    settings_path = target / "settings.json"
    if target.is_symlink() or settings_path.is_symlink():
        parser.error("Refusing a symlinked target or settings file")
    incoming = json.loads((ROOT / "settings.json").read_text())
    current = json.loads(settings_path.read_text()) if settings_path.exists() else {}
    if not isinstance(current, dict) or not isinstance(incoming, dict):
        parser.error("Settings must be JSON objects")
    updated = json.dumps(merge(current, incoming), indent=2) + "\n"
    writes = [(settings_path, updated)]
    if args.include_rules:
        writes.append((target / "CLAUDE.md", (ROOT / "funfigs-claude-template.md").read_text()))
    executable_paths = set()
    if args.engineering or args.all_skills:
        if (target / "rules").is_symlink():
            parser.error("Refusing a symlinked rules directory")
        writes.append((target / "rules" / "funfigs-engineering.md",
                       (ROOT / "rules" / "engineering.md").read_text()))
        skill_root = ROOT / "skills" / "funfigs"
        for source in sorted(skill_root.rglob("*")):
            if source.is_file():
                writes.append((target / "skills" / "funfigs" /
                               source.relative_to(skill_root), source.read_text()))
    if args.all_skills:
        for source in sorted((ROOT / "skills").rglob("*")):
            if source.is_file():
                destination = target / "skills" / source.relative_to(ROOT / "skills")
                writes.append((destination, source.read_bytes()))
                if source.stat().st_mode & 0o111:
                    executable_paths.add(destination)
    writes = list(dict(writes).items())
    changes = []
    for path, content in writes:
        if isinstance(content, str):
            content = content.encode()
        for candidate in (path, *path.parents):
            if candidate == target:
                break
            if candidate.is_symlink():
                parser.error(f"Refusing symlink: {candidate}")
        if path.exists() and path.read_bytes() == content:
            continue
        changes.append((path, content))
    print(f"Target: {target}")
    print("Settings merge preserves existing hooks, plugins, environment and permissions.")
    print("Shared rules: " + ("explicit snapshot replacement" if args.include_rules else "preserved"))
    print("Files to update: " + (", ".join(str(p.relative_to(target)) for p, _ in changes) or "none"))
    if args.action == "check" or not changes:
        return
    target.mkdir(parents=True, exist_ok=True)
    backup = target / "backups" / ("funfigs-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    if (target / "backups").is_symlink():
        parser.error("Refusing a symlinked backup directory")
    backup.mkdir(parents=True, mode=0o700)
    for path, _ in changes:
        if path.exists():
            saved = backup / path.relative_to(target)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
            saved.chmod(0o600)
    for path, content in changes:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as stream:
            path.chmod(0o700 if path in executable_paths else 0o600)
            stream.write(content)
    print(f"Installed. Previous files: {backup}")


if __name__ == "__main__":
    main()
