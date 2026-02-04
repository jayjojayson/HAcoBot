# Feature Übersicht

HAcoBot ist modular aufgebaut. Du kannst viele dieser Funktionen über Schalter in der Integration an- oder abschalten.

## 🧠 Multi-LLM Support

Verbinde den Bot mit der KI deiner Wahl:

- **Google Gemini** (empfohlen für Geschwindigkeit und Kosten)
- **OpenAI ChatGPT**
- **Ollama** (für lokale Privatsphäre)
- **Groq & DeepSeek**

## 🎨 Dashboard Designer

Erstelle Dashboards per Sprache oder Chat, zum Beispiel:

> „Erstelle eine Karte für mein Wohnzimmer mit Licht und Temperatur“

HAcoBot:
- generiert validen YAML-Code
- unterstützt `vertical-stack` und `horizontal-stack`
- kennt Custom Cards wie:
  - `mini-graph-card`
  - `sun-position-card`

## ⚙️ Automation & Blueprints

- Erstellt komplexe Automatisierungen per Chat
- Schreibt Blueprints mit Inputs und Selectors
- Kann bestehende Automatisierungen wieder löschen

## 📝 To-Do & Kalender

- Verwaltet Einkaufs- und Aufgabenlisten  
  (Hinzufügen, Streichen, Löschen)
- Prüft deinen Kalender
- Kann Termine löschen oder anpassen

## 📡 Live Steuerung

- Steuert Geräte wie:
  - `light`
  - `switch`
  - `cover`
  - weitere Home-Assistant-Entitäten
- Kann Home Assistant neu starten (wenn erlaubt)

## 🔍 Diagnose & Briefing

### Lagebericht
Frage z. B.:

> „Wie ist die Lage?“

HAcoBot liefert eine Zusammenfassung aus:
- Wetter
- Updates
- Systemstatus

### Log-Analyse
- Liest Fehler direkt aus der `home-assistant.log`
- Erkennt wiederkehrende oder kritische Probleme
