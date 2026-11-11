#!/usr/bin/env bash
# GameCI v0.1.73 parses its own reporter's text even after a successful custom build.
# Adapt only a successful Quest BuildReport + Editor exit 0 + a nonempty APK.
# License activation/return invocations have no Quest report and pass through unchanged.
set -uo pipefail
# mktemp creates a private 0600 log; preserve the caller's umask for Unity's
# generated files, which later host steps must be able to read.
log=$(mktemp /tmp/fauna-unity-build.XXXXXX)
trap 'rm -f -- "$log"' EXIT
"$@" 2>&1 | tee "$log"
status=("${PIPESTATUS[@]}")
if [ "${status[0]}" -ne 0 ]; then exit "${status[0]}"; fi
if [ "${status[1]}" -ne 0 ]; then exit "${status[1]}"; fi

if grep -q '^QUEST_BUILD_RESULT ' "$log"; then
  if ! grep -Eq '^QUEST_BUILD_RESULT Succeeded errors=0 warnings=[0-9]+ size=[0-9]+ path=.+$' "$log"; then
    echo 'Fauna CLI adapter: Quest BuildReport did not report success with zero errors' >&2
    exit 1
  fi
  apk="${GITHUB_WORKSPACE:?}/${BUILD_PATH:?}/${BUILD_FILE:?}"
  if [ ! -s "$apk" ] || [[ "$apk" != *.apk ]]; then
    echo 'Fauna CLI adapter: the reported build has no nonempty APK at its expected path' >&2
    exit 1
  fi
  printf '\n# Build results #\nErrors: 0\nSize: %s bytes\n\nBuild succeeded!\n' "$(stat -c %s "$apk")"
fi
