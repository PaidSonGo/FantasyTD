#!/usr/bin/env bash
# Runner-only evidence: sender/target process names and PIDs for SIGKILL, never argv/env.
set -euo pipefail
mode=$1
out=$2
trace=/sys/kernel/tracing/instances/fauna-ci
mkdir -p "$out"

if [ "$mode" = start ]; then
  if ! mountpoint -q /sys/kernel/tracing; then
    sudo -n mkdir -p /sys/kernel/tracing
    sudo -n mount -t tracefs tracefs /sys/kernel/tracing || {
      echo '::warning::Signal tracing unavailable: cannot mount tracefs'
      exit 0
    }
  fi
  if ! sudo -n mkdir -p "$trace"; then
    echo '::warning::Signal tracing unavailable: cannot create trace instance'
    exit 0
  fi
  sudo -n cat "$trace/events/signal/signal_generate/format" > "$out/signal-format.txt"
  echo 'sig == 9' | sudo -n tee "$trace/events/signal/signal_generate/filter" > /dev/null
  echo 1 | sudo -n tee "$trace/events/signal/signal_generate/enable" > /dev/null
  echo 1 | sudo -n tee "$trace/tracing_on" > /dev/null
  # At most 2 MiB; only SIGKILL events are enabled in this separate instance.
  sudo -n timeout 7200 head -c 2097152 "$trace/trace_pipe" > "$out/sigkill-trace.txt" &
  echo "$!" > "$out/signal-reader.pid"
  # Verify the trace with an owned, disposable sleep process, not with Unity.
  sleep 60 &
  victim=$!
  echo "control SIGKILL target host pid=$victim" > "$out/signal-control.txt"
  kill -KILL "$victim"
  wait "$victim" 2>/dev/null || true
  echo '::notice title=Fauna SIGKILL tracing::Enabled sender/target tracing; control target recorded'
elif [ "$mode" = stop ]; then
  if [ -f "$out/signal-reader.pid" ]; then
    echo 0 | sudo -n tee "$trace/tracing_on" > /dev/null
    echo 0 | sudo -n tee "$trace/events/signal/signal_generate/enable" > /dev/null
    sudo -n kill -TERM "$(cat "$out/signal-reader.pid")" || true
  fi
else
  echo 'Expected start or stop' >&2
  exit 2
fi
