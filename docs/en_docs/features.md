# Feature Overview

HAcoBot is modular. You can turn many of these functions on or off via switches in the integration.

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
| Script creation & management | ❌ | ✅ |
| Scene creation & management | ❌ | ✅ |
| Notification management | ❌ | ✅ |
| Security monitoring | ❌ | ✅ |
| Feature permission switches | ❌ | ✅ |
| Custom dashboard chat card | ❌ | ✅ |
| Voice assistant support | ✅ | ✅ |
| ReAct reasoning loop | ❌ | ✅ |
| Admin-level system interaction | ❌ | ✅ |

✅ Fully supported  
⚠️ Limited / basic implementation  
❌ Not supported


## 🧠 Multi-LLM Support

Connect the bot with the AI of your choice:

- **Google Gemini** (recommended for speed and cost)
- **OpenAI ChatGPT**
- **Ollama** (for local privacy)
- **Groq & DeepSeek**

## 💾 Long-Term Memory & Learning
HAcoBot can remember information **across conversations**, e.g.:

- "My name is Jan, please save."
- "I don't like updates on Sundays, please remember."

**Technical:**
- Local storage at  
  `/config/HAcoBot/hacobot_memory.json`  
- Fully **user-controlled**
- Can be deleted or deactivated at any time


## 🧠 Short-Term Memory
Remembers the current conversation context for:

- Multi-step instructions
- Follow-up questions
- Natural dialogues


## 🛡️ Modular Control (Feature Switches)
You decide **what HAcoBot is allowed to do**.  
Each capability can be enabled or disabled separately:

- **Updates & Maintenance**  
  Lists updates and installs them **only on explicit command**
- **System Restart**  
  Critical function, separately secured
- **Live Control**  
  Lights, switches, covers, scenes, scripts
- **To-Do Lists & Calendars**  
  Create, check off, delete entries
- **Dashboard Designer**  
  Generates complete Lovelace YAML
- **HAcoBot Thinks Ahead**  
  Activates memory & proactive anomaly detection
- **Diagnostics & Briefing**  
  System, weather & log analysis

## 🎨 Dashboard Designer

Create dashboards via voice or chat, for example:

> "Create a card for my living room with light and temperature"

HAcoBot:
- Generates valid YAML code
- Supports `vertical-stack` and `horizontal-stack`
- Knows custom cards like:
  - `mini-graph-card`
  - `sun-position-card`

## ⚙️ Automation & Blueprint Manager

- Create complex automations via chat
- Generate complete **Blueprints with Inputs & Selectors**
- Delete outdated or faulty automations
- Display overviews of your automations & blueprints

## 📡 Live Control

Control devices directly using natural language:

- `light.turn_on`
- `cover.set_position`
- Switches, scenes, scripts, and other Home Assistant entities

Can restart Home Assistant (if requested by user)!

## 📝 To-Do & Calendar

- Manages shopping and task lists  
  (Add, check off, delete)
- Checks your calendar
- Can delete or adjust appointments

## 🔍 Briefing

### Status Report
Ask e.g.:

> "Briefing?"
> "Status report?"
> "What's the status?"

HAcoBot delivers a summary of:
- Weather
- Updates
- System status
- Option to view ToDo List

### Log Analysis
- Reads errors directly from `home-assistant.log`
- Detects recurring or critical problems


## 📅 Calendar & To-Do Power User

- Read & selectively delete appointments
- To-Do lists:
  - Add entries
  - Check off (done)
  - Delete (remove)


## 📜 Script Manager

Create Home Assistant scripts via chat or voice:

- **What are scripts?** Action sequences without triggers (e.g. "Good Night Routine")
- **Create:** "Create a script for movie night"
- **Delete:** Individual scripts or all (with confirmation)
- **Usage:** Dashboard, Voice, Automations

More details: [Scripts Manager](scripts.md)


## 🎬 Scene Manager

Create scenes (snapshots of entity states):

- **What are scenes?** Saved states of lights, switches, etc.
- **Create:** "Create a scene for cinema mode"
- **Activate:** "Activate scene Relax"
- **Examples:** Cinema Mode, Romantic, Working, Relaxing

More details: [Scenes Manager](scenes.md)


## 🔔 Notifications & Alerts

Send notifications or receive proactive warnings:

- **Mobile App** Push notifications to your smartphone
- **Persistent Notifications** Warnings in the Home Assistant frontend
- **Proactive Warnings:**
  - Critical batteries (< 20%)
  - Open windows/doors when user leaves home
  - Faulty automations
  - Serious system problems

**Example:** "Send me a notification: Hang up laundry"

More details: [Notifications](notifications.md)
