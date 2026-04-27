#!/usr/bin/env python3
"""Arrow-key terminal selector for agent-team-builder interviews."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass


@dataclass
class Option:
    value: str
    label: str


def parse_option(raw: str) -> Option:
    if "=" in raw:
        value, label = raw.split("=", 1)
        return Option(value.strip(), label.strip())
    value = raw.strip()
    return Option(value, value)


def supports_interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def clear_screen() -> None:
    sys.stdout.write("\x1b[2J\x1b[H")


def render(question: str, options: list[Option], index: int, selected: set[int], multi: bool) -> None:
    clear_screen()
    sys.stdout.write(question + "\n\n")
    hint = "↑/↓ move, Space toggle, Enter confirm" if multi else "↑/↓ move, Enter confirm"
    sys.stdout.write(hint + "\n\n")
    for i, option in enumerate(options):
        cursor = ">" if i == index else " "
        mark = "[x]" if i in selected else "[ ]"
        if not multi:
            mark = "(*) " if i == index else "( ) "
        sys.stdout.write(f"{cursor} {mark} {option.label}\n")
    sys.stdout.flush()


def read_key_windows() -> str:
    import msvcrt

    ch = msvcrt.getwch()
    if ch in ("\x00", "\xe0"):
        ch2 = msvcrt.getwch()
        return {"H": "up", "P": "down"}.get(ch2, "")
    if ch in ("\r", "\n"):
        return "enter"
    if ch == " ":
        return "space"
    if ch in ("\x03", "\x1b"):
        return "escape"
    return ch


def read_key_posix() -> str:
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            return {"[A": "up", "[B": "down"}.get(seq, "escape")
        if ch in ("\r", "\n"):
            return "enter"
        if ch == " ":
            return "space"
        if ch == "\x03":
            return "escape"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_key() -> str:
    if os.name == "nt":
        return read_key_windows()
    return read_key_posix()


def interactive_select(question: str, options: list[Option], multi: bool, default: int) -> list[Option]:
    index = max(0, min(default, len(options) - 1))
    selected: set[int] = {index} if multi and default >= 0 else set()
    while True:
        render(question, options, index, selected, multi)
        key = read_key()
        if key == "up":
            index = (index - 1) % len(options)
        elif key == "down":
            index = (index + 1) % len(options)
        elif key == "space" and multi:
            if index in selected:
                selected.remove(index)
            else:
                selected.add(index)
        elif key == "enter":
            if multi:
                if not selected:
                    selected.add(index)
                return [options[i] for i in sorted(selected)]
            return [options[index]]
        elif key == "escape":
            raise KeyboardInterrupt


def fallback_select(question: str, options: list[Option], multi: bool, default: int) -> list[Option]:
    print(question)
    for i, option in enumerate(options, 1):
        marker = " (default)" if i - 1 == default else ""
        print(f"{i}. {option.label}{marker}")
    prompt = "Select numbers separated by comma: " if multi else "Select number: "
    raw = input(prompt).strip()
    if not raw and default >= 0:
        return [options[default]]
    indexes = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        indexes.append(max(1, min(int(part), len(options))) - 1)
    if not indexes:
        indexes = [max(0, default)]
    if not multi:
        indexes = indexes[:1]
    return [options[i] for i in indexes]


def main() -> int:
    parser = argparse.ArgumentParser(description="Arrow-key selection UI for agent interviews.")
    parser.add_argument("--question", required=True)
    parser.add_argument("--option", action="append", required=True, help="value=label")
    parser.add_argument("--multi", action="store_true")
    parser.add_argument("--default", type=int, default=0, help="zero-based default index")
    parser.add_argument("--json", action="store_true", help="print JSON result")
    args = parser.parse_args()

    options = [parse_option(raw) for raw in args.option]
    if not options:
        raise SystemExit("at least one option is required")

    if supports_interactive():
        chosen = interactive_select(args.question, options, args.multi, args.default)
    else:
        chosen = fallback_select(args.question, options, args.multi, args.default)

    result = {
        "multi": args.multi,
        "values": [item.value for item in chosen],
        "labels": [item.label for item in chosen],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(", ".join(result["labels"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
