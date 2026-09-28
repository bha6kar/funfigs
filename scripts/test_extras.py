import json
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

from client_setup import add_defaults, setup, STATUS_ITEMS
from launch import build
from statusline import render

ROOT = Path(__file__).resolve().parents[1]


class StatusTests(unittest.TestCase):
    def test_thresholds(self):
        for pct, colour, level in [(0, 32, "low"), (49, 32, "low"), (50, 33, "medium"),
                                   (79, 33, "medium"), (80, 31, "high"), (100, 31, "high")]:
            result = render({"context_window": {"used_percentage": pct}})
            self.assertIn(f"\033[{colour}m", result)
            self.assertIn(f"{pct}% used ({level})", result)

    def test_unknown_invalid_and_plain(self):
        for payload in [None, {}, {"context_window": {"used_percentage": float("nan")}},
                        {"context_window": []}, {"context_window": {"used_percentage": True}}]:
            self.assertIn("unavailable", render(payload))
        self.assertNotIn("\033", render({"context_window": {"used_percentage": 80}}, colour=False))
        self.assertNotIn("\033", render({"model": {"display_name": "X\033\nY"}}, colour=False))

    def test_cache_tokens_and_cost(self):
        output = render({"context_window": {"context_window_size": 200000,
                         "current_usage": {"input_tokens": 10000, "cache_read_input_tokens": 30000,
                                           "cache_creation_input_tokens": 60000}},
                         "cost": {"total_cost_usd": 1.234}}, colour=False)
        self.assertIn("50% used", output)
        self.assertIn("100.0k/200k", output)
        self.assertIn("est. session $1.23", output)


class SetupTests(unittest.TestCase):
    def test_toml_preserves_existing(self):
        source = '# comment\nmodel = "chosen"\n[tui]\n# keep\nnotifications = false\n[tui.other]\nx = 1\n'
        result = add_defaults(source, "tui", {"status_line": STATUS_ITEMS})
        self.assertIn("# keep", result)
        parsed = tomllib.loads(result)
        self.assertEqual(parsed["model"], "chosen")
        self.assertFalse(parsed["tui"]["notifications"])
        self.assertEqual(parsed["tui"]["other"], {"x": 1})
        self.assertEqual(result, add_defaults(result, "tui", {"status_line": ["different"]}))
        self.assertEqual('tui = {status_line = []}\n', add_defaults('tui = {status_line = []}\n', "tui", {"status_line": STATUS_ITEMS}))
        with self.assertRaises(ValueError):
            add_defaults('tui = {notifications = false}\n', "tui", {"status_line": STATUS_ITEMS})

    def test_install_backup_idempotence(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            claude = home / ".claude/settings.json"
            codex = home / ".codex/config.toml"
            claude.parent.mkdir()
            codex.parent.mkdir()
            original = '{"permissions":{"allow":["Read"]},"env":{"CUSTOM":"keep"}}'
            claude.write_text(original)
            codex.write_text('# private\nmodel = "chosen"\n[tui]\nnotifications = false\n')
            with patch("client_setup.shutil.which", return_value="/usr/local/bin/uv"):
                setup(ROOT, home)
                self.assertEqual(claude.read_text(), original)
                setup(ROOT, home, apply=True)
                saved = json.loads(claude.read_text())
                self.assertEqual(saved["permissions"], {"allow": ["Read"]})
                self.assertEqual(saved["env"]["CUSTOM"], "keep")
                self.assertIn("--offline", saved["statusLine"]["command"])
                self.assertEqual(tomllib.loads(codex.read_text())["model"], "chosen")
                backups = list((home / ".local/state/funfigs/backups").iterdir())
                self.assertEqual(len(backups), 1)
                self.assertEqual((backups[0] / ".claude/settings.json").read_text(), original)
                setup(ROOT, home, apply=True)
                self.assertEqual(len(list(backups[0].parent.iterdir())), 1)

    def test_preserves_status_and_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            (home / ".claude").mkdir()
            target = home / ".claude/settings.json"
            target.write_text('{"statusLine":{"command":"custom"}}')
            setup(ROOT, home, apply=True)
            self.assertEqual(json.loads(target.read_text())["statusLine"], {"command": "custom"})
            target.unlink()
            target.symlink_to(home / "outside")
            with self.assertRaises(ValueError):
                setup(ROOT, home, apply=True)


class LauncherTests(unittest.TestCase):
    def test_arguments_and_existing_environment(self):
        args, env = build("codex", None, ["a prompt with spaces"], environ={"UV_NO_PROGRESS": "0"})
        self.assertEqual(args[-1], "a prompt with spaces")
        self.assertEqual(env["UV_NO_PROGRESS"], "0")
        self.assertNotIn("CI", env)
        self.assertNotIn("NO_COLOR", env)

    def test_profiles_no_shell_expansion(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            (repo / "agent-env.json").write_text('{}')
            (repo / ".local").mkdir()
            (repo / ".local/profiles.json").write_text(json.dumps({"work": {
                "env": {"EXAMPLE": "work"}, "claude_args": ["--settings", "$(not-a-command)"]}}))
            args, env = build("claude", "work", [], repo, {})
            self.assertEqual(args, ["claude", "--settings", "$(not-a-command)"])
            self.assertEqual(env["EXAMPLE"], "work")
            with self.assertRaises(ValueError):
                build("claude", "personal", [], repo, {})


if __name__ == "__main__":
    unittest.main()
