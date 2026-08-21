# Contributing

## Contribution Scope

Each pull request should add or improve one reusable skill, one specialist agent, or the documentation required to support them. Keep unrelated cleanup separate so reviewers can verify the behavior and boundaries of the change.

## Adding a Skill

1. Create `.github/skills/<lowercase-hyphenated-name>/SKILL.md`.
2. Match the folder name in the skill's `name` front matter.
3. Write a keyword-rich description that explains when the skill should be used.
4. Include a purpose, repeatable procedure, structured output format, and explicit boundaries.
5. Declare a `tools` field in the front matter listing every tool the procedure calls.
6. Declare a `version` field in the front matter (e.g., `version: "1.0"`). Bump the major version when the output format changes in a way that breaks consuming agents.
7. Link the skill from each agent definition that needs it. Keep the README catalogue capability-based; do not maintain a list of consuming agents there.

## Adding an Agent

1. Create `.github/agents/<role>.agent.md` for one specific engineering responsibility.
2. Grant only the tools required for that responsibility.
3. Declare a `skills` field in the front matter listing every skill the agent invokes.
4. Ensure the agent's `tools` list is a superset of every declared skill's `tools` list. The CI validation script checks this automatically.
5. Link only the skills the agent needs; do not duplicate a skill's workflow in the agent.
6. Define a procedure, boundaries, and an output that can be reviewed by a human engineer.
7. Add the agent to the README catalogue and describe why an existing specialist cannot own the work.

## Compatibility Rules

- Preserve an existing skill's output headings and fields when agents or documentation depend on them.
- When an output must change, bump the skill's `version`, update every consuming agent, and include a migration note in the pull request description.
- Use relative links for all local agent and skill references.
- Do not rename or relocate an agent or skill without updating the README and all inbound references.

## Pull Request Checklist

- [ ] The change has one bounded engineering purpose.
- [ ] Agent and skill names follow the repository naming convention.
- [ ] The front matter contains a meaningful description.
- [ ] Every skill has a `tools` field and a `version` field.
- [ ] Every agent has a `skills` field listing its consumed skills.
- [ ] Each agent's `tools` list is a superset of all its skills' `tools` lists.
- [ ] Inputs, outputs, evidence requirements, and boundaries are clear.
- [ ] The change does not grant unnecessary tools or authority.
- [ ] All README, agent, and skill links resolve.
- [ ] Any consumers affected by an output change were updated.
- [ ] A reviewer can reproduce the conclusion from the cited evidence.
