#!/usr/bin/env python3
"""Utility script to launch the Unity project or a built game executable."""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent / "UnityProj"


def _default_build_candidates(root: Path) -> list[Path]:
    patterns = {
        "Windows": ["*.exe"],
        "Linux": ["*.x86_64", "*.x86", "*.AppImage"],
        "Darwin": ["*.app"],
    }
    selected = patterns.get(platform.system(), ["*"])
    found: list[Path] = []

    for pattern in selected:
        found.extend(sorted(root.rglob(pattern)))

    # Ignore editor/temp paths and metadata files.
    return [p for p in found if p.is_file() and "/Library/" not in str(p)]


def launch_process(command: list[str], cwd: Path | None = None) -> int:
    print("Launching:", " ".join(command))
    try:
        subprocess.Popen(command, cwd=cwd)
    except FileNotFoundError as exc:
        print(f"Error: command not found: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: could not launch process: {exc}", file=sys.stderr)
        return 1

    return 0


def launch_editor(unity_path: str) -> int:
    if not PROJECT_DIR.exists():
        print(f"Error: expected Unity project at: {PROJECT_DIR}", file=sys.stderr)
        return 1
    return launch_process([unity_path, "-projectPath", str(PROJECT_DIR)])


def launch_build(build_path: Path | None) -> int:
    if build_path is None:
        build_root = Path(__file__).resolve().parent / "Build"
        if not build_root.exists():
            print(
                "Error: no build path provided and ./Build does not exist. "
                "Use --build-path.",
                file=sys.stderr,
            )
            return 1

        candidates = _default_build_candidates(build_root)
        if not candidates:
            print(
                "Error: no runnable build executable found under ./Build. "
                "Use --build-path to specify one.",
                file=sys.stderr,
            )
            return 1

        build_path = candidates[0]
        print(f"Auto-detected build: {build_path}")

    if not build_path.exists():
        print(f"Error: build path does not exist: {build_path}", file=sys.stderr)
        return 1

    if build_path.suffix == ".app" and platform.system() == "Darwin":
        return launch_process(["open", str(build_path)])

    return launch_process([str(build_path)], cwd=build_path.parent)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Unity project in editor mode or launch a built game executable."
    )
    parser.add_argument(
        "--mode",
        choices=["editor", "build"],
        default="build",
        help="editor: open Unity editor project, build: launch build executable",
    )
    parser.add_argument(
        "--build-path",
        type=Path,
        help="Path to a specific game executable (.exe/.x86_64/.app etc).",
    )
    parser.add_argument(
        "--unity-path",
        default=os.getenv("UNITY_EDITOR_PATH", "unity"),
        help="Path to Unity executable (or set UNITY_EDITOR_PATH env variable).",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.mode == "editor":
        return launch_editor(args.unity_path)

    return launch_build(args.build_path)


if __name__ == "__main__":
    raise SystemExit(main())
