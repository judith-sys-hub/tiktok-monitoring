# TikTok Regional Monitoring

A lightweight tool to monitor trending TikTok content for regional Austrian news coverage (Styria & Carinthia). Collects videos by hashtag, filters for regional relevance, and outputs results as a self-contained HTML dashboard — optionally pushed to OneDrive and announced via a Teams notification.

## What it does

- Scrapes TikTok hashtags defined in `config.json`
- Scores videos by views, likes, and shares
- Filters for regional relevance (keywords + trusted accounts)
- Saves top 15 videos to a daily JSON archive
- Writes a self-contained HTML dashboard (no server needed)
- Optionally copies the dashboard to an OneDrive/SharePoint folder
- Optionally posts a top-3 summary card to a Microsoft Teams channel

## Requirements

- Python 3.9+
- A TikTok account (for the `ms_token`)

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/judith-sys-hub/tiktok-monitoring.git
cd tiktok-monitoring
```

**2. Create a virtual environment and install dependencies**

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\playwright install chromium
```

**3. Configure**
```bash
cp config_template.json config.json
```
Then open `config.json` and replace `YOUR_MS_TOKEN_HERE` with your own token (see below).

**4. Run manually**

macOS/Linux:
```bash
bash run.sh
```

Windows:
```powershell
.venv\Scripts\python monitor.py
```

Results are saved to `dashboards/YYYY-MM-DD_data.json` and the dashboard is written to `dashboards/dashboard_tiktok_trending.html`.

## Getting your ms_token

The `ms_token` is a session cookie from TikTok. It expires after a few weeks and needs to be refreshed manually.

1. Go to [tiktok.com](https://tiktok.com) while logged in
2. Open DevTools (`Cmd+Alt+I` / `F12`) → Application → Cookies → `.tiktok.com`
3. Find the cookie named exactly `msToken` (with domain `.tiktok.com`)
4. Copy its value and paste it into `config.json` under `"ms_token"`

## Teams notification + OneDrive dashboard (optional)

These two features activate only when the corresponding fields are set in `config.json`. If either field is missing or left as the placeholder value, that feature is silently skipped.

### OneDrive dashboard

Set `onedrive_output_dir` to a folder that syncs to SharePoint:

```json
"onedrive_output_dir": "C:\\Users\\YourName\\OneDrive - Your Organisation\\TikTok Monitoring"
```

After each run, `tiktok_trending_heute.html` is written to that folder. Share the folder with colleagues via SharePoint — they can bookmark the file and it updates automatically every morning.

### Teams notification

Set `teams_webhook_url` to a Power Automate webhook URL:

```json
"teams_webhook_url": "https://..."
```

To get the URL:
1. Open your Teams channel → **...** → **Workflows**
2. Search for **"Send a webhook warning to channel"** → select it
3. Name it (e.g. `TikTok Monitor`), choose your channel → **Add workflow**
4. Copy the HTTP POST URL and paste it into `config.json`

After each run, a summary card with the top 3 videos is posted to the channel.

## Automating daily runs

### macOS (launchd)

A launchd configuration file is included (`com.tiktokmonitoring.plist`) to run the script every day at 07:00.

```bash
cp com.tiktokmonitoring.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.tiktokmonitoring.plist
```

### Windows (Task Scheduler)

Run this once in PowerShell to register a daily task at 07:00:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "$PWD\.venv\Scripts\python.exe" `
    -Argument "$PWD\monitor.py" `
    -WorkingDirectory $PWD

$trigger = New-ScheduledTaskTrigger -Daily -At "07:00AM"

$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive -RunLevel Limited

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1)

Register-ScheduledTask -TaskName "TikTok Monitoring" `
    -Action $action -Trigger $trigger `
    -Principal $principal -Settings $settings -Force
```

The task runs when you are logged in. If the laptop was off at 07:00, it runs as soon as you log in.

## Customizing

All settings are in `config.json`:

| Setting | Description |
|---|---|
| `hashtags` | List of TikTok hashtags to monitor |
| `trusted_accounts` | Videos from these accounts always pass the relevance filter |
| `top_n` | Number of videos to keep per day (default: 15) |
| `hours_back` | How far back to look (default: 24h) |
| `max_videos_per_hashtag` | Max videos fetched per hashtag (default: 30) |
| `score_weights` | Relative weight of views, likes, shares for scoring |
| `onedrive_output_dir` | Path to OneDrive folder for dashboard (optional) |
| `teams_webhook_url` | Power Automate webhook URL for Teams ping (optional) |

## Security

`config.json` contains your personal `ms_token`. It is listed in `.gitignore` and will never be committed to this repository. The Teams webhook URL is also sensitive — treat it like a password and do not share it publicly.

## License

MIT
