from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_starter_vault import (  # noqa: E402
    CREDENTIAL_NAME_PREFIXES,
    EXPECTED_VAULT_FOLDERS,
    FORBIDDEN_NAMES,
    FORBIDDEN_PARTS,
    HIGH_RISK_SUFFIXES,
    OBSIDIAN_ALLOWLIST,
    PackageError,
    build_starter_vault,
)


class StarterVaultPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._temporary = tempfile.TemporaryDirectory()
        cls.temp = Path(cls._temporary.name)
        cls.version = "v0.0.0-test"
        cls.first = build_starter_vault(
            ROOT / "examples" / "demo-vault", cls.temp / "first", cls.version
        )
        cls.second = build_starter_vault(
            ROOT / "examples" / "demo-vault", cls.temp / "second", cls.version
        )
        cls.archive_root = f"open-para-vault-{cls.version}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary.cleanup()

    def test_successful_package_and_checksum(self) -> None:
        self.assertTrue(self.first.zip_path.is_file())
        self.assertTrue(self.first.checksum_path.is_file())
        self.assertEqual(
            self.first.checksum_path.read_text(encoding="ascii"),
            f"{self.first.sha256}  {self.first.zip_path.name}\n",
        )

    def test_archive_has_one_root_and_expected_vault_structure(self) -> None:
        names = set(self.first.members)
        roots = {PurePosixPath(name).parts[0] for name in names}
        self.assertEqual(roots, {self.archive_root})
        for folder in EXPECTED_VAULT_FOLDERS:
            self.assertIn(f"{self.archive_root}/{folder}/", names)
        self.assertIn(f"{self.archive_root}/Home.md", names)
        for config in OBSIDIAN_ALLOWLIST:
            self.assertIn(f"{self.archive_root}/.obsidian/{config}", names)

    def test_archive_excludes_forbidden_state(self) -> None:
        relative_names = [PurePosixPath(name).parts[1:] for name in self.first.members]
        for parts in relative_names:
            folded = {part.casefold() for part in parts}
            self.assertTrue(folded.isdisjoint(FORBIDDEN_PARTS))
            if parts:
                name = parts[-1].casefold()
                self.assertNotIn(name, FORBIDDEN_NAMES)
                self.assertFalse(name.startswith(CREDENTIAL_NAME_PREFIXES))
                self.assertNotIn(PurePosixPath(name).suffix, HIGH_RISK_SUFFIXES)
        obsidian_files = {
            parts[-1]
            for parts in relative_names
            if len(parts) == 2 and parts[0] == ".obsidian"
        }
        self.assertEqual(obsidian_files, set(OBSIDIAN_ALLOWLIST))

    def test_same_source_and_version_produce_identical_bytes(self) -> None:
        self.assertEqual(self.first.sha256, self.second.sha256)
        self.assertEqual(self.first.zip_path.read_bytes(), self.second.zip_path.read_bytes())

    def test_archive_extracts_as_a_ready_vault(self) -> None:
        extraction = self.temp / "extracted"
        with zipfile.ZipFile(self.first.zip_path, "r") as archive:
            archive.extractall(extraction)
        vault = extraction / self.archive_root
        self.assertTrue((vault / "Home.md").is_file())
        self.assertTrue((vault / "99_Templates" / "project.md").is_file())
        self.assertTrue((vault / ".obsidian" / "app.json").is_file())

    def test_unexpected_obsidian_state_fails_closed(self) -> None:
        fixture = self.temp / "unexpected-obsidian"
        shutil.copytree(ROOT / "examples" / "demo-vault", fixture)
        (fixture / ".obsidian" / "workspace.json").write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(PackageError, r"Unexpected \.obsidian state: workspace\.json"):
            build_starter_vault(fixture, self.temp / "rejected", self.version)


if __name__ == "__main__":
    unittest.main()
