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
Local MLServer deployment generator.
"""

import re
from pathlib import Path

from .base import Generator, ModelInfo


class LocalGenerator(Generator):
    """Generator for local MLServer deployment scripts."""

    name = "local"

    def generate(self, models: list[ModelInfo] | None = None) -> list[Path]:
        """
        Generate local MLServer run script.

        Args:
            models: Models to generate configs for (auto-detected if None)

        Returns:
            List of paths to generated files
        """
        if models is None:
            models = self.detect_models()

        generated_files = []
        target_dir = self.output_dir / "local"

        # From deploy/local, go up two levels (../.. = project_dir), then down to models
        models_rel_path = "../../models"

        # Validate path is safe (no shell metacharacters)
        if not re.match(r"^[a-zA-Z0-9_/.-]+$", models_rel_path):
            raise ValueError(f"Invalid models path: {models_rel_path}")

        # Generate run script
        script_content = self.render_template(
            "local/run-mlserver.sh.j2",
            {
                "models_dir": models_rel_path,
                "models": models,
                "port": 8080,
            },
        )
        script_path = self.write_file(
            target_dir / "run-mlserver.sh",
            script_content,
            executable=True,
        )
        generated_files.append(script_path)

        # Generate README
        readme_content = self._generate_readme(models)
        readme_path = self.write_file(target_dir / "README.md", readme_content)
        generated_files.append(readme_path)

        return generated_files

    def _generate_readme(self, models: list[ModelInfo]) -> str:
        """Generate README for local deployment."""
        model_list = (
            "\n".join(f"- {m.name}" for m in models) if models else "- (none detected)"
        )

        # Extract unique runtime packages for installation instructions
        # Runtime is typically "module_name.ClassName", we need just the module
        runtime_packages = set()
        for model in models:
            if model.runtime and "." in model.runtime:
                # Extract package name from "aissemble_inference_sumy.SumyRuntime"
                package = model.runtime.split(".")[0]
                # Convert underscores to hyphens for PyPI package names
                package = package.replace("_", "-")
                runtime_packages.add(package)

        runtime_install = ""
        if runtime_packages:
            packages_str = " ".join(sorted(runtime_packages))
            runtime_install = f"""
**Model-specific runtimes:**
```bash
pip install {packages_str}
```
"""

        return f"""# Local MLServer Deployment

This directory contains scripts for running your models locally with MLServer.

## Prerequisites

**Required:**
- Python 3.11+
- MLServer:
  ```bash
  pip install mlserver
  ```
{runtime_install}
**Note:** The run script will check for MLServer and display installation instructions if not found.

## Models

{model_list}

## Usage

Start MLServer:

```bash
./run-mlserver.sh
```

The server will start on http://localhost:8080

If MLServer is not installed, the script will display installation instructions.

## Testing

Once the server is running, you can test it with:

```bash
curl -X POST http://localhost:8080/v2/models/<model-name>/infer \\
  -H "Content-Type: application/json" \\
  -d '{{"inputs": [...]}}'
```

## Stopping

Press Ctrl+C to stop the server.

## Troubleshooting

**MLServer not found:**
- Ensure MLServer is installed: `pip install mlserver`
- Check that it's in your PATH: `which mlserver`

**Import errors when starting:**
- Install model-specific dependencies (see Prerequisites above)
- Verify your Python environment matches the model requirements (Python 3.11+)
"""
