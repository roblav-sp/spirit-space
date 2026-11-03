# AI Development Guide — Spirit Space

> Practical guidance for AI coding agents (and humans pairing with them).
> Token sizes below are **approximate guidelines, not hard limits**.

## 1. Context pack

Load only what the task needs. Never load the whole repository.

| Task type | Load |
|---|---|
| Any task | `constitution.md` (≤1,200 tok) + relevant `specs/glossary.md` entries (≤800 tok) |
| Feature work | that feature's `specs/features/<name>/spec.md` (≤2,500 tok) + its `plans/<name>.md` (≤1,800 tok) + `tasks/<name>.md` (≤1,500 tok) |
| Architecture change | relevant `specs/architecture/*.md` (≤2,000 tok each) + affected ADRs (≤700 tok each) |
| Contract change | relevant `specs/contracts/*.md` + `internal/game` exported API |
| Any code task | the specific source files in scope (see plan) |

Typical context pack: constitution + glossary + one feature spec + one plan +
one task file + 1–3 source files. That is usually under 10k tokens.

## 2. Rules for large documents

- Split a document when it exceeds its size guideline **or** mixes two
  unrelated concerns — size is the symptom, cohesion is the rule.
- Split features along user-visible capabilities, not along code files.
- Keep tuning tables in the feature spec that owns them; reference, never copy.

## 3. Atomic tasks

A task in `tasks/<feature>.md` must:
- have a single verifiable objective and ID (`TASK-<feature>-nn`),
- reference the requirement IDs it implements,
- list files in scope and constraints,
- state expected tests and verification evidence,
- be completable in one focused session without inventing requirements.

Forbidden: "implement backend", "finish UI", "polish game".

## 4. Ambiguity

- If a spec is ambiguous or contradicts the code/constitution, **stop and
  report the conflict**. Do not choose silently.
- Mark assumptions explicitly in the spec (`> Assumption:`) rather than
  encoding them invisibly in code.
- Never invent business requirements. If a behavior isn't specified, ask or
  write an open question in the feature spec.

## 5. Traceability

- New behavior ⇒ new or updated `FR`/`BR`/`AC` IDs in the feature spec.
- Every PR/task references requirement IDs; every requirement maps to at least
  one test or is marked `TODO` in `specs/traceability.md`.

## 6. Reviewing AI-generated code

- Verify Law 5: no `syscall/js` or DOM imports in `internal/game`.
- Verify Law 2: no wall-clock or global RNG in the simulation.
- Verify the change matches the spec's acceptance criteria, not just "works".
- Check `gofmt`, `go vet`, `go test`, WASM build all pass before approval.

## 7. Verification before "done"

A task is complete only when all of these hold:
1. `gofmt -l .` → empty; `go vet ./...` → clean (native packages);
2. `go test ./...` → pass;
3. `GOOS=js GOARCH=wasm go build -o main.wasm ./cmd/game` → succeeds;
4. requirement IDs updated in spec and traceability matrix;
5. behavior demonstrated (unit test evidence, or manual run for UI-only).
