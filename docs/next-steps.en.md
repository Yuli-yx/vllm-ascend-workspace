# MindIE Agent Roadmap & Next Steps

[中文](next-steps.md) · [Back to Documentation Center](README.en.md)

For the current system architecture and knowledge loop design, see [Architecture & Module Boundaries](architecture.en.md) and [Knowledge & Experience System](knowledge-system.en.md). All iterations follow the [Engineering Design Principles](design-principles.en.md).

Our initial [`0.0.1`](releases/0.0.1.en.md) release is live across six mainstream development environments (**Claude Code** and **OpenAI Codex CLI** on **macOS**, **native Windows**, and **Windows WSL**), alongside the formal [`mindie-agent-dsh`](https://github.com/mindie-agent/mindie-agent-dsh) `0.0.1` release.

Building on that foundation, **`0.0.2` completes our stack-wide "Anti Over-Defensive Programming & Four-Tier Live NPU Testing" refactoring across all 10 repositories while 100% preserving the `gpt6-astra` core architecture** (taking core business logic correctness as the sole baseline and directly deleting/rewriting unreasonable defensive imaginary-enemy checks and legacy shims):
- **Eliminated hot-path paranoia & local one-way self-bricking**: Removed per-`SELECT` SQLite `.owner`/Schema reflection checks, local upgrade/consent `suppressed`/`fault` self-bricking tombstones, and `TaskRootBusy` container rejections—retaining `unknown` receipt reconciliation strictly for irreversible external writes;
- **Removed cross-repo shadow state machines & reflection locks**: Deleted copy-pasted `*_fallback.py`/`*_bootstrap.py` shadow modules, Win32 ACL ceremonies, `inspect.signature` internal parameter locks, and giant inline Python strings (extracting `REMOTE_FILE_PY` into a standalone module);
- **Established the Tier 0 – Tier 3 Standing A2/A3 Live NPU Testing Pyramid**: Purged defensive `ValueError`/`symlink` filler tests and standardized non-destructive `@pytest.mark.live_npu` verification against standing A2 (`173.125.1.2`) and A3 (`192.168.13.165`/`.156`/`.154`) clusters.

---

## Current Engineering Priorities

1. **Real-World Engineering Benchmarks**
   - Using the streamlined `mindie-bench` harness verified on live A2 NPUs, run end-to-end benchmarks on real Ascend operator debugging, model migration, and inference tuning workloads to measure how much time and effort the experience loop saves in practice (we avoid making premature quantitative claims before benchmarks are complete).
2. **Broader Host & Domain Coverage**
   - **DSH Adapter Evolution**: Continue refining native entry, Stop capture/redaction/summary indexing, auto-fork contribution, feedback, and diagnostics in [`mindie-agent-dsh`](https://github.com/mindie-agent/mindie-agent-dsh) across platforms and live remote NPUs.
   - **Expand Standalone Skills**: Grow [`awesome-mindie-skills`](https://github.com/mindie-agent/awesome-mindie-skills) with additional ready-to-use workflows for Ascend profiling, accuracy verification, and kernel development.
3. **Upstream Host Issue Tracking**
   - Track upstream fixes in OpenAI Codex CLI for delivering cancellation signals to in-flight tool calls when a child agent (`spawn_agent`) is interrupted, updating our compatibility range once upstream ships the fix rather than adding intrusive process-hunting workarounds.
4. **Unified Remote Environment Management in `coordinator` (`coordinator` + `remote-dev` + `npu-top`)**
   - Agent-facing SSH host/key/mesh management (`mindie_hosts`), agentless Ascend NPU/server/mount probing (`mindie_probe`), container binding/provisioning (`mindie_container`), and lightweight NPU/port lease coordination (`mindie_lease`) are now unified in [`coordinator`](https://github.com/mindie-agent/coordinator) with automatic `machines.json` -> `remote-dev` `endpoints.json` bridging, while [`npu-top`](https://github.com/mindie-agent/npu-top) focuses purely on the human-facing Web dashboard and 90-day utilization heatmaps.
5. **Keep Everyday Workflows Zero-Ceremony**
   - Maintain a frictionless experience—one-sentence Agent-native installation, zero daily activation commands, and silent background updates—so developers can focus entirely on Ascend engineering.
