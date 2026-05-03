---
name: spec-driven-development
description: Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.
---

# Spec-Driven Development

## Overview

Write a structured specification before writing any code. The spec is the shared source of truth between you and the human engineer — it defines what we're building, why, and how we'll know it's done. Code without a spec is guessing.

## When to Use

- Starting a new project or feature
- Requirements are ambiguous or incomplete
- The change touches multiple files or modules
- You're about to make an architectural decision
- The task would take more than 30 minutes to implement

**When NOT to use:** Single-line fixes, typo corrections, or changes where requirements are unambiguous and self-contained.

## The Gated Workflow

Spec-driven development has four phases. Do not advance to the next phase until the current one is validated.

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

### Phase 1: Specify

Start with a high-level vision. Ask the human clarifying questions until requirements are concrete.

**Surface assumptions immediately.** Before writing any spec content, list what you're assuming:

```
ASSUMPTIONS I'M MAKING:
1. This is a web application (not native mobile)
2. Authentication uses session-based cookies (not JWT)
3. The database is PostgreSQL (based on existing Prisma schema)
4. We're targeting modern browsers only (no IE11)
→ Correct me now or I'll proceed with these.
```

Don't silently fill in ambiguous requirements. The spec's entire purpose is to surface misunderstandings *before* code gets written — assumptions are the most dangerous form of misunderstanding.

**Write a spec document covering these six core areas:**

1. **Objective** — What are we building and why? Who is the user? What does success look like?

2. **Commands** — Full executable commands with flags, not just tool names.
   ```
   Build: npm run build
   Test: npm test -- --coverage
   Lint: npm run lint --fix
   Dev: npm run dev
   ```

3. **Project Structure** — Where source code lives, where tests go, where docs belong.
   ```
   src/           → Application source code
   src/components → React components
   src/lib        → Shared utilities
   tests/         → Unit and integration tests
   e2e/           → End-to-end tests
   docs/          → Documentation
   ```

4. **Code Style** — One real code snippet showing your style beats three paragraphs describing it. Include naming conventions, formatting rules, and examples of good output.

5. **Testing Strategy** — What framework, where tests live, coverage expectations, which test levels for which concerns.

6. **Boundaries** — Three-tier system:
   - **Always do:** Run tests before commits, follow naming conventions, validate inputs
   - **Ask first:** Database schema changes, adding dependencies, changing CI config
   - **Never do:** Commit secrets, edit vendor directories, remove failing tests without approval

**Spec template:**

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements, test levels]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Open Questions
[Anything unresolved that needs human input]
```

**Reframe instructions as success criteria.** When receiving vague requirements, translate them into concrete conditions:

```
REQUIREMENT: "Make the dashboard faster"

REFRAMED SUCCESS CRITERIA:
- Dashboard LCP < 2.5s on 4G connection
- Initial data load completes in < 500ms
- No layout shift during load (CLS < 0.1)
→ Are these the right targets?
```

This lets you loop, retry, and problem-solve toward a clear goal rather than guessing what "faster" means.

### Phase 2: Plan

With the validated spec, generate a technical implementation plan:

1. Identify the major components and their dependencies
2. Determine the implementation order (what must be built first)
3. Note risks and mitigation strategies
4. Identify what can be built in parallel vs. what must be sequential
5. Define verification checkpoints between phases

The plan should be reviewable: the human should be able to read it and say "yes, that's the right approach" or "no, change X."

### Phase 3: Tasks

Break the plan into discrete, implementable tasks:

- Each task should be completable in a single focused session
- Each task has explicit acceptance criteria
- Each task includes a verification step (test, build, manual check)
- Tasks are ordered by dependency, not by perceived importance
- No task should require changing more than ~5 files

**Task template:**
```markdown
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [How to confirm — test command, build, manual check]
  - Files: [Which files will be touched]
