# Setup — TikTok Monitoring (macOS)

## 1. Python-Abhängigkeiten installieren

```bash
cd "/Users/judithdenkmayr/Claude Projektordner/tiktok_monitoring"
pip3 install -r requirements.txt
playwright install chromium
```

## 2. Script einmalig manuell testen

```bash
cd "/Users/judithdenkmayr/Claude Projektordner/tiktok_monitoring"
bash run.sh
```

Ausgabe landet in:
- `dashboards/YYYY-MM-DD_data.json` — die Videodaten
- `logs/monitor.log` — was passiert ist, mit Zeitstempel

## 3. Dashboard öffnen

1. `dashboards/dashboard_tiktok_trending.html` im Browser öffnen
2. „JSON laden" klicken → die neue `YYYY-MM-DD_data.json` auswählen

---

## 4. Automatischer Tagesstart (macOS launchd)

### Was ist launchd?

launchd ist macOS' eingebauter Job-Planer — zuverlässiger als klassische Cron-Jobs,
weil er versäumte Jobs nach dem Aufwachen des Macs nachholt.

### Struktur der Dateien

```
tiktok_monitoring/
├── com.tiktokmonitoring.plist   ← Konfiguration für launchd (Kopie hier)
├── run.sh                       ← wird täglich ausgeführt
└── logs/
    ├── monitor.log              ← Hauptlog mit Zeitstempeln
    ├── launchd_out.log          ← Systemausgabe von launchd
    └── launchd_err.log          ← Fehlermeldungen von launchd
```

Die aktive Datei liegt unter:
```
~/Library/LaunchAgents/com.tiktokmonitoring.plist
```

### Zeitplan

Täglich um **07:00 Uhr** — sofern der Mac läuft oder im Standby ist.
(Wenn der Mac um 07:00 ausgeschaltet ist, wird der Job beim nächsten Start nachgeholt.)

---

## 5. Verwaltung des automatischen Jobs

### Status prüfen

```bash
launchctl list | grep tiktok
```

Ausgabe: `- 0 com.tiktokmonitoring`
- Erste Spalte `-` = läuft gerade nicht (normal außerhalb 07:00)
- Zweite Spalte `0` = letzter Lauf war erfolgreich

### Job manuell sofort starten (zum Testen)

```bash
launchctl start com.tiktokmonitoring
```

Danach Log prüfen:
```bash
tail -30 "/Users/judithdenkmayr/Claude Projektordner/tiktok_monitoring/logs/monitor.log"
```

### Job deaktivieren (Pause)

```bash
launchctl unload ~/Library/LaunchAgents/com.tiktokmonitoring.plist
```

### Job wieder aktivieren

```bash
launchctl load ~/Library/LaunchAgents/com.tiktokmonitoring.plist
```

### Nach Änderungen an der Plist neu laden

```bash
launchctl unload ~/Library/LaunchAgents/com.tiktokmonitoring.plist
cp "/Users/judithdenkmayr/Claude Projektordner/tiktok_monitoring/com.tiktokmonitoring.plist" \
   ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.tiktokmonitoring.plist
```

---

## 6. Logs lesen

Letzten Lauf ansehen:
```bash
tail -30 "/Users/judithdenkmayr/Claude Projektordner/tiktok_monitoring/logs/monitor.log"
```

Beispiel einer normalen Ausgabe:
```
──────────────────────────────────────
START: 2026-04-28 07:00:01
... (Ausgabe von monitor.py) ...
ENDE:  2026-04-28 07:04:33 — OK
```

Bei Fehlern steht dort:
```
ENDE:  2026-04-28 07:01:05 — FEHLER (Exit 1)
```
→ Dann auch `logs/launchd_err.log` prüfen.

---

## 7. ms_token erneuern

Der Token läuft nach einigen Wochen ab. Zeichen: leere JSON-Dateien oder Fehler im Log.

1. tiktok.com im Browser aufrufen (eingeloggt)
2. DevTools öffnen (cmd+alt+I) → Reiter „Application" → „Cookies" → `.tiktok.com`
3. Wert von `msToken` kopieren
4. In `config.json` bei `"ms_token"` einfügen und speichern

Kein Neustart des Jobs nötig — wird beim nächsten Lauf automatisch verwendet.

---

## Wichtig: Sicherheit

`config.json` enthält den ms_token — diese Datei **nicht teilen** und
**nicht in ein öffentliches Repository committen**.
