# Feature Switches (Sicherheit)

Nach der Installation wird in Home Assistant ein Gerät **HAcoBot** erstellt.  
Dort findest du Schalter (Entities), mit denen du dem Bot gezielt **Rechte entziehen oder erlauben** kannst.

Dies dient der Sicherheit:  
Du kannst dem Bot z. B. erlauben, Dashboards zu bauen, ihm aber verbieten, Geräte zu schalten oder das System neu zu starten.

## Übersicht der Schalter

### Updates & Wartung
- Darf Updates auflisten
- Darf Updates auf Befehl installieren

### System Neustart
- Darf `homeassistant.restart` ausführen  
- **Kritisch!** Sollte nur bei Bedarf aktiviert werden

### Live Steuerung
- Darf Geräte steuern, z. B.:
  - `light`
  - `switch`
  - `cover`
  - `climate`
  - weitere Entitäten

### To-Do Listen Manager
- Darf To-Do-Listen lesen
- Darf Einträge hinzufügen, abhaken und löschen

### Kalender Manager
- Darf Kalendereinträge lesen
- Darf Termine löschen

### Dashboard Designer
- Darf YAML-Dateien für Dashboards erstellen

### Automation & Blueprints
- Darf Automatisierungen erstellen
- Darf Automatisierungen und Blueprints löschen

### Diagnose & Briefing
- Darf Logs lesen
- Darf den Systemstatus analysieren

### HAcoBot denkt mit
- Aktiviert das Langzeitgedächtnis
- Aktiviert proaktive Hintergrund-Scans
