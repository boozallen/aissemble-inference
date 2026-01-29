###
# #%L
# aiSSEMBLE::Open Inference Protocol::Deploy
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #L%
###
"""
Configuration management for oip-deploy.

Manages the .inference-deploy.yaml file that tracks generated configs,
versions, and checksums for update/merge functionality.
"""

import hashlib
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


@dataclass
class GeneratedFile:
    """Tracks a single generated file."""

    path: str
    checksum: str
    generator: str
    generated_at: str

    def __post_init__(self):
        """Validate checksum format."""
        if not re.match(r"^[a-f0-9]{64}$", self.checksum):
            raise ValueError(
                f"Invalid checksum format (expected SHA256 hex): {self.checksum}"
            )


@dataclass
class DeployConfig:
    """Configuration stored in .inference-deploy.yaml."""

    version: str = "1.0"
    generator_version: str = ""
    generated_at: str = ""
    targets: list[str] = field(default_factory=list)
    files: list[GeneratedFile] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> "DeployConfig":
        """
        Load config from a YAML file.

        Args:
            path: Path to .inference-deploy.yaml file

        Returns:
            DeployConfig instance

        Raises:
            ValueError: If YAML is malformed
        """
        if not path.exists():
            return cls()

        try:
            content = path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {path}: {e}")
        except OSError as e:
            raise ValueError(f"Cannot read {path}: {e}")

        if data is None:
            return cls()

        if not isinstance(data, dict):
            raise ValueError(f"Expected dict in {path}, got {type(data).__name__}")

        # Validate and load files with proper error handling
        files = []
        for file_data in data.get("files", []):
            if not isinstance(file_data, dict):
                print(
                    f"Warning: Skipping invalid file entry (not a dict): {file_data}",
                    file=sys.stderr,
                )
                continue

            try:
                files.append(GeneratedFile(**file_data))
            except TypeError as e:
                print(
                    f"Warning: Skipping invalid file entry: {e}",
                    file=sys.stderr,
                )
            except ValueError as e:
                print(
                    f"Warning: Skipping file entry with invalid checksum: {e}",
                    file=sys.stderr,
                )

        return cls(
            version=str(data.get("version", "1.0")),
            generator_version=str(data.get("generator_version", "")),
            generated_at=str(data.get("generated_at", "")),
            targets=list(data.get("targets", [])),
            files=files,
        )

    def save(self, path: Path) -> None:
        """Save config to a YAML file."""
        data: dict[str, Any] = {
            "version": self.version,
            "generator_version": self.generator_version,
            "generated_at": self.generated_at,
            "targets": self.targets,
            "files": [
                {
                    "path": f.path,
                    "checksum": f.checksum,
                    "generator": f.generator,
                    "generated_at": f.generated_at,
                }
                for f in self.files
            ],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.dump(data, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )

    def add_file(self, path: Path, generator: str, base_dir: Path) -> None:
        """Add or update a tracked file."""
        rel_path = str(path.relative_to(base_dir))
        checksum = compute_checksum(path)
        now = datetime.now(timezone.utc).isoformat()

        # Update existing or add new
        for f in self.files:
            if f.path == rel_path:
                f.checksum = checksum
                f.generated_at = now
                return

        self.files.append(
            GeneratedFile(
                path=rel_path,
                checksum=checksum,
                generator=generator,
                generated_at=now,
            )
        )

    def get_file(self, rel_path: str) -> GeneratedFile | None:
        """Get a tracked file by its relative path."""
        for f in self.files:
            if f.path == rel_path:
                return f
        return None


def compute_checksum(path: Path) -> str:
    """Compute SHA256 checksum of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()
