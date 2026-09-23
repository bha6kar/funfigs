"""Connect Claude Code and Codex to one local instruction, memory and skill store."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".funfigs-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def setup(repo, home, apply=False):
    repo, home = repo.resolve(), home.absolute()
    canonical = repo / "shared/AGENTS.md"
    if not canonical.is_file() or not (repo / "memory/MEMORY.md").is_file():
        raise ValueError("Create local-only shared/AGENTS.md and ensure memory/MEMORY.md exists before installation")
    if (home / ".codex/AGENTS.override.md").exists():
        raise ValueError("AGENTS.override.md would shadow shared Codex instructions; reconcile it first")
    links = [(home / ".claude/CLAUDE.md", canonical), (home / ".codex/AGENTS.md", canonical)]
    for skill in sorted((repo / "skills").iterdir()):
        if not (skill / "SKILL.md").is_file():
            continue
        links.append((home / ".claude/skills" / skill.name, skill))
        links.append((home / ".agents/skills" / skill.name, skill))
    settings = home / ".claude/settings.json"
    current = json.loads(settings.read_text()) if settings.exists() else {}
    if not isinstance(current, dict):
        raise ValueError("Claude settings must be a JSON object")
    current["autoMemoryDirectory"] = str(repo / "memory")
    current["autoMemoryEnabled"] = True
    writes = [(settings, (json.dumps(current, indent=2) + "\n").encode())]
    codex_config = home / ".codex/config.toml"
    if not codex_config.exists():
        writes.append((codex_config, (repo / "codex.config.toml").read_bytes()))
    # Rebind the canonical file if this local repository has moved.
    text = canonical.read_text()
    import re
    match = re.search(r"Our canonical instructions are (.+)/shared/AGENTS.md\.", text)
    if match and match.group(1) != str(repo):
        writes.append((canonical, text.replace(match.group(1), str(repo)).encode()))
    for path, _ in links + writes:
        for parent in path.parents:
            if parent == home or parent == repo:
                break
            if parent.is_symlink():
                raise ValueError(f"Refusing symlinked parent: {parent}")
    for path, _ in writes:
        if path.is_symlink():
            raise ValueError(f"Refusing symlinked settings/source file: {path}")
    links = [(p, s) for p, s in links if not (p.is_symlink() and p.resolve() == s)]
    writes = [(p, d) for p, d in writes if not p.exists() or p.read_bytes() != d]
    print(f"Shared instructions: {canonical}")
    print(f"Shared memory: {repo / 'memory'}")
    print(f"Changes: {len(links)} local links, {len(writes)} files")
    if not apply or not (links or writes):
        return
    backup = home / ".local/state/funfigs/backups" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    for parent in backup.parents:
        if parent == home:
            break
        if parent.is_symlink():
            raise ValueError(f"Refusing symlinked backup parent: {parent}")
    backup.mkdir(parents=True, mode=0o700)
    def save(path):
        relative = path.relative_to(home) if path.is_relative_to(home) else Path("repository") / path.name
        saved = backup / relative
        saved.parent.mkdir(parents=True, exist_ok=True)
        if path.is_symlink():
            saved.symlink_to(os.readlink(path), target_is_directory=path.is_dir())
        elif path.is_dir():
            shutil.copytree(path, saved, symlinks=True)
        elif path.exists():
            shutil.copy2(path, saved)
    # Back up every target before changing any of them.
    for path, _ in links + writes:
        save(path)
    for path, data in writes:
        atomic_write(path, data)
    for path, source in links:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.exists():
            # Existing directories have been fully backed up above.
            shutil.rmtree(path)
        path.symlink_to(source, target_is_directory=source.is_dir())
    print(f"Backups: {backup}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "install"])
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args()
    setup(ROOT, args.home.expanduser(), apply=args.action == "install")
