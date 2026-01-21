###
# #%L
# aiSSEMBLE::Open Inference Protocol::Common Test Utilities
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
"""MLServer fixture for test environments.

Provides a reusable abstraction for managing MLServer lifecycle during testing.
Consolidates process management, health checking, and graceful shutdown logic.
"""

import logging
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class MLServerFixture:
    """Manages MLServer lifecycle for testing.

    Provides two factory methods:
    - simple(): For static model directories (examples)
    - dynamic(): For temporary config generation (module tests)

    Attributes:
        url: MLServer base URL (e.g., "http://127.0.0.1:8080")
        port: HTTP port number
        process: Subprocess handle (for backward compatibility)
        temp_dir: Temporary directory path (None for simple mode)
    """

    def __init__(
        self,
        port: Optional[int] = None,
        models_dir: Optional[Path] = None,
        use_temp_dir: bool = False,
    ):
        """Initialize MLServer fixture.

        Args:
            port: HTTP port (None for dynamic allocation)
            models_dir: Path to models directory (for simple mode)
            use_temp_dir: Whether to use temporary directory (for dynamic mode)
        """
        self._port = port
        self._models_dir = models_dir
        self._use_temp_dir = use_temp_dir
        self._process: Optional[subprocess.Popen] = None
        self._temp_dir: Optional[str] = None

    def __enter__(self) -> "MLServerFixture":
        """Enter context manager - returns self for use in 'with' statement.

        Returns:
            Self for context manager protocol
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager - ensures cleanup even if exceptions occur.

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        self.stop()
        self.cleanup()

    @classmethod
    def simple(cls, port: int, models_dir: Path) -> "MLServerFixture":
        """Create fixture for static model directory (examples).

        Args:
            port: Fixed HTTP port
            models_dir: Path to existing models directory

        Returns:
            Configured MLServerFixture
        """
        return cls(port=port, models_dir=models_dir, use_temp_dir=False)

    @classmethod
    def dynamic(cls) -> "MLServerFixture":
        """Create fixture for dynamic config generation (module tests).

        Uses temporary directory and dynamic port allocation.

        Returns:
            Configured MLServerFixture
        """
        return cls(port=None, models_dir=None, use_temp_dir=True)

    @property
    def url(self) -> str:
        """Get MLServer base URL."""
        if self._port is None:
            raise RuntimeError("MLServer not started - call start() first")
        return f"http://127.0.0.1:{self._port}"

    @property
    def port(self) -> int:
        """Get MLServer HTTP port."""
        if self._port is None:
            raise RuntimeError("MLServer not started - call start() first")
        return self._port

    @property
    def process(self) -> Optional[subprocess.Popen]:
        """Get MLServer subprocess (backward compatibility)."""
        return self._process

    @property
    def temp_dir(self) -> Optional[str]:
        """Get temporary directory path (None for simple mode)."""
        return self._temp_dir

    def start(self, verbose: bool = False) -> None:
        """Start MLServer with static models directory.

        For simple mode only (examples with pre-configured models).

        Args:
            verbose: Enable verbose health check logging

        Raises:
            RuntimeError: If called in dynamic mode or already started
        """
        if self._use_temp_dir:
            raise RuntimeError("Use start_with_model() for dynamic mode")
        if self._process:
            raise RuntimeError("MLServer already started")
        if not self._models_dir:
            raise RuntimeError("No models directory configured")

        self._start_process(self._models_dir, verbose=verbose)

    def start_with_model(
        self,
        model_name: str,
        runtime: str,
        global_settings: Optional[dict] = None,
        **parameters,
    ) -> None:
        """Start MLServer with dynamically generated model configuration.

        For dynamic mode only (module tests with temporary configs).

        Args:
            model_name: Model name (e.g., "yolo", "sumy")
            runtime: Runtime implementation class
            global_settings: Optional global settings.json content
            **parameters: Model parameters for model-settings.json

        Raises:
            RuntimeError: If called in simple mode or already started
        """
        if not self._use_temp_dir:
            raise RuntimeError("Use start() for simple mode")
        if self._process:
            self.stop()

        from .config_builder import create_model_settings, create_settings

        self._temp_dir = tempfile.mkdtemp(prefix=f"{model_name}_test_")
        models_dir = Path(self._temp_dir) / "models"
        model_dir = models_dir / model_name
        model_dir.mkdir(parents=True)

        settings = global_settings or {
            "parallel_workers": 0,
            "host": "127.0.0.1",
        }
        create_settings(models_dir, settings)

        model_settings = {"name": model_name, "implementation": runtime}
        if parameters:
            model_settings["parameters"] = parameters

        create_model_settings(model_dir, model_settings)

        self._start_process(models_dir, verbose=True)

    def stop(self) -> None:
        """Stop MLServer gracefully.

        Attempts terminate, waits 10s, then kills if needed.
        """
        if not self._process:
            return

        # Only terminate if process is still running
        if self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("MLServer did not terminate gracefully, killing process")
                self._process.kill()
                # Add timeout to second wait to prevent indefinite hang
                try:
                    self._process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.error(
                        "MLServer did not respond to kill signal after 5s, "
                        "process may be in zombie state"
                    )

        self._process = None

    def cleanup(self) -> None:
        """Clean up temporary directory (dynamic mode only).

        Logs warnings if cleanup fails but does not raise exceptions.
        """
        if self._temp_dir and os.path.exists(self._temp_dir):
            import shutil

            try:
                shutil.rmtree(self._temp_dir)
                logger.debug(f"Cleaned up temp directory: {self._temp_dir}")
            except (OSError, PermissionError) as e:
                logger.warning(
                    f"Failed to clean up temp directory {self._temp_dir}: {e}. "
                    f"Manual cleanup may be required."
                )
            finally:
                # Always null out the temp_dir to prevent reuse attempts
                self._temp_dir = None

    def _start_process(self, models_dir: Path, verbose: bool = False) -> None:
        """Start MLServer process and wait for readiness.

        Args:
            models_dir: Path to models directory
            verbose: Enable verbose health check logging
        """
        if self._port is None:
            self._port = self._find_free_port()

        venv_bin = os.path.dirname(sys.executable)
        mlserver_cmd = os.path.join(venv_bin, "mlserver")

        env = os.environ.copy()
        env["MLSERVER_HTTP_PORT"] = str(self._port)
        env["MLSERVER_GRPC_PORT"] = str(self._port + 1)
        env["MLSERVER_METRICS_PORT"] = str(self._port + 2)

        self._process = subprocess.Popen(
            [mlserver_cmd, "start", str(models_dir)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self._wait_for_server(verbose=verbose)

    def _wait_for_server(self, timeout: int = 120, verbose: bool = False) -> None:
        """Wait for MLServer to become ready.

        Args:
            timeout: Maximum seconds to wait
            verbose: Log health check attempts every 10 tries

        Raises:
            RuntimeError: If MLServer exits prematurely
            TimeoutError: If server doesn't become ready in time
        """
        if not self._process:
            raise RuntimeError("No process to wait for")

        health_url = f"{self.url}/v2/health/ready"
        start_time = time.time()
        attempt = 0

        while time.time() - start_time < timeout:
            exit_code = self._process.poll()
            if exit_code is not None:
                stdout, stderr = self._process.communicate()
                raise RuntimeError(
                    f"MLServer exited with code {exit_code}.\n"
                    f"stdout: {stdout.decode()}\n"
                    f"stderr: {stderr.decode()}"
                )

            try:
                response = requests.get(health_url, timeout=2)
                if response.status_code == 200:
                    return
                if verbose and attempt % 10 == 0:
                    print(
                        f"Health check returned {response.status_code}: {response.text}"
                    )
            except requests.exceptions.ConnectionError as e:
                if verbose and attempt % 10 == 0:
                    print(f"Health check connection failed: {e}")
            except requests.exceptions.Timeout:
                if verbose and attempt % 10 == 0:
                    print("Health check timed out")
            except Exception as e:
                if verbose and attempt % 10 == 0:
                    print(f"Health check error: {e}")

            attempt += 1
            time.sleep(1)

        self._process.terminate()
        stdout, stderr = self._process.communicate(timeout=5)
        raise TimeoutError(
            f"MLServer did not become ready within {timeout} seconds.\n"
            f"stdout: {stdout.decode()}\n"
            f"stderr: {stderr.decode()}"
        )

    @staticmethod
    def _find_free_port() -> int:
        """Find a free port for MLServer.

        WARNING: Race condition exists between port allocation and usage.
        The port is freed when this method returns, and another process could
        theoretically bind to it before MLServer starts. This is generally safe
        for test environments but can cause flaky tests in high-concurrency
        scenarios (e.g., parallel CI builds).

        The socket is bound to 127.0.0.1 (localhost) to avoid conflicts with
        system services. The OS assigns an ephemeral port from its available pool.

        Returns:
            Available port number from OS ephemeral port range

        Note:
            If MLServer fails to start with "Address already in use", this race
            condition may be the cause. Consider adding retry logic or using
            fixed port ranges for parallel test execution.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
