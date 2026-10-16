# Next steps

Updated 2026-10-16. Follow the [nine design principles](design-principles.md),
[architecture](architecture.md) and [lifecycle contract](harness-boundary-and-lifecycle.md).
The [0.0.1 release record](releases/0.0.1.md) owns the released source identities,
dependency pins, native matrix and release state. Earlier acceptance records
retain their exact version and operation boundaries.

The first release is an ordinary `v0.0.1` GitHub Release for internal testing,
without a beta suffix or prerelease flag. Its six environments are Codex and
Claude Code on macOS, native Windows and Windows WSL. The release record
separately identifies installed native evidence, later source deltas, actual
merged commits and each repository's publication state. This page does not
infer publication of the architecture repository from an adapter Release.

1. Follow the [paired-release checklist](release-compatibility-and-update.md#组件与插件配套发布):
   publish first-party runtime dependencies before plugins, preserve independent
   component versions, and match every release tag to the exact commit in the
   plugin lock. Reuse unchanged releases. Check reviewed notes, ordinary Release
   flags and downloaded package hashes. Follow the release record rather than treating
   historical pending rows as new work. Preserve original failures and the
   corrected-fixture boundaries in the
   [root-cause review](releases/0.0.1-root-cause-review.md).
2. Track the accepted Codex child-cancellation issue upstream. A child interrupt
   may leave a pending helper/SSH operation or an already-started remote command
   running. Acceptance for 0.0.1 is not proof of repair or wider Harness support.
   Do not add a compensating watcher, arbitrary business deadline or private
   Harness distribution. Durable remote jobs retain their own lifecycle.
3. Evaluate future fixes against their actual changes and exact supported
   Harness versions. Reuse unchanged native, body/index and public-delivery
   evidence; do not replay failed or uncertain paid work. New failures remain
   visible and are not covered by the accepted child-cancellation limitation.
4. Pursue component benefit and version-over-version benchmarks as a separate
   track, with explicit workloads and measured results rather than first-release
   reliability timings.

Timing collected to diagnose a correctness or first-use failure does not
establish a benchmark or a quality/cost benefit.

Kimi, additional domains, automatic Skill extraction and old business Skills
remain outside this release. Ordinary tasks retain optional knowledge reads and
automatic capture governed by their saved choice and scope; they acquire no new
mandatory activation, reporting or closing workflow.
