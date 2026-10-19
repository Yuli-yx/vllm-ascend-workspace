# Maintaining this fork

This fork follows [mindie-agent/mindie-agent](https://github.com/mindie-agent/mindie-agent).
The 2026-10-19 migration merges upstream `35c4917be78066307248b39e43c2942d5850e219`
and keeps the original workspace history reachable without restoring the retired
bootstrap, runtime, Skills catalogue or source submodules to the product tree.

## Where our existing work lives

- [`codex/legacy-workspace-20261019`](https://github.com/Yuli-yx/vllm-ascend-workspace/tree/codex/legacy-workspace-20261019)
  preserves workspace `c7f899d74a36d0d031f488a3d81bad49de2be724`, its two source
  submodules and all eight fork-specific commits. It is the maintenance branch
  for workflows that still require the old workspace layout.
- [`awesome-va-skills`](https://github.com/Yuli-yx/awesome-va-skills) owns our
  reusable skill packages and their legacy shared helpers. Build, AISBench
  accuracy, A5/sudo support, shell-byte preservation, process-group stopping and
  shared-host process/log ownership were already exported there. The migration
  additionally publishes `pd-pure-role-benchmark` with its complete package in
  [commit `8252175`](https://github.com/Yuli-yx/awesome-va-skills/commit/8252175).
- Local model source, machine inventories, endpoints, credentials, experiments,
  archives and runtime evidence remain local. They are not imported into this
  product repository. Changing the parent branch must not update or reset the
  business repositories' own branches or working trees.

## Disposition of the eight fork commits

| Commit | Preserved behavior | Maintenance destination |
| --- | --- | --- |
| `ad0a5e725` | Pinned vLLM/Ascend builds and runtime verification | `awesome-va-skills/.agents/skills/vllm-ascend-build/` |
| `d3ebb6d08` | AISBench accuracy contract and result accounting | `awesome-va-skills/.agents/skills/aisbench-accuracy/` |
| `ec29c3293` | A5 hardware and sudo-host support | Legacy branch and skill collection; evaluate future changes in `coordinator` |
| `66eb84567` | Binary SSH stdin and LF/BOM shell-upload checks | Legacy branch and skill collection; evaluate future changes in `remote-dev` |
| `0007040ed` | Stop a remote job's process group | Legacy branch and skill collection; evaluate future changes in `remote-dev` |
| `aee30b5db` | Keep experiments and runtime state out of Git | Retained as fork-local ignore rules and this maintenance policy |
| `f6dc62815`, `c7f899d74` | Host-visible process ownership and machine/role log labels | `awesome-va-skills/.agents/skills/vllm-ascend-serving/references/process-ownership.md` |

The old scripts are preserved implementations, not drop-in adapters for the new
component APIs. Do not add them back under `.agents/` or `.remote-dev/` in this
repository to resolve a future upstream merge.

## Component audit boundary

Static source inspection used `remote-dev@717ba46f538b445d7993263945bd80e40d81d689`
and `coordinator@b1673d0696073a419a94737631cb170c6b91adde`:

- `remote-dev/core/ssh_transport.py` already sends encoded bytes to SSH.
- `remote-dev/processes/worker.py` already tracks job descendants, including
  detached descendants, and delivers termination signals to owned processes.
- `mindie_coordinator/device_inventory.py` already recognizes Ascend 950/A5.

These observations avoid blindly replaying obsolete patches. They do not prove
runtime equivalence for shell-upload CRLF/BOM rejection, password-sudo
provisioning, A5 mounts/environment, or every cancellation mode. Those items
remain preserved in the legacy implementation pending focused component work
and authorized runtime validation. No new component fix is claimed by this
migration.

## Updating again

Fetch `upstream/main` and merge it into this fork's `main` without rewriting
published history. Keep the upstream product tree and lifecycle contracts.
Limit fork-local additions here to documentation and portable ignore policy;
maintain executable changes in their owning component or skill repository.

The migration uses a separate checkout for the new `main`. The original
workspace stays on the legacy branch with its pending edits, archives and
business source checkouts intact. Committed branch preservation does not
publish uncommitted local files or submodule changes.
