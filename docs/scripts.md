# Script Manager

HAcoBot kann Home Assistant Scripts direkt per Chat oder Sprache erstellen und verwalten.

## Was sind Scripts?

Scripts sind **Action-Sequenzen ohne Trigger oder Conditions**. Sie sind ideal für manuelle Aktionen, die du auf Knopfdruck oder per Sprachbefehl ausführen möchtest.

**Beispiele:**
- "Gute Nacht Routine" (Lichter aus, Rollläden runter, Alarmanlage scharf)
- "Kaffee kochen" (Kaffeemaschine an, Licht in Küche an)
- "Filmabend" (TV an, Licht dimmen, Soundbar einschalten)

## Scripts erstellen

### Via Chat/Sprache

Sage einfach:

> "Erstelle ein Script für meine Gute-Nacht-Routine"

> "Erstelle ein Script: Schalte das Wohnzimmerlicht aus und die Rollläden runter"

HAcoBot erstellt automatisch das Script mit valider YAML-Syntax und nutzt die passenden Entities aus deinem System.

### Manuelle Erstellung

Du kannst auch selbst ein Script beschreiben:

> "Script 'Morgenroutine': Licht in der Küche auf 80%, Kaffeemaschine an, Rollläden auf 100%"

## Scripts löschen

Du kannst einzelne Scripts löschen:

> "Lösche das Script 'Gute Nacht'"

**Wichtig:** Einzelne Scripts werden SOFORT gelöscht, ohne Rückfrage.

Wenn du ALLE Scripts löschen möchtest, wird HAcoBot ZWINGEND vorher um Bestätigung fragen.

## Technische Details

- Scripts werden in `/config/scripts.yaml` gespeichert
- Nach Erstellung wird `script.reload` automatisch aufgerufen
- Scripts erscheinen als `script.script_name` Entities
- Sie können in Automationen, Dashboards oder per Service-Call genutzt werden

## Beispiel

**User:** "Erstelle ein Script für Filmabend"

**HAcoBot erstellt:**
```yaml
filmabend:
  alias: 'Filmabend'
  description: 'Startet den perfekten Filmabend'
  sequence:
    - service: light.turn_off
      target:
        entity_id: light.wohnzimmer
    - service: media_player.turn_on
      target:
        entity_id: media_player.tv_wohnzimmer
    - service: light.turn_on
      target:
        entity_id: light.ambiente
      data:
        brightness_pct: 20
```

**Verwendung:**
Nach der Erstellung kannst du das Script ausführen mit:
- Dashboard-Button
- Sprachbefehl: "Starte Filmabend"
- Automation
- Service Call: `script.filmabend`
