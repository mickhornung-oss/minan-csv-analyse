"""Runs reproducible technical quality gates for MinAn.

Gate order:
1) compile check (src + tests)
2) pytest
3) optional release build
4) optional release executable smoke
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = PROJECT_ROOT / "build_release.bat"
RELEASE_EXE = PROJECT_ROOT / "dist" / "MinAn_1_4" / "MinAn.exe"


def _run(cmd: list[str], *, cwd: Path = PROJECT_ROOT) -> None:
    printable = " ".join(cmd)
    print(f"[gate] {printable}")
    completed = subprocess.run(cmd, cwd=cwd)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def _compile_check() -> None:
    _run([sys.executable, "-m", "compileall", "-q", "src", "tests"])


def _pytest_check() -> None:
    _run([sys.executable, "-m", "pytest", "-q"])


def _build_release() -> None:
    if not BUILD_SCRIPT.exists():
        print(f"[gate][error] Missing build script: {BUILD_SCRIPT}")
        raise SystemExit(1)
    _run(["cmd", "/c", str(BUILD_SCRIPT)])


def _exe_smoke(seconds: int) -> None:
    if sys.platform != "win32":
        print("[gate][skip] EXE smoke is only supported on Windows.")
        return

    if not RELEASE_EXE.exists():
        print(f"[gate][error] Release executable not found: {RELEASE_EXE}")
        raise SystemExit(1)

    print(f"[gate] Launch smoke: {RELEASE_EXE}")
    process = subprocess.Popen([str(RELEASE_EXE)])
    try:
        time.sleep(seconds)
        if process.poll() is not None:
            print("[gate][error] EXE exited during smoke interval.")
            raise SystemExit(1)
        print("[gate] EXE stayed alive during smoke interval.")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MinAn technical quality gates")
    parser.add_argument(
        "--with-build",
        action="store_true",
        help="Include release build gate via build_release.bat",
    )
    parser.add_argument(
        "--with-exe-smoke",
        action="store_true",
        help="Include MinAn.exe launch smoke (requires --with-build or existing dist build)",
    )
    parser.add_argument(
        "--smoke-seconds",
        type=int,
        default=4,
        help="Seconds for EXE liveness check (default: 4)",
    )

    args = parser.parse_args()

    _compile_check()
    _pytest_check()

    if args.with_build:
        _build_release()

    if args.with_exe_smoke:
        _exe_smoke(args.smoke_seconds)

    print("[gate] all requested quality gates passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
