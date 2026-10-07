import json
import subprocess
import sys
from typing import Optional

from codegen import config


def run_program(program_path: str) -> tuple[Optional[dict], str]:
    """Run a generated program and parse its stdout as a JSON object.

    Returns (answer, error); exactly one of them is empty.
    """
    try:
        result = subprocess.run(
            [sys.executable, program_path],
            capture_output=True,
            text=True,
            timeout=config.PROGRAM_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, (
            f"PQ timed out after {config.PROGRAM_TIMEOUT_SECONDS} seconds - "
            "likely an infinite loop."
        )

    if result.returncode != 0:
        return None, result.stderr or "Unknown runtime error"

    try:
        answer = json.loads(result.stdout.strip())
        if not isinstance(answer, dict) or not answer:
            raise ValueError("JSON output must be a non-empty object")
    except Exception:
        return None, f"Invalid or empty JSON output. stdout was: {repr(result.stdout)}"

    return answer, ""
