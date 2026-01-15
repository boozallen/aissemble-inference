"""Behave environment hooks for MLServer management."""

import os
import subprocess
import sys
import time

import requests


def before_all(context):
    """Start MLServer before running tests.

    The YOLORuntime is now provided by the aissemble-oip-yolo module,
    which is installed as a proper package dependency.
    """
    example_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    models_dir = os.path.join(example_dir, "models")

    context.mlserver_port = 8080
    context.mlserver_url = f"http://127.0.0.1:{context.mlserver_port}"

    venv_bin = os.path.dirname(sys.executable)
    mlserver_cmd = os.path.join(venv_bin, "mlserver")

    context.mlserver_process = subprocess.Popen(
        [mlserver_cmd, "start", models_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    _wait_for_server(context.mlserver_url, context.mlserver_process, timeout=120)


def after_all(context):
    """Stop MLServer after all tests complete."""
    if hasattr(context, "mlserver_process") and context.mlserver_process:
        exit_code = context.mlserver_process.poll()
        if exit_code is not None:
            stdout, stderr = context.mlserver_process.communicate()
            print(f"\nMLServer exited with code {exit_code}")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
        else:
            context.mlserver_process.terminate()
            try:
                context.mlserver_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                context.mlserver_process.kill()
                context.mlserver_process.wait()


def _wait_for_server(url: str, process: subprocess.Popen, timeout: int = 120):
    """Wait for MLServer to become ready.

    Args:
        url: Base URL of MLServer
        process: The MLServer subprocess
        timeout: Maximum seconds to wait

    Raises:
        TimeoutError: If server doesn't become ready in time
    """
    health_url = f"{url}/v2/health/ready"
    start_time = time.time()

    while time.time() - start_time < timeout:
        exit_code = process.poll()
        if exit_code is not None:
            stdout, stderr = process.communicate()
            raise RuntimeError(
                f"MLServer exited with code {exit_code}.\n"
                f"stdout: {stdout.decode()}\n"
                f"stderr: {stderr.decode()}"
            )

        try:
            response = requests.get(health_url, timeout=2)
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        time.sleep(1)

    process.terminate()
    stdout, stderr = process.communicate(timeout=5)
    raise TimeoutError(
        f"MLServer did not become ready within {timeout} seconds.\n"
        f"stdout: {stdout.decode()}\n"
        f"stderr: {stderr.decode()}"
    )
