# Scene Manager

HAcoBot kann Home Assistant Scenes direkt per Chat oder Sprache erstellen und verwalten.

## Was sind Scenes?

Scenes sind **Snapshots von Entity-Zuständen**. Sie speichern die gewünschten Zustände von Lichtern, Schaltern, Klimaanlagen usw. und stellen diese auf Knopfdruck wieder her.

**Beispiele:**
- "Kino-Modus" (Licht aus, TV an, Soundbar laut)
- "Entspannen" (Licht gedimmt, sanfte Farben, ruhige Musik)
- "Arbeiten" (Licht hell, Schreibtischlampe an, Ablenkungen aus)
- "Romantic" (Kerzen an, Hauptlicht aus, leise Musik)

## Scenes erstellen

### Via Chat/Sprache

Sage einfach:

> "Erstelle eine Scene für Kino-Modus"

> "Erstelle eine Scene 'Entspannen': Wohnzimmerlicht auf 30%, Farbe warmweiß"

HAcoBot erstellt automatisch die Scene und nutzt die passenden Entities aus deinem System.

### Detaillierte Scene

Du kannst auch mehrere Entities gleichzeitig definieren:

> "Scene 'Arbeiten': Schreibtischlampe 100%, Wohnzimmerlicht aus, Stehlampe 80%"

## Scenes löschen

Du kannst einzelne Scenes löschen:

> "Lösche die Scene 'Kino-Modus'"

**Wichtig:** Einzelne Scenes werden SOFORT gelöscht, ohne Rückfrage.

Wenn du ALLE Scenes löschen möchtest, wird HAcoBot ZWINGEND vorher um Bestätigung fragen.

## Scenes aktivieren

Nach der Erstellung kannst du deine Scenes jederzeit aktivieren:

> "Aktiviere Kino-Modus"

> "Schalte Scene Entspannen ein"

## Technische Details

- Scenes werden in `/config/scenes.yaml` gespeichert
- Nach Erstellung wird `scene.reload` automatisch aufgerufen
- Scenes erscheinen als `scene.scene_name` Entities
- Sie können in Automationen, Dashboards oder per Service-Call genutzt werden

## Beispiel

**User:** "Erstelle eine Scene für Romantic-Abend"

**HAcoBot erstellt:**
```yaml
- id: 'romantic_abend'
  name: 'Romantic Abend'
  entities:
    light.wohnzimmer:
      state: off
    light.kerzen:
      state: on
      brightness: 180
      color_temp: 400
    media_player.sonos:
      state: playing
      volume_level: 0.3
```

**Verwendung:**
Nach der Erstellung kannst du die Scene aktivieren mit:
- Dashboard-Button
- Sprachbefehl: "Aktiviere Romantic Abend"
- Automation
- Service Call: `scene.turn_on` mit `entity_id: scene.romantic_abend`

## Unterschied zu Scripts

| Feature | Scene | Script |
| :--- | :--- | :--- |
| **Zweck** | Zustände wiederherstellen | Aktionen ausführen |
| **Struktur** | Entity-Zustände | Action-Sequenz |
| **Beispiel** | Licht auf 50%, Farbe blau | Licht einschalten, warten 5s, Licht ausschalten |
| **Verwendung** | Fixer Zustand | Dynamische Abläufe |

**Faustregel:** Nutze Scenes für "statische Zustände" und Scripts für "dynamische Abläufe".
