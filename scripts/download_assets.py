#!/usr/bin/env python3
"""Spirit Space development-time asset importer (stdlib only).

Official Kenney downloads may require browser interaction. Supply a downloaded
ZIP with --archive PACK=FILE, or an explicit trusted ZIP URL with
--source PACK=URL. The tool never guesses download links, never bypasses a
site's download flow, and never runs at game runtime (see ADR-0011).

Subcommands / modes
    --list                 show the official pack pages
    --archive PACK=ZIP     import a manually downloaded archive
    --source PACK=URL      import from an explicit HTTPS ZIP address
    --check                verify installed files against the manifest
    --dry-run              report what would happen, write nothing

Exit codes: 0 success, 1 one or more pack failures, 2 usage/manifest problem.
The tool never marks a license as approved; a human must review.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

PACKS = {
    "space-shooter-remastered": "https://kenney.nl/assets/space-shooter-remastered",
    "space-shooter-extension": "https://kenney.nl/assets/space-shooter-extension",
    "ui-pack-sci-fi": "https://kenney.nl/assets/ui-pack-sci-fi",
    "simple-space": "https://kenney.nl/assets/simple-space",
    "sci-fi-sounds": "https://kenney.nl/assets/sci-fi-sounds",
    "digital-audio": "https://kenney.nl/assets/digital-audio",
    "interface-sounds": "https://kenney.nl/assets/interface-sounds",
    "impact-sounds": "https://kenney.nl/assets/impact-sounds",
}
MAX_ARCHIVE = 120 * 1024 * 1024
MAX_TOTAL_EXTRACTED = 350 * 1024 * 1024
MAX_FILE = 40 * 1024 * 1024
ALLOWED_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".webp", ".svg",
    ".ogg", ".wav", ".mp3",
    ".txt", ".md", ".xml", ".json",
}
LICENSE_HINTS = ("license", "licence", "copyright", "credit", "attribution")
SCHEMA_VERSION = 1


class ManifestError(Exception):
    """The manifest exists but cannot be trusted."""


def checksum(path):
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_item(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected PACK=PATH or PACK=URL")
    pack, rest = value.split("=", 1)
    if pack not in PACKS:
        raise argparse.ArgumentTypeError(
            f"Unknown pack {pack!r}; choices: {', '.join(PACKS)}")
    if not rest:
        raise argparse.ArgumentTypeError("Missing source")
    return pack, rest


def fetch_archive(url, dest):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Only explicit HTTPS URLs are permitted")
    req = urllib.request.Request(
        url, headers={"User-Agent": "SpiritSpaceAssetImporter/2.0"})
    with urllib.request.urlopen(req, timeout=30) as response, dest.open("wb") as out:
        final = urllib.parse.urlparse(response.geturl())
        if final.scheme != "https":
            raise ValueError("Redirect downgraded from HTTPS")
        transferred = 0
        while True:
            data = response.read(1024 * 1024)
            if not data:
                break
            transferred += len(data)
            if transferred > MAX_ARCHIVE:
                raise ValueError(f"Archive exceeds {MAX_ARCHIVE // (1024 * 1024)} MiB limit")
            out.write(data)


def is_license_name(name):
    return any(hint in name.lower() for hint in LICENSE_HINTS)


def safe_members(zf):
    """Return [(ZipInfo, PurePosixPath, is_license)] after safety and size checks."""
    members = []
    declared_total = 0
    for member in zf.infolist():
        if member.is_dir():
            continue
        raw = member.filename.replace("\\", "/")
        path = pathlib.PurePosixPath(raw)
        if not path.parts or path.is_absolute() or ".." in path.parts or "" in path.parts:
            raise ValueError(f"Unsafe archive path: {member.filename!r}")
        if ":" in path.parts[0]:
            raise ValueError(f"Drive-qualified path rejected: {member.filename!r}")
        if (member.external_attr >> 16) & 0o170000 == 0o120000:
            raise ValueError(f"Symlink in ZIP rejected: {member.filename!r}")
        if member.file_size > MAX_FILE:
            raise ValueError(f"File too large: {member.filename!r}")
        declared_total += member.file_size
        if declared_total > MAX_TOTAL_EXTRACTED:
            raise ValueError(
                f"Uncompressed content exceeds {MAX_TOTAL_EXTRACTED // (1024 * 1024)} MiB")
        license_file = is_license_name(path.name)
        if not license_file and path.suffix.lower() not in ALLOWED_SUFFIXES:
            continue
        members.append((member, path, license_file))
    return members


def extract_pack(zf, members, temp_pack):
    """Extract members into temp_pack; count real bytes, not declared sizes."""
    installed = []
    license_files = []
    skipped = 0
    written = 0
    for info, relative, license_file in members:
        out = temp_pack.joinpath(*relative.parts)
        out.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(info) as src, out.open("wb") as target:
            while True:
                chunk = src.read(1024 * 1024)
                if not chunk:
                    break
                written += len(chunk)
                if written > MAX_TOTAL_EXTRACTED:
                    raise ValueError("Extraction exceeded the size limit (zip bomb?)")
                target.write(chunk)
        size = out.stat().st_size
        if size != info.file_size:
            skipped += 1
            out.unlink()
            continue
        installed.append(
            {"path": relative.as_posix(), "sha256": checksum(out), "bytes": size})
        if license_file:
            license_files.append(relative.as_posix())
    return installed, license_files, skipped


def swap_in(temp_pack, dest):
    """Replace dest with temp_pack on the *same filesystem*, restoring on failure."""
    backup = dest.parent / (dest.name + ".old")
    if backup.exists():
        shutil.rmtree(backup)
    if dest.exists():
        os.replace(dest, backup)
    try:
        os.replace(temp_pack, dest)
    except OSError:
        if backup.exists():
            os.replace(backup, dest)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def stage_pack(temp_pack, destination, pack):
    """Copy the staged tree beside the destination so the swap can be atomic."""
    staging = destination / f".{pack}.staging"
    if staging.exists():
        shutil.rmtree(staging)
    shutil.copytree(temp_pack, staging)
    return staging


def import_pack(pack, archive, destination, source_url, overwrite, dry_run):
    if not archive.is_file():
        raise FileNotFoundError(archive)
    if archive.stat().st_size > MAX_ARCHIVE:
        raise ValueError(f"Archive exceeds {MAX_ARCHIVE // (1024 * 1024)} MiB limit")
    dest = destination / pack
    if dest.exists() and not overwrite:
        raise FileExistsError(f"{dest} exists; use --overwrite to replace it")

    with zipfile.ZipFile(archive) as zf:
        members = safe_members(zf)
        if not members:
            raise ValueError("No supported assets found in the archive")
        if dry_run:
            return {
                "pack": pack,
                "dry_run": True,
                "files": len(members),
                "bytes": sum(m.file_size for m, _, _ in members),
                "license_files": [p.as_posix() for _, p, lic in members if lic],
            }
        destination.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="spirit-assets-") as tmp:
            temp_pack = pathlib.Path(tmp) / pack
            temp_pack.mkdir()
            installed, license_files, skipped = extract_pack(zf, members, temp_pack)
            if not installed:
                raise ValueError("No supported assets survived extraction")
            # TMPDIR may be on another filesystem, so copy beside the destination
            # before the (same-filesystem) rename swap.
            staging = stage_pack(temp_pack, destination, pack)
            swap_in(staging, dest)

    return {
        "pack": pack,
        "author": "Kenney",
        "license": "CC0 1.0 (verify the License file inside the supplied ZIP)",
        "official_page": PACKS[pack],
        "source_archive": source_url,
        "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "archive_sha256": checksum(archive),
        "archive_bytes": archive.stat().st_size,
        "license_files": license_files,
        "license_review": "REVIEW_REQUIRED" if not license_files else "CHECK_LICENSE_CONTENT",
        "skipped_entries": skipped,
        "files": installed,
    }


def load_manifest(path):
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "packs": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{path} is unreadable or invalid JSON: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ManifestError(
            f"{path} has an unsupported schema (want {SCHEMA_VERSION}); "
            "fix or remove it before importing")
    if not isinstance(data.get("packs"), list):
        raise ManifestError(f"{path} has no valid 'packs' list")
    for record in data["packs"]:
        if not isinstance(record, dict) or "pack" not in record:
            raise ManifestError(f"{path} contains a malformed pack record")
    return data


def write_manifest(path, records):
    data = load_manifest(path)
    lookup = {r["pack"]: r for r in data["packs"]}
    lookup.update({r["pack"]: r for r in records})
    data["schema_version"] = SCHEMA_VERSION
    data["packs"] = sorted(lookup.values(), key=lambda r: r["pack"])
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def check_manifest(path, destination):
    data = load_manifest(path)
    problems = 0
    checked = 0
    for record in data["packs"]:
        pack = record["pack"]
        for entry in record.get("files", []):
            target = destination / pack / entry["path"]
            checked += 1
            if not target.is_file():
                print(f"MISSING {pack}/{entry['path']}", file=sys.stderr)
                problems += 1
            elif checksum(target) != entry["sha256"]:
                print(f"MODIFIED {pack}/{entry['path']}", file=sys.stderr)
                problems += 1
    print(f"Checked {checked} files across {len(data['packs'])} pack(s); "
          f"{problems} problem(s)")
    return 1 if problems else 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="Show official pack pages")
    parser.add_argument("--archive", action="append", type=parse_item, default=[],
                        metavar="PACK=ZIP", help="Import a manually downloaded ZIP")
    parser.add_argument("--source", action="append", type=parse_item, default=[],
                        metavar="PACK=HTTPS_URL", help="Download from a trusted explicit ZIP URL")
    parser.add_argument("--output", type=pathlib.Path,
                        default=pathlib.Path("assets/vendor/kenney"))
    parser.add_argument("--manifest", type=pathlib.Path,
                        default=pathlib.Path("assets/asset-manifest.json"))
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true",
                        help="Verify installed files against the manifest")
    args = parser.parse_args(argv)

    if args.list:
        for name, page in PACKS.items():
            print(f"{name:27} {page}")
        if not (args.archive or args.source or args.check):
            return 0

    if args.check:
        try:
            return check_manifest(args.manifest, args.output)
        except ManifestError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    try:
        load_manifest(args.manifest)  # fail fast before downloading anything
    except ManifestError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    items = [(p, pathlib.Path(f).expanduser(), str(pathlib.Path(f).expanduser()))
             for p, f in args.archive]
    names = [p for p, _, _ in items] + [p for p, _ in args.source]
    if len(names) != len(set(names)):
        parser.error("Specify a pack only once per command")
    if not items and not args.source:
        if not args.list:
            parser.print_help()
        return 0

    if args.dry_run:
        for p, archive, _ in items:
            try:
                record = import_pack(p, archive, args.output, str(archive), False, True)
                print(f"DRY-RUN {p}: {record['files']} files, {record['bytes']} bytes, "
                      f"license files: {record['license_files'] or 'none'}")
            except (OSError, ValueError, zipfile.BadZipFile) as exc:
                print(f"ERROR {p}: {exc}", file=sys.stderr)
        for p, url in args.source:
            print(f"DRY-RUN {p}: would download {url}")
        return 0

    records = []
    failures = 0
    with tempfile.TemporaryDirectory(prefix="spirit-download-") as tmp:
        for p, url in args.source:
            archive = pathlib.Path(tmp) / f"{p}.zip"
            try:
                print(f"Downloading {p} from {url}")
                fetch_archive(url, archive)
                items.append((p, archive, url))
            except Exception as exc:  # network errors are all equivalent here
                failures += 1
                print(f"ERROR {p}: {exc}", file=sys.stderr)
        for p, archive, url in items:
            try:
                record = import_pack(p, archive, args.output, url, args.overwrite, False)
                records.append(record)
                print(f"Imported {p}: {len(record['files'])} supported files "
                      f"({len(record['license_files'])} license file(s)); "
                      f"review: {record['license_review']}")
            except (OSError, ValueError, zipfile.BadZipFile) as exc:
                failures += 1
                print(f"ERROR {p}: {exc}", file=sys.stderr)

    if records:
        write_manifest(args.manifest, records)
        print(f"Updated {args.manifest}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
