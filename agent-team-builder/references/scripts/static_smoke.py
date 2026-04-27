#!/usr/bin/env python3
"""Agent Team static smoke test."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

ROOT = Path(".")
AGENTS_DIR = ROOT / ".claude/agents"
SKILLS_DIR = ROOT / ".claude/skills"
HOOKS_DIR = ROOT / ".claude/hooks"
TOOLS_DIR = ROOT / ".agent-team/tools"
REGISTRY_PATH = ROOT / ".agent-team/registry.json"
SCHEMA_CANDIDATES = [
    ROOT / ".agent-team/schemas/registry.schema.json",
    ROOT / "references/schemas/registry.schema.json",
]
RESULTS: list[dict[str, str]] = []

GLOBAL_FORBIDDEN_TOOL_PATTERNS = [
    r"mcp__.*__delete_",
    r"mcp__.*__admin_",
    r"mcp__.*__write_iam",
]

DANGEROUS_COMMAND_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"terraform\s+apply",
    r"kubectl\s+delete",
    r"DROP\s+TABLE",
    r"git\s+push\s+--force",
    r"curl\s+.*\|\s*sh",
]


def check(name: str, passed: bool, detail: str = "") -> None:
    status = "PASS" if passed else "FAIL"
    RESULTS.append({"name": name, "status": status, "detail": detail})
    mark = "✓" if passed else "✗"
    suffix = f" — {detail}" if detail else ""
    print(f"{mark} [{status}] {name}{suffix}")


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    raw = match.group(1)
    if HAS_YAML:
        try:
            return yaml.safe_load(raw)
        except Exception:
            return None

    frontmatter = {}
    for line in raw.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def normalize_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def collect_hook_commands(settings_data: dict) -> list[str]:
    hooks_section = settings_data.get("hooks", {})
    commands: list[str] = []

    if isinstance(hooks_section, dict):
        for matchers in hooks_section.values():
            if not isinstance(matchers, list):
                continue
            for matcher_obj in matchers:
                if not isinstance(matcher_obj, dict):
                    continue
                for hook in matcher_obj.get("hooks", []):
                    if isinstance(hook, dict):
                        command = hook.get("command", "")
                        if command:
                            commands.append(command)
    elif isinstance(hooks_section, list):
        for hook in hooks_section:
            if isinstance(hook, dict):
                command = hook.get("command", "")
                if command:
                    commands.append(command)

    return commands


def find_schema_path() -> Path | None:
    for candidate in SCHEMA_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def validate_schema_subset(instance, schema, path="$") -> list[str]:
    errors: list[str] = []
    schema_type = schema.get("type")

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum")
        return errors

    if schema_type == "object":
        if not isinstance(instance, dict):
            return [f"{path}: expected object"]

        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required key {key!r}")

        if schema.get("additionalProperties", True) is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                errors.append(f"{path}: unexpected keys {extras}")

        for key, value in instance.items():
            if key in properties:
                errors.extend(
                    validate_schema_subset(value, properties[key], f"{path}.{key}")
                )

        return errors

    if schema_type == "array":
        if not isinstance(instance, list):
            return [f"{path}: expected array"]
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(instance):
                errors.extend(
                    validate_schema_subset(item, item_schema, f"{path}[{index}]")
                )
        return errors

    if schema_type == "string":
        if not isinstance(instance, str):
            return [f"{path}: expected string"]
        return errors

    if schema_type == "boolean":
        if not isinstance(instance, bool):
            return [f"{path}: expected boolean"]
        return errors

    if schema_type == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            return [f"{path}: expected integer"]
        minimum = schema.get("minimum")
        if minimum is not None and instance < minimum:
            errors.append(f"{path}: expected >= {minimum}")
        return errors

    return errors


# 1. Agent frontmatter
required_frontmatter = ["name", "description", "model", "tools"]
for path in sorted(AGENTS_DIR.rglob("*.md")):
    frontmatter = parse_frontmatter(path)
    if frontmatter is None:
        check(f"frontmatter:{path.name}", False, "no frontmatter found")
        continue
    missing = [key for key in required_frontmatter if key not in frontmatter]
    check(
        f"frontmatter:{path.name}",
        not missing,
        f"missing: {missing}" if missing else "",
    )

# 2. Required files
for rel_path, base_dir in [
    ("request-intake-agent.md", AGENTS_DIR),
    ("_common/terminal-choice/SKILL.md", SKILLS_DIR),
    ("_common/tdd-workflow/SKILL.md", SKILLS_DIR),
    ("_common/doc-updater/SKILL.md", SKILLS_DIR),
    ("_common/handoff-writer/SKILL.md", SKILLS_DIR),
    ("terminal_select.py", TOOLS_DIR),
]:
    target = base_dir / rel_path
    check(
        f"required:{rel_path}",
        target.exists(),
        "" if target.exists() else "file not found",
    )

# 3. CLAUDE.md marker blocks + import
claude_md = ROOT / "CLAUDE.md"
if claude_md.exists():
    text = claude_md.read_text(encoding="utf-8")
    check("CLAUDE.md:marker-start", "AGENT_TEAM_START" in text)
    check("CLAUDE.md:marker-end", "AGENT_TEAM_END" in text)
    check("CLAUDE.md:agents-import", "@AGENTS.md" in text)
    line_count = len(text.splitlines())
    check("CLAUDE.md:line-budget", line_count <= 200, f"{line_count} lines (limit 200)")
else:
    check("CLAUDE.md:exists", False, "file not found")

# 4. AGENTS.md line budget
agents_md = ROOT / "AGENTS.md"
if agents_md.exists():
    line_count = len(agents_md.read_text(encoding="utf-8").splitlines())
    check("AGENTS.md:line-budget", line_count <= 300, f"{line_count} lines (limit 300)")
else:
    check("AGENTS.md:exists", False, "file not found")

# 5. shared-rules budget + security hint
shared_rules = AGENTS_DIR / "_common/shared-rules.md"
if shared_rules.exists():
    text = shared_rules.read_text(encoding="utf-8")
    check(
        "shared-rules:security-section",
        any(token in text for token in ["secrets", "hardcod", "하드코딩"]),
    )
    line_count = len(text.splitlines())
    check("shared-rules:line-budget", line_count <= 200, f"{line_count} lines (limit 200)")

# 6. settings.json validity + duplicate hooks
settings = ROOT / ".claude/settings.json"
settings_data = None
if settings.exists():
    try:
        settings_data = json.loads(settings.read_text(encoding="utf-8"))
        check("settings.json:valid", True)
        commands = collect_hook_commands(settings_data)
        duplicates = sorted({cmd for cmd in commands if commands.count(cmd) > 1})
        check(
            "settings.json:no-duplicate-hooks",
            not duplicates,
            f"duplicates: {duplicates}" if duplicates else "",
        )
    except json.JSONDecodeError as exc:
        check("settings.json:valid", False, f"JSON parse error: {exc}")
else:
    check("settings.json:exists", False, "file not found")

# 7. Per-agent line budget
for path in sorted(AGENTS_DIR.rglob("*.md")):
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    check(f"line-budget:{path.name}", line_count <= 250, f"{line_count} lines (limit 250)")

# 8. Per-skill line budget
for path in sorted(SKILLS_DIR.rglob("SKILL.md")):
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    check(
        f"skill-line-budget:{path.parent.name}",
        line_count <= 500,
        f"{line_count} lines (limit 500)",
    )

# 9. tools / forbidden overlap and global forbidden patterns
for path in sorted(AGENTS_DIR.rglob("*.md")):
    frontmatter = parse_frontmatter(path)
    if not frontmatter:
        continue

    tools = normalize_list(frontmatter.get("tools", []))
    forbidden = normalize_list(frontmatter.get("forbidden", []))
    overlap = sorted(set(tools) & set(forbidden))
    check(
        f"forbidden-overlap:{path.name}",
        not overlap,
        f"tool(s) in both tools and forbidden: {overlap}" if overlap else "",
    )

    for tool in tools:
        for pattern in GLOBAL_FORBIDDEN_TOOL_PATTERNS:
            if re.search(pattern, tool):
                check(
                    f"global-forbidden-tool:{path.name}",
                    False,
                    f"tool {tool!r} matches pattern {pattern!r}",
                )
                break

# 10. Dangerous command patterns
if settings_data is not None:
    for command in collect_hook_commands(settings_data):
        for pattern in DANGEROUS_COMMAND_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                check(
                    f"dangerous-hook-command:{pattern}",
                    False,
                    f"pattern {pattern!r} found in settings hook command {command!r}",
                )

for path in sorted(HOOKS_DIR.rglob("*.sh")):
    text = path.read_text(encoding="utf-8")
    for pattern in DANGEROUS_COMMAND_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            check(
                f"dangerous-hook-script:{path.name}",
                False,
                f"pattern {pattern!r} found in {path}",
            )

for path in sorted(TOOLS_DIR.rglob("*.py")):
    if path.name == "static_smoke.py":
        continue
    text = path.read_text(encoding="utf-8")
    if "subprocess" not in text and "os.system" not in text:
        continue
    for pattern in DANGEROUS_COMMAND_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            check(
                f"dangerous-tool-script:{path.name}",
                False,
                f"pattern {pattern!r} found in {path}",
            )

# 11. registry schema validation
schema_path = find_schema_path()
if schema_path is None:
    check("registry.schema:exists", False, "schema file not found")
    schema_data = None
else:
    try:
        schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
        check("registry.schema:valid-json", True, str(schema_path))
    except json.JSONDecodeError as exc:
        schema_data = None
        check("registry.schema:valid-json", False, f"JSON parse error: {exc}")

if REGISTRY_PATH.exists():
    try:
        registry_data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        check("registry.json:valid-json", True)
        if schema_path is not None and schema_data is not None:
            errors = validate_schema_subset(registry_data, schema_data)
            check(
                "registry.json:schema",
                not errors,
                "; ".join(errors[:3]) if errors else "",
            )
    except json.JSONDecodeError as exc:
        check("registry.json:valid-json", False, f"JSON parse error: {exc}")
else:
    check(
        "registry.json:schema",
        True,
        "registry not present; validate after Step 9",
    )

# 12. .gitignore entries
gitignore = ROOT / ".gitignore"
if gitignore.exists():
    text = gitignore.read_text(encoding="utf-8")
    for entry in [".claude/handoff", "intake_", "backups/"]:
        check(f"gitignore:{entry}", entry in text)

passed = sum(1 for result in RESULTS if result["status"] == "PASS")
failed = sum(1 for result in RESULTS if result["status"] == "FAIL")
print(f"\n=== Static Smoke: {passed} PASS / {failed} FAIL ===")
sys.exit(0 if failed == 0 else 1)
