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
Docker deployment generator.

Uses uv for dependency management to ensure reproducible builds.
Updates pyproject.toml with runtime dependencies and generates
Dockerfile that installs from the lock file.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import tomlkit

from .base import Generator, ModelInfo


class DockerGenerator(Generator):
    """Generator for Docker deployment configurations."""

    name = "docker"

    def generate(self, models: list[ModelInfo] | None = None) -> list[Path]:
        """
        Generate Docker deployment configs.

        Updates pyproject.toml with runtime dependencies, runs uv lock,
        and generates Dockerfile that installs from the lock file.

        Args:
            models: Models to generate configs for (auto-detected if None)

        Returns:
            List of paths to generated files
        """
        if models is None:
            models = self.detect_models()

        self._check_uv_installed()

        generated_files = []
        target_dir = self.output_dir / "docker"

        # Extract runtime packages and update pyproject.toml
        runtime_packages = self._extract_runtime_packages(models)
        pyproject_path = self.project_dir / "pyproject.toml"

        if not pyproject_path.exists():
            raise FileNotFoundError(
                f"pyproject.toml not found at {pyproject_path}. "
                "Docker generator requires a pyproject.toml for dependency management."
            )

        self._update_pyproject_toml(pyproject_path, runtime_packages)
        self._run_uv_lock()

        # Generate Dockerfile
        dockerfile_content = self.render_template(
            "docker/Dockerfile.j2",
            {
                "python_version": "3.11",
            },
        )
        dockerfile_path = self.write_file(target_dir / "Dockerfile", dockerfile_content)
        generated_files.append(dockerfile_path)

        # Generate docker-compose.yml
        compose_content = self.render_template(
            "docker/docker-compose.yml.j2",
            {
                "http_port": 8080,
                "grpc_port": 8081,
                "models": models,
            },
        )
        compose_path = self.write_file(
            target_dir / "docker-compose.yml", compose_content
        )
        generated_files.append(compose_path)

        # Generate .dockerignore
        dockerignore_content = self.render_template(
            "docker/.dockerignore.j2",
            {},
        )
        dockerignore_path = self.write_file(
            target_dir / ".dockerignore", dockerignore_content
        )
        generated_files.append(dockerignore_path)

        # Generate README
        readme_content = self.render_template(
            "docker/README.md.j2",
            {
                "models": models,
                "runtime_packages": runtime_packages,
                "http_port": 8080,
                "grpc_port": 8081,
            },
        )
        readme_path = self.write_file(target_dir / "README.md", readme_content)
        generated_files.append(readme_path)

        return generated_files

    def _check_uv_installed(self) -> None:
        """Check that uv is installed and available."""
        if shutil.which("uv") is None:
            raise RuntimeError(
                "uv is not installed or not in PATH. "
                "Install uv: https://docs.astral.sh/uv/getting-started/installation/"
            )

    def _extract_runtime_packages(self, models: list[ModelInfo]) -> list[str]:
        """
        Extract PyPI package names from model runtime implementations.

        Args:
            models: List of models to extract packages from

        Returns:
            List of PyPI package specifiers (e.g., ["aissemble-oip-sumy>=1.0"])
        """
        packages = set()
        packages.add("mlserver>=1.6.0")

        for model in models:
            if model.runtime and "." in model.runtime:
                # Extract package name from "aissemble_oip_sumy.SumyRuntime"
                module_name = model.runtime.split(".")[0]
                # Convert underscores to hyphens for PyPI package names
                package_name = module_name.replace("_", "-")
                packages.add(package_name)

        return sorted(packages)

    def _update_pyproject_toml(
        self, pyproject_path: Path, runtime_packages: list[str]
    ) -> None:
        """
        Update pyproject.toml with runtime dependency group.

        Args:
            pyproject_path: Path to pyproject.toml
            runtime_packages: List of package specifiers to add
        """
        content = pyproject_path.read_text(encoding="utf-8")
        doc = tomlkit.parse(content)

        # Ensure dependency-groups section exists
        if "dependency-groups" not in doc:
            doc["dependency-groups"] = tomlkit.table()

        # Update or create runtime group
        runtime_array = tomlkit.array()
        for pkg in runtime_packages:
            runtime_array.append(pkg)
        runtime_array.multiline(True)

        doc["dependency-groups"]["runtime"] = runtime_array

        pyproject_path.write_text(tomlkit.dumps(doc), encoding="utf-8")
        print(f"  Updated {pyproject_path} with runtime dependencies", file=sys.stderr)

    def _run_uv_lock(self) -> None:
        """Run uv lock to update the lock file."""
        print("  Running uv lock...", file=sys.stderr)
        result = subprocess.run(
            ["uv", "lock"],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"uv lock failed:\n{result.stderr}\n"
                "Ensure all runtime packages are available on PyPI."
            )

