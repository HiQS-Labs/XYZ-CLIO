# GH3 device collection and cutover handoff

Current milestone (2026-10-02): CLIO #5 and Rebalance #303 landed and the Studio is locally deployed with verified history/header/same-note preservation. Other Macs remain disabled; accepted historical gaps need no additional collection. Earlier collection notes below are historical. Use INSTALL.md and Rebalance #282 for current rollout gates.

PR4 landed; runtime installed. Cutover held on authoritative originals, lossless reconciliation of ten historical sections, and one shared-note publisher. Capture and ordinary IDE work continue. Do not activate SQLite or change the shared note while these remain unknown.

1. On each Mac, record the resolved CLIO source and any original JSONL archives. Copy them privately, preserving complete raw lines, unknown metadata and device identity. Include older MacStudio sources: the current JSONL alone cannot account for1,861 rendered IDs. MBP14 and MBP16 currently account for another170 and437 absent IDs. These labels are inventory hints, not proven origin UUIDs. Do not reconstruct omitted metadata from Markdown or commit snapshots to the Pulse repo before#282.
2. Inventory every writer of the shared note: its launchd label, exact ProgramArguments, interval, current state, manual/cron writers, and sync conflict siblings. Preserve plist/config/cursor/receipt files privately. The canonical MacStudio exporter remains com.claude.prompt-log-to-md at300 seconds. Do not run the installer’s new-job example over it.
3. Return readable private source locations and the publisher inventory to this session. Sources can be prepared with this read-only-to-live-data snippet on each Mac; it only creates a new private collection directory:

```python
from pathlib import Path
import hashlib, os, plistlib, time
root = Path.home() / 'Backups' / 'CLIO' / ('collection-' + str(time.time_ns()))
root.mkdir(parents=True, mode=0o700)
source = Path.home() / '.claude/prompt-log.jsonl'
raw = source.read_bytes()
assert raw and raw.endswith(b'\n'), 'Retry: source is empty or last append incomplete'
dest = root / 'prompt-log.jsonl'
fd = os.open(dest, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
with os.fdopen(fd, 'wb') as f:
    f.write(raw); f.flush(); os.fsync(f.fileno())
assert hashlib.sha256(dest.read_bytes()).digest() == hashlib.sha256(raw).digest()
for p in (Path.home() / 'Library/LaunchAgents').glob('*.plist'):
    job = plistlib.loads(p.read_bytes())
    args = job.get('ProgramArguments', [])
    if any('prompt-log-to-md' in str(a) for a in args):
        copy = root / p.name
        fd = os.open(copy, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'wb') as f:
            f.write(p.read_bytes()); f.flush(); os.fsync(f.fileno())
        print(job.get('Label'), args, job.get('StartInterval'))
print('Private collection:', root)
```

4. Import and verify every authoritative original into the privately staged DB. Account for duplicates, malformed/quarantined lines, pending receipts and every historical entry. Prepare an exact offline reconciliation diff preserving personal content and every section; reviewed migrate-view’s one-marker and full-payload guards stay intact. Rehearse cutover and rollback after new captures once those inputs exist.
5. Only when source coverage and the single publisher are proven, pause shared-note exporters immediately before replacement. Keep capture/tailers running except the bounded activation lock. For a confirmed launchd label the pause is `launchctl bootout gui/$(id -u)/com.claude.prompt-log-to-md`; verify it is unloaded. This instruction is preparation, not evidence any other Mac is paused. Manual/cron writers need their equivalent pause.
6. Complete online delta import and bounded activation using INSTALL.md; register the SAME installed destination with migrate-view --publishers-paused. Verify original note backup/hash, personal header, membership and full-history retention. Resume only the designated publisher using its unchanged plist and schedule. Other Macs continue capturing; their future complete sources must reach the publisher through the existing fleet mechanism after#282, not a new CLIO push loop. Do not resume old shared-note exporters behind the combined publisher.

Private-copy repair already restores the two currently missing local deliveries, but it does not solve the2,468 original-source gap or ten-section migration. No live note repair has been applied. The local runtime is installed and legacy publication continues with its intentional delivery-loss alarm.
