"""Exercise installation against temporary configuration directories."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("config.py")


class InstallTests(unittest.TestCase):
    def test_preview_merge_backup_and_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            original = '{"permissions":{"allow":["Read"]},"env":{"EXAMPLE":"kept"}}'
            (target / "settings.json").write_text(original)
            (target / "CLAUDE.md").write_text("live rules\n")
            def run(action, *args):
                return subprocess.run([sys.executable, str(SCRIPT), action,
                                       "--target", directory, *args],
                                      check=True, capture_output=True, text=True)
            run("check")
            self.assertEqual((target / "settings.json").read_text(), original)
            self.assertFalse((target / "backups").exists())
            run("install")
            result = json.loads((target / "settings.json").read_text())
            self.assertEqual(result["env"], {"EXAMPLE": "kept"})
            self.assertEqual(result["permissions"]["allow"], ["Read", "WebSearch"])
            self.assertEqual((target / "CLAUDE.md").read_text(), "live rules\n")
            backups = list((target / "backups").iterdir())
            self.assertTrue(backups[0].name.startswith("funfigs-"))
            self.assertEqual((backups[0] / "settings.json").read_text(), original)
            run("install")
            self.assertEqual(len(list((target / "backups").iterdir())), 1)
            snapshot = SCRIPT.parent.parent / "funfigs-claude-template.md"
            if snapshot.is_file():
                run("install", "--include-rules")
                self.assertEqual((target / "CLAUDE.md").read_text(), snapshot.read_text())
            else:
                with self.assertRaises(subprocess.CalledProcessError):
                    run("install", "--include-rules")
                self.assertEqual((target / "CLAUDE.md").read_text(), "live rules\n")
            run("install", "--engineering")
            self.assertEqual((target / "rules" / "funfigs-engineering.md").read_text(),
                             (SCRIPT.parent.parent / "rules" / "engineering.md").read_text())
            library = SCRIPT.parent.parent / "skills" / "funfigs"
            installed = target / "skills" / "funfigs"
            for source in library.rglob("*"):
                if source.is_file():
                    self.assertEqual((installed / source.relative_to(library)).read_bytes(),
                                     source.read_bytes())
            count = len(list((target / "backups").iterdir()))
            run("install", "--engineering")
            self.assertEqual(len(list((target / "backups").iterdir())), count)
            run("install", "--all-skills")
            for source in (SCRIPT.parent.parent / "skills").rglob("*"):
                if source.is_file():
                    destination = target / "skills" / source.relative_to(SCRIPT.parent.parent / "skills")
                    self.assertEqual(destination.read_bytes(), source.read_bytes())
                    if source.stat().st_mode & 0o111:
                        self.assertTrue(destination.stat().st_mode & 0o100)

    def test_symlinked_skill_directory_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            outside = Path(directory) / "outside"
            target.mkdir()
            outside.mkdir()
            (target / "skills").symlink_to(outside, target_is_directory=True)
            result = subprocess.run([sys.executable, str(SCRIPT), "install", "--engineering",
                                     "--target", str(target)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((target / "settings.json").exists())
            self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
