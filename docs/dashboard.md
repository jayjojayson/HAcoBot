# Dashboard Designer

HAcoBot kann YAML-Code für Lovelace-Dashboards generieren.  
Die erzeugten Dateien werden unter folgendem Pfad gespeichert: `/config/HAcoBot/Dashboard-Cards/`

## Befehle

Beispiele für Sprach- oder Chat-Befehle:

- „Erstelle eine Karte für mein Büro mit Licht und Heizung.“
- „Erstelle eine sun-position-card.“

## Features

### Stacks
- Nutzt automatisch `vertical-stack` oder `horizontal-stack` für Gruppierungen

### Custom Cards
- Unterstützt Karten aus HACS  
  z. B. `mini-graph-card`

### Intelligenz
- Sucht selbstständig die passenden Entitäten aus deinem System
- Berücksichtigt Raum- und Gerätenamen

## Die HAcoBot Karte (Frontend)

Die Integration bringt eine spezielle **Chat-Karte** für dein Dashboard mit.

### Hinzufügen

1. **Dashboard → Bearbeiten → Karte hinzufügen**
2. Suche nach **„HAcoBot Chat“**

Falls die Karte nicht gefunden wird:
- Browser-Cache leeren (**STRG + F5**)
- oder manuell hinzufügen mit:
