
<img width="90%" height="auto" alt="sun-position-card-ubersicht" src="https://github.com/jayjojayson/HAcoBot/docs/images/HAcoBot.svg" />

# HAcoBot - Home Assistant Command Bot 🤖

HAcoBot ist ein fortschrittlicher, KI-gesteuerter Command Bot für Home Assistant. Er integriert sich nativ in die **Assist**-Chat-Funktion und ermöglicht es dir, 
dein Smart Home nicht nur zu steuern, sondern auch zu administrieren.

Anders als herkömmliche Sprachassistenten hat HAcoBot Zugriff auf Werkzeuge, um Automatisierungen zu schreiben, komplette Blueprints zu erstellen, Dashboard Cards zu designen und Systemprobleme zu diagnostizieren.
Es können auch Backups und Updates über HAcoBot installiert werden. HAcoBot ist also ziemlich mächtig in eurem System!

Aktuell befindet sich die Integration in der alpha Phase. 
Die Funktionen sind gegeben, es kann aber hier und da zu Nachfragen von HAcoBot kommen oder er kann manche Anweisungen nicht ausführen. 
Ihr könnt ihm aber schon jetzt Sachen beibringen, die nicht nur im Kurzzeigedächnis hängen bleiben.

---

## ✨ Features

### 🧠 Multi-LLM Support
Wähle deinen bevorzugten KI-Anbieter:

- **Google Gemini** (Empfohlen: `gemini-2.0-flash`)
- **OpenAI ChatGPT** (`gpt-4o`)
- **Groq** (High-Speed Inferenz)
- **DeepSeek** (Coding Specialist)
- **Ollama** (Lokal/Kostenlos)

### 💾 Langzeitgedächtnis & Lernen
HAcoBot kann sich Informationen über Gespräche hinweg merken, z. B.:

- „Mein Name ist Jay, merke dir das“
- „Ich mag keine Updates am Sonntag, speichere das“

🔐 **Technisch umgesetzt als:**
- lokale Speicherung in Home Assistant (`.storage`)
- vollständig unter deiner Kontrolle

### 🧠 Kurzzeitgedächtnis
Merkt sich den aktuellen Gesprächskontext für:
- flüssige Rückfragen
- mehrstufige Anweisungen
- natürliche Dialoge

### 🛡️ Modulare Kontrolle (Feature-Switches)
Du entscheidest, **was HAcoBot darf**.  
Jede Fähigkeit kann einzeln aktiviert oder deaktiviert werden:

- **Updates & Wartung**  
  Installiert Core-, Add-on- und HACS-Updates
- **System-Neustart**  
  Kritische Funktion, separat abgesichert
- **Live-Steuerung**  
  Lichter, Schalter, Cover, Szenen
- **To-Do-Listen & Kalender**  
  Erstellen, ändern, löschen von Einträgen
- **Dashboard Designer**  
  Generiert Lovelace-YAML
- **HAcoBot denkt mit**  
  Aktiviert Gedächtnis & proaktive Anomalie-Suche
- usw...

### ⚙️ Automation & Blueprint Manager
- Erstelle komplexe Automatisierungen per Chat  
- Generiere Blueprints mit Inputs & Selectors  
- Lösche veraltete oder fehlerhafte Automatisierungen  
- Lass dir Übersichten deiner Automationen & Blueprints anzeigen 

### 🎨 Dashboard Designer
Sag einfach:  
> "Erstelle eine Karte für mein Wohnzimmer mit Licht und Temperatur"

HAcoBot generiert den vollständigen YAML-Code:
- Vertical / Horizontal Stacks  
- Tile Cards  
- u.v.m.
- Speicherung unter /config/dashboard_drafts/

### 📡 Live-Steuerung
Steuere Geräte direkt per natürlicher Sprache:

- `light.turn_on`
- `cover.set_position`
- Schalter, Szenen, Scripts u. v. m.

### 📅 Kalender & To-Do-Listen
- Kalender-Einträge anlegen, ändern, löschen
- To-Do-Listen erstellen, abhaken, bereinigen

### 🔍 Proaktive Diagnose & Briefing
Frage z. B. nach:

- **„Lagebericht“**
- **„Briefing“**
- **„System Report“**

#### HAcoBot analysiert dabei:

- Wetter & Vorhersagen
- anstehende Updates
- Fehlerlogs (`home-assistant.log`)
- nicht verfügbare („tote“) Entitäten
- leere oder kritische Batterien
- versteckte Attribute (z. B. Zellspannungen)

---


## 🚀 Installation

### Manuell

1. Lade diesen Ordner herunter  
2. Kopiere den Ordner  
   `custom_components/hacobot`  
   nach  
   `/config/custom_components/`
3. Starte Home Assistant neu

---

## ⚙️ Konfiguration

1. Gehe zu **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. Suche nach **HAcoBot**
3. Wähle deinen Anbieter (z. B. Google Gemini) und gib deinen API-Key ein
4. *(Optional)* Wähle das Modell (z. B. `gemini-2.0-flash`)
5. *(Optional)* Ollama lokale Server IP eintragen

## 🧑‍💻 Nutzung

1. Klicke auf das **Chat-Symbol (Assist)** oben rechts in Home Assistant
2. Wähle im Dropdown den Assistenten, der HAcoBot als  
   **"Unterhaltungs-Agent"** nutzt

### Beispiele für Prompts

- "Erstelle eine Dashboard-Karte für alle meine Batterien"
- "Erstelle einen Blueprint für..."
- "Erstelle ein Backup"
- "Starte Home Assistant neu"
- "Führe Update "XYZ" aus"
- "Wie wird das Wetter morgen?"
- "Schalte das Licht im Flur an und im Wohnzimmer aus"
- "Frage nach Systemständen (Temperaturen, Stromverbrauch, Fenster)"
- "System Report, Überblick, aktuelle Lage"
- "Was kannst du alles für mich tun?"

---

## 🛠️ Funktionsweise

HAcoBot arbeitet mit einem **ReAct-Loop (Reasoning & Acting)**:

1. Analyse deiner Anfrage  
2. Entscheidung, welche Tools benötigt werden  
3. Ausführung (z. B. Logs lesen, Entitäten prüfen)  
4. Verständliche Ergebnis-Zusammenfassung  

So entsteht ein **echter Admin-Agent**, nicht nur ein Chatbot.

---

#### ❤️ Entwickelt von **@jayjojayson**
