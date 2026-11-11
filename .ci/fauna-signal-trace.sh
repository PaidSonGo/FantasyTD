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
  # Native user call sites help distinguish a runtime abort from an external killer.
  for option in userstacktrace sym-userobj sym-addr; do
    echo 1 | sudo -n tee "$trace/options/$option" > /dev/null || true
  done
  echo 1 | sudo -n tee "$trace/events/signal/signal_generate/enable" > /dev/null
  echo 1 | sudo -n tee "$trace/tracing_on" > /dev/null
  # At most 2 MiB; only SIGKILL events are enabled in this separate instance.
  # Snapshot the ring at stop, rather than terminating a buffered trace_pipe reader.
  # Keep the native mapping of short-lived Editor processes for symbol lookup.
  sudo -n nohup python3 "$(dirname "$0")/fauna-ci-diagnostics.py" native-maps --out "$out" > "$out/native-maps-monitor.log" 2>&1 < /dev/null &
  # Verify the trace with an owned, disposable sleep process, not with Unity.
  sleep 60 &
  victim=$!
  echo "control SIGKILL target host pid=$victim" > "$out/signal-control.txt"
  kill -KILL "$victim"
  wait "$victim" 2>/dev/null || true
  sudo -n head -c 2097152 "$trace/trace" > "$out/signal-control-trace.txt"
  if ! grep -q "pid=$victim " "$out/signal-control-trace.txt"; then
    echo '::error::SIGKILL trace failed its disposable process control; do not start Unity'
    exit 1
  fi
  touch "$out/signal-tracing-enabled"
  echo '::notice title=Fauna SIGKILL tracing::Control verified; sender/target and native stack tracing enabled'
elif [ "$mode" = stop ]; then
  touch "$out/stop-native-maps"
  if [ -f "$out/signal-tracing-enabled" ]; then
    echo 0 | sudo -n tee "$trace/tracing_on" > /dev/null
    sudo -n head -c 2097152 "$trace/trace" > "$out/sigkill-trace.txt"
    echo 0 | sudo -n tee "$trace/events/signal/signal_generate/enable" > /dev/null
  fi
else
  echo 'Expected start or stop' >&2
  exit 2
fi
