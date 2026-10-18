# MindIE Agent Engineering Design Principles & Guidelines

[中文](design-principles.md) · [Back to Documentation Center](README.en.md)

MindIE Agent is built with a single goal: **make general-purpose AI coding agents genuinely effective, effortless, and unobtrusive for Ascend NPU and LLM inference engineering.**

Starting from nine foundational product and boundary principles, our engineering guidelines have evolved through real-world Ascend troubleshooting, cross-platform support (macOS, native Windows, Windows WSL), and multi-host integration (Claude Code, OpenAI Codex CLI, Kimi Code, DeepSeek Harness) into a comprehensive set of product and operational rules.

---

## Part 1: Nine Core Product & Tool Boundary Principles

These nine principles define what should be a tool, what should be a Skill or knowledge package, and how to minimize friction for both humans and Agents:

1. **Measure efficiency by the total cost of achieving the user's real goal (Top Priority)**
   - Total cost includes **understanding, configuration, waiting, debugging, and rework**—not just raw execution time.
   - Reliability mechanisms are worthwhile only when they reduce these real costs. Never burden every everyday task with heavy ceremony just to guard against rare edge cases. When other considerations conflict with this rule, Principle 1 wins.
2. **Turn only well-bounded, closed problems into tools**
   - A tool must have clear preconditions, inputs, outputs, and failure modes (e.g., reading a remote file, querying live NPU telemetry, or redacting secrets).
   - Leave open-ended, context-dependent judgment to the Agent; extract only repeatable, deterministic operations into stable tools, and never expand scope just for the sake of building a tool.
3. **Never increase cognitive load for the Agent or the user (Single Unified `/mindie-agent` Entry)**
   - From the user's perspective, every interaction and setting is wrapped inside a single unified entrypoint: **`/mindie-agent`**. Users should never have to learn or type internal subcommands such as `/mindie-agent:init`, `/mindie-agent:status`, or long flag strings—they simply use `/mindie-agent` with natural language, and internal state routing is handled behind the scenes.
   - A CLI that forces users to memorize subcommands, exposes tangled internal state, or requires reading source code to understand an error is a classic anti-pattern.
4. **Give every tool a single, well-defined boundary**
   - Each tool should solve one cohesive problem. It can execute the necessary multi-step mechanics internally so the Agent does not have to micromanage every step, while avoiding monolithic "kitchen-sink" tools that mix unrelated responsibilities.
5. **Skills provide a map and practice Progressive Disclosure, not a straitjacket**
   - Keep the top-level Skill concise and focused on core troubleshooting, knowledge lookup, and remote execution; place low-frequency setup wizards, historical import, and recovery details into secondary `references/` documents that the Agent loads **progressively on demand** only when relevant.
   - Concrete troubleshooting lessons belong in the Knowledge base rather than rigid step-by-step mandates inside a Skill.
6. **Knowledge is advisory reference material, never mandatory dogma**
   - Knowledge packages store applicability conditions, evidence, and caveats in plain Markdown. A search hit or merged PR never makes an entry infallible—decisions must always be grounded in the live behavior of the current system.
   - The Agent consults or records experience on demand, with **no mandatory lookups, mandatory writes, rigid fill-in-the-blank templates, or end-of-task closing rituals**.
7. **Manual on-demand activation for Knowledge & Skills; default auto-trigger for Remote Dev and Opt-In Experience Capture**
   - **Manual `/mindie-agent` trigger for Knowledge & Skills**: When troubleshooting Ascend issues, adapting operators, or tuning inference, the user explicitly types `/mindie-agent <problem description>`, keeping non-Ascend coding sessions clutter-free.
   - **Default auto-trigger for `remote-dev`**: Whenever a prompt involves remote servers, containers, or NPU commands, `remote-dev` tools intervene automatically in normal conversation.
   - **Automatic background experience loop after opt-in**: Once the user enables community contribution during installation or first-time setup, every subsequent session automatically captures, redacts, and packages experience on `Stop` in the background—**without the user ever needing to ask for it in their prompts**.
