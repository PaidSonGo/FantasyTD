# Fauna M2 — publication verification after artifact-service recovery

## Current verification after a successful service probe

The tiny **non-game** artifact probe [43100584345](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100584345) completed SUCCESS, creating `fauna-artifact-api-probe`, artifact13892025629,224bytes. This confirms the same artifact API accepted a new upload after the HTML/502 failures; it is **not an APK or a game test**.

After verifying that no workflow was active, one corrected full run was dispatched: **[43100909842](https://github.com/PaidSonGo/FantasyTD/actions/runs/43100909842)**, exact UnitySHA `1ec67f586a3eeca9466fa429bb640b365f90c6ee`, `apk=true,m2=true`, executed CI revision `ba21a84e7f56c2d61271ea70cf54cca9d7030047`. It includes the umask repair and primary-artifact-before-optional-diagnostics policy. It is **IN PROGRESS**, not a delivery/verification success claim. The previous main run is completed FAILURE as documented below. No game code changed and no further build will be launched without a new diagnosed reason.

## Previous completed failure — 2026-11-11

**The delivery goal is NOT complete. There is no published APK artifact for the current source.**

- Unity / PR #10 HEAD remains exactly `1ec67f586a3eeca9466fa429bb640b365f90c6ee`. No game, camera, input, model, package or design changes were made during this CI repair.
- [Unity PR #10](https://github.com/PaidSonGo/Unity/pull/10), [FantasyTD CI PR #41](https://github.com/PaidSonGo/FantasyTD/pull/41); both drafts, no merge.
- Unity **6000.6.0f1**, full cold-import EditMode: **387 PASS / 0 FAIL**, **47.075 s** in [run 43092132765 / test job 130771694333](https://github.com/PaidSonGo/FantasyTD/actions/runs/43092132765/job/130771694333). This includes **24/24 UI** and **5/5 M2 scene** cases. [Real XML/log artifact](https://github.com/PaidSonGo/FantasyTD/actions/runs/43092132765/artifacts/13890415984).
- [APK job 130776291186](https://github.com/PaidSonGo/FantasyTD/actions/runs/43092132765/job/130776291186): **Build the licensed Quest APK with GameCI CLI — SUCCESS**. **Require an APK — SUCCESS**: the exact `build/Android/FaunaM2Sandbox.apk` existed and passed full ZIP CRC and ARM64 IL2CPP payload checks.
- The diagnostic report raised **PermissionError reading unity/Logs/shadercompiler-UnityShaderCompiler-0.log** (full log recovered after service recovery); diagnostic upload and APK upload then failed separately. No `FaunaVsKosmici-Quest-apk` artifact appears in either the run or repository artifact API. The run ultimately completed **FAILURE** at21:02UTC. Both upload failures report: **Failed to CreateArtifact: Failed to make request after5 attempts: Unexpected token '<', "<!DOCTYPE "... is not valid JSON**. This is the actual artifact-API failure, not an Editor compile failure. Do not present the workflow as green.
- Exact upload error text remains unavailable: the log connector returns `ReadTimeout`; a direct authenticated read follows GitHub to `productionresultssa3.blob.core.windows.net` and receives **403 Forbidden**, including with additional network access enabled. The APK checksum/manifest inspection could not be completed because no downloadable APK was published. Do not substitute the ZIP digest of the EditMode artifact for an APK digest.
- Read-only log collector [43097953722](https://github.com/PaidSonGo/FantasyTD/actions/runs/43097953722) ended **startup_failure**, with no jobs. GitHub's own run page says: **“An unexpected error has occurred and we've been automatically notified”**, suggests checking Actions service health, request ID `191d9c78-de11-11f1-8295-d4aaf349dec4`. This is not a YAML error or evidence of a license/game failure.
- One controlled read-only retry on pinned Ubuntu22.04, [43098571631](https://github.com/PaidSonGo/FantasyTD/actions/runs/43098571631), completed **FAILURE**. Its actual runner log says **gh: Server Error (HTTP502)** while fetching the main job log (job130784287897,20:57:25UTC). Thus log retrieval also fails from a GitHub-hosted runner, not just this workspace. It did not start Unity or cancel the main run. No further Unity build was dispatched.

Status: **UNITY_TESTED / ANDROID_BUILD_SUCCEEDED / ARTIFACT_UPLOAD_FAILED / DELIVERY_BLOCKED / QUEST_UNVERIFIED**.

## Changes prepared after the successful build

The executed main workflow revision was `ff5a5528d4c5072579e0316032a4e7bd4a071882`. Its strict compatibility adapter removed the confirmed GameCI parser false failure. Its restrictive umask also propagated to Unity — an unintended regression I introduced. A new regression test failed with child umask0077 instead of0022, then passed after removing the global umask (mktemp itself already creates a private0600 log).

- Fix `1e33ada3a6d9360dce7bf50655a3f8e74f84d3db`: preserve child permissions; tolerate unreadable diagnostic log files with a notice; publish the primary APK/test evidence before optional resource archives; cap optional diagnostic uploads at3min and make only those diagnostics nonblocking. Compilation, test totals, APK CRC and mandatory APK upload remain strict.
- Read-only evidence runner `0181ba9ca216fa72e339441dc5091c1b373b2450`: pinned Ubuntu22.04,5min job limit; no Unity execution.
- **7/7 local CI-adapter tests passed** after the fix. Bash syntax, YAML/embedded Python AST, artifact ordering, timeouts, strictness of core gates, and git diff checks passed. These are CI fixture tests, not Unity or headset tests.
- The latest CI configuration has **not** completed an end-to-end verification run after these last fixes. After the service probe succeeded, the old full log became readable: it confirms PermissionError for the shadercompiler log at20:30:10UTC, followed by two separate CreateArtifact failures. The child-umask regression was independently reproduced before that log recovery and fixed. Do not conflate file permissions with the artifact API returning HTML. The same recovered log confirms QUEST_BUILD_RESULT Succeeded errors=0 warnings=14 and the adapter's Build succeeded! banner.
- FantasyTD is public. No paid runner/service, spending limit, license secret, RAM/swap cap or ASLR setting was changed.

## Best free compilation alternative

Use an already licensed **local Unity6000.6.0f1** with Android Build Support, its SDK/NDK/OpenJDK, on the owner's workstation. Use the **PaidSonGo/Unity root**, not FantasyTD/UnityProject. Verify that `git rev-parse HEAD` equals the full Unity SHA above and that no game changes are uncommitted. A clean clone avoids the restored-Library issue. This reuses the existing M2 generators/build guards; it does not recreate any game system.

Set `FAUNA_UNITY_EDITOR` to the real installed Editor executable, `FAUNA_PROJECT` to that checkout, and `FAUNA_OUTPUT` to an existing absolute output directory. Then run (POSIX shell syntax; the same Unity arguments work with Unity.exe in PowerShell):

```bash
"$FAUNA_UNITY_EDITOR" -batchmode -nographics -projectPath "$FAUNA_PROJECT" \
  -runTests -testPlatform EditMode -testResults "$FAUNA_OUTPUT/editmode.xml" \
  -logFile "$FAUNA_OUTPUT/editmode.log"

"$FAUNA_UNITY_EDITOR" -batchmode -nographics -buildTarget Android \
  -projectPath "$FAUNA_PROJECT" \
  -executeMethod LaneDefense.EditorTools.QuestBuild.BuildM2Apk \
  -customBuildPath "$FAUNA_OUTPUT/FaunaM2Sandbox.apk" \
  -logFile "$FAUNA_OUTPUT/android.log"
```

The first command must finish with nonzero executed tests and zero failures. The second must log `QUEST_BUILD_RESULT Succeeded`, exit0 and produce the actual nonempty APK. Check its manifest/ARM64/IL2CPP/OpenXR and SHA256 locally; do not rely on log wording alone. This path avoids GitHub's artifact service and the CLI reporter parser.

**Not executed here:** there is no local Editor binary in this workspace; UnityMCP get_active returns SSE429. Cloud browser access is unavailable, and connected local Browser tools were not callable. No local build, real screenshot, APK download or physical Quest test is claimed.

## Handoff / next action for Claude

1. Read the completed run43092132765 and its artifacts after GitHub recovers. The read-only collector43098571631 failed with HTTP502; do not repeatedly launch readers/builds against that unresolved backend failure.
2. If GitHub recovers a current APK artifact, inspect it via existing `fauna-evidence.yml`, `apk=true`, `run=43092132765` — no Unity rebuild. Verify actual filename, checksum, namespace, head-tracking/category and native binaries.
3. If uploads definitively failed and no artifact can be recovered, first resolve the actual GitHub upload/startup error (do not assume OOM, licensing, quota or payment), then perform one controlled full workflow from the current CI branch for the exact Unity SHA. All game/UI implementation is already present; do not recreate it.
4. Use the local licensed build alternative if Actions infrastructure remains unavailable. Quest3 ergonomics, input, camera/comfort, rendering and72FPS remain a separate physical test.

## Diagnosed failures and focused changes

| Run | Change / observation | Actual result |
|---|---|---|
| [43080679743](https://github.com/PaidSonGo/FantasyTD/actions/runs/43080679743) | Claude `23a6d2b` fixed the nonexecutable installer by calling the pinned script through bash. | Editor killed before tests; APK skipped. |
| [43082906419](https://github.com/PaidSonGo/FantasyTD/actions/runs/43082906419) | Host signal trace `f4f4444`. `Unity Main Thre-3623 … signal_generate: sig=9 code=0 comm=Unity Main Thre pid=3623`. | **Unity itself sent SIGKILL to its own PID.** Last sampled peak ~0.85 GB / 15.92 GB, OOM counters zero. No test executed. |
| [43084277016](https://github.com/PaidSonGo/FantasyTD/actions/runs/43084277016) | `441d088`: pin Unity jobs to supported Ubuntu 22.04 instead of migrating ubuntu-latest/26.04. Same Library restored. | Still failed at native Mono reload. OS pin alone did **not** fix startup. |
| [43086150449](https://github.com/PaidSonGo/FantasyTD/actions/runs/43086150449) | `758573c`: no Library restore in either Unity job; trace snapshot/control and native maps. | Fresh tests 387/387; separate fresh Android import + build **Succeeded, 0 errors, 14 warnings**. No Editor self-SIGKILL in either job. CLI post-build parser failed; APK upload skipped. |
| [43092132765](https://github.com/PaidSonGo/FantasyTD/actions/runs/43092132765) | `ff5a552`: strict report compatibility adapter plus exact APK/CRC/ARM64 guard and candidate retention. | Fresh EditMode **387/387 (47.075 s)**; CLI build **SUCCESS**; exact APK/CRC/ARM64 gate **SUCCESS**. Diagnostic reporting and both uploads failed; no APK artifact. Run completed FAILURE: artifact creation returned HTML instead of JSON after5 attempts. |

The restored-Library issue is intermittent: older restored starts also passed. The exact internal Unity call and triggering Library subtree were not isolated. Clean imports eliminated the reproduced early failure in both jobs of run 43086150449; the cache remains disabled. The kernel trace establishes the SIGKILL sender, not the reason inside Unity. [An independent related cache report](https://github.com/evenflow58/Dungeon-Keeper/issues/118) is corroborating context, not proof about this project.

The observed post-build failure is exact: CLI v0.1.73 `UnityBuildValidation.validateBuild` accepts `Build succeeded!` or its own `# Build results #` banner. Our existing custom builder reports `QUEST_BUILD_RESULT Succeeded …`; GameCI's shell prints `Build succeeded` without the exclamation mark. Unity exited 0, produced the file, and returned its entitlement license before the CLI threw its parser error.

`.ci/fauna-gameci-build-log.sh` uses the official `ENGINE_LAUNCH_WRAPPER` hook. It preserves Editor/tee failures and emits the parser's expected banner only when the Quest report says Succeeded/zero errors, the Editor exited 0, and the expected APK is nonempty. Activation/return calls cannot fabricate a build report. **7/7 local adapter boundary tests passed** (shell fixtures, not Unity tests), including exit137, failed report, nonzero errors, missing APK and license-only invocation.

The package step checks the exact M2 filename, ZIP CRC and ARM64 IL2CPP payload. It can retain a valid candidate after a post-build tool failure without turning the failed job green. Existing `fauna-evidence.yml` has an `apk=true` mode to download an existing artifact on a GitHub runner, check aapt manifest/package/VR head tracking and category, ARM64/IL2CPP/OpenXR, CRC and the actual APK SHA-256. That inspection never starts Unity or rebuilds the project.

Claude's installer fix is preserved and actually passed. No license secret, RAM/swap limit, ASLR setting, Unity version, package, gameplay, camera, controller binding or model was changed. No paid service was used.

## Verification limits

- The 387 tests cover the existing three-day run/win/loss/restart and progression, plus UI costs/refusals, five animal choices, quick slots, target/preview validity, three rewards/atomic confirmation, instincts/cancellation, mutations/slots, phase HUD and reset. These are automated Unity EditMode scenarios, not physical Quest tests.
- Real screenshots unavailable: Unity reported `graphicsDeviceType=Null`. No generated illustration was substituted.
- Quest 3 installation/launch, stereo/tracking, Touch Plus ergonomics, HUD/wrist readability, camera/comfort, materials and sustained 72 FPS remain unverified.
- Cold Android import emitted nonblocking AssetImportWorker/OpenXR initialization and shader-deprecation diagnostics. Main BuildReport still explicitly reported Succeeded, 0 errors and 14 warnings; retain these logs for later review rather than misidentifying them as the CLI parser failure.

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
