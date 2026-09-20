# Repository layout and commit policy

This workspace has two kinds of content: reusable development infrastructure and local investigation state. Keep that boundary explicit so a fresh clone remains small, safe, and immediately useful.

## Tracked source of truth

| Path | Ownership | Commit policy |
| --- | --- | --- |
| `.agents/skills/<skill>/` | Canonical agent workflows | Commit the whole package: `SKILL.md`, scripts, references, agent metadata, and tests as applicable. |
| `.agents/lib/` | Shared workspace and VAWS libraries | Commit reusable, tested behavior that is not owned by one skill. |
| `.agents/scripts/` | Shared command entrypoints | Commit parameterized helpers; do not embed machine-specific defaults. |
| `.agents/tests/` | Cross-skill regression tests | Commit with the behavior they protect. |
| `.remote-dev/` | Generic remote-operation substrate | Commit code, schemas, tests, and design docs; never commit `state/` or local endpoints. |
| `.claude/`, `.cursor/`, `.trae/` | Tool integration | Prefer thin adapters that route to `.agents/skills/`; avoid copied implementations. |
| `docs/` | Repository-level design and maintenance docs | Commit stable architecture, contribution, and operational-policy documentation. |
| `vllm/`, `vllm-ascend/` | Upstream submodules | The workspace tracks only their gitlinks. Changes belong to their respective repositories. |

## Local-only areas

| Path | Purpose | Why it stays untracked |
| --- | --- | --- |
| `.vaws-local/` | Machine inventory, sessions, leases, job and service state | Contains host-specific mutable state. |
| `.remote-dev/state/` | Remote tool state and artifact manifests | Generated per endpoint and operation. |
| `.remote-dev/endpoints.local.json` | Developer endpoint inventory | May contain private hosts and user-specific paths. |
| `.worktrees/` | Isolated local checkouts | Generated and potentially large. |
| `experiments/` | Reproduction scripts, one-off patches, issue ledgers | Tied to a specific model, topology, version, or incident. |
| `artifacts/` | Logs, reports, benchmark output, snapshots, archives, captures | Generated evidence that is large and may contain environment details. |

## Promotion rule

Do not commit an experiment directory merely because one file in it is useful. Promote reusable work deliberately:

1. Identify behavior that applies beyond the original issue, machine, model, and date.
2. Remove IPs, credentials, personal paths, fixed device IDs, image-specific patches, and captured output.
3. Parameterize the remaining behavior and place it in the owning skill, shared library, or remote substrate.
4. Add usage documentation and focused regression coverage.
5. Keep the original evidence under `experiments/` or `artifacts/` for local traceability.

Examples of good promotion candidates include preflight checks, lifecycle helpers, exact-once cleanup, transport validation, and structured result parsing. Raw logs, runtime source snapshots, benchmark databases, packet captures, delivery archives, and issue-specific handoff documents are not promotion candidates.

## Commit boundaries

Prefer one independently reviewable behavior per commit. Documentation and tests for that behavior travel in the same commit. If one file contains unrelated changes, stage it by hunk instead of combining machine support, transport fixes, and process-lifecycle changes in one commit.
