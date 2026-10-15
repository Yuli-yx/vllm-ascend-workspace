# Next steps

Updated 2026-10-15. Follow the [nine design principles](design-principles.md),
[architecture](architecture.md) and [lifecycle contract](harness-boundary-and-lifecycle.md).
The [0.0.1 release record](releases/0.0.1.md) owns the current candidate,
dependency pins, native matrix and release state. Earlier acceptance records
retain their exact version and operation boundaries.

The first release is an ordinary `v0.0.1` GitHub Release for internal testing,
without a beta suffix or prerelease flag. It includes Codex and Claude Code on
macOS and native Windows. It has not been published.

1. Complete the [root-cause investigation](releases/0.0.1-root-cause-review.md).
   Measure the actual Windows sync/query work before deciding which deadlines
   are wrong. Trace Codex Stop dispatch and Claude Code background ownership
   through the native boundaries. Preserve evidence that disproves a hypothesis.
2. Fix the demonstrated causes and adjacent affected paths. Refactor shared
   ownership or platform contracts when separate implementations have diverged.
   Do not substitute longer waits, retries or another owner for an unexplained
   failure. Retain caller cancellation and uncertain-effect receipts.
3. Verify each corrected path through the installed native product, including
   first and incremental capture/indexing. Reuse unchanged valid read and
   component evidence. Distinguish fixture failures, component tests, native
   events, real public delivery and independent consumption.
4. Complete publication preparation against the verified combination: reviewed
   changes, immutable source/dependency identities, install and state protection,
   release notes, and explicit remaining evidence gaps. Core failures remain
   blockers; elapsed preparation time does not lower the required behavior.

Component benefit and version-over-version benchmarks are independent of this
first release. Timing collected to diagnose a correctness or first-use failure
does not establish a benchmark or a quality/cost benefit.

Kimi, additional domains, automatic Skill extraction and old business Skills
remain outside this release. Ordinary tasks retain optional knowledge reads and
automatic capture governed by their saved choice and scope; they acquire no new
mandatory activation, reporting or closing workflow.
