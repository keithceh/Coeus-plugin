# Contributing to Coeus

Thank you for your interest in contributing to Coeus. Please read these guidelines before submitting issues or pull requests.

---

## Legal Requirements

### License

This project is licensed under the **Business Source License 1.1**. By contributing, you agree that your contributions will be licensed under the same terms. See [LICENSE](LICENSE).

### Contributor License Agreement (CLA)

All contributors must sign the [Contributor License Agreement](CLA.md) before their pull requests can be merged. This is handled automatically by CLA Assistant when you open a PR — the bot will prompt you to sign.

---

## Reporting Bugs

1. Search [existing issues](https://github.com/keithceh/Coeus/issues) to avoid duplicates.
2. Use the **Bug Report** issue template.
3. Include the affected skill, steps to reproduce, expected vs. actual behaviour, and your Claude version.

---

## Requesting Features

1. Search existing issues and discussions first.
2. Use the **Feature Request** issue template.
3. Describe the problem the feature solves, not just the feature itself.
4. Cite any methodology or prior art if proposing changes to the deliberation logic.

---

## Submitting Pull Requests

1. Fork the repository and create a feature branch from `main`.
2. Make focused, minimal changes — one concern per PR.
3. Update or add documentation for any changed behaviour.
4. Ensure your changes do not break the skill structure (each skill must have a valid `SKILL.md` with correct YAML frontmatter).
5. Fill out the Pull Request template completely.
6. Sign the CLA when prompted.

---

## Style Guidelines

When contributing to skill logic, follow these principles:

### Model Agnosticism
Skills must not hard-code assumptions about specific Claude model capabilities. Use abstract role names (e.g., "Model A", "Blue faction") rather than model version strings in logic paths.

### Deterministic Phase Gates
Each phase in LLM-council must have explicit entry conditions and exit criteria. Do not add phases that can be skipped silently.

### Caveman Scope Discipline
The caveman step must only compress the *prompt* or *instruction*, never the user's deliverables, artifacts, or structured outputs (e.g., `Final_Plan.md`, `Premortem_Report.md`). This applies in Morpheus (Step 2), The Architect (Steps A2 and C3), and any future skill that chains caveman.

### Architect Route Integrity
The Architect's ROUTE A and ROUTE C must remain fully distinct. ROUTE C must always produce a confirmed Problem Definition Document before prompt-master is invoked. Never allow the explore phase to silently collapse into ROUTE A without surfacing the problem definition to the user.

### Scientific Rigour
Uncertainty claims must be explicitly flagged. Do not add steps that produce confident outputs without surfacing confidence levels or caveats.

### Prompt Clarity
All prompt-master outputs must include model routing guidance and be legible to a human reviewer without further context.

### Security Defaults
Skills must not instruct Claude to bypass safety guidelines, ignore system prompts, or impersonate specific real individuals (models in LLM-council are simulations, not impersonations).

---

## Questions

Open a [Discussion](https://github.com/keithceh/Coeus/discussions) for general questions, or an issue for specific bugs and feature requests.
