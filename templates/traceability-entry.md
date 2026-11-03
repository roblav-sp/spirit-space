# Requirement-to-Test Traceability Entry

> Add one row to `specs/traceability.md` per requirement.

| Requirement | Feature spec | Architecture element | Contract | Source | Tests | Status |
|---|---|---|---|---|---|---|
| FR-XXX | `specs/features/<f>/spec.md` | component/function | contract + guarantee ID | `path/file.go` | `TestXxx` / `TODO` | ✔ verified / **TODO** |

Rules:
- `Status` is `✔ verified` only when the listed test actually covers the
  requirement; otherwise `TODO`.
- Never invent file or test names. Manual verification is allowed but must
  say so.