8. **Reuse proven host, OS, and ecosystem mechanisms first**
   - Whenever task semantics and compatibility requirements are met, reuse mechanisms already provided by the host CLI, operating system, `uv`, and mature libraries, as well as existing build artifacts and verified results.
   - Identify concrete gaps before writing custom code, keep custom glue minimal, and delete replaced legacy managers or duplicate state stores once a native mechanism is adopted.
9. **Keep tools observable and diagnosable; never hide errors**
   - Surfacing honest, actionable errors is a hard product requirement. When a required step fails, report it clearly—**never disguise a read failure as "empty data," a corrupted database as "first-time use," or a local save as "published."**
   - Clearly distinguish **completed**, **failed**, and **uncertain (`unknown`)** outcomes. If a primary operation succeeds but cleanup or bookkeeping fails, report both separately so the caller is never tricked into repeating a completed action.

---

## Part 2: Evolved Engineering & Operational Guidelines

As MindIE Agent matured across hosts and operating systems, we codified five operational guidelines extending Principles 8 and 9:

### 10. Build Only for Proven Gaps and Remove Legacy Baggage
- **Verify with lightweight probes first**: Before refactoring updaters, hooks, or process management, verify host and OS behavior (timeouts, cancellation, abrupt termination) using minimal model-free probes.
- **No dual-track state**: Once a replacement mechanism is verified, delete the superseded custom updater, duplicate state tables, and obsolete configs while preserving existing user Markdown packages, cursors, and consent settings.
- **Data-format-driven compatibility**: Before formal release, rewrite intermediate implementations cleanly without carrying multi-generation shims. After formal release, design compatibility around actual schema and contract changes rather than guessing from version strings.

### 11. Decouple User Consent from Code Installation Identity (Configure Once, Run Automatically Thereafter)
- **Configure once, active by default thereafter**: A user's contribution preference, public target repository, and authorized project scope are persistent user settings decoupled from the installed code revision. Once enabled, background capture and redaction run automatically at the end of every eligible task without requiring per-task user instructions.
- **No re-prompting or silent overrides**: Restarting sessions, reinstalling, or silently updating a plugin preserves existing consent and explicit disablement without re-prompting or silently turning disabled settings back on.

