#!/usr/bin/env python3
"""
Validate agent-skill tool compatibility.

For each agent, check that its declared `tools` list is a superset of
every declared skill's `tools` list for all skills listed in the agent's
`skills` field.

Also checks:
  - Every skill has `tools` and `version` in its frontmatter.
  - Every agent has a `skills` field in its frontmatter.

Exit code 0 = all checks pass, 1 = one or more violations found.

No external dependencies — frontmatter is parsed with pure regex.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(REPO_ROOT, ".github", "agents")
SKILLS_DIR = os.path.join(REPO_ROOT, ".github", "skills")


def _parse_inline_list(value):
    """Parse a YAML inline list like [a, b, c] into a Python list."""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"').strip("'") for item in inner.split(",")]
    return []


def _parse_scalar(value):
    """Parse a YAML scalar value, stripping quotes."""
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_frontmatter(filepath):
    """Extract and parse YAML frontmatter from a markdown file.

    Handles the subset of YAML used in agent/skill frontmatter:
    simple key: value and key: [inline, list] pairs.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("["):
            result[key] = _parse_inline_list(value)
        else:
            result[key] = _parse_scalar(value)
    return result


def load_skills():
    """Load all skill frontmatter keyed by skill name."""
    skills = {}
    if not os.path.isdir(SKILLS_DIR):
        return skills
    for entry in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, entry, "SKILL.md")
        if not os.path.isfile(skill_path):
            continue
        fm = parse_frontmatter(skill_path)
        name = fm.get("name", entry)
        skills[name] = {
            "path": skill_path,
            "tools": set(fm.get("tools", []) or []),
            "version": fm.get("version", "unversioned"),
        }
    return skills


def load_agents():
    """Load all agent frontmatter keyed by agent name."""
    agents = {}
    if not os.path.isdir(AGENTS_DIR):
        return agents
    for entry in os.listdir(AGENTS_DIR):
        if not entry.endswith(".agent.md"):
            continue
        agent_path = os.path.join(AGENTS_DIR, entry)
        fm = parse_frontmatter(agent_path)
        name = fm.get("name", entry.replace(".agent.md", ""))
        agents[name] = {
            "path": agent_path,
            "tools": set(fm.get("tools", []) or []),
            "skills": fm.get("skills", []) or [],
        }
    return agents


def validate(skills, agents):
    """Run all validation checks and return a list of error strings."""
    errors = []

    # Check 1: Every skill must have `tools` and `version`
    for skill_name, skill_info in sorted(skills.items()):
        if not skill_info["tools"]:
            errors.append(
                f"Skill '{skill_name}' ({skill_info['path']}): "
                f"missing required 'tools' field in frontmatter"
            )
        if skill_info["version"] == "unversioned":
            errors.append(
                f"Skill '{skill_name}' ({skill_info['path']}): "
                f"missing required 'version' field in frontmatter"
            )

    # Check 2: Every agent must have `skills`
    for agent_name, agent_info in sorted(agents.items()):
        if not agent_info["skills"]:
            errors.append(
                f"Agent '{agent_name}' ({agent_info['path']}): "
                f"missing required 'skills' field in frontmatter"
            )

    # Check 3: Agent tools must be a superset of each consumed skill's tools
    for agent_name, agent_info in sorted(agents.items()):
        for skill_name in agent_info["skills"]:
            if skill_name not in skills:
                errors.append(
                    f"Agent '{agent_name}' declares skill '{skill_name}' "
                    f"but no skill with that name exists in {SKILLS_DIR}"
                )
                continue
            skill_tools = skills[skill_name]["tools"]
            missing = skill_tools - agent_info["tools"]
            if missing:
                errors.append(
                    f"Agent '{agent_name}' ({agent_info['path']}): "
                    f"tools {sorted(agent_info['tools'])} do not cover "
                    f"skill '{skill_name}' tools {sorted(skill_tools)} "
                    f"— missing: {sorted(missing)}"
                )

    return errors


def main():
    skills = load_skills()
    agents = load_agents()

    print(f"Loaded {len(skills)} skills and {len(agents)} agents\n")

    errors = validate(skills, agents)

    if errors:
        print(f"\u274c  {len(errors)} validation error(s):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\u2705  All checks passed:")
        print(f"     - Every skill has tools + version")
        print(f"     - Every agent has a skills list")
        print(f"     - Every agent's tools cover its skills' tools")
        sys.exit(0)


if __name__ == "__main__":
    main()
