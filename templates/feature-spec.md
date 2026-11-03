# Feature Specification — <name>

> One feature per directory: `specs/features/<name>/`. Keep ≤ ~2,500 tokens;
> split when unrelated workflows appear.

## Context
Why this capability exists and which product requirement it implements.

## Actors
Who/what interacts with this feature.

## Preconditions
State required before the feature can act.

## Functional requirements
- **FR-XXX.n** — one requirement per line, stable IDs.

## Business rules
- **BR-XXX**: rule. Reference `specs/glossary.md` for terms; do not redefine.

## Acceptance criteria
- **AC-XXX** — Given …, when …, then … (testable; name the test if it exists).

## Edge cases
- Boundary conditions, simultaneous events, idempotency.

## Error behavior
- What can fail and what happens.

## Non-functional requirements
- Reference NFR IDs (determinism, performance, …).

## Security requirements
- Reference SEC IDs or state "none beyond product-level".

## Observability requirements
- Logs/metrics/traces, or "none (client-only)".

## Out of scope
Explicitly excluded behavior.

## Open questions
Unresolved product decisions. Do not encode answers silently in code.
