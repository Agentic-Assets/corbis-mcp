#!/usr/bin/env python3
"""Portable static checks for the thin Corbis remote-MCP source package.

Run without network access for descriptor and documentation contracts:

    python3 tests/validate_package.py

Pass --release to check structural public release material. This fails closed
until that material has been supplied, but it does not grant founder approval:

    python3 tests/validate_package.py --release

Pass --smoke to perform the intentionally separate, unauthenticated endpoint
and OAuth protected-resource metadata probes. The smoke probe uses no tokens,
does not start OAuth, and does not invoke a tool.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unittest
import zlib
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://www.corbis.ai/api/mcp/universal"
REPOSITORY_URL = "https://github.com/Agentic-Assets/corbis-mcp"
PACKAGE_ID = "corbis"
DISPLAY_NAME = "Corbis"
PUBLISHER = "Agentic Assets"
MANIFEST_FILES = {
    "claude": REPOSITORY_ROOT / ".claude-plugin/plugin.json",
    "codex": REPOSITORY_ROOT / ".codex-plugin/plugin.json",
    "cursor": REPOSITORY_ROOT / ".cursor-plugin/plugin.json",
}
MCP_FILES = {
    "codex": REPOSITORY_ROOT / ".mcp.json",
    "cursor": REPOSITORY_ROOT / "mcp.json",
}
REQUIRED_PACKAGE_FILES = [
    *MANIFEST_FILES.values(),
    *MCP_FILES.values(),
    REPOSITORY_ROOT / "README.md",
    REPOSITORY_ROOT / "CHANGELOG.md",
]
OPTIONAL_PUBLIC_TEXT_FILES = [
    REPOSITORY_ROOT / "LICENSE",
    REPOSITORY_ROOT / "SECURITY.md",
    REPOSITORY_ROOT / "SUPPORT.md",
]
RELEASE_REQUIRED_TEXT_RELATIVE_PATHS = (
    Path("LICENSE"),
    Path("SECURITY.md"),
    Path("SUPPORT.md"),
)
RELEASE_REQUIRED_ASSET_RELATIVE_PATHS = (
    Path("assets/icon.png"),
    Path("assets/logo.png"),
    Path("assets/logo-dark.png"),
)
RELEASE_REQUIRED_RELATIVE_PATHS = (
    *RELEASE_REQUIRED_TEXT_RELATIVE_PATHS,
    *RELEASE_REQUIRED_ASSET_RELATIVE_PATHS,
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_PUBLIC_PNG_BYTES = 5 * 1024 * 1024
MAX_PUBLIC_PNG_DECODED_BYTES = 64 * 1024 * 1024
PNG_CHANNELS = {
    0: 1,
    2: 3,
    3: 1,
    4: 2,
    6: 4,
}
PNG_BIT_DEPTHS = {
    0: {1, 2, 4, 8, 16},
    2: {8, 16},
    3: {1, 2, 4, 8},
    4: {8, 16},
    6: {8, 16},
}
ADAM7_PASSES = (
    (0, 0, 8, 8),
    (4, 0, 8, 8),
    (0, 4, 4, 8),
    (2, 0, 4, 4),
    (0, 2, 2, 4),
    (1, 0, 2, 2),
    (0, 1, 1, 2),
)
ALLOWED_TOP_LEVEL_ENTRIES = {
    ".agents",
    ".claude-plugin",
    ".codex-plugin",
    ".cursor-plugin",
    ".gitattributes",
    ".gitignore",
    ".mcp.json",
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "assets",
    "docs",
    "goals",
    "mcp.json",
    "skills-lock.json",
    "tests",
}
FORBIDDEN_TREE_ENTRY_NAMES = {
    ".DS_Store",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
FORBIDDEN_TOP_LEVEL_ENTRIES = {
    "Dockerfile",
    "package-lock.json",
    "package.json",
    "pnpm-lock.yaml",
    "pyproject.toml",
    "requirements.txt",
    "yarn.lock",
}
PLACEHOLDER_PATTERN = re.compile(
    r"(?:TODO|TBD|CHANGE[ _-]?ME|YOUR[_ -]|example\.com|\[INSERT[^]]*\])",
    re.IGNORECASE,
)
SENSITIVE_KEY_PATTERN = re.compile(
    r"(?:api[_-]?key|access[_-]?token|bearer|client[_-]?secret|password|authorization)",
    re.IGNORECASE,
)
FORBIDDEN_URL_PREFIXES = ("http:", "file:", "data:", "javascript:")
FORBIDDEN_VALUE_PATTERN = re.compile(
    r"(?:-----BEGIN [^-]+-----|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{16,}|"
    r"Bearer\s+(?!token\b|access\b|credential\b)[A-Za-z0-9._~-]{16,}|"
    r"(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\"']?[A-Za-z0-9._~-]{16,})",
    re.IGNORECASE,
)
LOCAL_OR_PRIVATE_PATH_PATTERN = re.compile(
    r"(?:file:|localhost|127\.0\.0\.1|0\.0\.0\.0|::1|"
    r"10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.|"
    r"/(?:Users|home)/|~/(?:\.claude|\.codex|\.cursor))",
    re.IGNORECASE,
)
MANIFEST_ALLOWED_KEYS = {
    "claude": {
        "$schema", "name", "displayName", "version", "description", "author",
        "repository", "mcpServers", "defaultEnabled",
    },
    "codex": {
        "name", "version", "description", "author", "repository", "mcpServers", "interface",
    },
    "cursor": {
        "name", "version", "description", "author", "repository", "mcpServers",
    },
}


def load_json(file_path: Path) -> dict[str, object]:
    with file_path.open(encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise AssertionError(f"{file_path.relative_to(REPOSITORY_ROOT)} must contain a JSON object")
    return value


def iter_strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, nested_value in value.items():
            yield str(key)
            yield from iter_strings(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from iter_strings(nested_value)


def iter_keys(value: object):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield str(key)
            yield from iter_keys(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from iter_keys(nested_value)


def assert_relative_file_reference(case: unittest.TestCase, manifest_name: str, value: object) -> Path:
    case.assertIsInstance(value, str, f"{manifest_name} MCP reference must be a string")
    reference = value
    assert isinstance(reference, str)
    case.assertTrue(reference.startswith("./"), f"{manifest_name} MCP reference must start with ./")
    case.assertNotIn("..", Path(reference).parts, f"{manifest_name} MCP reference cannot traverse")
    resolved = (REPOSITORY_ROOT / reference).resolve()
    case.assertTrue(resolved.is_relative_to(REPOSITORY_ROOT), f"{manifest_name} MCP reference must remain in package")
    case.assertTrue(resolved.is_file(), f"{manifest_name} MCP reference must exist")
    return resolved


def iter_source_paths():
    for directory_name, directory_names, file_names in os.walk(REPOSITORY_ROOT):
        directory_path = Path(directory_name)
        directory_names[:] = [name for name in directory_names if name != ".git"]
        for nested_directory in directory_names:
            yield directory_path / nested_directory
        for file_name in file_names:
            yield directory_path / file_name


def public_package_text_files() -> list[Path]:
    text_files = [*REQUIRED_PACKAGE_FILES, *OPTIONAL_PUBLIC_TEXT_FILES]
    return [file_path for file_path in text_files if file_path.is_file()]


def missing_release_material(root: Path = REPOSITORY_ROOT) -> list[str]:
    """Return structural release paths that are missing, directories, or symlinks.

    The default package checks deliberately allow a reviewable source package
    before public legal, support, and brand decisions are made. A release
    attempt must not silently inherit that allowance.
    """

    return [
        str(relative_path)
        for relative_path in RELEASE_REQUIRED_RELATIVE_PATHS
        if not (root / relative_path).is_file() or (root / relative_path).is_symlink()
    ]


def expected_png_decoded_size(
    width: int,
    height: int,
    bit_depth: int,
    color_type: int,
    interlace_method: int,
) -> int:
    channels = PNG_CHANNELS[color_type]

    def scanline_size(pixel_width: int) -> int:
        return 1 + (pixel_width * channels * bit_depth + 7) // 8

    if interlace_method == 0:
        return height * scanline_size(width)

    total_size = 0
    for start_x, start_y, step_x, step_y in ADAM7_PASSES:
        pass_width = max(0, (width - start_x + step_x - 1) // step_x)
        pass_height = max(0, (height - start_y + step_y - 1) // step_y)
        if pass_width and pass_height:
            total_size += pass_height * scanline_size(pass_width)
    return total_size


def validate_release_png(asset: Path, relative: Path) -> None:
    message = f"Release material has an invalid PNG asset: {relative}"
    asset_size = asset.stat().st_size
    if not 45 <= asset_size <= MAX_PUBLIC_PNG_BYTES:
        raise RuntimeError(message)
    content = asset.read_bytes()
    if not content.startswith(PNG_SIGNATURE):
        raise RuntimeError(message)

    position = len(PNG_SIGNATURE)
    first_chunk = True
    saw_idat = False
    saw_iend = False
    idat_chunks: list[bytes] = []
    after_idat = False
    expected_decoded_size: int | None = None
    while position < len(content):
        if position + 12 > len(content):
            raise RuntimeError(message)
        length = int.from_bytes(content[position:position + 4], "big")
        chunk_type = content[position + 4:position + 8]
        chunk_end = position + 12 + length
        if chunk_end > len(content):
            raise RuntimeError(message)
        chunk_data = content[position + 8:position + 8 + length]
        declared_crc = int.from_bytes(content[position + 8 + length:chunk_end], "big")
        if zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF != declared_crc:
            raise RuntimeError(message)
        if first_chunk:
            width = int.from_bytes(chunk_data[:4], "big")
            height = int.from_bytes(chunk_data[4:8], "big")
            bit_depth = chunk_data[8]
            color_type = chunk_data[9]
            compression_method = chunk_data[10]
            filter_method = chunk_data[11]
            interlace_method = chunk_data[12]
            if (
                chunk_type != b"IHDR"
                or length != 13
                or width <= 0
                or height <= 0
                or color_type not in PNG_CHANNELS
                or bit_depth not in PNG_BIT_DEPTHS[color_type]
                or compression_method != 0
                or filter_method != 0
                or interlace_method not in {0, 1}
            ):
                raise RuntimeError(message)
            expected_decoded_size = expected_png_decoded_size(
                width, height, bit_depth, color_type, interlace_method
            )
            if expected_decoded_size > MAX_PUBLIC_PNG_DECODED_BYTES:
                raise RuntimeError(message)
            first_chunk = False
        elif chunk_type == b"IDAT":
            if after_idat:
                raise RuntimeError(message)
            saw_idat = True
            idat_chunks.append(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0 or chunk_end != len(content):
                raise RuntimeError(message)
            saw_iend = True
            break
        else:
            if saw_idat:
                after_idat = True
            if not all(65 <= byte <= 90 or 97 <= byte <= 122 for byte in chunk_type):
                raise RuntimeError(message)
            if chunk_type[0] & 0x20 == 0:
                raise RuntimeError(message)
        position = chunk_end
    if first_chunk or not saw_idat or not saw_iend or expected_decoded_size is None:
        raise RuntimeError(message)

    try:
        decompressor = zlib.decompressobj()
        decoded_size = 0
        for chunk_data in idat_chunks:
            remaining = chunk_data
            while remaining:
                decoded = decompressor.decompress(remaining, 64 * 1024)
                decoded_size += len(decoded)
                if decoded_size > MAX_PUBLIC_PNG_DECODED_BYTES:
                    raise RuntimeError(message)
                next_remaining = decompressor.unconsumed_tail
                if next_remaining == remaining and not decoded:
                    raise RuntimeError(message)
                remaining = next_remaining
        decoded_size += len(decompressor.flush(64 * 1024))
    except zlib.error as exc:
        raise RuntimeError(message) from exc
    if (
        decoded_size > MAX_PUBLIC_PNG_DECODED_BYTES
        or decoded_size != expected_decoded_size
        or not decompressor.eof
        or decompressor.unused_data
    ):
        raise RuntimeError(message)


def validate_release_material(root: Path = REPOSITORY_ROOT) -> None:
    missing = missing_release_material(root)
    if missing:
        raise RuntimeError(
            "Release material is incomplete; add regular public release files: "
            + ", ".join(missing)
        )
    for relative_path in RELEASE_REQUIRED_TEXT_RELATIVE_PATHS:
        candidate = root / relative_path
        try:
            content = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"Release text material must be UTF-8: {relative_path}") from exc
        if not content.strip():
            raise RuntimeError(f"Release text material must be non-empty: {relative_path}")
        if PLACEHOLDER_PATTERN.search(content):
            raise RuntimeError(f"Release text material contains a placeholder: {relative_path}")
        if FORBIDDEN_VALUE_PATTERN.search(content) or LOCAL_OR_PRIVATE_PATH_PATTERN.search(content):
            raise RuntimeError(f"Release text material contains prohibited content: {relative_path}")
    for relative_path in RELEASE_REQUIRED_ASSET_RELATIVE_PATHS:
        validate_release_png(root / relative_path, relative_path)


class PackageContractTests(unittest.TestCase):
    def test_credential_detector_is_specific_to_values(self) -> None:
        self.assertIsNotNone(FORBIDDEN_VALUE_PATTERN.search("Bearer abcdefghijklmnop"))
        self.assertIsNotNone(FORBIDDEN_VALUE_PATTERN.search("client_secret=abcdefghijklmnop"))
        self.assertIsNone(FORBIDDEN_VALUE_PATTERN.search("Bearer token"))
        self.assertIsNone(FORBIDDEN_VALUE_PATTERN.search("OAuth is the default path"))

    def test_source_tree_excludes_caches_and_undeclared_top_level_components(self) -> None:
        top_level_entries = {
            entry.name for entry in REPOSITORY_ROOT.iterdir() if entry.name != ".git"
        }
        unexpected = sorted(top_level_entries.difference(ALLOWED_TOP_LEVEL_ENTRIES))
        forbidden_top_level = sorted(top_level_entries.intersection(FORBIDDEN_TOP_LEVEL_ENTRIES))
        forbidden_paths = sorted(
            str(path.relative_to(REPOSITORY_ROOT))
            for path in iter_source_paths()
            if path.name in FORBIDDEN_TREE_ENTRY_NAMES
        )

        self.assertEqual(unexpected, [], f"Unexpected top-level package components: {unexpected}")
        self.assertEqual(forbidden_top_level, [], f"Dependency or runtime files are prohibited: {forbidden_top_level}")
        self.assertEqual(forbidden_paths, [], f"Caches or build artifacts are prohibited: {forbidden_paths}")

    def test_required_package_files_exist(self) -> None:
        missing = [str(file_path.relative_to(REPOSITORY_ROOT)) for file_path in REQUIRED_PACKAGE_FILES if not file_path.is_file()]
        self.assertEqual(missing, [], f"Missing package files: {', '.join(missing)}")

    def test_release_material_contract_is_explicit_and_rejects_symlinks(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(
                missing_release_material(root),
                [str(path) for path in RELEASE_REQUIRED_RELATIVE_PATHS],
            )

            for relative_path in RELEASE_REQUIRED_TEXT_RELATIVE_PATHS:
                candidate = root / relative_path
                candidate.parent.mkdir(parents=True, exist_ok=True)
                candidate.write_text("Reviewed public release material\n", encoding="utf-8")
            valid_png = bytes.fromhex(
                "89504e470d0a1a0a0000000d49484452000000010000000108000000003a7e9b55"
                "0000000a49444154789c63f80f0001010100b138f6140000000049454e44ae426082"
            )
            for relative_path in RELEASE_REQUIRED_ASSET_RELATIVE_PATHS:
                candidate = root / relative_path
                candidate.parent.mkdir(parents=True, exist_ok=True)
                candidate.write_bytes(valid_png)
            self.assertEqual(missing_release_material(root), [])
            validate_release_material(root)

            support_path = root / "SUPPORT.md"
            support_path.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "must be non-empty: SUPPORT.md"):
                validate_release_material(root)
            support_path.write_text("Reviewed public release material\n", encoding="utf-8")

            icon_path = root / "assets/icon.png"
            icon_path.write_bytes(b"not a PNG")
            with self.assertRaisesRegex(RuntimeError, "invalid PNG asset: assets/icon.png"):
                validate_release_material(root)
            icon_path.write_bytes(valid_png)

            def png_chunk(chunk_type: bytes, chunk_data: bytes) -> bytes:
                return (
                    len(chunk_data).to_bytes(4, "big")
                    + chunk_type
                    + chunk_data
                    + (zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF).to_bytes(4, "big")
                )

            png_header = PNG_SIGNATURE + png_chunk(
                b"IHDR", bytes.fromhex("00000001000000010800000000")
            )
            valid_idat = bytes.fromhex("789c63f80f0001010100")
            split_idat_png = (
                png_header
                + png_chunk(b"IDAT", valid_idat[:5])
                + png_chunk(b"IDAT", valid_idat[5:])
                + png_chunk(b"IEND", b"")
            )
            icon_path.write_bytes(split_idat_png)
            validate_release_material(root)

            corrupt_png = (
                png_header
                + png_chunk(b"IDAT", b"not-a-zlib-stream")
                + png_chunk(b"IEND", b"")
            )
            icon_path.write_bytes(corrupt_png)
            with self.assertRaisesRegex(RuntimeError, "invalid PNG asset: assets/icon.png"):
                validate_release_material(root)

            trailing_data_png = (
                png_header + png_chunk(b"IDAT", valid_idat + b"\x00") + png_chunk(b"IEND", b"")
            )
            icon_path.write_bytes(trailing_data_png)
            with self.assertRaisesRegex(RuntimeError, "invalid PNG asset: assets/icon.png"):
                validate_release_material(root)

            rgba_png_header = PNG_SIGNATURE + png_chunk(
                b"IHDR", bytes.fromhex("00000001000000010806000000")
            )
            short_scanline_png = (
                rgba_png_header
                + png_chunk(b"IDAT", zlib.compress(b"\x00"))
                + png_chunk(b"IEND", b"")
            )
            icon_path.write_bytes(short_scanline_png)
            with self.assertRaisesRegex(RuntimeError, "invalid PNG asset: assets/icon.png"):
                validate_release_material(root)
            icon_path.write_bytes(valid_png)

            license_path = root / "LICENSE"
            release_copy = root / "approved-license-copy"
            release_copy.write_text(license_path.read_text(encoding="utf-8"), encoding="utf-8")
            license_path.unlink()
            license_path.symlink_to(release_copy)
            self.assertEqual(missing_release_material(root), ["LICENSE"])

    def test_manifest_metadata_is_consistent(self) -> None:
        manifests = {name: load_json(file_path) for name, file_path in MANIFEST_FILES.items()}
        versions = {manifest["version"] for manifest in manifests.values()}

        self.assertEqual(versions.__len__(), 1, "All client manifests must carry one release version")
        version = versions.pop()
        self.assertIsInstance(version, str)
        self.assertRegex(str(version), r"^\d+\.\d+\.\d+$", "Version must be plain SemVer")

        for manifest_name, manifest in manifests.items():
            self.assertEqual(manifest.get("name"), PACKAGE_ID, f"{manifest_name} package ID drifted")
            self.assertEqual(manifest.get("repository"), REPOSITORY_URL, f"{manifest_name} repository drifted")
            author = manifest.get("author")
            self.assertIsInstance(author, dict, f"{manifest_name} author must be an object")
            self.assertEqual(author.get("name"), PUBLISHER, f"{manifest_name} publisher drifted")
            self.assertIn("authenticated account", str(manifest.get("description", "")), f"{manifest_name} must retain entitlement-aware copy")

        self.assertEqual(manifests["claude"].get("displayName"), DISPLAY_NAME)
        codex_interface = manifests["codex"].get("interface")
        self.assertIsInstance(codex_interface, dict)
        self.assertEqual(codex_interface.get("displayName"), DISPLAY_NAME)

    def test_manifests_have_no_undeclared_components_or_local_assets(self) -> None:
        for manifest_name, file_path in MANIFEST_FILES.items():
            manifest = load_json(file_path)
            self.assertEqual(
                set(manifest).difference(MANIFEST_ALLOWED_KEYS[manifest_name]),
                set(),
                f"{manifest_name} declares an unsupported component or unexpected field",
            )
            for asset_key in ("composerIcon", "logo", "screenshots"):
                interface = manifest.get("interface")
                if not isinstance(interface, dict) or asset_key not in interface:
                    continue
                asset_values = interface[asset_key]
                if isinstance(asset_values, str):
                    asset_values = [asset_values]
                self.assertIsInstance(asset_values, list)
                for asset_value in asset_values:
                    asset_reference = assert_relative_file_reference(self, f"{manifest_name} {asset_key}", asset_value)
                    self.assertTrue(asset_reference.is_relative_to(REPOSITORY_ROOT / "assets"))

    def test_manifests_reference_their_client_specific_mcp_files(self) -> None:
        codex_reference = assert_relative_file_reference(
            self, "Codex", load_json(MANIFEST_FILES["codex"]).get("mcpServers")
        )
        cursor_reference = assert_relative_file_reference(
            self, "Cursor", load_json(MANIFEST_FILES["cursor"]).get("mcpServers")
        )

        self.assertEqual(codex_reference, MCP_FILES["codex"].resolve())
        self.assertEqual(cursor_reference, MCP_FILES["cursor"].resolve())

    def test_exact_endpoint_and_client_specific_mcp_shapes(self) -> None:
        codex_mcp = load_json(MCP_FILES["codex"])
        cursor_mcp = load_json(MCP_FILES["cursor"])

        self.assertEqual(set(codex_mcp), {"mcpServers"})
        self.assertEqual(set(cursor_mcp), {"mcpServers"})
        self.assertEqual(codex_mcp["mcpServers"], {PACKAGE_ID: {"url": ENDPOINT}})
        self.assertEqual(cursor_mcp["mcpServers"], {PACKAGE_ID: {"url": ENDPOINT}})

        claude_manifest = load_json(MANIFEST_FILES["claude"])
        claude_mcp = claude_manifest.get("mcpServers")
        self.assertIsInstance(claude_mcp, dict)
        assert isinstance(claude_mcp, dict)
        self.assertEqual(
            claude_mcp[PACKAGE_ID]["url"], ENDPOINT,
            "The Claude remote MCP configuration must use the exact endpoint",
        )
        self.assertEqual(
            claude_mcp[PACKAGE_ID]["type"], "http",
            "Claude must use the HTTP transport for the remote endpoint",
        )

    def test_readme_matches_the_checked_in_codex_mcp_shape(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`mcpServers`", readme)
        self.assertNotIn("`mcp_servers`", readme)

    def test_no_placeholders_credentials_or_unsafe_urls_appear_in_config(self) -> None:
        configuration = {
            **{name: load_json(file_path) for name, file_path in MANIFEST_FILES.items()},
            **{name: load_json(file_path) for name, file_path in MCP_FILES.items()},
        }
        all_strings = list(iter_strings(configuration))
        all_keys = list(iter_keys(configuration))
        placeholders = [value for value in all_strings if PLACEHOLDER_PATTERN.search(value)]
        sensitive_keys = [value for value in all_keys if SENSITIVE_KEY_PATTERN.search(value)]
        unsafe_urls = [
            value
            for value in all_strings
            if value.lower().startswith(FORBIDDEN_URL_PREFIXES)
            or "localhost" in value.lower()
            or "/users/" in value.lower()
        ]
        sensitive_values = [value for value in all_strings if FORBIDDEN_VALUE_PATTERN.search(value)]

        self.assertEqual(placeholders, [], f"Placeholder material is prohibited: {placeholders}")
        self.assertEqual(sensitive_keys, [], f"Credential material is prohibited: {sensitive_keys}")
        self.assertEqual(sensitive_values, [], f"Credential material is prohibited: {sensitive_values}")
        self.assertEqual(unsafe_urls, [], f"Unsafe or local URL material is prohibited: {unsafe_urls}")

        endpoint = urlparse(ENDPOINT)
        self.assertEqual(endpoint.scheme, "https")
        self.assertEqual(endpoint.query, "")
        self.assertEqual(endpoint.fragment, "")

    def test_candidate_public_text_contains_no_credentials_or_local_paths(self) -> None:
        findings: list[str] = []
        for file_path in public_package_text_files():
            content = file_path.read_text(encoding="utf-8")
            relative_path = file_path.relative_to(REPOSITORY_ROOT)
            if PLACEHOLDER_PATTERN.search(content):
                findings.append(f"{relative_path}: placeholder")
            if FORBIDDEN_VALUE_PATTERN.search(content):
                findings.append(f"{relative_path}: credential-like value")
            if LOCAL_OR_PRIVATE_PATH_PATTERN.search(content):
                findings.append(f"{relative_path}: local or private path")

        self.assertEqual(findings, [], f"Public package text has prohibited material: {findings}")

    def test_declared_public_package_links_exist_and_remain_contained(self) -> None:
        missing: list[str] = []
        for file_path in public_package_text_files():
            content = file_path.read_text(encoding="utf-8")
            local_targets = re.findall(r"\[[^]]+\]\(([^)#]+)(?:#[^)]+)?\)", content)
            for target in local_targets:
                if target.startswith(("https://", "http://", "mailto:")):
                    continue
                resolved = (REPOSITORY_ROOT / target).resolve()
                if not resolved.is_relative_to(REPOSITORY_ROOT) or not resolved.exists():
                    missing.append(f"{file_path.relative_to(REPOSITORY_ROOT)}: {target}")
        self.assertEqual(missing, [], f"README contains missing or escaping local links: {missing}")


def run_smoke_probe() -> None:
    checked_at = datetime.now(UTC).isoformat()
    metadata_url = "https://www.corbis.ai/.well-known/oauth-protected-resource/api/mcp/universal"
    requests = {
        "endpoint": Request(ENDPOINT, method="GET"),
        "protected-resource metadata": Request(metadata_url, method="GET"),
    }
    print(f"Live smoke probe started at {checked_at}")
    for label, request in requests.items():
        with urlopen(request, timeout=15) as response:  # nosec B310: fixed HTTPS endpoints above
            if response.status != 200:
                raise RuntimeError(f"{label} returned HTTP {response.status}")
            if label == "protected-resource metadata":
                payload = json.loads(response.read().decode("utf-8"))
                if payload.get("resource") != ENDPOINT:
                    raise RuntimeError("Protected-resource metadata does not identify the approved endpoint")
            print(f"{label}: HTTP {response.status}")
    print("Live smoke probe passed. It did not authenticate or invoke tools.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--release",
        action="store_true",
        help="Check structural public legal, support, and asset material; it does not grant human approval",
    )
    parser.add_argument("--smoke", action="store_true", help="Run the separate unauthenticated network smoke probe")
    arguments, unittest_arguments = parser.parse_known_args()
    test_result = unittest.main(argv=[sys.argv[0], *unittest_arguments], exit=False).result
    if not test_result.wasSuccessful():
        raise SystemExit(1)
    if arguments.release:
        validate_release_material()
    if arguments.smoke:
        run_smoke_probe()
