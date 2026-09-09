"""Portable static checks for the thin Corbis remote-MCP source package.

Run without network access for descriptor and documentation contracts:

    python3 tests/validate_package.py

Pass --release to check structural public release material. This fails closed
until that material has been supplied, but it does not grant founder approval:

    python3 tests/validate_package.py --release

Pass --smoke to perform the intentionally separate, unauthenticated endpoint
and OAuth metadata probes. The smoke probe uses no tokens, does not start
OAuth, and sends only GET requests for discovery metadata. It never invokes
a tool, registers a client, or obtains a token. The application and Marketplace
own the protected-request HTTP 401 and Bearer challenge checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unittest
import zlib
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urlunparse
from urllib.request import (
    HTTPRedirectHandler,
    ProxyHandler,
    Request,
    build_opener,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://www.corbis.ai/api/mcp/universal"
ENDPOINT_ORIGIN = "https://www.corbis.ai"
ROOT_AUTHORIZATION_SERVER_METADATA_URL = (
    f"{ENDPOINT_ORIGIN}/.well-known/oauth-authorization-server"
)
ROOT_PROTECTED_RESOURCE_METADATA_URL = (
    f"{ENDPOINT_ORIGIN}/.well-known/oauth-protected-resource"
)
RFC_PROTECTED_RESOURCE_METADATA_URL = (
    f"{ENDPOINT_ORIGIN}/.well-known/oauth-protected-resource/api/mcp/universal"
)
REPOSITORY_URL = "https://github.com/Agentic-Assets/corbis-mcp"
WEBSITE_URL = "https://www.corbis.ai"
PRIVACY_POLICY_URL = "https://www.corbis.ai/privacy"
TERMS_OF_SERVICE_URL = "https://www.corbis.ai/terms"
LICENSE_IDENTIFIER = "MIT"
PACKAGE_ID = "corbis"
MCP_SERVER_ID = "corbis-mcp"
DISPLAY_NAME = "Corbis"
PUBLISHER = "Agentic Assets"
RELEASE_VERSION = "0.1.6"
CORBIS_RESEARCH_ICON_SHA256 = "80188a21893d91b9e18f603bce504df80f85ad068bed06cb25a0de9d87545984"
MANIFEST_FILES = {
    "claude": REPOSITORY_ROOT / ".claude-plugin/plugin.json",
    "codex": REPOSITORY_ROOT / ".codex-plugin/plugin.json",
    "cursor": REPOSITORY_ROOT / ".cursor-plugin/plugin.json",
}
MCP_FILES = {
    "codex": REPOSITORY_ROOT / ".mcp.json",
    "cursor": REPOSITORY_ROOT / "mcp.json",
}
SOURCE_PROVENANCE_FILE = REPOSITORY_ROOT / "provenance.json"
CLAUDE_BRIDGE_FILE = REPOSITORY_ROOT / "CLAUDE.md"
CANONICAL_CLAUDE_BRIDGE = "# AGENTS.md is the canonical context file. Only add context there.\n@AGENTS.md\n"
REQUIRED_PACKAGE_FILES = [
    *MANIFEST_FILES.values(),
    *MCP_FILES.values(),
    REPOSITORY_ROOT / "README.md",
    REPOSITORY_ROOT / "CHANGELOG.md",
    SOURCE_PROVENANCE_FILE,
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
MAX_SMOKE_RESPONSE_BYTES = 1024 * 1024
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
    "provenance.json",
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
        "$schema", "name", "displayName", "version", "description", "author", "homepage",
        "repository", "mcpServers", "defaultEnabled",
    },
    "codex": {
        "name", "version", "description", "author", "homepage", "repository", "mcpServers", "interface",
    },
    "cursor": {
        "name", "version", "description", "author", "homepage", "repository", "license", "logo", "mcpServers",
    },
}


@dataclass(frozen=True)
class SmokeHttpResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes
    url: str


SmokeFetcher = Callable[[Request], SmokeHttpResponse]


class _RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


SMOKE_OPENER = build_opener(ProxyHandler({}), _RejectRedirects())


def fetch_smoke_response(request: Request) -> SmokeHttpResponse:
    """Fetch one fixed smoke URL while preserving intentional HTTP errors."""

    try:
        try:
            response = SMOKE_OPENER.open(request, timeout=15)  # nosec B310: validated HTTPS URLs only
        except HTTPError as error:
            response = error
        with response:
            result = SmokeHttpResponse(
                status=response.status,
                headers=_normalized_headers(response.headers),
                body=response.read(MAX_SMOKE_RESPONSE_BYTES + 1),
                url=response.geturl(),
            )
    except (URLError, TimeoutError, OSError) as error:
        raise RuntimeError("Live smoke request failed at the network transport") from error
    if len(result.body) > MAX_SMOKE_RESPONSE_BYTES:
        raise RuntimeError("Live smoke response exceeded the one-megabyte safety limit")
    return result


def _normalized_headers(headers: object) -> dict[str, str]:
    normalized: dict[str, str] = {}
    items = getattr(headers, "items", None)
    if not callable(items):
        return normalized
    for key, value in items():
        normalized_key = str(key).lower()
        normalized_value = str(value)
        if normalized_key in normalized:
            normalized[normalized_key] = f"{normalized[normalized_key]}, {normalized_value}"
        else:
            normalized[normalized_key] = normalized_value
    return normalized


def _https_url(
    label: str,
    value: object,
    *,
    same_origin_as: str | None = None,
    allow_query: bool = False,
) -> str:
    if (
        not isinstance(value, str) or not value
        or any(ord(character) <= 32 or ord(character) >= 127 for character in value)
        or "\\" in value
    ):
        raise RuntimeError(f"{label} must be a non-empty HTTPS URL")
    try:
        parsed = urlparse(value)
        _ = parsed.port  # Access validates malformed or out-of-range ports.
    except ValueError as error:
        raise RuntimeError(f"{label} must be a valid HTTPS URL") from error
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or (parsed.query and not allow_query)
    ):
        raise RuntimeError(f"{label} must be a valid HTTPS URL")
    if same_origin_as is not None and _url_origin(value) != _url_origin(same_origin_as):
        raise RuntimeError(f"{label} must use the Corbis endpoint origin")
    return value


def _url_origin(value: str) -> tuple[str, str, int | None]:
    parsed = urlparse(value)
    port = parsed.port
    if port is None:
        port = 443 if parsed.scheme == "https" else 80 if parsed.scheme == "http" else None
    return parsed.scheme, parsed.hostname or "", port


def _json_object(label: str, response: SmokeHttpResponse) -> dict[str, object]:
    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if content_type != "application/json":
        raise RuntimeError(f"{label} must return application/json")

    def reject_duplicate_members(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON member: {key}")
            result[key] = value
        return result

    def reject_nonfinite_constant(value: str) -> object:
        raise ValueError(f"invalid JSON constant: {value}")

    try:
        payload = json.loads(
            response.body.decode("utf-8"),
            object_pairs_hook=reject_duplicate_members,
            parse_constant=reject_nonfinite_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"{label} returned malformed JSON") from error
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} must return a JSON object")  # noqa: TRY004 - one smoke failure type
    return payload


def _nonempty_string_array(label: str, value: object) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
    ):
        raise RuntimeError(f"{label} must be a non-empty array of strings")
    if len(set(value)) != len(value):
        raise RuntimeError(f"{label} must not contain duplicates")
    return tuple(value)


def validate_protected_resource_metadata(
    label: str,
    payload: Mapping[str, object],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if payload.get("resource") != ENDPOINT:
        raise RuntimeError(f"{label} does not identify the exact Corbis MCP resource")
    authorization_servers = _nonempty_string_array(
        f"{label} authorization_servers",
        payload.get("authorization_servers"),
    )
    for authorization_server in authorization_servers:
        _https_url(
            f"{label} authorization server",
            authorization_server,
            same_origin_as=ENDPOINT,
        )
    scopes = _nonempty_string_array(f"{label} scopes_supported", payload.get("scopes_supported"))
    if any(not re.fullmatch(r"[\x21\x23-\x5B\x5D-\x7E]+", scope) for scope in scopes):
        raise RuntimeError(f"{label} scopes_supported contains an invalid OAuth scope")
    bearer_methods = _nonempty_string_array(
        f"{label} bearer_methods_supported",
        payload.get("bearer_methods_supported"),
    )
    if "header" not in bearer_methods:
        raise RuntimeError(f"{label} must support header bearer tokens")
    return authorization_servers, scopes


def authorization_server_metadata_url(issuer: str) -> str:
    _https_url("authorization server issuer", issuer, same_origin_as=ENDPOINT)
    parsed = urlparse(issuer)
    issuer_path = parsed.path.rstrip("/")
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            f"/.well-known/oauth-authorization-server{issuer_path}",
            "",
            "",
            "",
        )
    )


def validate_authorization_server_metadata(
    issuer: str,
    payload: Mapping[str, object],
) -> None:
    if payload.get("issuer") != issuer:
        raise RuntimeError("Authorization-server metadata issuer does not match the advertised issuer")
    expected_endpoints = {
        "authorization_endpoint": f"{issuer.rstrip('/')}/oauth/authorize",
        "token_endpoint": f"{issuer.rstrip('/')}/oauth/token",
        "registration_endpoint": f"{issuer.rstrip('/')}/oauth/register",
    }
    for field, expected_endpoint in expected_endpoints.items():
        _https_url(
            f"Authorization-server metadata {field}",
            payload.get(field),
            same_origin_as=issuer,
        )
        if payload.get(field) != expected_endpoint:
            raise RuntimeError(
                f"Authorization-server metadata {field} does not match the advertised issuer"
            )
    response_types = _nonempty_string_array(
        "Authorization-server metadata response_types_supported",
        payload.get("response_types_supported"),
    )
    if "code" not in response_types:
        raise RuntimeError("Authorization-server metadata must support response type code")
    grants = _nonempty_string_array(
        "Authorization-server metadata grant_types_supported",
        payload.get("grant_types_supported"),
    )
    missing_grants = {"authorization_code", "refresh_token"}.difference(grants)
    if missing_grants:
        raise RuntimeError(
            "Authorization-server metadata must support authorization_code and refresh_token grants"
        )
    code_challenge_methods = _nonempty_string_array(
        "Authorization-server metadata code_challenge_methods_supported",
        payload.get("code_challenge_methods_supported"),
    )
    if "S256" not in code_challenge_methods:
        raise RuntimeError("Authorization-server metadata must support PKCE S256")


def _fetch_exact(fetcher: SmokeFetcher, label: str, request: Request) -> SmokeHttpResponse:
    response = fetcher(request)
    if len(response.body) > MAX_SMOKE_RESPONSE_BYTES:
        raise RuntimeError(f"{label} exceeded the one-megabyte safety limit")
    if response.url != request.full_url:
        raise RuntimeError(f"{label} redirected away from its exact URL")
    return response


def validate_live_oauth_smoke(fetcher: SmokeFetcher = fetch_smoke_response) -> list[str]:
    observations: list[str] = []

    advertised_servers: tuple[str, ...] | None = None
    metadata_requests = (
        ("endpoint metadata", ENDPOINT),
        ("root protected-resource metadata", ROOT_PROTECTED_RESOURCE_METADATA_URL),
        ("RFC protected-resource metadata", RFC_PROTECTED_RESOURCE_METADATA_URL),
    )
    for label, metadata_url in metadata_requests:
        response = _fetch_exact(fetcher, label, Request(metadata_url, method="GET"))
        if response.status != 200:
            raise RuntimeError(f"{label} returned HTTP {response.status}; expected 200")
        authorization_servers, _ = validate_protected_resource_metadata(
            label,
            _json_object(label, response),
        )
        if advertised_servers is None:
            advertised_servers = authorization_servers
        elif authorization_servers != advertised_servers:
            raise RuntimeError(f"{label} advertises mismatched authorization servers")
        observations.append(f"{label}: HTTP 200")

    if advertised_servers is None:
        raise RuntimeError("No protected-resource metadata advertised an authorization server")
    for issuer in advertised_servers:
        # Corbis exposes both aliases. Require both so a broken compatibility
        # route cannot be hidden by a successful RFC discovery response.
        metadata_urls = dict.fromkeys((
            authorization_server_metadata_url(issuer),
            ROOT_AUTHORIZATION_SERVER_METADATA_URL,
        ))
        for metadata_url in metadata_urls:
            label = f"authorization-server metadata at {metadata_url}"
            response = _fetch_exact(fetcher, label, Request(metadata_url, method="GET"))
            if response.status != 200:
                raise RuntimeError(f"{label} returned HTTP {response.status}; expected 200")
            validate_authorization_server_metadata(issuer, _json_object(label, response))
            observations.append(f"{label}: HTTP 200")
    return observations


def load_json(file_path: Path) -> dict[str, object]:
    with file_path.open(encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise AssertionError(f"{file_path.relative_to(REPOSITORY_ROOT)} must contain a JSON object")  # noqa: TRY004 - package assertion
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


def is_regular_release_file(root: Path, relative_path: Path) -> bool:
    """Return whether a required release path is a non-symlinked regular file.

    Every path component must be a real directory or file in the source tree.
    Checking only the leaf is insufficient because ``assets/`` could itself be
    a symlink to content absent from a signed source tag.
    """

    candidate = root
    for component in relative_path.parts:
        candidate /= component
        if candidate.is_symlink():
            return False
    return candidate.is_file()


def missing_release_material(root: Path = REPOSITORY_ROOT) -> list[str]:
    """Return structural release paths that are missing, directories, or symlinks.

    The default package checks deliberately allow a reviewable source package
    before public legal, support, and brand decisions are made. A release
    attempt must not silently inherit that allowance.
    """

    return [
        str(relative_path)
        for relative_path in RELEASE_REQUIRED_RELATIVE_PATHS
        if not is_regular_release_file(root, relative_path)
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


def validate_png_scanline_filters(
    decoded: bytes,
    width: int,
    height: int,
    bit_depth: int,
    color_type: int,
    interlace_method: int,
) -> bool:
    """Return whether every PNG scanline has a filter allowed by method zero."""

    channels = PNG_CHANNELS[color_type]

    def scanline_size(pixel_width: int) -> int:
        return 1 + (pixel_width * channels * bit_depth + 7) // 8

    passes = ((0, 0, 1, 1),) if interlace_method == 0 else ADAM7_PASSES
    position = 0
    for start_x, start_y, step_x, step_y in passes:
        pass_width = max(0, (width - start_x + step_x - 1) // step_x)
        pass_height = max(0, (height - start_y + step_y - 1) // step_y)
        scanline_length = scanline_size(pass_width)
        for _ in range(pass_height if pass_width else 0):
            if position >= len(decoded) or decoded[position] > 4:
                return False
            position += scanline_length
    return position == len(decoded)


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
    saw_plte = False
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
        elif chunk_type == b"PLTE":
            if (
                saw_idat
                or saw_plte
                or color_type not in {2, 3, 6}
                or not 3 <= length <= 768
                or length % 3
                or (color_type == 3 and length // 3 > 2**bit_depth)
            ):
                raise RuntimeError(message)
            saw_plte = True
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
    if (
        first_chunk
        or not saw_idat
        or not saw_iend
        or expected_decoded_size is None
        or (color_type == 3 and not saw_plte)
    ):
        raise RuntimeError(message)

    try:
        decompressor = zlib.decompressobj()
        decoded_size = 0
        decoded_chunks: list[bytes] = []
        for chunk_data in idat_chunks:
            remaining = chunk_data
            while remaining:
                decoded = decompressor.decompress(remaining, 64 * 1024)
                decoded_size += len(decoded)
                decoded_chunks.append(decoded)
                if decoded_size > MAX_PUBLIC_PNG_DECODED_BYTES:
                    raise RuntimeError(message)
                next_remaining = decompressor.unconsumed_tail
                if next_remaining == remaining and not decoded:
                    raise RuntimeError(message)
                remaining = next_remaining
        flushed = decompressor.flush(64 * 1024)
        decoded_size += len(flushed)
        decoded_chunks.append(flushed)
    except zlib.error as exc:
        raise RuntimeError(message) from exc
    if (
        decoded_size > MAX_PUBLIC_PNG_DECODED_BYTES
        or decoded_size != expected_decoded_size
        or not decompressor.eof
        or decompressor.unused_data
        or not validate_png_scanline_filters(
            b"".join(decoded_chunks), width, height, bit_depth, color_type, interlace_method
        )
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

    def test_claude_bridge_is_the_canonical_two_line_stub(self) -> None:
        self.assertEqual(CLAUDE_BRIDGE_FILE.read_text(encoding="utf-8"), CANONICAL_CLAUDE_BRIDGE)

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

            invalid_filter_png = (
                png_header
                + png_chunk(b"IDAT", zlib.compress(b"\x05\x00"))
                + png_chunk(b"IEND", b"")
            )
            icon_path.write_bytes(invalid_filter_png)
            with self.assertRaisesRegex(RuntimeError, "invalid PNG asset: assets/icon.png"):
                validate_release_material(root)

            indexed_without_palette_png = (
                PNG_SIGNATURE
                + png_chunk(b"IHDR", bytes.fromhex("00000001000000010103000000"))
                + png_chunk(b"IDAT", zlib.compress(b"\x00\x00"))
                + png_chunk(b"IEND", b"")
            )
            icon_path.write_bytes(indexed_without_palette_png)
            with self.assertRaisesRegex(RuntimeError, "invalid PNG asset: assets/icon.png"):
                validate_release_material(root)

            indexed_oversized_palette_png = (
                PNG_SIGNATURE
                + png_chunk(b"IHDR", bytes.fromhex("00000001000000010103000000"))
                + png_chunk(b"PLTE", bytes.fromhex("000000ffffff808080"))
                + png_chunk(b"IDAT", zlib.compress(b"\x00\x00"))
                + png_chunk(b"IEND", b"")
            )
            icon_path.write_bytes(indexed_oversized_palette_png)
            with self.assertRaisesRegex(RuntimeError, "invalid PNG asset: assets/icon.png"):
                validate_release_material(root)
            icon_path.write_bytes(valid_png)

            license_path = root / "LICENSE"
            release_copy = root / "approved-license-copy"
            release_copy.write_text(license_path.read_text(encoding="utf-8"), encoding="utf-8")
            license_path.unlink()
            license_path.symlink_to(release_copy)
            self.assertEqual(missing_release_material(root), ["LICENSE"])

            license_path.unlink()
            license_path.write_text("Reviewed public release material\n", encoding="utf-8")
            assets_path = root / "assets"
            for relative_path in RELEASE_REQUIRED_ASSET_RELATIVE_PATHS:
                (root / relative_path).unlink()
            assets_path.rmdir()
            copied_assets_path = root / "approved-brand-assets"
            copied_assets_path.mkdir()
            for relative_path in RELEASE_REQUIRED_ASSET_RELATIVE_PATHS:
                (copied_assets_path / relative_path.name).write_bytes(valid_png)
            assets_path.symlink_to(copied_assets_path, target_is_directory=True)
            self.assertEqual(
                missing_release_material(root),
                [str(path) for path in RELEASE_REQUIRED_ASSET_RELATIVE_PATHS],
            )

    def test_manifest_metadata_is_consistent(self) -> None:
        manifests = {name: load_json(file_path) for name, file_path in MANIFEST_FILES.items()}
        versions = {manifest["version"] for manifest in manifests.values()}

        self.assertEqual(versions.__len__(), 1, "All client manifests must carry one release version")
        version = versions.pop()
        self.assertIsInstance(version, str)
        self.assertRegex(str(version), r"^\d+\.\d+\.\d+$", "Version must be plain SemVer")
        self.assertEqual(version, RELEASE_VERSION, "Descriptor versions must match the documented source candidate")

        for manifest_name, manifest in manifests.items():
            self.assertEqual(manifest.get("name"), PACKAGE_ID, f"{manifest_name} package ID drifted")
            self.assertEqual(manifest.get("repository"), REPOSITORY_URL, f"{manifest_name} repository drifted")
            self.assertEqual(manifest.get("homepage"), WEBSITE_URL, f"{manifest_name} website drifted")
            author = manifest.get("author")
            self.assertIsInstance(author, dict, f"{manifest_name} author must be an object")
            self.assertEqual(author.get("name"), PUBLISHER, f"{manifest_name} publisher drifted")
            self.assertIn("authenticated account", str(manifest.get("description", "")), f"{manifest_name} must retain entitlement-aware copy")

        self.assertRegex(
            DISPLAY_NAME,
            r"^[A-Z][a-z]+(?: [A-Z][a-z]+)*$",
            "The human-facing connector label must use title case with spaces, not a technical identifier",
        )
        self.assertNotEqual(
            DISPLAY_NAME.lower(),
            MCP_SERVER_ID,
            "The human-facing connector label must remain distinct from the technical MCP identifier",
        )
        self.assertEqual(manifests["claude"].get("displayName"), DISPLAY_NAME)
        codex_interface = manifests["codex"].get("interface")
        self.assertIsInstance(codex_interface, dict)
        self.assertEqual(codex_interface.get("displayName"), DISPLAY_NAME)
        self.assertEqual(codex_interface.get("websiteURL"), WEBSITE_URL)
        self.assertEqual(codex_interface.get("privacyPolicyURL"), PRIVACY_POLICY_URL)
        self.assertEqual(codex_interface.get("termsOfServiceURL"), TERMS_OF_SERVICE_URL)
        self.assertEqual(codex_interface.get("composerIcon"), "./assets/icon.png")
        cursor_manifest = manifests["cursor"]
        self.assertEqual(cursor_manifest.get("license"), LICENSE_IDENTIFIER)
        self.assertEqual(cursor_manifest.get("logo"), "./assets/icon.png")
        cursor_logo = assert_relative_file_reference(self, "Cursor logo", cursor_manifest.get("logo"))
        self.assertTrue(cursor_logo.is_relative_to(REPOSITORY_ROOT / "assets"))
        self.assertEqual(
            hashlib.sha256((REPOSITORY_ROOT / "assets/icon.png").read_bytes()).hexdigest(),
            CORBIS_RESEARCH_ICON_SHA256,
            "Codex must use the exact approved Corbis Research icon",
        )

        for manifest_name, manifest in manifests.items():
            description = str(manifest.get("description", ""))
            self.assertIn(DISPLAY_NAME, description, f"{manifest_name} must use the human-facing connector label")
            self.assertNotIn(MCP_SERVER_ID, description, f"{manifest_name} must not expose the technical identifier as display copy")

        changelog = (REPOSITORY_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(
            changelog,
            re.compile(
                rf"^## {re.escape(RELEASE_VERSION)} - (?:Unreleased|\d{{4}}-\d{{2}}-\d{{2}})$",
                re.MULTILINE,
            ),
            "The current source candidate must have a matching release-material entry",
        )

    def test_source_provenance_describes_only_the_source_candidate(self) -> None:
        provenance = load_json(SOURCE_PROVENANCE_FILE)
        self.assertEqual(provenance, {})
        self.assertFalse(
            {"source_tag", "source_tag_object", "source_commit", "payload_digest"}.intersection(provenance),
            "Source provenance must not assert promotion-time tag or digest facts",
        )

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
        self.assertNotEqual(
            MCP_SERVER_ID,
            PACKAGE_ID,
            "The remote MCP server identifier must remain distinct from the package identifier",
        )
        self.assertEqual(codex_mcp["mcpServers"], {MCP_SERVER_ID: {"url": ENDPOINT}})
        self.assertEqual(cursor_mcp["mcpServers"], {MCP_SERVER_ID: {"url": ENDPOINT}})

        unsupported_server_display_keys = {"displayName", "display_name", "label", "title"}
        for client_name, mcp_config in (("codex", codex_mcp), ("cursor", cursor_mcp)):
            server_config = mcp_config["mcpServers"][MCP_SERVER_ID]
            self.assertTrue(
                unsupported_server_display_keys.isdisjoint(server_config),
                f"{client_name} has no supported per-server display-label field; use documented plugin metadata only",
            )

        claude_manifest = load_json(MANIFEST_FILES["claude"])
        claude_mcp = claude_manifest.get("mcpServers")
        self.assertIsInstance(claude_mcp, dict)
        assert isinstance(claude_mcp, dict)
        self.assertEqual(
            claude_mcp[MCP_SERVER_ID]["url"], ENDPOINT,
            "The Claude remote MCP configuration must use the exact endpoint",
        )
        self.assertEqual(
            claude_mcp[MCP_SERVER_ID]["type"], "http",
            "Claude must use the HTTP transport for the remote endpoint",
        )
        self.assertTrue(
            unsupported_server_display_keys.isdisjoint(claude_mcp[MCP_SERVER_ID]),
            "Claude has no supported per-server display-label field; use documented plugin metadata only",
        )

    def test_readme_prioritizes_the_public_label_over_the_technical_identifier(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("# Corbis MCP", readme)
        self.assertIn("Peer-reviewed research at the speed of conversation.", readme)
        for image in (
            "assets/corbis-landing-page.png",
            "assets/corbis-research-insights.png",
            "assets/corbis-datasets.png",
        ):
            self.assertIn(image, readme)
        self.assertNotIn(f"`{MCP_SERVER_ID}`", readme)
        self.assertNotIn("`mcpServers`", readme)
        self.assertNotIn("Marketplace selector", readme)

    def test_readme_visuals_are_decodable_public_pngs(self) -> None:
        for relative_path in (
            Path("assets/corbis-landing-page.png"),
            Path("assets/corbis-research-insights.png"),
            Path("assets/corbis-datasets.png"),
        ):
            validate_release_png(REPOSITORY_ROOT / relative_path, relative_path)

    def test_no_placeholders_credentials_or_unsafe_urls_appear_in_config(self) -> None:
        configuration = {
            **{name: load_json(file_path) for name, file_path in MANIFEST_FILES.items()},
            **{name: load_json(file_path) for name, file_path in MCP_FILES.items()},
            "source_provenance": load_json(SOURCE_PROVENANCE_FILE),
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


class FakeSmokeFetcher:
    def __init__(self, responses: Mapping[tuple[str, str], SmokeHttpResponse]) -> None:
        self.responses = responses
        self.requests: list[Request] = []

    def __call__(self, request: Request) -> SmokeHttpResponse:
        self.requests.append(request)
        key = (request.get_method(), request.full_url)
        if key not in self.responses:
            raise AssertionError(f"Unexpected smoke request: {key}")
        return self.responses[key]


class OAuthSmokeContractTests(unittest.TestCase):
    authorization_server = "https://www.corbis.ai/api/mcp"
    authorization_metadata_url = (
        "https://www.corbis.ai/.well-known/oauth-authorization-server/api/mcp"
    )

    def protected_metadata(self, **overrides: object) -> dict[str, object]:
        payload: dict[str, object] = {
            "resource": ENDPOINT,
            "authorization_servers": [self.authorization_server],
            "scopes_supported": ["read:papers", "read:profile"],
            "bearer_methods_supported": ["header"],
        }
        payload.update(overrides)
        return payload

    def authorization_metadata(self, **overrides: object) -> dict[str, object]:
        payload: dict[str, object] = {
            "issuer": self.authorization_server,
            "authorization_endpoint": f"{self.authorization_server}/oauth/authorize",
            "token_endpoint": f"{self.authorization_server}/oauth/token",
            "registration_endpoint": f"{self.authorization_server}/oauth/register",
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token"],
            "code_challenge_methods_supported": ["S256"],
        }
        payload.update(overrides)
        return payload

    def json_response(
        self,
        url: str,
        payload: object,
        *,
        status: int = 200,
        content_type: str = "application/json",
        response_url: str | None = None,
    ) -> SmokeHttpResponse:
        return SmokeHttpResponse(
            status=status,
            headers={"content-type": content_type},
            body=json.dumps(payload).encode("utf-8"),
            url=response_url or url,
        )

    def valid_responses(self) -> dict[tuple[str, str], SmokeHttpResponse]:
        return {
            ("GET", ENDPOINT): self.json_response(ENDPOINT, self.protected_metadata()),
            ("GET", ROOT_PROTECTED_RESOURCE_METADATA_URL): self.json_response(
                ROOT_PROTECTED_RESOURCE_METADATA_URL,
                self.protected_metadata(),
            ),
            ("GET", RFC_PROTECTED_RESOURCE_METADATA_URL): self.json_response(
                RFC_PROTECTED_RESOURCE_METADATA_URL,
                self.protected_metadata(),
            ),
            ("GET", ROOT_AUTHORIZATION_SERVER_METADATA_URL): self.json_response(
                ROOT_AUTHORIZATION_SERVER_METADATA_URL,
                self.authorization_metadata(),
            ),
            ("GET", self.authorization_metadata_url): self.json_response(
                self.authorization_metadata_url,
                self.authorization_metadata(),
            ),
        }

    def test_smoke_accepts_base_200_protected_resource_metadata(self) -> None:
        fetcher = FakeSmokeFetcher(self.valid_responses())

        observations = validate_live_oauth_smoke(fetcher)

        self.assertIn("endpoint metadata: HTTP 200", observations)
        self.assertIn(
            ("GET", self.authorization_metadata_url),
            [(request.get_method(), request.full_url) for request in fetcher.requests],
        )

    def test_smoke_rejects_service_info_json_without_exact_resource(self) -> None:
        responses = self.valid_responses()
        responses[("GET", ENDPOINT)] = self.json_response(
            ENDPOINT,
            {"name": "Corbis MCP Server", "version": "2.0.0"},
        )

        with self.assertRaisesRegex(RuntimeError, "exact Corbis MCP resource"):
            validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_rejects_malformed_base_metadata(self) -> None:
        malformed_responses = {
            "invalid JSON": SmokeHttpResponse(
                status=200,
                headers={"content-type": "application/json"},
                body=b"{",
                url=ENDPOINT,
            ),
            "duplicate JSON member": SmokeHttpResponse(
                status=200,
                headers={"content-type": "application/json"},
                body=(
                    b'{"resource":"https://www.corbis.ai/api/mcp/universal",'
                    b'"resource":"https://www.corbis.ai/api/mcp/universal"}'
                ),
                url=ENDPOINT,
            ),
            "non-object JSON": self.json_response(ENDPOINT, []),
            "wrong content type": self.json_response(
                ENDPOINT,
                self.protected_metadata(),
                content_type="text/plain",
            ),
        }
        for label, base_response in malformed_responses.items():
            with self.subTest(label=label):
                responses = self.valid_responses()
                responses[("GET", ENDPOINT)] = base_response
                with self.assertRaises(RuntimeError):
                    validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_rejects_unexpected_base_status(self) -> None:
        for status in (204, 401, 403, 500):
            with self.subTest(status=status):
                responses = self.valid_responses()
                responses[("GET", ENDPOINT)] = SmokeHttpResponse(
                    status=status,
                    headers={},
                    body=b"",
                    url=ENDPOINT,
                )
                with self.assertRaisesRegex(RuntimeError, "expected 200"):
                    validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_rejects_invalid_protected_resource_metadata(self) -> None:
        invalid_documents = {
            "missing resource": self.protected_metadata(resource=None),
            "mismatched resource": self.protected_metadata(resource=f"{ENDPOINT}/"),
            "missing authorization server": self.protected_metadata(authorization_servers=[]),
            "off-origin authorization server": self.protected_metadata(
                authorization_servers=["https://auth.example.com"]
            ),
            "missing scopes": self.protected_metadata(scopes_supported=[]),
            "invalid scope": self.protected_metadata(scopes_supported=["read papers"]),
            "missing header bearer method": self.protected_metadata(
                bearer_methods_supported=["query"]
            ),
        }
        for label, payload in invalid_documents.items():
            with self.subTest(label=label):
                responses = self.valid_responses()
                responses[("GET", RFC_PROTECTED_RESOURCE_METADATA_URL)] = self.json_response(
                    RFC_PROTECTED_RESOURCE_METADATA_URL,
                    payload,
                )
                with self.assertRaises(RuntimeError):
                    validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_rejects_mismatched_authorization_servers_across_metadata(self) -> None:
        responses = self.valid_responses()
        responses[("GET", RFC_PROTECTED_RESOURCE_METADATA_URL)] = self.json_response(
            RFC_PROTECTED_RESOURCE_METADATA_URL,
            self.protected_metadata(
                authorization_servers=["https://www.corbis.ai/oauth/alternate"]
            ),
        )

        with self.assertRaisesRegex(RuntimeError, "mismatched authorization servers"):
            validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_rejects_invalid_authorization_server_metadata(self) -> None:
        invalid_documents = {
            "mismatched issuer": self.authorization_metadata(
                issuer="https://www.corbis.ai/api/mcp/other"
            ),
            "missing authorization endpoint": self.authorization_metadata(
                authorization_endpoint=None
            ),
            "off-origin token endpoint": self.authorization_metadata(
                token_endpoint="https://tokens.example.com/oauth/token"
            ),
            "mismatched same-origin token endpoint": self.authorization_metadata(
                token_endpoint="https://www.corbis.ai/oauth/token"
            ),
            "missing registration endpoint": self.authorization_metadata(
                registration_endpoint=None
            ),
            "missing authorization grant": self.authorization_metadata(
                grant_types_supported=["refresh_token"]
            ),
            "missing refresh grant": self.authorization_metadata(
                grant_types_supported=["authorization_code"]
            ),
            "missing S256": self.authorization_metadata(
                code_challenge_methods_supported=["plain"]
            ),
        }
        for label, payload in invalid_documents.items():
            with self.subTest(label=label):
                responses = self.valid_responses()
                responses[("GET", self.authorization_metadata_url)] = self.json_response(
                    self.authorization_metadata_url,
                    payload,
                )
                with self.assertRaises(RuntimeError):
                    validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_rejects_malformed_authorization_server_metadata(self) -> None:
        invalid_responses = {
            "malformed JSON": SmokeHttpResponse(
                status=200,
                headers={"content-type": "application/json"},
                body=b"{",
                url=self.authorization_metadata_url,
            ),
            "non-object JSON": self.json_response(self.authorization_metadata_url, []),
            "wrong status": SmokeHttpResponse(
                status=503,
                headers={"content-type": "application/json"},
                body=b"{}",
                url=self.authorization_metadata_url,
            ),
        }
        for label, authorization_response in invalid_responses.items():
            with self.subTest(label=label):
                responses = self.valid_responses()
                responses[("GET", self.authorization_metadata_url)] = authorization_response
                with self.assertRaises(RuntimeError):
                    validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_rejects_redirects_from_exact_metadata_urls(self) -> None:
        responses = self.valid_responses()
        responses[("GET", ROOT_PROTECTED_RESOURCE_METADATA_URL)] = self.json_response(
            ROOT_PROTECTED_RESOURCE_METADATA_URL,
            self.protected_metadata(),
            response_url=RFC_PROTECTED_RESOURCE_METADATA_URL,
        )

        with self.assertRaisesRegex(RuntimeError, "redirected away from its exact URL"):
            validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_smoke_sends_only_credential_free_get_metadata_requests(self) -> None:
        fetcher = FakeSmokeFetcher(self.valid_responses())
        validate_live_oauth_smoke(fetcher)
        self.assertEqual(len(fetcher.requests), 5)
        self.assertEqual({request.full_url for request in fetcher.requests}, {
            ENDPOINT, ROOT_PROTECTED_RESOURCE_METADATA_URL,
            RFC_PROTECTED_RESOURCE_METADATA_URL, self.authorization_metadata_url,
            ROOT_AUTHORIZATION_SERVER_METADATA_URL,
        })
        for request in fetcher.requests:
            with self.subTest(url=request.full_url):
                self.assertEqual(request.get_method(), "GET")
                self.assertIsNone(request.data)
                headers = {key.lower(): value for key, value in request.header_items()}
                self.assertNotIn("authorization", headers)
                self.assertNotIn("cookie", headers)

    def test_base_401_fails_without_following_challenges_or_posting(self) -> None:
        responses = self.valid_responses()
        responses[("GET", ENDPOINT)] = SmokeHttpResponse(
            401, {"www-authenticate": 'Bearer resource_metadata="https://evil.example/"'},
            b"", ENDPOINT,
        )
        fetcher = FakeSmokeFetcher(responses)
        with self.assertRaisesRegex(RuntimeError, "endpoint metadata returned HTTP 401"):
            validate_live_oauth_smoke(fetcher)
        self.assertEqual(len(fetcher.requests), 1)
        self.assertEqual(fetcher.requests[0].get_method(), "GET")

    def test_live_smoke_opener_ignores_environment_proxy_credentials(self) -> None:
        proxy_handlers = [
            handler for handler in SMOKE_OPENER.handlers if isinstance(handler, ProxyHandler)
        ]
        self.assertEqual(proxy_handlers, [])


    def test_both_authorization_aliases_are_checked(self) -> None:
        fetcher = FakeSmokeFetcher(self.valid_responses())
        validate_live_oauth_smoke(fetcher)
        urls = [request.full_url for request in fetcher.requests]
        for url in (self.authorization_metadata_url, ROOT_AUTHORIZATION_SERVER_METADATA_URL):
            self.assertEqual(urls.count(url), 1)

    def test_each_authorization_alias_requires_every_capability(self) -> None:
        overrides = [
            {"issuer": self.authorization_server + "/"},
            {"response_types_supported": None},
            {"response_types_supported": []},
            {"response_types_supported": "code"},
            {"response_types_supported": ["token"]},
            {"response_types_supported": ["code", "code"]},
            {"grant_types_supported": ["authorization_code"]},
            {"grant_types_supported": ["refresh_token"]},
            {"code_challenge_methods_supported": ["plain"]},
        ]
        for field in ("authorization_endpoint", "token_endpoint", "registration_endpoint"):
            for value in (None, "http://www.corbis.ai/oauth", "https://evil.example/oauth",
                          self.authorization_server + "/wrong",
                          self.authorization_server + "/oauth/token?key=example"):
                overrides.append({field: value})
        for url in (self.authorization_metadata_url, ROOT_AUTHORIZATION_SERVER_METADATA_URL):
            for override in overrides:
                with self.subTest(url=url, override=override):
                    responses = self.valid_responses()
                    responses[("GET", url)] = self.json_response(
                        url, self.authorization_metadata(**override)
                    )
                    with self.assertRaises(RuntimeError):
                        validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_each_metadata_route_requires_success_at_exact_url(self) -> None:
        for url in (ROOT_PROTECTED_RESOURCE_METADATA_URL, RFC_PROTECTED_RESOURCE_METADATA_URL,
                    self.authorization_metadata_url, ROOT_AUTHORIZATION_SERVER_METADATA_URL):
            for status in (301, 302, 303, 307, 308, 401, 404, 500):
                with self.subTest(url=url, status=status):
                    responses = self.valid_responses()
                    responses[("GET", url)] = SmokeHttpResponse(status, {}, b"", url)
                    with self.assertRaisesRegex(RuntimeError, "expected 200"):
                        validate_live_oauth_smoke(FakeSmokeFetcher(responses))
            with self.subTest(url=url, redirected=True):
                responses = self.valid_responses()
                original = responses[("GET", url)]
                responses[("GET", url)] = SmokeHttpResponse(
                    original.status, original.headers, original.body, url + "/"
                )
                with self.assertRaisesRegex(RuntimeError, "exact URL"):
                    validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_all_metadata_rejects_duplicate_nonfinite_and_invalid_json(self) -> None:
        bodies = [b'{"nested":{"key":1,"key":2}}', b'{"key":1,"key":2}',
                  b'{"key":NaN}', b'{"key":Infinity}', b'{"key":-Infinity}',
                  b'\xff', b'{', b'[]', b'null']
        for body in bodies:
            with self.subTest(body=body), self.assertRaises(RuntimeError):
                _json_object("metadata", SmokeHttpResponse(
                    200, {"content-type": "application/json"}, body, ENDPOINT
                ))
        self.assertEqual(_json_object("metadata", SmokeHttpResponse(
            200, {"content-type": "Application/JSON; charset=utf-8"}, b'{"key":1}', ENDPOINT
        )), {"key": 1})

    def test_urls_reject_credentials_non_https_and_normalization_tricks(self) -> None:
        invalid = [None, "", "http://www.corbis.ai/api/mcp", "//www.corbis.ai/api/mcp",
                   "https://user:secret@www.corbis.ai/api/mcp",
                   "https://www.corbis.ai.evil.example/api/mcp",
                   "https://www.corbis.ai:444/api/mcp", "https://www.corbis.ai:bad/api/mcp",
                   "https://www.corbis.ai/api/mcp?key=example",
                   "https://www.corbis.ai/api/mcp#fragment",
                   " https://www.corbis.ai/api/mcp", "https://www.corbis.ai/api/\nmcp",
                   "https://www.corbis.ai/api/ mcp", "https://www.corbis.ai/api/\\mcp"]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                _https_url("issuer", value, same_origin_as=ENDPOINT)

    def test_protected_resource_arrays_are_nonempty_unique_and_typed(self) -> None:
        for field in ("authorization_servers", "scopes_supported", "bearer_methods_supported"):
            valid_value = self.protected_metadata()[field]
            for value in (None, [], "not an array", [1], [""], valid_value * 2):
                with self.subTest(field=field, value=value), self.assertRaises(RuntimeError):
                    validate_protected_resource_metadata(
                        "metadata", self.protected_metadata(**{field: value})
                    )

    def test_fetcher_reads_bounded_bodies_and_closes_success_and_http_errors(self) -> None:
        from io import BytesIO
        from unittest.mock import patch

        class Response(BytesIO):
            status = 200

            @property
            def headers(self):
                return {"Content-Type": "application/json"}

            def geturl(self):
                return ENDPOINT

            def read(self, size=-1):
                self.requested_size = size
                return super().read(size)

        for status in (200, 401):
            for size in (MAX_SMOKE_RESPONSE_BYTES, MAX_SMOKE_RESPONSE_BYTES + 1):
                with self.subTest(status=status, size=size):
                    stream = Response(b"x" * size)
                    kwargs = {"return_value": stream} if status == 200 else {
                        "side_effect": HTTPError(ENDPOINT, 401, "Unauthorized", {}, stream)
                    }
                    with patch.object(SMOKE_OPENER, "open", **kwargs) as opened:
                        if size > MAX_SMOKE_RESPONSE_BYTES:
                            with self.assertRaisesRegex(RuntimeError, "safety limit"):
                                fetch_smoke_response(Request(ENDPOINT))
                        else:
                            self.assertEqual(fetch_smoke_response(Request(ENDPOINT)).status, status)
                        self.assertEqual(opened.call_args.kwargs["timeout"], 15)
                    self.assertEqual(stream.requested_size, MAX_SMOKE_RESPONSE_BYTES + 1)
                    self.assertTrue(stream.closed)

    def test_injected_fetcher_cannot_bypass_body_limit(self) -> None:
        for key in self.valid_responses():
            with self.subTest(key=key):
                responses = self.valid_responses()
                original = responses[key]
                responses[key] = SmokeHttpResponse(
                    original.status, original.headers,
                    b"x" * (MAX_SMOKE_RESPONSE_BYTES + 1), original.url,
                )
                with self.assertRaisesRegex(RuntimeError, "safety limit"):
                    validate_live_oauth_smoke(FakeSmokeFetcher(responses))

    def test_transport_failures_are_reported_without_sensitive_details(self) -> None:
        from unittest.mock import patch
        for error in (URLError("private transport detail"), TimeoutError("private detail")):
            with self.subTest(error=type(error).__name__), patch.object(
                SMOKE_OPENER, "open", side_effect=error
            ):
                with self.assertRaisesRegex(RuntimeError, "network transport") as raised:
                    fetch_smoke_response(Request(ENDPOINT))
                self.assertNotIn("private", str(raised.exception))

    def test_read_failures_close_responses_and_report_transport_failure(self) -> None:
        from io import BytesIO
        from unittest.mock import Mock, patch

        for status in (200, 401):
            for error_type in (TimeoutError, OSError):
                with self.subTest(status=status, error_type=error_type.__name__):
                    stream = BytesIO()
                    stream.status = status
                    stream.headers = {}
                    stream.geturl = Mock(return_value=ENDPOINT)
                    stream.read = Mock(side_effect=error_type("private detail"))
                    kwargs = {"return_value": stream} if status == 200 else {
                        "side_effect": HTTPError(ENDPOINT, status, "Unauthorized", {}, stream)
                    }
                    with patch.object(SMOKE_OPENER, "open", **kwargs):
                        with self.assertRaisesRegex(RuntimeError, "network transport") as raised:
                            fetch_smoke_response(Request(ENDPOINT))
                        self.assertNotIn("private", str(raised.exception))
                    self.assertTrue(stream.closed)

    def test_redirect_handler_never_issues_a_followup_request(self) -> None:
        from email.message import Message
        from io import BytesIO
        from unittest.mock import Mock
        for code in (301, 302, 303, 307, 308):
            with self.subTest(code=code):
                handler = _RejectRedirects()
                handler.parent = Mock()
                headers = Message()
                headers["Location"] = "https://attacker.example/"
                self.assertIsNone(getattr(handler, f"http_error_{code}")(
                    Request(ENDPOINT), BytesIO(b""), code, "Redirect", headers
                ))
                handler.parent.open.assert_not_called()

def run_smoke_probe() -> None:
    checked_at = datetime.now(UTC).isoformat()
    print(f"Live smoke probe started at {checked_at}")
    for observation in validate_live_oauth_smoke():
        print(observation)
    print(
        "Live smoke probe passed. It sent no credentials, did not start OAuth, "
        "and made only GET metadata requests. No tool was invoked. "
        "It does not check protected-request 401 challenges, authenticated OAuth, "
        "or client acceptance."
    )


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
        try:
            run_smoke_probe()
        except RuntimeError as error:
            print(f"Live smoke probe failed: {error}", file=sys.stderr)
            raise SystemExit(1) from error
