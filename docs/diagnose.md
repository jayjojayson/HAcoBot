# Diagnose & Briefing

HAcoBot fungiert als dein persönlicher **System-Administrator** für Home Assistant.

## Das Briefing

Frage einfach nach:

- „Wie ist die Lage?“
- „Briefing“
- „Report“

Der Bot generiert eine kompakte Übersicht bestehend aus:

### Wetter
- Aktueller Zustand
- Temperatur  
  (direkt aus den Entitäts-Attributen)

### Updates
- Liste verfügbarer Updates:
  - Home Assistant Core
  - Add-ons
  - HACS

### Systemstatus
- Analyse der `home-assistant.log`
- Erkennung von:
  - Fehlern
  - Warnungen

## Proaktive Warnungen

Wenn der Modus **„HAcoBot denkt mit“** aktiviert ist, scannt der Bot im Hintergrund nach:

- „Toten“ Geräten  
  (Status `unavailable`)
- Leeren Batterien  
  (< 20 %)

Bei kritischen Problemen kann HAcoBot automatisch eine **Benachrichtigung in Home Assistant** erstellen.
