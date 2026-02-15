<img width="100%" height="auto" alt="HAcoBot" src="https://github.com/jayjojayson/HAcoBot/blob/main/docs/images/HAcoBot_1024.png" />

# HAcoBot – Home Assistant Command Bot 🤖

HAcoBot is an advanced, **AI-powered admin & command agent** for Home Assistant.  
It integrates natively into the **Assist chat interface** and allows you to not only control your smart home, but also **administer, analyze, and evolve it**.

Unlike traditional voice assistants, HAcoBot features:

- Access to **system-level tools**
- **Short-term and long-term memory**
- **Proactive reasoning**
- Its own **custom Lovelace dashboard card**

HAcoBot is not just a chatbot — it is a **true Home Assistant admin agent**.

> ⚠️ **Status:** Beta  
> Core functionality is available. In some cases HAcoBot may ask follow-up questions or abort actions.  
> Knowledge and preferences can already be stored persistently.

---

## ✨ Features

### 🧠 Multi-LLM Support
Choose your preferred AI provider:

- **Google Gemini** (Recommended: `gemini-2.0-flash`)
- **OpenAI ChatGPT** (`gpt-4o`)
- **Groq** (High-speed inference)
- **DeepSeek** (Coding specialist)
- **OpenRouter** (Access to many models with one key)
- **Ollama** (Local, private & free via custom URL)


### 💾 Long-Term Memory & Learning
HAcoBot can remember information **across conversations**, for example:

- “My name is Jan”
- “I don’t want updates on Sundays”

**Technical details:**
- Local storage at  
  `/config/HAcoBot/hacobot_memory.json`
- Fully **user-controlled**
- Can be disabled or cleared at any time


### 🧠 Short-Term Memory
Remembers the current conversation context for:

- Multi-step instructions
- Follow-up questions
- Natural, fluid dialogs


### 🛡️ Modular Control (Feature Switches)
You decide **what HAcoBot is allowed to do**.  
Each capability can be enabled or disabled individually:

- **Updates & Maintenance**  
  Lists updates and installs them **only on explicit command**
- **System Restart**  
  Critical function, protected separately
- **Live Control**  
  Lights, switches, covers, scenes, scripts
- **To-Do Lists & Calendars**  
  Create, modify, delete entries
- **Dashboard Designer**  
  Generates complete Lovelace YAML
- **Script Manager**  
  Create and manage Home Assistant scripts
- **Scene Manager**  
  Create and manage scenes
- **Notifications & Alerts**  
  Send notifications and receive proactive warnings
- **HAcoBot Thinks Ahead**  
  Enables memory & proactive anomaly detection
- **Diagnostics & Briefing**  
  System, weather & log analysis


### ⚙️ Automation & Blueprint Manager
- Create complex automations via chat
- Generate full **Blueprints with inputs & selectors**
- Delete outdated or broken automations
- Get overviews of your automations & blueprints


### 🎨 Dashboard Designer
Just say:

> “Create a card for my living room with lights and temperature”

HAcoBot generates **fully working YAML**, including:

- Vertical / Horizontal stacks
- Tile cards
- Custom cards (e.g. `mini-graph-card`, `sun-position-card`)
- Smart entity selection & layout

📁 Stored in:  
`/config/HAcoBot/Dashboard-Cards/`


### 📡 Live Device Control
Control your devices using natural language:

- `light.turn_on`
- `cover.set_position`
- Switches, scenes, scripts, and more


### 📅 Calendar & To-Do Power Features
- Read and selectively delete calendar events
- To-do lists:
  - Add items
  - Mark as done
  - Permanently remove entries


### 📜 Script Manager
- Create Home Assistant scripts via chat or voice
- Action sequences without triggers (e.g., "Good Night Routine")
- Delete individual scripts or all scripts (with confirmation)


### 🎬 Scene Manager
- Create scenes (snapshots of entity states)
- Examples: Cinema Mode, Relaxing, Working
- Activate scenes via voice or automation


### 🔔 Notifications & Alerts
- Send notifications to mobile apps or persistent notifications
- Proactive warnings:
  - Critical batteries (< 20%)
  - Open windows/doors when user leaves home
  - Faulty automations
  - Critical system problems


### 🔍 Proactive Diagnostics & Briefing
Ask things like:

- **“Status report”**
- **“Briefing”**
- **“System report”**

HAcoBot analyzes:

- Weather & forecast (including attributes)
- Pending updates
- Error logs (`home-assistant.log`)
- Unavailable (“dead”) entities
- Low or critical batteries
- Hidden sensor attributes (e.g. cell voltages)

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

1. simply follow the Link to integrate this repository to HACS  
 [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jayjojayson&repository=hass-victron-vrm-api&category=integration)

3. go to `Settings -> Devices and Services -> Integration`
4. click on `Add Integration`
5. search for `HAcoBot`
6. install the integration
7. restart Home Assistant 

### Manual via HACS (not recommended)

1. install the HACS integration in Home Assistant
2. go to **HACS → Integrations → Custom repositories**
3. add the repository URL: `https://github.com/jayjojayson/HAcoBot`
4. install the integration

### Manual (not recommended)

1. download the repository  
2. copy the folder  
   `custom_components/hacobot`  
   to  
   `/config/custom_components/`
3. restart Home Assistant
4. go to `Settings -> Devices and Services -> Integration`
5. click on `Add Integration`
6. search for `HAcoBot`
7. install the integration
8. restart Home Assistant 

---

## ⚙️ Configuration (Backend)

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **HAcoBot**
3. Select your AI provider (e.g. Google Gemini)
4. Enter your API key  
   *(for Ollama: any value, but not empty)*
5. *(Optional)* Select the model
6. *(Ollama)* Enter your local URL  
   e.g. `http://192.168.1.10:11434/v1`

---

## 🖥️ Dashboard Card (Frontend)

HAcoBot ships with its own **chat dashboard card** 🎉

1. Clear browser cache (`CTRL + F5`)
2. Dashboard → **Add card**
3. Select **HAcoBot Chat**  
   or add manually:

```yaml
type: custom:hacobot-card
