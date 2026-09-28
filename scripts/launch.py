"""Launch a client with quiet defaults and an optional local profile."""

import argparse
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build(client, profile, arguments, repo=ROOT, environ=None):
    env = dict(os.environ if environ is None else environ)
    for key, value in json.loads((repo / "agent-env.json").read_text()).items():
        env.setdefault(key, value)
    extra = []
    if profile:
        path = repo / ".local/profiles.json"
        if not path.is_file():
            raise ValueError("Create .local/profiles.json from profiles.example.json first")
        profiles = json.loads(path.read_text())
        selected = profiles.get(profile)
        if not isinstance(selected, dict):
            raise ValueError("Selected profile is missing or invalid")
        overrides = selected.get("env", {})
        extra = selected.get(client + "_args", [])
        if not isinstance(overrides, dict) or not all(
            isinstance(k, str) and isinstance(v, str) and "=" not in k and "\0" not in k + v
            for k, v in overrides.items()
        ):
            raise ValueError("Profile env must contain valid string environment values")
        if not isinstance(extra, list) or not all(isinstance(a, str) for a in extra):
            raise ValueError("Profile client arguments must be a list of strings")
        env.update(overrides)
        env["FUNFIGS_PROFILE"] = profile
    args = [client]
    if client == "codex":
        args += ["--add-dir", str(repo)]
    return args + extra + arguments, env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("client", choices=["claude", "codex"])
    parser.add_argument("--profile", choices=["personal", "work"])
    options, arguments = parser.parse_known_args()
    if arguments[:1] == ["--"]:
        arguments = arguments[1:]
    args, env = build(options.client, options.profile, arguments)
    executable = shutil.which(options.client, path=env.get("PATH"))
    if executable is None:
        parser.error(f"{options.client} is not on PATH")
    os.execve(executable, args, env)


if __name__ == "__main__":
    main()
