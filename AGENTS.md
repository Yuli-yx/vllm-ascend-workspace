# MindIE Agent

This repository owns product architecture, domain boundaries, and entry documentation (`docs/`).
Native Harness plugins live in `mindie-agent-codex`, `mindie-agent-cc`, and `mindie-agent-kimi`.
Shared runtime components live in `knowledge`, `remote-dev`, `diagnostics`, `npu-top`, and `coordinator`.

## 1. Core Operating Rules (Always Active)

- **Repository Boundary**: This repo contains documentation and architecture assets only—no runtime bootstrap, MCP server, client hook, Skill catalogue, or dependency lock. Do not add legacy VAWS aliases or alter the user's unrelated skills, plugins, or MCP configurations.
- **Inner-Loop Efficiency (Principle 1 — Total Cost First)**:
  - Edit files directly in the active checkout and verify only the affected scope.
  - Never invent intermediate freeze steps, duplicate snapshot directories, or `readback.json`/`restoration.json`/`shadow.json` audit ceremonies during routine development.
- **Transparency & State Honesty (Principle 9)**:
  - Keep implementation status, target design, and real acceptance evidence distinct.
  - Errors must remain visible to the caller; distinguish `completed`, `failed`, and `unknown` external effects. Never mask a failure or blindly retry an uncertain external write.

## 2. Progressive Disclosure Map (Read Only When Triggered)

Do not preload all documentation into context. Read only the document matching your current task:

- **Architecture & Domain Boundaries** → [`docs/architecture.md`](docs/architecture.md)
- **9 Product & Engineering Principles** → [`docs/design-principles.md`](docs/design-principles.md)
- **Harness Plugin Boundary, Hooks & Lifecycle** → [`docs/harness-boundary-and-lifecycle.md`](docs/harness-boundary-and-lifecycle.md) & [`docs/native-runtime-reuse.md`](docs/native-runtime-reuse.md)
- **Knowledge Flywheel & Privacy Redaction** → [`docs/knowledge-system.md`](docs/knowledge-system.md)
- **Diagnostics & Issue Reporting** → [`docs/diagnostics-and-reporting.md`](docs/diagnostics-and-reporting.md)
- **Gate — Submitting or Updating a Development PR**:
  - Read and complete [`docs/design-principles.md#三开发-pr-提交前自查清单pre-pr-review`](docs/design-principles.md#三开发-pr-提交前自查清单pre-pr-review) before creating/updating any PR (including drafts), and include the concise review summary in the PR description.
- **Gate — Publishing a Formal Component or Plugin Release**:
  - Read and execute [`docs/release-compatibility-and-update.md#组件与插件配套发布`](docs/release-compatibility-and-update.md#组件与插件配套发布) only when publishing or auditing a formal GitHub Release.
