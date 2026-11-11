#!/usr/bin/env python3
"""Bounded resource evidence for Fauna CI. Never inspect container environments/credentials."""
import argparse
import glob
import json
import os
from pathlib import Path
import re
import subprocess
import time


def command(args, timeout=15):
    try:
        p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return p.stdout.strip() if p.returncode == 0 else 'unavailable (exit %s)' % p.returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 'unavailable (%s)' % type(exc).__name__


def read(path):
    try:
        return Path(path).read_text().strip()
    except OSError:
        return 'unavailable'


def snapshot():
    mem = {}
    for line in read('/proc/meminfo').splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            if key in ('MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree'):
                mem[key] = value.strip()
    containers = []
    ids = command(['docker', 'ps', '-aq', '--no-trunc']).splitlines()
    for cid in ids:
        if not re.fullmatch('[0-9a-f]{64}', cid):
            continue
        # Explicit allowlist: never serialize Config.Env, command arguments or labels.
        fmt = '{"id":"{{.Id}}","image":"{{.Config.Image}}","memory":{{.HostConfig.Memory}},"memorySwap":{{.HostConfig.MemorySwap}},"nanoCpus":{{.HostConfig.NanoCpus}},"pid":{{.State.Pid}},"exit":{{.State.ExitCode}},"oomKilled":{{.State.OOMKilled}}}'
        raw = command(['docker', 'inspect', '--format', fmt, cid])
        try:
            item = json.loads(raw)
        except ValueError:
            continue
        pid = item['pid']
        if pid:
            for line in read('/proc/%s/cgroup' % pid).splitlines():
                if line.startswith('0::'):
                    cg = Path('/sys/fs/cgroup') / line[3:].lstrip('/')
                    item['cgroup'] = {n: read(cg / n) for n in ('memory.max', 'memory.swap.max', 'memory.current', 'memory.peak', 'memory.events')}
        containers.append(item)
    return {'time': time.time(), 'memory': mem, 'disk': command(['df', '-h', '/']), 'containers': containers}


def notice(title, value):
    text = str(value).replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
    print('::notice title=%s::%s' % (title, text[:5000]), flush=True)


def monitor(out):
    out.mkdir(parents=True, exist_ok=True)
    # Keep OOM/die events even when GameCI removes the container before the post-step.
    with (out / 'docker-events.jsonl').open('w') as events:
        child = subprocess.Popen(['docker', 'events', '--filter', 'event=oom', '--filter', 'event=die',
                                  '--format', '{"time":{{.Time}},"action":"{{.Action}}","id":"{{.Actor.ID}}"}'], stdout=events, stderr=subprocess.DEVNULL)
        try:
            with (out / 'resources.jsonl').open('a') as stream:
                while not (out / 'stop').exists():
                    stream.write(json.dumps(snapshot()) + '\n')
                    stream.flush()
                    time.sleep(3)
        finally:
            child.terminate()
            child.wait(timeout=10)


def report(out, workspace):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'stop').touch()
    final = snapshot()
    notice('Fauna host resources', json.dumps(final['memory']) + ' disk=' + final['disk'])
    rows = []
    if (out / 'resources.jsonl').exists():
        for line in (out / 'resources.jsonl').read_text().splitlines():
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    seen = {}
    for row in rows + [final]:
        for c in row['containers']:
            previous = seen.get(c['id'], {})
            if 'cgroup' not in c and 'cgroup' in previous:
                c['cgroup'] = previous['cgroup']
            seen[c['id']] = c
    for c in seen.values():
        notice('Fauna Docker limits and cgroup evidence', json.dumps(c))
    events = read(out / 'docker-events.jsonl')
    notice('Fauna Docker OOM/die events', events[-4000:])
    start = int(rows[0]['time']) if rows else int(time.time())
    kernel = command(['sudo', '-n', 'journalctl', '-k', '--since', '@%s' % start, '--no-pager'])
    oom = [line for line in kernel.splitlines() if re.search(r'out of memory|oom-kill|Killed process|memory cgroup', line, re.I)]
    notice('Fauna kernel OOM evidence', '\n'.join(oom[-12:]) or 'No matching kernel entries; absence alone does not establish the cause of SIGKILL.')
    logs = []
    for pattern in ('test-results/**/*.log', 'unity/Logs/**/*.log', 'build/**/*.log'):
        logs.extend(glob.glob(str(workspace / pattern), recursive=True))
    errors = []
    phases = []
    for name in logs:
        for line in Path(name).read_text(errors='replace').splitlines():
            if re.search(r'error CS\d+|Compilation failed|Scripts have compiler errors|SIGKILL|out of memory|fatal error', line, re.I):
                errors.append(line[:900])
            if re.search(r'Start importing |Importing asset|RefreshInfo:|AssetImportWorker|Test Run Summary|Build completed|M2_UI_RENDER_|M2_UI_FONT', line):
                phases.append(line[:500])
    for line in errors[-12:]:
        notice('Fauna Unity failure evidence', line)
    notice('Fauna last Unity phases', '\n'.join(phases[-8:]) or 'No phase markers in available Unity logs.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['monitor', 'report'])
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--workspace', type=Path, default=Path.cwd())
    args = ap.parse_args()
    if args.mode == 'monitor':
        monitor(args.out)
    else:
        report(args.out, args.workspace)
