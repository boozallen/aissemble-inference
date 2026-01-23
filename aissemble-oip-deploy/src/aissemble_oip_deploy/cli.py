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
CLI commands for oip-deploy.

Provides the `oip deploy` command group for generating deployment configurations.
Generators are discovered via entry points, allowing custom generators to be
installed as separate packages.
"""

from datetime import datetime, timezone
from pathlib import Path

import click

from . import __version__
from .config import DeployConfig
from .registry import GeneratorRegistry


def get_registry() -> GeneratorRegistry:
    """Get the generator registry instance."""
    return GeneratorRegistry.instance()


@click.group()
@click.version_option(version=__version__)
def main():
    """OIP deployment tooling - generate deployment configs for OIP-compatible models."""
    pass


@main.group()
def deploy():
    """Generate and manage deployment configurations."""
    pass


@deploy.command("init")
@click.option(
    "--target",
    "-t",
    multiple=True,
    default=None,
    help="Deployment target(s) to generate configs for. Use 'all' for all targets.",
)
@click.option(
    "--model-dir",
    "-m",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to models directory (default: ./models)",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Output directory for generated configs (default: ./deploy)",
)
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Project root directory (default: current directory)",
)
def init(
    target: tuple[str, ...] | None,
    model_dir: Path | None,
    output_dir: Path | None,
    project_dir: Path | None,
):
    """Initialize deployment configurations for your models.

    Generates deployment configs in the deploy/ directory for the specified
    target(s). Use --target all to generate for all available targets.

    Generators are discovered via entry points, so custom generators can be
    installed as separate packages.

    Examples:

        oip deploy init --target local

        oip deploy init --target docker --target kubernetes

        oip deploy init --target all
    """
    registry = get_registry()
    available = registry.list_available()

    if not available:
        click.echo("Error: No generators found. Install a generator package or check")
        click.echo("that aissemble-oip-deploy is installed correctly.")
        raise SystemExit(1)

    # Default to 'local' if available, otherwise first available
    if target is None or len(target) == 0:
        if "local" in available:
            targets = ["local"]
        else:
            targets = [available[0]]
    else:
        targets = list(target)

    # Expand 'all' to all available targets
    if "all" in targets:
        targets = available

    # Validate targets
    for t in targets:
        if t not in available and t != "all":
            click.echo(f"Error: Unknown target '{t}'")
            click.echo(f"Available targets: {', '.join(available)}")
            raise SystemExit(1)

    project_dir = project_dir or Path.cwd()
    output_dir = output_dir or project_dir / "deploy"

    # Check if running from wrong directory (inside deploy/)
    cwd = Path.cwd()
    if cwd.name == "deploy" and project_dir == cwd:
        click.echo(
            "Error: It looks like you're running from inside a deploy/ directory."
        )
        click.echo(
            "Please run from your project root (where pyproject.toml and models/ are)."
        )
        click.echo()
        click.echo("Example:")
        click.echo("  cd /path/to/your-project")
        click.echo("  oip deploy init --target docker")
        raise SystemExit(1)

    # Check for project root indicators
    has_pyproject = (project_dir / "pyproject.toml").exists()
    has_models = (project_dir / "models").exists()
    if not has_pyproject and not has_models:
        click.echo(
            f"Warning: No pyproject.toml or models/ directory found in {project_dir}"
        )
        click.echo("Are you running from your project root?")
        click.echo()
        if not click.confirm("Continue anyway?"):
            raise SystemExit(1)

    # Load or create config
    config_path = output_dir / ".oip-deploy.yaml"
    config = DeployConfig.load(config_path)
    config.generator_version = __version__
    config.generated_at = datetime.now(timezone.utc).isoformat()

    click.echo(f"Generating deployment configs in {output_dir}")
    click.echo(f"Targets: {', '.join(targets)}")
    click.echo()

    all_generated_files = []

    for target_name in targets:
        generator_cls = registry.get(target_name)
        if generator_cls is None:
            click.echo(f"  [{target_name}] Error: Generator not found")
            continue

        generator = generator_cls(project_dir, output_dir)

        # Detect models
        models_path = model_dir or project_dir / "models"
        models = generator.detect_models(models_path)

        if not models:
            click.echo(f"  [{target_name}] Warning: No models found in {models_path}")
        else:
            model_names = ", ".join(m.name for m in models)
            click.echo(f"  [{target_name}] Found models: {model_names}")

        # Generate configs
        generated_files = generator.generate(models)
        all_generated_files.extend(generated_files)

        for file_path in generated_files:
            config.add_file(file_path, target_name, output_dir)
            rel_path = file_path.relative_to(output_dir)
            click.echo(f"  [{target_name}] Generated: {rel_path}")

        if target_name not in config.targets:
            config.targets.append(target_name)

    # Save config
    config.save(config_path)
    click.echo()
    click.echo(f"Config saved to {config_path.relative_to(project_dir)}")

    # Print next steps
    click.echo()
    click.echo("Next steps:")
    if "local" in targets:
        click.echo("  Local:  cd deploy/local && ./run-mlserver.sh")
    if "docker" in targets:
        click.echo("  Docker: cd deploy/docker && docker-compose up --build")
    if "kubernetes" in targets:
        click.echo("  K8s:    kubectl apply -k deploy/kubernetes/base")
    if "kserve" in targets:
        click.echo("  KServe: kubectl apply -f deploy/kserve/inference-service.yaml")


@deploy.command("list-targets")
def list_targets():
    """List available deployment targets.

    Generators are discovered via entry points. Install additional generator
    packages to add more targets.
    """
    registry = get_registry()
    available = registry.list_available()

    if not available:
        click.echo("No generators found.")
        click.echo()
        click.echo("Install a generator package or check that aissemble-oip-deploy")
        click.echo("is installed correctly.")
        return

    click.echo("Available deployment targets:")
    click.echo()
    for name in available:
        generator_cls = registry.get(name)
        # Get description from docstring if available
        doc = generator_cls.__doc__ if generator_cls else None
        if doc:
            # Get first line of docstring
            desc = doc.strip().split("\n")[0]
            click.echo(f"  {name:15} - {desc}")
        else:
            click.echo(f"  {name}")

    click.echo()
    click.echo("Custom generators can be added via the 'oip.generators' entry point.")


if __name__ == "__main__":
    main()
