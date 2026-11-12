#!/usr/bin/env python3
"""Tests for scripts/download_assets.py using synthetic ZIPs (stdlib only).

Run from the repository root:

    python3 -m unittest discover -s scripts/tests -v

No network access and no real Kenney asset is used. Every archive is built in a
temporary directory by the test itself.
"""
import importlib.util
import io
import json
import pathlib
import shutil
import sys
import tempfile
import unittest
import zipfile
from unittest import mock

HERE = pathlib.Path(__file__).resolve()
SCRIPT = HERE.parent.parent / "download_assets.py"


def load_module():
    spec = importlib.util.spec_from_file_location("download_assets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["download_assets"] = module
    spec.loader.exec_module(module)
    return module


assets = load_module()


def make_zip(path, entries, compression=zipfile.ZIP_STORED):
    """entries: list of (name, bytes) or (name, bytes, external_attr)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression) as zf:
        for entry in entries:
            name, data = entry[0], entry[1]
            info = zipfile.ZipInfo(name)
            info.external_attr = entry[2] if len(entry) > 2 else 0o600 << 16
            zf.writestr(info, data)
    return path


class ImporterTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="spirit-assets-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.out = self.tmp / "assets" / "vendor" / "kenney"
        self.manifest = self.tmp / "assets" / "asset-manifest.json"

    def import_one(self, entries, pack="ui-pack-sci-fi", **kwargs):
        archive = make_zip(self.tmp / f"{pack}.zip", entries)
        return assets.import_pack(
            pack, archive, self.out, str(archive),
            kwargs.get("overwrite", False), kwargs.get("dry_run", False))

    # --- happy paths -----------------------------------------------------

    def test_import_records_checksums_and_license(self):
        record = self.import_one([
            ("PNG/playerShip1_blue.png", b"\x89PNG fake"),
            ("License.txt", b"CC0 1.0 Universal"),
            ("readme.md", b"# pack"),
        ])
        self.assertEqual(record["license_review"], "CHECK_LICENSE_CONTENT")
        self.assertEqual(record["license_files"], ["License.txt"])
        paths = sorted(f["path"] for f in record["files"])
        self.assertEqual(paths, ["License.txt", "PNG/playerShip1_blue.png", "readme.md"])
        installed = self.out / "ui-pack-sci-fi" / "PNG" / "playerShip1_blue.png"
        self.assertTrue(installed.is_file())
        by_path = {f["path"]: f for f in record["files"]}
        self.assertEqual(by_path["PNG/playerShip1_blue.png"]["sha256"],
                         assets.checksum(installed))
        self.assertEqual(by_path["PNG/playerShip1_blue.png"]["bytes"], len(b"\x89PNG fake"))

    def test_missing_license_requires_review(self):
        record = self.import_one([("sprites/a.png", b"a")])
        self.assertEqual(record["license_review"], "REVIEW_REQUIRED")
        self.assertEqual(record["license_files"], [])

    def test_license_without_extension_is_kept(self):
        record = self.import_one([
            ("sprites/a.png", b"a"),
            ("License", b"CC0"),
        ])
        self.assertIn("License", record["license_files"])
        self.assertTrue((self.out / "ui-pack-sci-fi" / "License").is_file())

    def test_disallowed_suffix_is_skipped(self):
        record = self.import_one([
            ("sprites/a.png", b"a"),
            ("tools/evil.exe", b"MZ"),
        ])
        self.assertEqual([f["path"] for f in record["files"]], ["sprites/a.png"])
        self.assertFalse((self.out / "ui-pack-sci-fi" / "tools" / "evil.exe").exists())

    # --- safety ---------------------------------------------------------

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            self.import_one([("../evil.png", b"x")])

    def test_absolute_path_rejected(self):
        with self.assertRaises(ValueError):
            self.import_one([("/etc/evil.png", b"x")])

    def test_drive_qualified_path_rejected(self):
        with self.assertRaises(ValueError):
            self.import_one([("C:/evil.png", b"x")])

    def test_symlink_rejected(self):
        with self.assertRaises(ValueError):
            self.import_one([("link.png", b"x", (0o120777) << 16)])

    def test_oversized_content_rejected_with_patched_limit(self):
        with mock.patch.object(assets, "MAX_TOTAL_EXTRACTED", 4):
            with self.assertRaises(ValueError):
                self.import_one([("sprites/a.png", b"12345678")])

    def test_oversized_single_file_rejected(self):
        with mock.patch.object(assets, "MAX_FILE", 2):
            with self.assertRaises(ValueError):
                self.import_one([("sprites/a.png", b"1234")])

    def test_empty_archive_rejected(self):
        with self.assertRaises(ValueError):
            self.import_one([("notes.exe", b"ignored")])

    # --- overwrite behaviour --------------------------------------------

    def test_existing_pack_requires_overwrite(self):
        self.import_one([("sprites/a.png", b"first")])
        with self.assertRaises(FileExistsError):
            self.import_one([("sprites/a.png", b"second")])
        self.assertEqual((self.out / "ui-pack-sci-fi" / "sprites" / "a.png").read_bytes(),
                         b"first")

    def test_overwrite_replaces_tree(self):
        self.import_one([("sprites/a.png", b"first")])
        self.import_one([("sprites/b.png", b"second")], overwrite=True)
        pack = self.out / "ui-pack-sci-fi"
        self.assertFalse((pack / "sprites" / "a.png").exists())
        self.assertEqual((pack / "sprites" / "b.png").read_bytes(), b"second")
        self.assertFalse((self.out / "ui-pack-sci-fi.old").exists())
        self.assertFalse((self.out / ".ui-pack-sci-fi.staging").exists())

    # --- dry run --------------------------------------------------------

    def test_dry_run_writes_nothing(self):
        archive = make_zip(self.tmp / "p.zip", [("sprites/a.png", b"a")])
        record = assets.import_pack("ui-pack-sci-fi", archive, self.out,
                                    str(archive), False, True)
        self.assertTrue(record["dry_run"])
        self.assertEqual(record["files"], 1)
        self.assertFalse(self.out.exists())

    # --- manifest handling ---------------------------------------------

    def test_manifest_merge_and_schema(self):
        a = self.import_one([("sprites/a.png", b"a")], pack="ui-pack-sci-fi")
        b = self.import_one([("sounds/x.ogg", b"o")], pack="sci-fi-sounds")
        assets.write_manifest(self.manifest, [a])
        assets.write_manifest(self.manifest, [b])
        data = json.loads(self.manifest.read_text())
        self.assertEqual(data["schema_version"], assets.SCHEMA_VERSION)
        self.assertEqual([r["pack"] for r in data["packs"]],
                         ["sci-fi-sounds", "ui-pack-sci-fi"])

    def test_corrupt_manifest_is_fatal_and_writes_nothing(self):
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        self.manifest.write_text("{not json")
        archive = make_zip(self.tmp / "p.zip", [("sprites/a.png", b"a")])
        code = assets.main(["--archive", f"ui-pack-sci-fi={archive}",
                            "--output", str(self.out),
                            "--manifest", str(self.manifest)])
        self.assertEqual(code, 2)
        self.assertFalse(self.out.exists())
        self.assertEqual(self.manifest.read_text(), "{not json")

    def test_wrong_schema_version_is_fatal(self):
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        self.manifest.write_text(json.dumps({"schema_version": 99, "packs": []}))
        with self.assertRaises(assets.ManifestError):
            assets.load_manifest(self.manifest)

    # --- check mode -----------------------------------------------------

    def test_check_detects_missing_and_modified_files(self):
        record = self.import_one([("sprites/a.png", b"a"), ("sprites/b.png", b"b")])
        assets.write_manifest(self.manifest, [record])
        self.assertEqual(assets.check_manifest(self.manifest, self.out), 0)
        (self.out / "ui-pack-sci-fi" / "sprites" / "a.png").unlink()
        (self.out / "ui-pack-sci-fi" / "sprites" / "b.png").write_bytes(b"tampered")
        self.assertEqual(assets.check_manifest(self.manifest, self.out), 1)

    # --- CLI plumbing ---------------------------------------------------

    def test_duplicate_pack_rejected_by_cli(self):
        zip_a = make_zip(self.tmp / "a.zip", [("sprites/a.png", b"a")])
        zip_b = make_zip(self.tmp / "b.zip", [("sprites/b.png", b"b")])
        with self.assertRaises(SystemExit):
            assets.main(["--archive", f"ui-pack-sci-fi={zip_a}",
                         "--archive", f"ui-pack-sci-fi={zip_b}",
                         "--output", str(self.out),
                         "--manifest", str(self.manifest)])

    def test_unknown_pack_rejected(self):
        with self.assertRaises(Exception):
            assets.parse_item("not-a-pack=file.zip")

    def test_list_prints_official_pages(self):
        buffer = io.StringIO()
        with mock.patch("sys.stdout", buffer):
            self.assertEqual(assets.main(["--list"]), 0)
        out = buffer.getvalue()
        self.assertIn("space-shooter-remastered", out)
        self.assertIn("https://kenney.nl/assets/", out)

    def test_cli_import_end_to_end(self):
        archive = make_zip(self.tmp / "p.zip", [
            ("PNG/ship.png", b"png"),
            ("License.txt", b"CC0"),
        ])
        code = assets.main(["--archive", f"space-shooter-remastered={archive}",
                            "--output", str(self.out),
                            "--manifest", str(self.manifest)])
        self.assertEqual(code, 0)
        data = json.loads(self.manifest.read_text())
        self.assertEqual(data["packs"][0]["pack"], "space-shooter-remastered")
        self.assertEqual(data["packs"][0]["license_review"], "CHECK_LICENSE_CONTENT")


if __name__ == "__main__":
    unittest.main(verbosity=2)
