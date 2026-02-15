<img width="100%" height="auto" alt="HAcoBot" src="https://github.com/jayjojayson/HAcoBot/blob/main/docs/images/HAcoBot_1024.png" />

# HAcoBot – Home Assistant Command Bot 🤖

HAcoBot ist ein fortschrittlicher, **KI-gesteuerter Admin- & Command-Agent** für Home Assistant.  
Er integriert sich nativ in die **Assist-Chat-Funktion** und ermöglicht es dir, dein Smart Home nicht nur zu steuern, sondern auch **zu administrieren, zu analysieren und weiterzuentwickeln**.

Im Gegensatz zu klassischen Sprachassistenten besitzt HAcoBot:

- Zugriff auf **System-Werkzeuge**
- ein **Kurz- & Langzeitgedächtnis**
- die Fähigkeit, **proaktiv mitzudenken**
- eine **eigene Lovelace-Dashboard-Karte**

HAcoBot ist damit kein Chatbot, sondern ein **echter Home-Assistant-Admin-Agent**.

> ⚠️ **Status:** Beta  
> Die Kernfunktionen sind vorhanden. In einzelnen Situationen kann HAcoBot nachfragen oder Aktionen abbrechen.  
> Wissen und Präferenzen können aber bereits dauerhaft gespeichert werden.

---

## ✨ Features

### 🧠 Multi-LLM Support
Wähle deinen bevorzugten KI-Anbieter:

- **Google Gemini** (Empfohlen: `gemini-2.0-flash`)
- **OpenAI ChatGPT** (`gpt-4o`)
- **Groq** (High-Speed Inferenz)
- **DeepSeek** (Coding Specialist)
- **OpenRouter** (Zugriff auf viele Modelle mit einem Key)
- **Ollama** (lokal, privat & kostenlos per eigener URL)


### 💾 Langzeitgedächtnis & Lernen
HAcoBot kann sich Informationen **über Gespräche hinweg merken**, z. B.:

- „Mein Name ist Jan“
- „Ich mag keine Updates am Sonntag“

**Technisch:**
- lokale Speicherung unter  
  `/config/HAcoBot/hacobot_memory.json`  
- vollständig **offline kontrollierbar**
- jederzeit lösch- oder deaktivierbar


### 🧠 Kurzzeitgedächtnis
Merkt sich den aktuellen Gesprächskontext für:

- mehrstufige Anweisungen
- Rückfragen
- natürliche Dialoge


### 🛡️ Modulare Kontrolle (Feature-Switches)
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
- **Script Manager**  
  Erstelle und verwalte Home Assistant Scripts
- **Scene Manager**  
  Erstelle und verwalte Scenes
- **Benachrichtigungen & Alerts**  
  Sende Benachrichtigungen und erhalte proaktive Warnungen
- **HAcoBot denkt mit**  
  Aktiviert Gedächtnis & proaktive Anomalie-Suche
- **Diagnose & Briefing**  
  System-, Wetter- & Log-Analyse


### ⚙️ Automation & Blueprint Manager
- Erstelle komplexe Automatisierungen per Chat
- Generiere vollständige **Blueprints mit Inputs & Selectors**
- Lösche veraltete oder fehlerhafte Automationen
- Zeige Übersichten deiner Automationen & Blueprints an


### 🎨 Dashboard Designer
Sag einfach:

> „Erstelle eine Karte für mein Wohnzimmer mit Licht und Temperatur“

HAcoBot generiert den **kompletten YAML-Code**:

- Vertical / Horizontal Stacks
- Tile Cards
- Custom Cards (z. B. `mini-graph-card`, `sun-position-card`)
- intelligente Struktur & Entity-Auswahl

📁 Speicherung unter:  
`/config/HAcoBot/Dashboard-Cards/`


### 📡 Live-Steuerung
Steuere Geräte direkt per natürlicher Sprache:

- `light.turn_on`
- `cover.set_position`
- Schalter, Szenen, Scripts u. v. m.


### 📅 Kalender & To-Do-Power-User
- Termine lesen & gezielt löschen
- To-Do-Listen:
  - Einträge hinzufügen
  - abhaken (erledigt)
  - löschen (entfernen)


### 📜 Script Manager
- Erstelle Home Assistant Scripts per Chat oder Sprache
- Action-Sequenzen ohne Trigger (z.B. "Gute Nacht Routine")
- Lösche einzelne Scripts oder alle Scripts (mit Bestätigung)


### 🎬 Scene Manager
- Erstelle Scenes (Snapshots von Entity-Zuständen)
- Beispiele: Kino-Modus, Entspannen, Arbeiten
- Aktiviere Scenes per Sprache oder Automation


### 🔔 Benachrichtigungen & Alerts
- Sende Benachrichtigungen an Mobile Apps oder Persistent Notifications
- Proaktive Warnungen:
  - Kritische Batterien (< 20%)
  - Offene Fenster/Türen wenn User das Haus verlässt
  - Fehlerhafte Automationen
  - Gravierende Systemprobleme



### 🔍 Proaktive Diagnose & Briefing
Frage z. B. nach:

- **„Lagebericht“**
- **„Briefing“**
- **„System Report“**

HAcoBot analysiert dabei:

- Wetter & Vorhersage (inkl. Attribute)
- anstehende Updates
- Fehlerlogs (`home-assistant.log`)
- nicht verfügbare („tote“) Entitäten
- leere oder kritische Batterien
- versteckte Sensor-Attribute (z. B. Zellspannungen)

---

## 🧩 Feature Comparison – HAcoBot vs. Home Assistant Assist

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
| Script creation & management | ❌ | ✅ |
| Scene creation & management | ❌ | ✅ |
| Notification management | ❌ | ✅ |
| Security monitoring (open doors/windows) | ❌ | ✅ |
| Feature permission switches | ❌ | ✅ |
| Custom dashboard chat card | ❌ | ✅ |
| Voice assistant support | ✅ | ✅ |
| ReAct reasoning loop | ❌ | ✅ |
| Admin-level system interaction | ❌ | ✅ |

✅ Fully supported  
⚠️ Limited / basic implementation  
❌ Not supported


---

## 🚀 Installation

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

---

## ⚙️ Konfiguration (Backend)

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. **HAcoBot** auswählen
3. KI-Anbieter wählen (z. B. Google Gemini)
4. API-Key eintragen  
   *(bei Ollama: beliebig, aber nicht leer)*
5. *(Optional)* Modell auswählen
6. *(Ollama)* lokale URL angeben  
   z. B. `http://192.168.1.10:11434/v1`

---

## 🖥️ Dashboard-Karte (Frontend)

HAcoBot bringt eine eigene **Chat-Karte** mit 🎉

1. Browser-Cache leeren (`STRG + F5`)
2. Dashboard → **Karte hinzufügen**
3. **HAcoBot Chat** auswählen  
   oder manuell:

```yaml
type: custom:hacobot-card
