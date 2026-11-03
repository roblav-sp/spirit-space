# AI Task Context Pack — <task id>

> Fill this before starting an AI-assisted task (see ai-development-guide.md).
> Keep the pack under ~10k tokens total.

## Task
TASK-XXX-NN from `tasks/<feature>.md` — one-line objective.

## Documents loaded
- [ ] `constitution.md`
- [ ] `specs/glossary.md`
- [ ] `specs/features/<f>/spec.md`
- [ ] `plans/<f>.md`, `tasks/<f>.md`
- [ ] Relevant contracts: …
- [ ] Relevant ADRs: …

## Source files in scope
- `path/file.go` — what will change there

## Requirements touched
FR-…, BR-…, AC-…

## Constraints checklist
- [ ] No DOM imports in `internal/game` (Law 5)
- [ ] No wall-clock/global RNG in simulation (Law 2)
- [ ] stdlib only (Law 6)
- [ ] All movement multiplied by dt (Law 4)

## Verification
- [ ] `gofmt -l .` empty
- [ ] `go vet ./...` clean
- [ ] `go test ./...` pass
- [ ] WASM build succeeds
- [ ] Traceability updated
