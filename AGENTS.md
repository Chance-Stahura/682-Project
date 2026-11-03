# AI Development Instructions

## Project Context

Before proposing architectural changes, consult:

- PROJECT.md
- README.md

## Development Constraints

- Do not introduce technologies that conflict
  with the project requirements.

- Do not modify unrelated components.

- Preserve existing architectural decisions
  unless explicitly instructed otherwise.

- Prefer incremental changes over large refactors.

## Implementation Guidelines

- Explain proposed changes before implementation.
- Identify which requirements a change satisfies.
- Do not introduce unnecessary dependencies.
- Maintain consistency with existing code.

## Scope Management

If a requested change conflicts with the project
requirements, identify the conflict before proceeding.

If requirements are ambiguous, request clarification
rather than inventing additional requirements.

## Research Reproducability

- Treat the researchers' original Perl codebas as the baseline implementation. 
- DO NOT MODIFY THE ORIGINAL RESEARCHERS'ALGORITHMS WITHOUT EXPLICIT APPROVAL. 
- Prefer implementing preprocessing, dataset generation, and result analysis in separate Python scripts.
- Use Bash scripts to coordinate execution of the existing Perl pipeline when appropriate. 
- Clearly distinguish baseline reproduction, positive controls, and negative controls.
- Do not assume experimental results confirm or refute the researchers' conclusions without appropriate comparisons.