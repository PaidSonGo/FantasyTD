# Fauna M2 UI — stage closed, handed to Claude; APK blocked

## Wynik etapu i przekazanie Claude

Na prośbę właściciela **etap Codex zakończony i przekazany Claude**. Brak dalszych prób CI lub zmian kodu po tym raporcie. PR-y niescalone.

- Dokładny Unity SHA: `1ec67f586a3eeca9466fa429bb640b365f90c6ee`.
- Unity **6000.6.0f1**: kompilacja, generowanie sceny/zależności i pełne EditMode **387 PASS / 0 FAIL**, w tym **24 nowe przypadki UI**. [Test job](https://github.com/PaidSonGo/FantasyTD/actions/runs/43077272338/job/130720379555).
- [Ostatni zakończony workflow](https://github.com/PaidSonGo/FantasyTD/actions/runs/43077272338) ma wynik **FAILURE w etapie instalacji CLI dla APK**, po zaliczeniu testów. Job `130723791167`, krok `Install the same pinned official GameCI CLI used by the test runner`, exit **126**. Krok budowania Unity i upload APK zostały pominięte.
- **Nowy APK dla tego SHA nie został wygenerowany.** Nie oznaczam pełnego celu builda jako ukończonego.
- Historyczny rzeczywisty APK nowego UI: [run 43064500956 / artefakt 13876781845](https://github.com/PaidSonGo/FantasyTD/actions/runs/43064500956/artifacts/13876781845), SHA `a33ac75e2b5de0d5b60cf1ad8e978bd42554cfdb`, 385/385. To wcześniejsza wersja, bez ostatniej poprawki zapamiętanego celu i komunikatu odmowy instynktu; **nie jest APK najnowszego SHA**.

## Konkretny bloker i następny krok

Oficjalna akcja `game-ci/cli@v0.1.73` wywołuje bezpośrednio `install.sh`, lecz zarówno ten plik, jak i `scripts/install.sh` mają w repo tryb Git **100644**. Lokalne odtworzenie bezpośredniego wywołania daje `Permission denied`, exit126. To błąd instalacji narzędzia, przed Dockerem/Unity; nie błąd gry ani brak sekretów.

Claude: zmienić wyłącznie instalację CLI na uruchomienie `bash scripts/install.sh` z pobranego, przypiętego źródła albo na pobranie i rozpakowanie przypiętego archiwum po weryfikacji sumy. Archiwum `game-ci-linux-x64.tar.gz` z wydania v0.1.73 zostało lokalnie pobrane i sprawdzone: SHA256 `3d4cc79952121ea46173d4d1eb8f2b6c6bcc866191489ec754e1511ab90d2fcd`. Nie przywracać `--version` w komendzie build (kolizja globalnego przełącznika); obecne argumenty `--versioningStrategy None` i reszta opcji przeszły lokalną walidację parsera.

Następnie jeden kontrolowany przebieg z pełnym SHA powyżej. Kod UI jest już zweryfikowany; nie implementować go ponownie. Jeśli SIGKILL powróci po uruchomieniu Unity, ustalić nadawcę sygnału i stan runnera, bez automatycznego nazywania go OOM. Wcześniejszy builder137 wystąpił przy przeładowaniu bibliotek, peak2,79GB/limit15,92GB, oom=0/OOMKilled=false. Dane nie ustalają przyczyny historycznego137.

Alternatywa kompilacji: lokalny licencjonowany Editor **6000.6.0f1 z Android module**, checkout dokładnego SHA, `LaneDefense.EditorTools.QuestBuild.BuildM2Apk` (menu M2 Build Quest APK lub batchmode `-buildTarget Android -executeMethod ... -customBuildPath <...>/FaunaM2Sandbox.apk`). Nie korzystać z płatnych usług bez zgody.

## Granice weryfikacji

Automatycznie sprawdzone: HUD każdej fazy, gatunki i koszty, legalne/zabronione i bezpłatne podglądy, DNA/energia, skróty i zdarzenie promienia, zapamiętany cel A, niesione zwierzę, trzy nagrody i pojedynczy odbiór, dwa instynkty/anulowanie/brakDNA, sześć mutacji/sloty, numerowane pola, instruktaż i restart. Istniejące testy sceny obejmują rzeczywistą symulację trzech dni, ataki, wygraną/przegraną i rozwój. Nie są to testy fizycznego urządzenia.

Brak zrzutów sceny: próba rzeczywistego renderowania zgłosiła `graphicsDeviceType=Null`, Unity MCP SSE429. Bez ilustracji udających screenshot. **Quest3/72FPS niezweryfikowane**: czytelność i nakładanie paneli w ruchu, zasięg nadgarstka/promienia, przyciski Touch Plus, uruchomienie/stereo/tracking i komfort. Problem kamery/XR Origin pozostaje osobnym zadaniem.

Infrastructure workflow revision: `0722e50019cd9382c51d58063d7d511e785121c4`. FantasyTD/UnityProject and Claude game branches unchanged. No PR merged, no paid service used, no speculative RAM/swap cap change.

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
