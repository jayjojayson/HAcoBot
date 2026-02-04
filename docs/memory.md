# Langzeitgedächtnis

HAcoBot verfügt über ein **persistentes Gedächtnis**.  
Das bedeutet, er vergisst Informationen nicht, wenn du das Chat-Fenster schließt oder Home Assistant neu startest.

## Wie funktioniert es?

Der Bot speichert Fakten in einer JSON-Datei in deinem Konfigurationsordner: `/config/HAcoBot/hacobot_memory.json`

Diese Datei ist:
- für dich **lesbar**
- **editierbar**
- dauerhaft gespeichert

## Was wird gespeichert?

### User-Fakten
- Dein Name
- Persönliche Vorlieben  
  z. B. „Ich mag keine Updates am Wochenende“

### System-Notizen
- Informationen, die der Bot über deine Installation gelernt hat
- Relevante Zusammenhänge für bessere Entscheidungen

## Datenschutz

- Alle Daten bleiben **lokal** auf deinem Home-Assistant-Server
- Wenn du die Integration löschst, wird auch dieser Ordner automatisch bereinigt