```

### Phase 4: Implement

Execute tasks one at a time following `incremental-implementation` and `test-driven-development` skills. Use `context-engineering` to load the right spec sections and source files at each step rather than flooding the agent with the entire spec.

## Keeping the Spec Alive

The spec is a living document, not a one-time artifact:

- **Update when decisions change** — If you discover the data model needs to change, update the spec first, then implement.
- **Update when scope changes** — Features added or cut should be reflected in the spec.
- **Commit the spec** — The spec belongs in version control alongside the code.
- **Reference the spec in PRs** — Link back to the spec section that each PR implements.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | Simple tasks don't need *long* specs, but they still need acceptance criteria. A two-line spec is fine. |
| "I'll write the spec after I code it" | That's documentation, not specification. The spec's value is in forcing clarity *before* code. |
| "The spec will slow us down" | A 15-minute spec prevents hours of rework. Waterfall in 15 minutes beats debugging in 15 hours. |
| "Requirements will change anyway" | That's why the spec is a living document. An outdated spec is still better than no spec. |
| "The user knows what they want" | Even clear requests have implicit assumptions. The spec surfaces those assumptions. |

## Red Flags

- Starting to write code without any written requirements
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or task list
- Making architectural decisions without documenting them
- Skipping the spec because "it's obvious what to build"

## Verification

Before proceeding to implementation, confirm:

- [ ] The spec covers all six core areas
- [ ] The human has reviewed and approved the spec
- [ ] Success criteria are specific and testable
- [ ] Boundaries (Always/Ask First/Never) are defined
- [ ] The spec is saved to a file in the repository

---

# Spec: seCureLI modernization MVP (2026)

This section is the **active product spec** for this fork. Process guidance above still applies; implement work against this document and keep it updated when scope changes.

## Objective

Bring the CLI to a **maintainable, 2026-ready baseline** without a rewrite: current Python support, machine-readable scan output for automation and GitHub, safer `init` UX, and a quick health check command. Success = upstream parity on core flows plus these four deliverables, clean CI, and no new default telemetry or secret exfiltration.

**Users:** developers running seCureLI locally and in CI; maintainers extending the Python codebase.

**Non-goals (this spec):** Rust core, AI remediation, SBOM/license suites, opinionated profiles (startup/enterprise), HTML report UI, plugin registry, full policy-as-code.

## Assumptions

1. CLI stays **Python + Typer**; pre-commit remains the hook execution engine.
2. **SARIF 2.1.0** output is sufficient at a minimal viable level (rule IDs, locations, messages) for upload to compatible consumers; full GitHub Code Scanning parity can iterate later.
3. **JSON** format is stable for scripting; breaking JSON shape is a semver concern later, not blocked for MVP.
4. Unblocking **Python 3.12+** may require changing how `dependency-injector` is pinned (e.g. released version with 3.12 support or a narrow fork/git pin) — exact resolution is implementation detail; outcome is supported 3.12 in `pyproject` and CI.

## Tech stack

- Python (target **3.12** minimum supported for this track; keep **3.9–3.11** working if low cost, else document lift in CHANGELOG).
- Poetry / existing `pyproject.toml` layout.
- Typer, Pydantic (**v2** after migration), pre-commit, pytest.

## Commands (target surface)

```bash
# Existing — keep working
poetry install
poetry run poe test
poetry run secureli scan
poetry run secureli init

# New / extended
poetry run secureli scan --format text    # default; current behavior
poetry run secureli scan --format json
poetry run secureli scan --format sarif
poetry run secureli init --dry-run        # no writes; print planned changes
poetry run secureli doctor                # environment + repo readiness checks
```

CI (existing patterns): extend matrix to include Python 3.12 where applicable.

## Project structure (touch points)

- `secureli/main.py` — new flags / `doctor` command registration.
- `secureli/actions/scan.py` — orchestrate formatters; exit codes unchanged (fail on findings).
- New small module e.g. `secureli/modules/shared/scan_output/` or `formatters/` — JSON + SARIF builders (pure functions, testable).
- `secureli/actions/initializer.py` (or equivalent) — dry-run path: compute same plan as today, skip writes, print summary.
- New `secureli/actions/doctor.py` (or service) — read-only checks.
- `tests/` — unit tests for formatters and doctor; extend CLI tests for new flags.

## Code style

- Match existing module layout, type hints, and Typer `Option` patterns.
- Formatters take a structured in-memory result (reuse or extend `ScanResult` / failures list), not raw ANSI strings.
- SARIF: build a dict matching SARIF 2.1.0 schema where practical; validate with a focused test (golden file or required keys).

Example (illustrative):

```python
def scan_failures_to_sarif(failures: list[ScanFailure], tool_name: str) -> dict:
    """Return SARIF Log dict; no I/O."""
    ...
```

## Testing strategy

- **pytest** for new pure functions (SARIF/JSON structure, doctor rules).
- CLI: extend existing `tests/application/test_main.py` (or parallel) for `--format`, `--dry-run`, `doctor`.
- Golden or snapshot tests for **one** representative SARIF and JSON payload to prevent drift.
- Run full `poe test` before merge; no reduction in existing coverage without approval.

## Boundaries

- **Always:** default `scan` output remains human **text** unless `--format` is set; never print raw secrets in JSON/SARIF (messages as delivered by hooks today — do not add new secret-bearing fields).
- **Ask first:** dropping Python 3.9/3.10 support, new runtime dependencies, changing default hook sets, semantic changes to `init` without `--dry-run`.
- **Never:** enable remote logging/telemetry by default; commit real credentials; vendor unrelated submodules for MVP.

## Success criteria

1. **Python 3.12** installs and passes test suite in CI; `python` constraint in `pyproject.toml` documents supported range.
2. `secureli scan --format json` writes **valid JSON** to stdout (or configured stream) and exits non-zero on failures; empty/failure cases covered by tests.
3. `secureli scan --format sarif` emits **SARIF 2.1.0** JSON with at least one `run` and `results` when failures exist; documented limitation if any field is omitted.
4. `secureli init --dry-run` performs **no filesystem writes** to pre-commit or `.secureli` config paths; output lists intended actions; tested.
5. `secureli doctor` exits **0** when checks pass, **non-zero** with actionable messages when pre-commit missing, wrong Python, or expected config missing; documented in README.
6. README (short section) documents new flags and CI example snippet for `scan --format json` (SARIF optional line).

## Implementation order

1. Python 3.12 + Pydantic v2 + dependency fixes (unblocks everything else).
2. JSON formatter + `--format` wiring (simplest machine output).
3. SARIF formatter + tests.
4. `init --dry-run`.
5. `doctor` + docs.

## Open questions

- Keep 3.9–3.11 in matrix for how long after 3.12 lands?
- SARIF rule IDs: map from hook IDs only, or include custom scanner IDs uniformly?
