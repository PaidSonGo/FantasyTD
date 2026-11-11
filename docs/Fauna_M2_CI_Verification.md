# Fauna M2 — Unity verified, new APK published

**Status: APK_BUILT_UNVERIFIED** — compilation, tests, scene/build dependencies and actual APK contents verified; physical Quest3 runtime remains untested.

## Exact source and completed runs

- Unity PR: https://github.com/PaidSonGo/Unity/pull/10
- Exact Unity/PR10 HEAD: `1ec67f586a3eeca9466fa429bb640b365f90c6ee`. **No Unity source change during this CI repair.** The new HUD/wrist, rewards1of3, instincts, six mutations, original models, TouchPlus mappings, camera/XROrigin and LivingRun remain intact.
- CI PR: https://github.com/PaidSonGo/FantasyTD/pull/41. Both existing branches reused; no new branch, merge or force-push.
- [Full licensed workflow43100909842](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100909842): **completed SUCCESS**.
- Executed main CI revision: `ba21a84e7f56c2d61271ea70cf54cca9d7030047` (includes the permission/publication fixes below). This is the FantasyTD workflow revision, not the Unity game SHA.
- Unity **6000.6.0f1**; official `unityci/editor:ubuntu-6000.6.0f1-android-3`, digest `sha256:847eb830373fa73946fb3e41a97e54fbcb25fff70b4ddaf7b8ccff6b5cd61169`; supported Ubuntu22.04 host. No Unity/package upgrade or RAM/swap/ASLR change.
- [Compile + full EditMode job130791866760](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100909842/job/130791866760): **387 PASS /0 FAIL**,42.962s, cold import, including **24/24 M2Interface** and **5/5 M2 scene** cases. The external TestResults check is neutral but explicitly reports387/387 passed; the actual test job and workflow are SUCCESS. [Actual XML/log artifact13892046899](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100909842/artifacts/13892046899).
- [Android job130796265583](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100909842/job/130796265583): **SUCCESS, no failed steps**, including diagnostic reporting and both uploads. Unity reports `QUEST_BUILD_RESULT Succeeded errors=0 warnings=18`. Warnings remain in the real logs; they were not hidden or confused with test failures.
- Scene `Assets/_Project/Scenes/M2LivingReserve.unity`; `QuestBuild.BuildM2Apk`; Android IL2CPP/ARM64, minSdk32; `QUEST_VALIDATION ok` and `QUEST_MANIFEST ok`.

## Actual downloadable APK and independent inspection

**[Download the new APK artifact13894020998](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100909842/artifacts/13894020998)** — `FaunaVsKosmici-Quest-apk`, containing the actual `FaunaM2Sandbox.apk`. Standard14day artifact retention.

- APK file size: **73,363,572 bytes**.
- Actual APK SHA256 (computed in build job and independently after download):
  `a865ec89f8fdec85076867b4c76876ede5214ff6e498876569674a98b00d870b`.
- Artifact ZIP size:67,338,338 bytes. ZIP digest — **not** the APK digest:
  `sha256:db85c886bf0c36be8746a2e079289424bc852ce98caad7d108fe7b7754a19653`.
