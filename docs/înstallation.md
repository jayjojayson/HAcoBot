# Installation

### HACS

1. Folge einfach dem Link, um dieses Repository zu HACS hinzuzufügen:  
 [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jayjojayson&repository=hass-victron-vrm-api&category=integration)

3. Gehe zu `Einstellungen -> Geräte & Dienste -> Integrationen`
4. Klicke auf `Integration hinzufügen`
5. Suche nach `HAcoBot`
6. Installiere die Integration
7. Starte Home Assistant neu

### Manuell via HACS (nicht empfohlen)

1. Installiere HACS in Home Assistant
2. Gehe zu **HACS → Integrationen → Benutzerdefinierte Repositories**
3. Füge die Repository-URL hinzu: `https://github.com/jayjojayson/HAcoBot`
4. Installiere die Integration

### Manuell (nicht empfohlen)

1. Repository herunterladen
2. Ordner
   `custom_components/hacobot`
   nach
   `/config/custom_components/`
   kopieren
3. Home Assistant neu starten
4. Gehe zu `Einstellungen -> Geräte & Dienste -> Integrationen`
5. Klicke auf `Integration hinzufügen`
6. Suche nach `HAcoBot`
7. Installiere die Integration
8. Starte Home Assistant neu

## Wichtig: Browser-Cache leeren

Da HAcoBot eine eigene Dashboard-Karte mitbringt, **musst du nach dem Neustart zwingend den Browser-Cache leeren**, damit die JavaScript-Dateien korrekt geladen werden.

- Tastenkombination: **STRG + F5**

> **Hinweis:**
> Wenn die Integration nicht in der Liste erscheint, leere den Browser-Cache erneut und lade die Seite neu.
