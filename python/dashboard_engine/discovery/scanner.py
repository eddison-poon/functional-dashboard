"""Repository scanner for Phase 3.1."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .classifier import classify_asset_kind, classify_review_state
from .enums import AssetKind, ReviewState
from .models import DiscoveredAsset, DiscoveryIssue, DiscoveryReport
from .parsers import extract_asset_id, extract_title, parse_asset_file


_DEFAULT_ROOT_CANDIDATES = (
    "test_cases",
    "test-assets",
    "test_assets",
)
_SUPPORTED_SUFFIXES = {".json", ".md", ".markdown"}
_IGNORED_NAMES = {
    ".DS_Store",
    "README.md",
    "readme.md",
    ".gitkeep",
}
_IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "venv",
    ".venv",
}


class RepositoryDiscovery:
    """Discover test assets from lifecycle folders in a repository."""

    def __init__(
        self,
        repository_root: str | Path,
        *,
        asset_roots: Iterable[str | Path] | None = None,
        strict_unknown_kind: bool = False,
        strict_unknown_state: bool = False,
    ) -> None:
        self.repository_root = Path(repository_root).expanduser().resolve()
        self.asset_roots = tuple(Path(value) for value in asset_roots) if asset_roots else None
        self.strict_unknown_kind = strict_unknown_kind
        self.strict_unknown_state = strict_unknown_state

    def discover(self) -> DiscoveryReport:
        if not self.repository_root.exists():
            raise FileNotFoundError(f"Repository root does not exist: {self.repository_root}")
        if not self.repository_root.is_dir():
            raise NotADirectoryError(f"Repository root is not a directory: {self.repository_root}")

        roots = self._resolve_asset_roots()
        assets: list[DiscoveredAsset] = []
        issues: list[DiscoveryIssue] = []
        ignored_files = 0
        scanned_files = 0
        seen_ids: dict[str, Path] = {}

        if not roots:
            issues.append(
                DiscoveryIssue(
                    path=self.repository_root,
                    code="NO_ASSET_ROOT",
                    message=(
                        "No test asset root was found. Expected one of: "
                        + ", ".join(_DEFAULT_ROOT_CANDIDATES)
                    ),
                )
            )

        for root in roots:
            for path in sorted(root.rglob("*")):
                if not path.is_file():
                    continue
                if self._is_ignored(path):
                    ignored_files += 1
                    continue
                if path.suffix.lower() not in _SUPPORTED_SUFFIXES:
                    ignored_files += 1
                    continue

                scanned_files += 1
                relative_path = path.relative_to(self.repository_root)

                try:
                    metadata, source_format = parse_asset_file(path)
                except (OSError, UnicodeError, ValueError) as exc:
                    issues.append(
                        DiscoveryIssue(
                            path=relative_path,
                            code="PARSE_ERROR",
                            message=str(exc),
                        )
                    )
                    continue

                asset_kind = classify_asset_kind(relative_path, metadata)
                review_state = classify_review_state(relative_path)
                asset_id = extract_asset_id(metadata)
                title = extract_title(metadata)

                if asset_kind is AssetKind.UNKNOWN and self.strict_unknown_kind:
                    issues.append(
                        DiscoveryIssue(
                            path=relative_path,
                            code="UNKNOWN_ASSET_KIND",
                            message="Asset type could not be classified.",
                        )
                    )

                if review_state is ReviewState.UNKNOWN and self.strict_unknown_state:
                    issues.append(
                        DiscoveryIssue(
                            path=relative_path,
                            code="UNKNOWN_REVIEW_STATE",
                            message="Lifecycle state could not be derived from the path.",
                        )
                    )

                if not asset_id:
                    issues.append(
                        DiscoveryIssue(
                            path=relative_path,
                            code="MISSING_ASSET_ID",
                            message="No canonical asset ID was found.",
                        )
                    )
                elif asset_id in seen_ids:
                    issues.append(
                        DiscoveryIssue(
                            path=relative_path,
                            code="DUPLICATE_ASSET_ID",
                            message=f"Asset ID {asset_id!r} also appears in {seen_ids[asset_id]}.",
                        )
                    )
                else:
                    seen_ids[asset_id] = relative_path

                clean_metadata = {
                    key: value
                    for key, value in metadata.items()
                    if not key.startswith("_")
                }

                assets.append(
                    DiscoveredAsset(
                        path=path,
                        relative_path=relative_path.as_posix(),
                        asset_kind=asset_kind,
                        review_state=review_state,
                        asset_id=asset_id,
                        title=title,
                        source_format=source_format,
                        metadata=clean_metadata,
                    )
                )

        return DiscoveryReport(
            repository_root=self.repository_root,
            assets=tuple(assets),
            issues=tuple(issues),
            scanned_files=scanned_files,
            ignored_files=ignored_files,
        )

    def _resolve_asset_roots(self) -> tuple[Path, ...]:
        if self.asset_roots is not None:
            roots = []
            for configured in self.asset_roots:
                candidate = configured if configured.is_absolute() else self.repository_root / configured
                if candidate.exists() and candidate.is_dir():
                    roots.append(candidate.resolve())
            return tuple(roots)

        return tuple(
            (self.repository_root / name).resolve()
            for name in _DEFAULT_ROOT_CANDIDATES
            if (self.repository_root / name).is_dir()
        )

    def _is_ignored(self, path: Path) -> bool:
        if path.name in _IGNORED_NAMES:
            return True
        return bool(set(path.parts) & _IGNORED_DIRECTORIES)
