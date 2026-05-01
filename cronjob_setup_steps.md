# macOS Cron Job Setup — Step by Step

## Goal
Run a Python monitoring script automatically every day at 07:00 using macOS launchd.

## Steps

**1. Create a logs directory**
```bash
mkdir -p tiktok_monitoring/logs
```

**2. Improve run.sh with timestamp logging**
Added start/end timestamps and exit code to `run.sh` so every run is traceable in `logs/monitor.log`.

**3. Create a launchd plist file**
`com.tiktokmonitoring.plist` defines:
- what to run (`run.sh`)
- when to run (daily at 07:00 via `StartCalendarInterval`)
- where to write output (`logs/launchd_out.log`, `logs/launchd_err.log`)

**4. Install the plist**
```bash
cp com.tiktokmonitoring.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.tiktokmonitoring.plist
```

**5. Verify registration**
```bash
launchctl list | grep tiktok
# Expected: -  0  com.tiktokmonitoring
```

**6. Test manually**
```bash
launchctl start com.tiktokmonitoring
tail -30 logs/monitor.log
```

## Key commands for ongoing use

| Action | Command |
|---|---|
| Check status | `launchctl list \| grep tiktok` |
| Run manually | `launchctl start com.tiktokmonitoring` |
| Pause | `launchctl unload ~/Library/LaunchAgents/com.tiktokmonitoring.plist` |
| Resume | `launchctl load ~/Library/LaunchAgents/com.tiktokmonitoring.plist` |
| Read log | `tail -30 logs/monitor.log` |

## Why launchd over crontab
launchd is macOS-native and catches up on missed jobs after sleep/wake cycles.
A laptop is rarely on exactly at 07:00 — launchd handles that gracefully.
