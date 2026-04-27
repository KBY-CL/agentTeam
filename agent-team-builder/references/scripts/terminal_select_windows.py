#!/usr/bin/env python3
"""Launch terminal_select.py in a separate Windows cmd window and return its JSON result."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


def build_child_args(args: argparse.Namespace, out_path: Path) -> list[str]:
    selector = Path(__file__).with_name("terminal_select.py")
    child = [
        sys.executable,
        str(selector),
        "--question",
        args.question,
        "--default",
        str(args.default),
        "--json",
        "--out",
        str(out_path),
        "--pause-on-complete",
    ]
    if args.multi:
        child.append("--multi")
    for option in args.option:
        child.extend(["--option", option])
    return child


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open a real Windows cmd selector window for non-TTY agent shells."
    )
    parser.add_argument("--question", required=True)
    parser.add_argument("--option", action="append", required=True, help="value=label")
    parser.add_argument("--multi", action="store_true")
    parser.add_argument("--default", type=int, default=0)
    parser.add_argument("--out", help="result JSON path")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    if os.name != "nt":
        print(
            json.dumps(
                {
                    "status": "UNSUPPORTED",
                    "reason": "terminal_select_windows.py only supports Windows",
                },
                ensure_ascii=False,
            )
        )
        return 2

    out_path = Path(args.out) if args.out else Path(tempfile.gettempdir()) / (
        f"terminal_choice_{os.getpid()}.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    child_args = build_child_args(args, out_path)
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    try:
        process = subprocess.Popen(
            child_args,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            env=env,
            cwd=str(Path.cwd()),
        )
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "LAUNCH_FAILED",
                    "reason": str(exc),
                    "traceback": traceback.format_exc(),
                },
                ensure_ascii=False,
            )
        )
        return 4

    deadline = time.monotonic() + args.timeout
    while time.monotonic() < deadline:
        if out_path.exists():
            text = out_path.read_text(encoding="utf-8")
            try:
                json.loads(text)
            except json.JSONDecodeError:
                time.sleep(0.1)
                continue
            print(text)
            return 0
        if process.poll() is not None:
            break
        time.sleep(0.2)

    print(
        json.dumps(
            {
                "status": "NO_SELECTION",
                "reason": "selection window closed or timed out before writing a result",
                "child_exit_code": process.poll(),
                "out": str(out_path),
            },
            ensure_ascii=False,
        )
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