- [Independent existing-artifact inspection43105609603](https://github.com/PaidSonGo/FantasyTD/actions/runs/43105609603), job130808023211: **completed SUCCESS**. It downloaded the real published APK on a GitHub runner; it did not start Unity or rebuild the game. Inspector revision `f8c082c60a094ec3093125221c19f60642cb0295`.
- ZIP CRC valid; namespace **`com.paidsongo.faunam2sandbox`**; only ABI **arm64-v8a**; actual `lib/arm64-v8a/libil2cpp.so` present.
- Actual OpenXR libraries: `lib/arm64-v8a/libUnityOpenXR.so`, `lib/arm64-v8a/libopenxr_loader.so`.
- aapt verified required `android.hardware.vr.headtracking` and launch category `com.oculus.intent.category.VR`.
- The inspector checksum exactly matched the build job checksum. No old385/385 or363/363 APK is presented as the current build.

## What was actually tested

The real Unity tests generate the169cell M2 scene and validate its one XR Origin, model prefabs, input bindings, scene and build dependencies. Existing defended/undefended scenarios exercise the three-day LivingRun, placement and attacks, three rewards and one atomic choice, day2 evolution/instinct/mutation, day3 win/loss and restart.

The24 UI cases cover five animal choices and real DNA costs, tool/card updates, legal/illegal targets, previews without spending resources, DNA/energy refusals, quick categories/recent slots, right-ray menu events, remembered A target and carried animals, reward cards and duplicate confirmation, instinct alternatives/cancellation/insufficientDNA, mutations and slots, numbered cells, HUD phases/tutorial and reset. These are automated **Unity EditMode scenarios**, not physical Quest tests or a claim about first-time-user ergonomics.

Local CI-adapter boundary tests: **7/7 PASS**, separate from the387 Unity tests. They cover true success, Editor137, failed report, nonzero errors, missing APK, license-only invocations and preservation of the caller's child umask. The umask regression was red before its fix and green afterward. Bash syntax, Python3.10-compatible inspector snippets, YAML, strict core gates, artifact order/timeouts and git diff checks passed.

## Focused CI changes and evidence

| Commit / run | Finding and resulting change |
|---|---|
| Claude `23a6d2ba3febfe21b78df8f8f0bf23fc6a1cbd7a` | Preserved fix: call pinned CLIv0.1.73 installer through bash; Git100644 previously caused126. Installer actually passed in the real Android jobs. |
| `f4f44446466209cc40b0f2402522c171ed693ff0`, [43082906419](https://github.com/PaidSonGo/FantasyTD/actions/runs/43082906419) | Kernel signal trace established **Unity's main thread sent SIGKILL to its own PID3623**, code0. Last sampled peak~0.85GB/cap15.92GB and zero OOM counters. No CLI kill/timeout caused that observed event. |
| `441d0883f399fa6fa617a6143b5789b842db8d6b`, [43084277016](https://github.com/PaidSonGo/FantasyTD/actions/runs/43084277016) | Pin supported Ubuntu22.04 instead of ubuntu-latest26.04. Restored Library still failed; OS pin alone was **not** the fix. |
| `758573c71f18f5b9bb1652e2c2b5d8060a4daa3a`, [43086150449](https://github.com/PaidSonGo/FantasyTD/actions/runs/43086150449) | Disable Library restore in both jobs. Clean tests387/387 and separate clean Android build Succeeded0errors. CLI then falsely rejected the custom report and skipped upload. |
| `ff5a5528d4c5072579e0316032a4e7bd4a071882`, [43092132765](https://github.com/PaidSonGo/FantasyTD/actions/runs/43092132765) | Strict ENGINE_LAUNCH_WRAPPER adapter emits the official parser's result banner only after real QuestSucceeded/zero errors, Editor exit0 and expected APK>0. CLI build and APK CRC/ARM64 gate both passed. Its global umask077 was an unintended regression I introduced; the recovered log confirmed PermissionError reading a shadercompiler log. |
| Same previous run; failed publication | Both uploads exhausted5 attempts because **CreateArtifact returned HTML <!DOCTYPE instead of JSON**. A read-only log collector had GitHubstartup_failure; its pinned-host retry [43098571631](https://github.com/PaidSonGo/FantasyTD/actions/runs/43098571631) got HTTP502 from a GitHub runner. These were distinct from the file-permission error and from Unity compilation. |
| `1e33ada3a6d9360dce7bf50655a3f8e74f84d3db` | Preserve child permissions (mktemp log remains private), tolerate unreadable optional logs with a notice, publish primary test/APK evidence first, bound optional diagnostic uploads to3min. Core compilation, nonzero test count, APK CRC/ARM64 and mandatory APK upload remain strict. Verified end to end in43100909842. |
| [Service-only probe43100584345](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100584345) | After those failures, a224byte **non-game** upload succeeded. Only then was one corrected full run dispatched; it became the successful published build above. No blind repeat against the known failed artifact API. |
| Helper `f8c082c60a094ec3093125221c19f60642cb0295` | Existing fauna-evidence workflow supports bounded old-job reads, tiny API probes and actual APK inspection without Unity. Inspector hash code supports the pinned Ubuntu22 Python3.10. Actual APK inspection passed. |

The restored-Library failure was intermittent; older restored starts also passed. The exact internal Unity function/triggering Library subtree was not isolated. Clean imports repeatedly passed, so the unsafe cache stays disabled. The kernel trace proves the SIGKILL sender, not the full reason inside Unity. [Related independent cache report](https://github.com/evenflow58/Dungeon-Keeper/issues/118) is context, not project-specific proof. Do not relabel historical137 as confirmed OOM or missing license.

The official CLI parser requires `Build succeeded!` or its `# Build results #` banner; the existing custom Quest method reports `QUEST_BUILD_RESULT Succeeded`, and the shell prints `Build succeeded` without the exclamation mark. The adapter preserves original failures and prints the required banner only with the strict successful-build evidence above. It does not modify game code or the official binary, skip tests, or turn failed core steps green.

## Limits and handoff

- Physical Quest3 **NOT TESTED**: install/launch, stereo/tracking, TouchPlus aiming/input, wrist/HUD readability in movement, camera/comfort, materials and measured72FPS. Status is not QUEST_SMOKE_TESTED or PRODUCTION_VERIFIED.
- Real rendered screenshots unavailable here: `graphicsDeviceType=Null`; UnityMCP SSE429. No illustration was substituted for a screenshot.
- The owner's parallel Linux Codex task can diagnose Unity Hub SigningIn, launch the exact source in local Unity6000.6.0f1 and perform real PlayMode/UI screenshots/Console QA. Keep it read-only in game/CI code to avoid conflicts. Local Hub login is independent of the working CI authorization.
- Claude next: read this report and the existing PR10/41; review the actual APK/source and reported warnings. No reason to rebuild the same source or recreate rewards/instincts/mutations/UI. Physical Quest validation remains for the owner's chosen next phase; camera changes are a separate task. No merge without explicit owner instruction.
- Both source and CI changes are committed/pushed. The shared handoff journal records final results and releases only Codex's reservation. Claude Terrain/Fx reservations and entries are preserved. **Codex stage ends after this verified delivery**, as requested.
- Repository is public; no paid service, license secret, billing, RAM/swap or ASLR setting was changed. FantasyTD/UnityProject and Claude game branches were untouched.

The older evidence below is historical, with a different Unity SHA; its APK is not the new M2 UI artifact.

## Historical verification before the UI work (363 tests)

This report concerns the external PaidSonGo/Unity project only. FantasyTD/UnityProject and its game are unchanged.

- Unity PR: https://github.com/PaidSonGo/Unity/pull/10
- Exact verified Unity commit: `50a361d8b4e8a79d30765f1e13ec9ee4f542495a`.
- Existing Unity branch: `codex/m2-playable-loop-20261111` (no new Unity branch).
- CI changes: https://github.com/PaidSonGo/FantasyTD/pull/41, isolated from Claude's CI branch.
- Workflow + diagnostic script revision actually executed: `add3d9cc54a8b01dfa372847ba5be2ae888d03c3`.
- Completed run: https://github.com/PaidSonGo/FantasyTD/actions/runs/43043907539 — **SUCCESS**.
- Unity 6000.6.0f1 compile + EditMode: **363 PASS / 0 FAIL**, 44.050 seconds of tests. Check `130605962232`.
- Quest APK job `130606189382`: **SUCCESS**, including builder, Require an APK, and artifact upload.
- APK artifact: https://github.com/PaidSonGo/FantasyTD/actions/runs/43043907539/artifacts/13867209176
- Artifact name: `FaunaVsKosmici-Quest-apk`; build name `FaunaM2Sandbox`, expected APK `FaunaM2Sandbox.apk`.
- Artifact ZIP size: 67,128,372 bytes. Artifact ZIP digest (not the APK file digest):
  `sha256:d6f49ab9e90dda16ac3b88c60e9c77b301ad343fa8be7117ce8b863fa1b906fb`.

## What actually ran

The real Unity EditMode suite generated the M2 scene and checked 169 cells, one XR Origin, model prefabs and
scene/build dependencies. The complete defended scene scenario covers day 1 placement/combat, three reward cards,
a single reward choice, day 2 evolution with exclusive instinct selection and implantation of the earned mutation,
day 3 victory, and restart. A separate scenario reaches defeat. Restart checks day, DNA, energy, animals/views,
mutation samples, alien DNA and rewards. Negative cases cover no DNA, invalid choice, cancellation without cost,
no mutation slot, duplicate mutations and repeated reward confirmation. Six mutation cases execute their real logic.

The Android build uses the same exact Unity SHA, `m2=true`, `QuestBuild.BuildM2Apk`, the existing Quest build guards,
and the existing licensed workflow. A successful Require APK step and the nonempty uploaded artifact establish that
an actual APK was produced. The APK was not installed or executed on physical Quest hardware during this work.

Local C# 9/.NET 8 logic tests: 268/268. These are supplementary to the Unity result, not a substitute for it.

## Exit 137 investigation

The owner supplied the earlier full-log finding: account activation succeeded after the machine-binding warning,
then Unity exited 137 before test completion. Therefore neither missing license nor game-test failure was established.
The missing-local-image message is normal Docker pull behavior, not proof of a failed download.

To obtain evidence without guessing, the existing workflow now explicitly pulls the exact Android image before
starting Unity, and records selected host/Docker/cgroup fields, Docker OOM/die events and available kernel OOM lines.
The report publishes bounded annotations readable through GitHub API, in addition to downloadable artifacts.
Container environments, command arguments, labels and credentials are not inspected.

Diagnostic run https://github.com/PaidSonGo/FantasyTD/actions/runs/43042265020 passed 362/362 on the then-current
Unity `c0d3f4901fce40a8d045b2810cba44fce6e7415b`. Host RAM about 16 GB, swap about 3 GB, 4 CPUs. Container RAM limit
15,920,529,408 B; combined RAM/swap limit 31,841,058,816 B; observed cgroup peak 8,468,103,168 B; oom=0, oom_kill=0.
Image pull and activation succeeded. The final Unity test run peaked at 7,184,224,256 B, likewise with zero OOM counters.

The final APK container exited 0, OOMKilled=false, with no Docker OOM event. Its final annotation has PID 0 after exit,
so it does not retain the last live cgroup peak; resource history remains in the diagnostic artifact:
https://github.com/PaidSonGo/FantasyTD/actions/runs/43043907539/artifacts/13869050668
The earlier test diagnostic artifact is also available in the run.

Image: `unityci/editor:ubuntu-6000.6.0f1-android-3`, verified digest
`sha256:847eb830373fa73946fb3e41a97e54fbcb25fff70b4ddaf7b8ccff6b5cd61169`.
About 73 GB disk remained after the final build. No paid runner/service or speculative memory/swap change was used.

**Historical cause remains unproven:** the earlier SIGKILL did not recur. Its exact origin cannot be reconstructed
from exit 137 alone without that ephemeral runner's OOM/kill telemetry. Current observations do not justify calling
it confirmed OOM. They do prove successful image pull, activation, compile/tests and APK generation in the new runs.

## Remaining verification and observations

- Physical Quest 3: installation/launch, stereo/tracking, Touch Plus bindings and aiming, sling/rescue interactions,
  wrist/HUD readability, camera/fade/comfort, materials, sustained 72 Hz. No physical-device or Play Mode PASS is claimed.
- The APK diagnostic log contains nonfatal AssetImportWorker assertions on `!AssetDatabase::IsAssetImportWorkerProcess()`.
  Builder, APK guard and artifact upload still succeeded. This observation is retained for later editor/package diagnosis;
  no package, camera, art or unrelated game changes were introduced to suppress it.
- Both PRs remain drafts. No PR was merged, no Claude branch overwritten, no new game mechanics added in stabilization.
