# TikTok Regional Monitoring

A lightweight tool to monitor trending TikTok content for regional Austrian news coverage (Styria & Carinthia). Collects videos by hashtag, filters for regional relevance, and serves results via a local HTML dashboard.

## What it does

- Scrapes TikTok hashtags defined in `config.json`
- Scores videos by views, likes, and shares
- Filters for regional relevance (keywords + trusted accounts)
- Saves top 15 videos to a daily JSON file
- Displays results in a browser-based dashboard (no server needed)

## Requirements

- Python 3.9+
- A TikTok account (for the `ms_token`)

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/tiktok-monitoring.git
cd tiktok-monitoring
```

**2. Install dependencies**
```bash
pip3 install -r requirements.txt
playwright install chromium
```

**3. Configure**
```bash
cp config_template.json config.json
```
Then open `config.json` and replace `YOUR_MS_TOKEN_HERE` with your own token (see below).

**4. Run manually**
```bash
bash run.sh
```
Results are saved to `dashboards/YYYY-MM-DD_data.json`.

**5. Open the dashboard**
Open `dashboards/dashboard_tiktok_trending.html` in your browser, click "JSON laden", and select the latest data file.

## Getting your ms_token

The `ms_token` is a session cookie from TikTok. It expires after a few weeks and needs to be refreshed manually.

1. Go to [tiktok.com](https://tiktok.com) while logged in
2. Open DevTools (`Cmd+Alt+I` / `F12`) → Application → Cookies → `.tiktok.com`
3. Copy the value of `msToken`
4. Paste it into `config.json` under `"ms_token"`

## Automating daily runs (macOS)

A launchd configuration file is included (`com.tiktokmonitoring.plist`) to run the script automatically every day at 07:00.

```bash
cp com.tiktokmonitoring.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.tiktokmonitoring.plist
```

Check status:
```bash
launchctl list | grep tiktok
```

Run manually:
```bash
launchctl start com.tiktokmonitoring
```

## Customizing

All settings are in `config.json`:

| Setting | Description |
|---|---|
| `hashtags` | List of TikTok hashtags to monitor |
| `trusted_accounts` | Videos from these accounts always pass the relevance filter |
| `top_n` | Number of videos to save per day (default: 15) |
| `hours_back` | How far back to look (default: 24h) |
| `score_weights` | Relative weight of views, likes, shares for scoring |

## Security

`config.json` contains your personal `ms_token`. It is listed in `.gitignore` and will never be committed to this repository. Never share it publicly.

## License

MIT
