# Contributing

## Contribution Scope

Each pull request should add or improve one reusable skill, one specialist agent, or the documentation required to support them. Keep unrelated cleanup separate so reviewers can verify the behavior and boundaries of the change.

## Adding a Skill

1. Create `.github/skills/<lowercase-hyphenated-name>/SKILL.md`.
2. Match the folder name in the skill's `name` front matter.
3. Write a keyword-rich description that explains when the skill should be used.
4. Include a purpose, repeatable procedure, structured output format, and explicit boundaries.
5. Link the skill from each agent definition that needs it. Keep the README catalogue capability-based; do not maintain a list of consuming agents there.

## Adding an Agent

1. Create `.github/agents/<role>.agent.md` for one specific engineering responsibility.
2. Grant only the tools required for that responsibility.
3. Link only the skills the agent needs; do not duplicate a skill's workflow in the agent.
4. Define a procedure, boundaries, and an output that can be reviewed by a human engineer.
5. Add the agent to the README catalogue and describe why an existing specialist cannot own the work.

## Compatibility Rules

- Preserve an existing skill's output headings and fields when agents or documentation depend on them.
- When an output must change, update every consuming agent and include a migration note in the pull request description.
- Use relative links for all local agent and skill references.
- Do not rename or relocate an agent or skill without updating the README and all inbound references.

## Pull Request Checklist

- [ ] The change has one bounded engineering purpose.
- [ ] Agent and skill names follow the repository naming convention.
- [ ] The front matter contains a meaningful description.
- [ ] Inputs, outputs, evidence requirements, and boundaries are clear.
- [ ] The change does not grant unnecessary tools or authority.
- [ ] All README, agent, and skill links resolve.
- [ ] Any consumers affected by an output change were updated.
- [ ] A reviewer can reproduce the conclusion from the cited evidence.