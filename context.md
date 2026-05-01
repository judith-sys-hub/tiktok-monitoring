# context.md — TikTok Monitoring

**Stand:** 2026-04-22
**Status:** Testphase (Einzelnutzer)

---

## Projektziel

Zeitlich und örtlich begrenzte Trendanalyse von TikTok-Inhalten mit lokalem Nachrichtenwert für Kärnten und die Steiermark. Ziel ist es, virales oder newsrelevantes Material aus der Region früh zu erkennen und für den Newsroom nutzbar zu machen.

---

## Scope

### Regionen

**Kärnten:**
Feldkirchen, Hermagor, Klagenfurt Stadt, Klagenfurt Land, St. Veit an der Glan, Spittal an der Drau, Villach Stadt, Villach-Land, Völkermarkt, Wolfsberg

**Steiermark:**
Lienz, Liezen, Leoben, Bruck-Mürzzuschlag, Hartberg-Fürstenfeld, Weiz

### Inhalte (Chronikthemen)

- Unfälle, Polizei- und Feuerwehreinsätze
- Tierrettungen
- Kuriose oder überraschende Situationen: Supermärkte, belebte Plätze, Lokale, öffentliche Verkehrsmittel, Straßen

### Hashtags (Monitoring-Set)

```
#meanwhileinaustria #österreichmeme #styria #carinthia
#graz #grazistanders #urbangraz #klagenfurt #villach
#steirisch #mariatrost #jakomini #grazmeme #grazerhumor
#grazleben #steiermark #lagergasse #gakturgraz #grazerstraßenbahn
#kürbiskernöl #grazzentrum #grazisanders #lokalhumor #grazcity
#studentenstadt #uhrturm #schlossberg #graznews #grazaltstadt
#steiermarknews #österreich #lokalnachrichten #regionalnews
#blaulicht #grazkriminal #polizei #grazumgebung
```

---

## Methodik

1. Tägliches Hashtag-Screening (manuell oder halbautomatisch)
2. Bewertung nach Nachrichtenwert: Relevanz, Aktualität, Verbreitungsgrad
3. Ablage relevanter Funde in `/research` mit Datum, Hashtag, Link, Kurzbeschreibung
4. Dashboard-Auswertung: Welche Hashtags, Themen und Regionen dominieren in welchem Zeitraum

---

## KPIs

| Kennzahl | Beschreibung |
|---|---|
| Gefundene Treffer/Woche | Anzahl newsrelevanter Videos pro Woche |
| Hashtag-Frequenz | Welche Tags liefern die meisten Treffer |
| Regionaler Schwerpunkt | Welche Bezirke tauchen am häufigsten auf |
| Reaktionszeit | Zeit zwischen TikTok-Upload und Newsroom-Weiterleitung |

---

## Nutzer & Rollen

| Phase | Nutzer | Rolle |
|---|---|---|
| Testphase | Judith Denkmayr | Allein, Aufbau & Validierung |
| Produktivbetrieb | Newsroom-Dienst | Tägliches Screening, Funds melden |

---

## Ordnerstruktur

```
/tiktok_monitoring/
├── context.md          ← dieses Dokument
├── dashboards/         ← Dashboard-Designs und Auswertungsvorlagen
└── /research/          ← Einzelfunde, täglich geloggt
```

---

## Offene Punkte

- [ ] Tool-Entscheidung: manuelles Screening vs. API-gestütztes Monitoring
- [ ] Übergabeformat für Newsroom-Dienst definieren
- [ ] Zeitlichen Scope festlegen (Pilotdauer)
