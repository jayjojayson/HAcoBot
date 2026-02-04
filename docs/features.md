# Feature Übersicht

HAcoBot ist modular aufgebaut. Du kannst viele dieser Funktionen über Schalter in der Integration an- oder abschalten.

## 🧩 Comparison – HAcoBot vs. HA Assist

| Capability | Home Assistant Assist | HAcoBot |
| :--- | :---: | :---: |
| Natural language device control | ✅ | ✅ |
| Multi-step conversations | ⚠️ Limited | ✅ |
| Short-term conversation memory | ⚠️ Basic | ✅ |
| Long-term memory across chats | ❌ | ✅ |
| Multi-LLM provider support | ⚠️ Limited | ✅ |
| Local LLM support (Ollama) | ⚠️ Partial | ✅ |
| Automation creation via chat | ❌ | ✅ |
| Blueprint generation | ❌ | ✅ |
| Automation analysis & debugging | ❌ | ✅ |
| Dashboard YAML generation | ❌ | ✅ |
| Custom card awareness | ❌ | ✅ |
| Proactive anomaly detection | ❌ | ✅ |
| System diagnostics & reports | ⚠️ Basic | ✅ |
| Log file analysis | ❌ | ✅ |
| Dead entity detection | ❌ | ✅ |
| Battery health analysis | ❌ | ✅ |
| Update overview | ⚠️ Basic | ✅ |
| Install updates via chat | ❌ | ✅ |
| Backup management | ❌ | ✅ |
| Calendar management | ⚠️ Basic | ✅ |
| To-Do list management | ⚠️ Basic | ✅ |
| Feature permission switches | ❌ | ✅ |
| Custom dashboard chat card | ❌ | ✅ |
| Voice assistant support | ✅ | ✅ |
| ReAct reasoning loop | ❌ | ✅ |
| Admin-level system interaction | ❌ | ✅ |

✅ Fully supported  
⚠️ Limited / basic implementation  
❌ Not supported


## 🧠 Multi-LLM Support

Verbinde den Bot mit der KI deiner Wahl:

- **Google Gemini** (empfohlen für Geschwindigkeit und Kosten)
- **OpenAI ChatGPT**
- **Ollama** (für lokale Privatsphäre)
- **Groq & DeepSeek**

## 💾 Langzeitgedächtnis & Lernen
HAcoBot kann sich Informationen **über Gespräche hinweg merken**, z. B.:

- „Mein Name ist Jan“
- „Ich mag keine Updates am Sonntag“

**Technisch:**
- lokale Speicherung unter  
  `/config/HAcoBot/hacobot_memory.json`  
- vollständig **offline kontrollierbar**
- jederzeit lösch- oder deaktivierbar


## 🧠 Kurzzeitgedächtnis
Merkt sich den aktuellen Gesprächskontext für:

- mehrstufige Anweisungen
- Rückfragen
- natürliche Dialoge


## 🛡️ Modulare Kontrolle (Feature-Switches)
Du entscheidest **was HAcoBot darf**.  
Jede Fähigkeit kann separat aktiviert oder deaktiviert werden:

- **Updates & Wartung**  
  Listet Updates und installiert sie **nur auf expliziten Befehl**
- **System-Neustart**  
  Kritische Funktion, extra abgesichert
- **Live-Steuerung**  
  Lichter, Schalter, Cover, Szenen, Scripts
- **To-Do-Listen & Kalender**  
  Erstellen, abhaken, löschen von Einträgen
- **Dashboard Designer**  
  Generiert vollständigen Lovelace-YAML
- **HAcoBot denkt mit**  
  Aktiviert Gedächtnis & proaktive Anomalie-Suche
- **Diagnose & Briefing**  
  System-, Wetter- & Log-Analyse

## 🎨 Dashboard Designer

Erstelle Dashboards per Sprache oder Chat, zum Beispiel:

> „Erstelle eine Karte für mein Wohnzimmer mit Licht und Temperatur“

HAcoBot:
- generiert validen YAML-Code
- unterstützt `vertical-stack` und `horizontal-stack`
- kennt Custom Cards wie:
  - `mini-graph-card`
  - `sun-position-card`

## ⚙️ Automation & Blueprint Manager

- Erstelle komplexe Automatisierungen per Chat
- Generiere vollständige **Blueprints mit Inputs & Selectors**
- Lösche veraltete oder fehlerhafte Automationen
- Zeige Übersichten deiner Automationen & Blueprints an


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
- Kann Home Assistant neu starten (wenn Nutzer auffordert)

## 🔍 Briefing

### Lagebericht
Frage z. B.:

> „Briefing?“
> „Lagebericht?“
> „Wie ist die Lage?“

HAcoBot liefert eine Zusammenfassung aus:
- Wetter
- Updates
- Systemstatus
- Option ToDo List anzusehen

### Log-Analyse
- Liest Fehler direkt aus der `home-assistant.log`
- Erkennt wiederkehrende oder kritische Probleme

## 📡 Live-Steuerung

Steuere Geräte direkt per natürlicher Sprache:

- `light.turn_on`
- `cover.set_position`
- Schalter, Szenen, Scripts u. v. m.


## 📅 Kalender & To-Do-Power-User

- Termine lesen & gezielt löschen
- To-Do-Listen:
  - Einträge hinzufügen
  - abhaken (erledigt)
  - löschen (entfernen)
