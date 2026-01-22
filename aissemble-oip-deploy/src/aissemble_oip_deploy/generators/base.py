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
Base generator class for deployment config generation.
"""

import json
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, TemplateNotFound, select_autoescape


@dataclass
class ModelInfo:
    """Information about a model discovered in the project."""

    name: str
    path: Path
    settings: dict[str, Any] = field(default_factory=dict)

    @property
    def runtime(self) -> str | None:
        """Get the runtime implementation class."""
        return self.settings.get("implementation")

    @property
    def parameters(self) -> dict[str, Any]:
        """Get model parameters."""
        return self.settings.get("parameters", {})


class Generator(ABC):
    """Abstract base class for deployment config generators."""

    # Name used in CLI (e.g., 'local', 'docker', 'kubernetes')
    name: str = ""

    def __init__(self, project_dir: Path, output_dir: Path | None = None):
        """
        Initialize the generator.

        Args:
            project_dir: Root directory of the user's project
            output_dir: Where to write generated configs (default: project_dir/deploy)
        """
        self.project_dir = project_dir.resolve()
        self.output_dir = (output_dir or project_dir / "deploy").resolve()
        self.jinja_env = Environment(
            loader=PackageLoader("aissemble_oip_deploy", "templates"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def detect_models(
        self, models_dir: Path | None = None, max_depth: int = 5
    ) -> list[ModelInfo]:
        """
        Discover models in the project.

        Args:
            models_dir: Directory to search for models (default: project_dir/models)
            max_depth: Maximum directory depth to search (prevents resource exhaustion)

        Returns:
            List of discovered ModelInfo objects
        """
        models_dir = models_dir or self.project_dir / "models"
        models = []

        if not models_dir.exists():
            return models

        # Use rglob with depth check to prevent abuse
        for model_settings_path in models_dir.rglob("model-settings.json"):
            # Check depth relative to models_dir
            try:
                rel_path = model_settings_path.relative_to(models_dir)
                if len(rel_path.parts) > max_depth + 1:  # +1 for the file itself
                    continue
            except ValueError:
                # Path is outside models_dir somehow, skip it
                continue

            model_dir = model_settings_path.parent
            model_name = model_dir.name

            # Skip the root models directory if it has a settings.json
            if model_dir == models_dir:
                continue

            try:
                settings_text = model_settings_path.read_text(encoding="utf-8")
                settings = json.loads(settings_text)
            except json.JSONDecodeError as e:
                print(
                    f"Warning: Invalid JSON in {model_settings_path}: {e}",
                    file=sys.stderr,
                )
                settings = {}
            except OSError as e:
                print(
                    f"Warning: Cannot read {model_settings_path}: {e}",
                    file=sys.stderr,
                )
                settings = {}

            models.append(
                ModelInfo(
                    name=model_name,
                    path=model_dir,
                    settings=settings,
                )
            )

        return models

    @abstractmethod
    def generate(self, models: list[ModelInfo] | None = None) -> list[Path]:
        """
        Generate deployment configs.

        Args:
            models: Models to generate configs for (auto-detected if None)

        Returns:
            List of paths to generated files
        """
        pass

    def render_template(self, template_name: str, context: dict[str, Any]) -> str:
        """
        Render a Jinja2 template with the given context.

        Args:
            template_name: Name of the template file
            context: Template variables

        Returns:
            Rendered template content

        Raises:
            TemplateNotFound: If template doesn't exist
        """
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except TemplateNotFound:
            raise TemplateNotFound(
                f"Template '{template_name}' not found. Check that the generator has the correct templates."
            )

    def write_file(self, path: Path, content: str, executable: bool = False) -> Path:
        """
        Write content to a file, creating directories as needed.

        Args:
            path: Path to write to (must be within output_dir)
            content: Content to write
            executable: Whether to make the file executable

        Returns:
            The path that was written to

        Raises:
            ValueError: If path is outside output_dir (path traversal protection)
        """
        # Ensure path is within output_dir (prevent path traversal attacks)
        try:
            resolved_path = path.resolve()
            resolved_output = self.output_dir.resolve()
            resolved_path.relative_to(resolved_output)
        except ValueError:
            raise ValueError(
                f"Cannot write file outside output directory. "
                f"Attempted: {path}, Output dir: {self.output_dir}"
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if executable:
            path.chmod(0o755)
        return path