### 12. Paired Component and Plugin Releases
- **Release dependencies before plugins**: Every first-party runtime dependency pinned by a plugin (`diagnostics`, `remote-dev`, `knowledge`) must first have a published, non-draft, non-prerelease GitHub Release whose tag resolves to the exact locked commit and whose uploaded wheel/sdist artifacts match `uv.lock`.
- **Independent component versioning**: Each repository maintains its own version sequence and reuses unchanged Releases without artificial version bumps. See the [Paired Component and Plugin Release Checklist](release-compatibility-and-update.en.md#paired-component-and-plugin-releases).

### 13. Silent Background Updates with Atomic Idle Cutover
- **Compatibility-first selection**: Each plugin Release declares its verified Harness version range in `harness-compatibility.json` and automatically selects the highest compatible formal Release rather than chasing an unverified `main` branch.
- **Zero hot-path blocking**: More than 24 hours after the last successful check, natural usage triggers an asynchronous background check and runtime build; everyday tool calls perform only a fast local timestamp check.
- **Atomic cutover when idle**: After downloading and building the locked `uv` environment outside the active runtime, the updater waits until no active RPC, capture, or indexing job is running, acquires the exclusive lock, retires the old worker, and atomically switches the active installation binding without user prompts or manual session reloads. See [Release Compatibility & Silent Update](release-compatibility-and-update.en.md).

### 14. Fail-Visible Semantics, No Silent Fallbacks, and `unknown` Side-Effect Protection
- **No silent fallbacks or fake success**:
  - Never catch an exception and silently return `{}`, empty lists, skip corrupted state, or disguise a failure as `"status": "active"` / `exit 0`;
  - **Never let secondary bookkeeping overwrite primary success**: When a remote NPU command or core operation has already succeeded and returned valid output, a local SQLite receipt lock timeout or background grandchild pipe cleanup delay must preserve the primary result and attach a diagnostic warning—never flip a succeeded call to `isError = True`;
  - **Guard against exception hierarchy swallowing (`TimeoutError` $\subset$ `OSError`)**: Always handle `TimeoutError` explicitly before `except OSError:` in Python 3 so self-raised timeouts are never silently swallowed as generic file I/O errors.
- **Protect uncertain (`unknown`) external writes**: If a paid model call or external Git/PR write times out or loses its receipt, record it as `unknown` and reconcile read-only against the remote target before any future write—never blindly retry it as if it had not run.
- **Protocol safety never hides business faults**: A Hook may exit cleanly so the host model does not loop, but any underlying capture or service failure must still be surfaced through the host's warning field or the next tool call's diagnostic status.

### 15. Timeout Arithmetic Consistency & Anti Over-Defensive Programming
1. **Timeout Arithmetic Invariants**:
   - **Outer timeout must strictly exceed inner step budgets plus cleanup grace (`outer_timeout >= sum(inner_budgets) + cleanup_grace`)**:
     - Never wrap a `30s` inner command inside a `1.5s` `HOOK_TOTAL`, set local `STOP_DRAIN (2.0s) == remote STOP_GRACE (2.0s)` (failing locally at the exact millisecond `SIGKILL` is sent), or set verifier `deadline = timeout - 0.1s` without leaving time for `finally: inventory()` (which falsely triggers `UnknownExternalEffects`);
     - Multi-stage diagnostics (e.g., Stage 1 with SSH ControlMaster and Stage 2 bypassing ControlMaster) must have independent timeout budgets so a hung Stage 1 never starves Stage 2;
     - Never write `timeout 10 cmd || cmd` in shell scripts (when `timeout` exits with `124` on a hung driver, `||` immediately runs `cmd` without a timeout and hangs forever).
   - **Eliminate bimodal timeout extremes (no sub-second hot-path guillotines or unbounded `timeout=None`)**:
     - **No sub-second (`< 1s`) SQLite lock timeouts**: Multi-thread/cross-process SQLite locks must never use `100ms–250ms` micro-timeouts (which abort normal queries or permanently drop `Stop` session captures under normal indexing load); enable WAL mode and use `3.0s–5.0s` timeouts;
     - **No unbounded `timeout=None` on subprocesses or handshakes**: Every external subprocess (`gitleaks`, summary commands, candidate validation, `docker inspect/top` under host locks) must specify an explicit bounded timeout, and RPC handshakes (`ready.wait`) must be governed by `deadline` from function entry.
2. **Anti Over-Defensive Self-Bricking**:
   - **No one-way self-bricking state machines**: Recoverable config drift, transient upgrade slowdowns, or untracked scratch files (`git status --porcelain`) must never permanently lock the system into an unrecoverable `fault`/`suppressed` state or block valid container execution;
   - **No repetitive full-tree hashing or signature-reflection locks**: Never re-`stat` `.owner` on every `SELECT`, hash every `.so` file 3–4 times per task, lock internal function parameter defaults with `inspect.signature` in production probes, or copy-paste hundreds of lines of shadow `*_fallback.py` / `*_bootstrap.py` state machines across repositories.

### 16. Testing Design Guidelines: Eliminate Filler Tests, Embrace Tiered Live A2/A3 NPU Verification
See [Tiered Testing Architecture & Case Design Guidelines](testing-architecture.en.md) for the complete specification:
1. **Test Validity Redlines (Every Test Must Earn Its Keep)**:
   - **No defensive paranoia or prose-matching tests**: Never write tests that merely check Python types/defensive `ValueError` branches, repeatedly test `chmod 0o777`/`symlink` hypothetical attacks, assert static constant/enum string lists, or regex-grep `README.md`/`SKILL.md` prose;
   - **Never ratify silent error swallowing in tests**: Never write tests asserting that an underlying failure or timeout returns `exit 0` / `{}` / `"active"`;
   - **No production-script tampering or deceptive mocks**: Never overwrite production script files (e.g., replacing `admission_ops.py` with fake stubs) in integration tests or fabricate `MagicMock` objects that diverge from real server/hardware schemas.
2. **Four-Tier Testing Pyramid (Tier 0 – Tier 3, Default Standing A2/A3 Ascend NPU Environment)**:
   - **Tier 0 (Pure In-Memory Core Logic Unit Tests, `< 5s`)**: Zero subprocesses, zero network, zero `sleep`; covers parsers (backed by real A2 910B / A3 910C / A5 hardware Golden Captures), state-machine transitions (`InMemoryHostQueue` and real in-memory loops), redaction rules, domain retrieval precision/recall, and protocol translation.
   - **Tier 1 (Local Component Contract & Process Boundary Tests, `< 15s`)**: Reuses session-scoped pre-built Git/SQLite templates to verify cross-process locks, `python -I` isolated startup, and millisecond injectable timeout cleanup (never run network `pip install` or 10MB-scale `fsync` barrages inside tests).
   - **Tier 2 (Standing A2/A3 NPU Non-Destructive Live Integration `@pytest.mark.live_npu`, `< 25s`)**: Connects directly to the standing A2 (`173.125.1.2`) and A3 (`192.168.13.165` / `.156` / `.154`) clusters using isolated sandbox directories (e.g., `state_dir="/tmp/mindie-npu-test-<uuid>"`) without disturbing active workloads; routinely verifies live `npu-smi` probing, multi-Die `Phy-ID` mapping, Docker container pass-through, Linux `/proc` process-tree draining, and lease anti-preemption.
   - **Tier 3 (End-to-End Host CLI & `mindie-bench` Live Canary Acceptance, `< 90s`)**: Drives real host CLIs and `mindie-bench` Canary tasks to verify the complete loop.

---

## Part 3: Pre-PR Design Principles Checklist

Every development PR across all MindIE Agent repositories (covering code, configuration, dependencies, CI, and documentation) must review its final diff against these principles before submission:

| Dimension | Review Question |
|---|---|
| **1. Total Cost** | What real friction or cost does this change remove? Does it add unnecessary background work, repetitive full-tree hashing/IO checks, or extra user steps? |
| **2. Tool Boundary** | Is any toolified logic solving a closed, well-bounded problem rather than freezing open-ended judgment into a rigid flow? |
| **3. Cognitive Load** | Does the change keep internal state and parameters simple for both users and Agents? |
| **4. Single Responsibility** | Are module boundaries clean without cross-repo leakage, duplicate state stores, or copy-pasted `*_fallback.py`/`*_bootstrap.py` shadow state machines? |
| **5. Informational Skills** | Do Skills remain clear, helpful guides rather than mandatory procedural checklists? |
| **6. Advisory Knowledge** | Do knowledge entries and feedback remain advisory without mandatory lookups, writes, or truth certification? |
| **7. On-Demand Activation** | Does everything trigger strictly on demand without unrequested background work or closing rituals? |
| **8. Reuse & Paired State** | Were host/OS/mature tools reused first? Were replaced implementations deleted while preserving user data, consent, and `unknown` receipts? |
| **9. Error Visibility & No Silent Fallback** | Do failure paths report honest, actionable errors without `except Exception:` silent `{}` / `"active"` / `exit 0` fallbacks, `except OSError:` swallowing `TimeoutError`, blind retries of `unknown` writes, or local bookkeeping/cleanup timeouts overwriting succeeded remote results? |
| **10. Timeout Arithmetic & Bounds** | Do all new/modified timeouts satisfy **`outer_timeout >= sum(inner_budgets) + cleanup_grace` (e.g., `SIGTERM->SIGKILL` / `inventory` drain)**? Are sub-second (`<1s`) SQLite lock guillotines, unbounded `timeout=None` subprocess calls, pre-`deadline` handshakes, and `timeout N cmd \|\| cmd` re-runs eliminated? |
| **11. Anti Over-Defensive Self-Bricking** | Does the change avoid one-way unrecoverable `fault`/`suppressed` lockouts, git-dirty container rejection, `inspect.signature` parameter locks, or heavy hot-path paranoia checks? |
| **12. Tiered Test Validity** | Do new tests verify real business/domain quality rather than defensive `chmod`/`symlink`/`ValueError` paranoia, silent-fallback assertions, production-script tampering, or doc-grepping, while meeting Tier 0 (`<5s`) – Tier 3 budgets and live A2/A3 NPU rules? |

Include a concise `## 设计原则 Review` (Design Principles Review) summary in every development PR description documenting the reviewed commit, conclusions, fixes applied, and verification performed.
