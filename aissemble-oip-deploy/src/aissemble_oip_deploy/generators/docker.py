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

Generates Dockerfile and docker-compose.yml for containerized MLServer deployment.

For dev versions: Uses uv-monorepo-dependency-tool to build wheels with pinned
dependencies, including all transitive local path dependencies.

For release versions: Generates requirements.txt to install from PyPI.
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

        Args:
            models: Models to generate configs for (auto-detected if None)

        Returns:
            List of paths to generated files
        """
        if models is None:
            models = self.detect_models()

        generated_files = []
        target_dir = self.output_dir / "docker"

        # Extract runtime packages for documentation and requirements
        runtime_packages = self._extract_runtime_packages(models)

        # Check if this is a dev version
        is_dev = self._is_dev_version()

        if is_dev:
            # Build wheels for local testing
            wheels_dir = target_dir / "wheels"
            wheel_files = self._build_all_wheels(wheels_dir)
            generated_files.extend(wheel_files)
            use_wheels = True
        else:
            # Generate requirements.txt for PyPI install
            requirements_content = "\n".join(runtime_packages) + "\n"
            requirements_path = self.write_file(
                target_dir / "requirements.txt", requirements_content
            )
            generated_files.append(requirements_path)
            use_wheels = False

        # Generate Dockerfile
        dockerfile_content = self.render_template(
            "docker/Dockerfile.j2",
            {
                "python_version": "3.11",
                "use_wheels": use_wheels,
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
                "use_wheels": use_wheels,
            },
        )
        readme_path = self.write_file(target_dir / "README.md", readme_content)
        generated_files.append(readme_path)

        return generated_files

    def _is_dev_version(self) -> bool:
        """
        Check if the project version is a dev version.

        Returns:
            True if version contains '.dev', False otherwise
        """
        pyproject_path = self.project_dir / "pyproject.toml"
        if not pyproject_path.exists():
            return False

        content = pyproject_path.read_text(encoding="utf-8")
        doc = tomlkit.parse(content)

        version = doc.get("project", {}).get("version", "")
        return ".dev" in version

    def _build_all_wheels(self, wheels_dir: Path) -> list[Path]:
        """
        Build wheels for this project and all local path dependencies.

        Recursively finds and builds all monorepo packages that this project
        depends on, ensuring Docker has all required wheels.

        Args:
            wheels_dir: Directory to copy built wheels to

        Returns:
            List of paths to copied wheel files
        """
        if shutil.which("uv") is None:
            raise RuntimeError(
                "uv is not installed or not in PATH. "
                "Install uv: https://docs.astral.sh/uv/getting-started/installation/"
            )

        wheels_dir.mkdir(parents=True, exist_ok=True)

        # Find all projects to build (this project + path dependencies)
        projects_to_build = self._find_all_path_dependencies(self.project_dir)

        print(
            f"  Building wheels for {len(projects_to_build)} project(s) (dev mode)...",
            file=sys.stderr,
        )

        copied_wheels = []
        for project_path in projects_to_build:
            wheel_path = self._build_single_wheel(project_path, wheels_dir)
            if wheel_path:
                copied_wheels.append(wheel_path)

        if not copied_wheels:
            raise RuntimeError(
                "No wheel files were built. "
                "Check that uv-monorepo-dependency-tool completed successfully."
            )

        print(f"  Built {len(copied_wheels)} wheel(s) to {wheels_dir}", file=sys.stderr)
        return copied_wheels

    def _find_all_path_dependencies(self, start_dir: Path) -> list[Path]:
        """
        Recursively find all local path dependencies.

        Args:
            start_dir: Starting project directory

        Returns:
            List of project directories to build (including start_dir)
        """
        visited = set()
        to_visit = [start_dir.resolve()]
        result = []

        while to_visit:
            current = to_visit.pop(0)
            if current in visited:
                continue
            visited.add(current)
            result.append(current)

            # Find path dependencies in this project
            path_deps = self._get_path_dependencies(current)
            for dep_path in path_deps:
                resolved = (current / dep_path).resolve()
                if resolved.exists() and resolved not in visited:
                    to_visit.append(resolved)

        return result

    def _get_path_dependencies(self, project_dir: Path) -> list[str]:
        """
        Extract path dependencies from a project's pyproject.toml.

        Args:
            project_dir: Project directory containing pyproject.toml

        Returns:
            List of relative path strings to dependencies
        """
        pyproject_path = project_dir / "pyproject.toml"
        if not pyproject_path.exists():
            return []

        content = pyproject_path.read_text(encoding="utf-8")
        doc = tomlkit.parse(content)

        # Look for [tool.uv.sources] section
        sources = doc.get("tool", {}).get("uv", {}).get("sources", {})

        paths = []
        for _name, source in sources.items():
            if isinstance(source, dict) and "path" in source:
                paths.append(source["path"])

        return paths

    def _build_single_wheel(self, project_dir: Path, wheels_dir: Path) -> Path | None:
        """
        Build a wheel for a single project using uv-monorepo-dependency-tool.

        Args:
            project_dir: Project directory to build
            wheels_dir: Directory to copy the wheel to

        Returns:
            Path to the copied wheel file, or None if build failed
        """
        project_name = project_dir.name
        print(f"    Building {project_name}...", file=sys.stderr)

        result = subprocess.run(
            [
                "uv",
                "tool",
                "run",
                "uv-monorepo-dependency-tool",
                "build-rewrite-path-deps",
                "--version-pinning-strategy=mixed",
            ],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(
                f"    Warning: Failed to build {project_name}: {result.stderr}",
                file=sys.stderr,
            )
            return None

        # Find and copy the built wheel
        dist_dir = project_dir / "dist"
        if not dist_dir.exists():
            print(
                f"    Warning: No dist/ directory for {project_name}", file=sys.stderr
            )
            return None

        # Get the most recent wheel
        wheels = sorted(dist_dir.glob("*.whl"), key=lambda p: p.stat().st_mtime)
        if not wheels:
            print(f"    Warning: No wheel found for {project_name}", file=sys.stderr)
            return None

        wheel_file = wheels[-1]  # Most recent
        dest_path = wheels_dir / wheel_file.name
        shutil.copy2(wheel_file, dest_path)
        print(f"      Copied {wheel_file.name}", file=sys.stderr)
        return dest_path

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
