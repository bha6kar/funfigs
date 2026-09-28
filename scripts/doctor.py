"""Read-only installation checks; no credentials or private settings are printed."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def check(repo=ROOT, home=None):
    home = home or Path.home()
    failures = []

    def report(ok, label, optional=False):
        print(f"{'OK' if ok else 'WARN' if optional else 'FAIL'}: {label}")
        if not ok and not optional:
            failures.append(label)

    for name in ("uv", "git", "rg", "claude", "codex"):
        report(shutil.which(name) is not None, f"{name} on PATH", optional=name in {"claude", "codex"})
        paths = {str((Path(d) / name).resolve()) for d in os.get_exec_path()
                 if os.access(Path(d) / name, os.X_OK) and (Path(d) / name).is_file()}
        if len(paths) > 1:
            print(f"WARN: multiple {name} executables on PATH; inspect before removing anything")
    for relative in (".claude/CLAUDE.md", ".codex/AGENTS.md"):
        link = home / relative
        report(link.is_file() and link.resolve() == (repo / "shared/AGENTS.md").resolve(), relative + " shares local rules")
    for skill in sorted((repo / "skills").iterdir()):
        if not (skill / "SKILL.md").is_file():
            continue
        for parent in (".claude/skills", ".agents/skills"):
            link = home / parent / skill.name
            report(link.is_dir() and link.resolve() == skill.resolve(), f"{parent}/{skill.name} links to Funfigs")
    for parent in (home / ".claude/skills/synced", home / ".agents/skills/synced"):
        if parent.exists():
            duplicates = {p.parent.name for p in parent.glob("*/*/SKILL.md")
                          if (repo / "skills" / p.parent.name / "SKILL.md").is_file()}
            if duplicates:
                print(f"WARN: {parent}: duplicate names: {', '.join(sorted(duplicates))}")
    env = json.loads((repo / "agent-env.json").read_text())
    for relative, loader in ((".claude/settings.json", json.loads), (".codex/config.toml", tomllib.loads)):
        try:
            config = loader((home / relative).read_text())
            report(isinstance(config, dict), relative + " parses")
            if relative.startswith(".claude"):
                report(bool(config.get("statusLine")), "Claude status line configured", optional=True)
                report(config.get("autoMemoryDirectory") == str(repo / "memory"), "Claude shared memory directory")
                values = config.get("env", {})
            else:
                report(bool(config.get("tui", {}).get("status_line")), "Codex CLI footer configured", optional=True)
                values = config.get("shell_environment_policy", {}).get("set", {})
            report(all(values.get(k) == v for k, v in env.items()), relative + " quiet defaults match", optional=True)
        except (OSError, ValueError, TypeError, AttributeError):
            report(False, relative + " missing or invalid")
    forbidden = ["shared/AGENTS.md", "funfigs-claude-template.md", ".local",
                 "skills/docx", "skills/pdf", "skills/pptx", "skills/xlsx", "skills/skill-creator"]
    result = subprocess.run(["git", "ls-files", "--", *forbidden], cwd=repo, text=True, capture_output=True)
    report(result.returncode == 0 and not result.stdout.strip(), "private rules and local-only bundles excluded from Git")
    print("INFO: profiles select launch arguments, not a security boundary or skill isolation")
    print("INFO: custom colour bar is Claude terminal-only; Codex desktop uses its own UI")
    return 1 if failures else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    args = parser.parse_args()
    raise SystemExit(check(home=args.home.expanduser()))
