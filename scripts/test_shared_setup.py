import json
from pathlib import Path
import tempfile
import unittest
from shared_setup import setup


class SharedSetupTests(unittest.TestCase):
    def test_shared_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = Path(temporary).resolve() / "repo", Path(temporary).resolve() / "home"
            for name, text in {
                "shared/AGENTS.md": "Our canonical instructions are /old/shared/AGENTS.md.\n",
                "memory/MEMORY.md": "Shared notes\n",
                "skills/funfigs-memory/SKILL.md": "Memory skill\n",
                "skills/import-memory/SKILL.md": "Claude-only skill\n",
                "codex.config.toml": 'sandbox_mode = "workspace-write"\n',
            }.items():
                path = repo / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
            (home / ".claude").mkdir(parents=True)
            (home / ".codex").mkdir()
            (home / ".claude/CLAUDE.md").write_text("Original rules")
            (home / ".claude/settings.json").write_text('{"custom": true}')
            (home / ".codex/config.toml").write_text("# Existing config\n")
            setup(repo, home)
            self.assertFalse((home / ".codex/AGENTS.md").exists())
            setup(repo, home, apply=True)
            claude, codex = home / ".claude/CLAUDE.md", home / ".codex/AGENTS.md"
            self.assertEqual(claude.resolve(), codex.resolve())
            self.assertIn(str(repo), codex.read_text())
            claude.write_text("Changed shared rules")
            self.assertEqual(codex.read_text(), "Changed shared rules")
            settings = json.loads((home / ".claude/settings.json").read_text())
            self.assertTrue(settings["custom"])
            self.assertEqual(Path(settings["autoMemoryDirectory"]), repo / "memory")
            self.assertEqual((home / ".codex/config.toml").read_text(), "# Existing config\n")
            self.assertEqual((home / ".agents/skills/funfigs-memory").resolve(), repo / "skills/funfigs-memory")
            self.assertEqual((home / ".agents/skills/import-memory").resolve(), repo / "skills/import-memory")
            backups = list((home / ".local/state/funfigs/backups").iterdir())
            self.assertEqual((backups[0] / ".claude/CLAUDE.md").read_text(), "Original rules")
            setup(repo, home, apply=True)
            self.assertEqual(len(list(backups[0].parent.iterdir())), 1)
            (home / ".codex/AGENTS.override.md").write_text("Conflict")
            with self.assertRaises(ValueError):
                setup(repo, home, apply=True)


if __name__ == "__main__":
    unittest.main()
