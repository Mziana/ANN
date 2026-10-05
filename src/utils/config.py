"""Load YAML configuration files from the configs/ directory.

Every tunable parameter of this project lives in a YAML file under configs/.
Nothing in src/ is allowed to hardcode a symbol, a path or a spread value, so
this module is the single entry point for reading them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "configs"


class ConfigError(FileNotFoundError):
    """Raised when a configuration file is missing or unreadable."""


def resolve_config_dir(config_dir: Path | None = None) -> Path:
    """Return the directory that holds the YAML configuration files.

    Args:
        config_dir: Explicit directory. When omitted, the project-level
            ``configs/`` directory is used.

    Returns:
        Path to the configuration directory.
    """
    return Path(config_dir) if config_dir is not None else CONFIG_DIR


def load_config(name: str, config_dir: Path | None = None) -> dict[str, Any]:
    """Load a YAML configuration file by stem name.

    Args:
        name: File stem without extension, for example ``"data"``.
        config_dir: Optional directory override, mostly for tests.

    Returns:
        Parsed YAML content as a dictionary.

    Raises:
        ConfigError: If the file does not exist, cannot be parsed, or does not
            contain a mapping at the top level.
    """
    directory = resolve_config_dir(config_dir)
    path = directory / f"{name}.yaml"

    if not path.is_file():
        available = sorted(p.stem for p in directory.glob("*.yaml"))
        raise ConfigError(f"Config not found: {path}. Available: {available}")

    try:
        content = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(content, dict):
        raise ConfigError(f"Config {path} must contain a mapping, got {type(content).__name__}")

    return content
