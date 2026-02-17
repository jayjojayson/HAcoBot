"""Die KI Logik für den HAcoBot."""
import json
import os
import logging
import datetime
from openai import AsyncOpenAI
from homeassistant.core import HomeAssistant
from homeassistant.components import conversation
from homeassistant.helpers import intent, entity_registry, storage
from homeassistant.util import ulid, dt as dt_util

from .const import (
    BLUEPRINT_PATH, 
    CONF_PROVIDER, 
    CONF_URL,
    PROVIDER_GOOGLE, 
    PROVIDER_OPENAI, 
    PROVIDER_GROQ, 
    PROVIDER_DEEPSEEK,
    PROVIDER_OLLAMA,
    PROVIDER_OPENROUTER,
    DOMAIN
)

from .prompts import (
    get_base_rules,
    get_working_mode,
    get_intent_priority,
    get_entity_search_rules,
    get_response_format,
    get_proactive_prompt,
    get_info_prompt,
    get_updates_prompt,
    get_todo_prompt,
    get_calendar_prompt,
    get_control_prompt,
    get_system_prompt,
    get_dashboard_prompt,
    get_automation_prompt,
    get_scripts_prompt,
    get_scenes_prompt,
    get_notify_prompt,
    get_scheduling_prompt,
    get_tool_definitions
)

_LOGGER = logging.getLogger(__name__)
DASHBOARD_PATH = "dashboard_drafts"
STORAGE_KEY = "hacobot.memory"
STORAGE_VERSION = 1

class HAcoBotAgent(conversation.AbstractConversationAgent):
    """Der HAcoBot (Home Assistant Command Bot)."""

    def __init__(self, hass: HomeAssistant, entry, api_key: str, model_name: str):
        self.hass = hass
        self.entry = entry
        self.model_name = model_name
        self.api_key = api_key  # WICHTIG: Speichern für spätere Init
        self.provider = entry.data.get(CONF_PROVIDER, PROVIDER_GOOGLE)
        self.custom_url = entry.data.get(CONF_URL)
        self.history = {}
        
        # Persistenter Speicher
        self.root_path = hass.config.path("HAcoBot")
        self.dashboard_path = os.path.join(self.root_path, "Dashboard-Cards")
        self.memory_file = os.path.join(self.root_path, "hacobot_memory.json")
        self._store = storage.Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._memory_data = {} 
        self.remove_listener = None
        
        # WICHTIG: Client auf None setzen (verhindert Blocking Call in __init__)
        self.client = None 

        _LOGGER.info(f"HAcoBot vorbereitet mit Provider: {self.provider}")

    async def async_initialize(self):
        """Initialisiert den OpenAI Client im Executor (verhindert Blocking Calls)."""
        def _create_client():
            if self.provider == PROVIDER_GOOGLE:
                return AsyncOpenAI(api_key=self.api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
            elif self.provider == PROVIDER_OPENAI:
                return AsyncOpenAI(api_key=self.api_key)
            elif self.provider == PROVIDER_GROQ:
                return AsyncOpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
            elif self.provider == PROVIDER_DEEPSEEK:
                return AsyncOpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
            elif self.provider == PROVIDER_OLLAMA:
                base_url = self.custom_url if self.custom_url else "http://localhost:11434/v1"
                return AsyncOpenAI(api_key=self.api_key if self.api_key else "ollama", base_url=base_url)
            elif self.provider == PROVIDER_OPENROUTER:
                return AsyncOpenAI(api_key=self.api_key, base_url="https://openrouter.ai/api/v1")
            else:
                return AsyncOpenAI(api_key=self.api_key)

        # Hier passiert die Magie: Ausführung im Thread-Pool
        self.client = await self.hass.async_add_executor_job(_create_client)
        _LOGGER.info("HAcoBot Client erfolgreich initialisiert.")

    @property
    def supported_languages(self):
        return ["de", "en"]

    async def _load_memory(self):
        """Lädt das Langzeitgedächtnis."""
        def load():
            if not os.path.exists(self.dashboard_path):
                os.makedirs(self.dashboard_path, exist_ok=True)
            
            if os.path.exists(self.memory_file):
                try:
                    with open(self.memory_file, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception as e:
                    _LOGGER.error(f"Fehler beim Laden des Gedächtnisses: {e}")
                    return {"user_facts": {}, "system_notes": []}
            else:
                return {"user_facts": {}, "system_notes": [], "scheduled_tasks": []}

        self._memory_data = await self.hass.async_add_executor_job(load)
        
        # Ensure correct data types
        if not isinstance(self._memory_data, dict):
             self._memory_data = {}

        if "user_facts" not in self._memory_data or not isinstance(self._memory_data["user_facts"], dict):
            self._memory_data["user_facts"] = {}

        if "system_notes" not in self._memory_data or not isinstance(self._memory_data["system_notes"], list):
            self._memory_data["system_notes"] = []

        if "scheduled_tasks" not in self._memory_data or not isinstance(self._memory_data["scheduled_tasks"], list):
            self._memory_data["scheduled_tasks"] = []
            
        # Start background check if not running
        if not self.remove_listener:
             from homeassistant.helpers.event import async_track_time_interval
             self.remove_listener = async_track_time_interval(self.hass, self._check_scheduled_tasks, datetime.timedelta(seconds=60))

    async def _save_memory_to_disk(self):
        """Speichert das Gedächtnis."""
        def save():
            try:
                if not os.path.exists(self.root_path):
                    os.makedirs(self.root_path, exist_ok=True)
                with open(self.memory_file, "w", encoding="utf-8") as f:
                    json.dump(self._memory_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                _LOGGER.error(f"Fehler beim Speichern des Gedächtnisses: {e}")
        await self.hass.async_add_executor_job(save)

    def _is_feature_enabled(self, feature_key):
        """Prüft Feature-Schalter."""
        ent_reg = entity_registry.async_get(self.hass)
        unique_id = f"{self.entry.entry_id}_{feature_key}"
        entity_id = ent_reg.async_get_entity_id("switch", DOMAIN, unique_id)
        if entity_id:
            state = self.hass.states.get(entity_id)
            if state and state.state == "off":
                return False
        return True 

    def _build_memory_context(self, include_scheduled: bool) -> str:
        """Erzeugt den Memory-Block für den System-Prompt."""
        if not self._memory_data:
            return "Keine Einträge."

        user_facts = self._memory_data.get("user_facts", {})
        scheduled = self._memory_data.get("scheduled_tasks", []) if include_scheduled else []

        mem_parts = []
        if user_facts:
            mem_parts.append("FAKTEN:")
            mem_parts.extend([f"- {k}: {v}" for k, v in user_facts.items()])

        system_notes = self._memory_data.get("system_notes", [])
        if system_notes:
            mem_parts.append("VERHALTENSREGELN & NOTIZEN:")
            mem_parts.extend([f"- {note}" for note in system_notes])

        if scheduled:
            mem_parts.append("GEPLANTE AUFGABEN:")
            mem_parts.extend([
                f"- [{i}] {t['time']} {t.get('date', '')}: {t.get('task', t.get('prompt', 'Unbekannt'))}"
                for i, t in enumerate(scheduled)
            ])

        return "\n".join(mem_parts) if mem_parts else "Keine Einträge."

    async def async_process(self, user_input: conversation.ConversationInput) -> conversation.ConversationResult:
        """Verarbeitet den Prompt."""
        
        # Sicherstellen, dass alles geladen ist
        if not self._memory_data:
            await self._load_memory()
            
        if not self.client:
             await self.async_initialize()

        # --- FEATURE FLAGS ---
        feat_proactive = self._is_feature_enabled("proactive")
        feat_updates = self._is_feature_enabled("updates")
        feat_todo = self._is_feature_enabled("todo")
        feat_calendar = self._is_feature_enabled("calendar")
        feat_control = self._is_feature_enabled("control")
        feat_system = self._is_feature_enabled("system_control")
        feat_dashboard = self._is_feature_enabled("dashboard")
        feat_automation = self._is_feature_enabled("automation")
        feat_scripts = self._is_feature_enabled("scripts")
        feat_scenes = self._is_feature_enabled("scenes")
        feat_notify = self._is_feature_enabled("notify")
        feat_info = self._is_feature_enabled("info")
        feat_scheduling = self._is_feature_enabled("proactive") # Tied to proactive or new flag

        # --- KONTEXT BAUEN ---
        states = self.hass.states.async_all()
        entity_list = []
        for state in states:
            eid = state.entity_id
            if eid.startswith("update.") and not feat_updates: continue
            if eid.startswith("todo.") and not feat_todo: continue
            if eid.startswith("calendar.") and not feat_calendar: continue
            if eid.startswith("zone.") or eid.startswith("geo_location."): continue
            
            friendly_name = state.attributes.get("friendly_name", eid)
            entity_info = f"{eid} ({friendly_name}) = {state.state}"
            if unit := state.attributes.get("unit_of_measurement"): entity_info += f" {unit}"
            entity_list.append(entity_info)
            
        context_str = "\n".join(entity_list)
        if len(context_str) > 80000: context_str = context_str[:80000] + "... [truncated]"

        # Memory String
        memory_str = self._build_memory_context(include_scheduled=feat_proactive)

        
        # Build prompt from modular functions
        prompt_parts = []
        prompt_parts.extend(get_base_rules())
        prompt_parts.extend(get_working_mode())
        prompt_parts.extend(get_intent_priority())
        prompt_parts.extend(get_entity_search_rules())
        prompt_parts.extend(get_response_format())
        
        # Add memory section
        prompt_parts.append("LANGZEITGEDÄCHTNIS")
        prompt_parts.append(f"{memory_str}")
        prompt_parts.append("")
        
        # Tool definitions dictionary
        tool_defs = get_tool_definitions()
        tools = []

        # Feature: PROACTIVE
        if feat_proactive:
            prompt_parts.extend(get_proactive_prompt())
            tools.append(tool_defs["manage_memory"])
            tools.append(tool_defs["scan_for_trouble"])
        else:
            prompt_parts.append("HINWEIS: Proaktives Mitdenken ist DEAKTIVIERT.")

        # Feature: DIAGNOSE
        if feat_info:
            prompt_parts.extend(get_info_prompt())
            tools.append(tool_defs["check_system_health"])
            tools.append(tool_defs["get_logs"])
            tools.append(tool_defs["get_entity_infos"])
        else:
            prompt_parts.append("HINWEIS: Diagnose ist DEAKTIVIERT.")

        # Feature: UPDATES
        if feat_updates:
            prompt_parts.extend(get_updates_prompt())
        else:
            prompt_parts.append("HINWEIS: Updates sind DEAKTIVIERT.")
        
        # Feature: TO-DO
        if feat_todo:
            prompt_parts.extend(get_todo_prompt())
            tools.append(tool_defs["list_todo_items"])
        else:
            prompt_parts.append("HINWEIS: To-Do Listen sind DEAKTIVIERT.")

        # Feature: KALENDER
        if feat_calendar:
            prompt_parts.extend(get_calendar_prompt())
            tools.append(tool_defs["list_calendar_events"])
        else:
            prompt_parts.append("HINWEIS: Kalender ist DEAKTIVIERT.")

        # Feature: LIVE CONTROL
        if feat_control:
            prompt_parts.extend(get_control_prompt())
        else:
            prompt_parts.append("HINWEIS: Live Steuerung ist DEAKTIVIERT.")

        # Feature: SYSTEM CONTROL
        if feat_system:
            prompt_parts.extend(get_system_prompt())
        else:
            prompt_parts.append("HINWEIS: System Neustart ist DEAKTIVIERT.")

        # Generic service tool (shared by multiple features)
        if any([feat_control, feat_updates, feat_todo, feat_calendar, feat_system, feat_notify]):
            tools.append(tool_defs["execute_service"])

        # Feature: DASHBOARD
        if feat_dashboard:
            prompt_parts.extend(get_dashboard_prompt())
            tools.append(tool_defs["create_dashboard_file"])
            tools.append(tool_defs["list_custom_cards"])
        else:
            prompt_parts.append("HINWEIS: Dashboard-Erstellung ist DEAKTIVIERT.")

        # Feature: AUTOMATION
        if feat_automation:
            prompt_parts.extend(get_automation_prompt())
            tools.append(tool_defs["create_automation"])
            tools.append(tool_defs["delete_automation"])
            tools.append(tool_defs["create_blueprint"])
            tools.append(tool_defs["delete_blueprint"])
            tools.append(tool_defs["create_backup"])
        else:
            prompt_parts.append("HINWEIS: Automation & Blueprints sind DEAKTIVIERT.")

        # Feature: SCRIPTS
        if feat_scripts:
            prompt_parts.extend(get_scripts_prompt())
            tools.append(tool_defs["create_script"])
            tools.append(tool_defs["delete_script"])
        else:
            prompt_parts.append("HINWEIS: Script Manager ist DEAKTIVIERT.")

        # Feature: SCENES
        if feat_scenes:
            prompt_parts.extend(get_scenes_prompt())
            tools.append(tool_defs["create_scene"])
            tools.append(tool_defs["delete_scene"])
        else:
            prompt_parts.append("HINWEIS: Scene Manager ist DEAKTIVIERT.")

        # Feature: NOTIFY 
        # Feature: NOTIFY 
        if feat_notify:
            prompt_parts.extend(get_notify_prompt())
        else:
            prompt_parts.append("HINWEIS: Benachrichtigungen & Alerts sind DEAKTIVIERT.")

        # Feature: SCHEDULING 
        if feat_scheduling:
            prompt_parts.extend(get_scheduling_prompt())
            tools.append(tool_defs["add_scheduled_task"])
            tools.append(tool_defs["delete_scheduled_task"])
            tools.append(tool_defs["list_scheduled_tasks"])
        else:
            prompt_parts.append("HINWEIS: Scheduling ist DEAKTIVIERT.")

        prompt_parts.append("AKTUELLE ZUSTÄNDE")
        prompt_parts.append("- Diese Liste ist vollständig")
        prompt_parts.append("- Nutze NUR semantisch passende Entities")
        prompt_parts.append(f"\n{context_str}")
        prompt_parts.append("Antworte kurz auf Deutsch.")

        system_prompt = {
            "role": "system",
            "content": "\n".join(prompt_parts)
        }

        # --- RE-ACT LOOP ---
        conversation_id = user_input.conversation_id
        if conversation_id not in self.history: self.history[conversation_id] = []
        if len(self.history[conversation_id]) > 10: self.history[conversation_id] = self.history[conversation_id][-10:]
        current_user_message = {"role": "user", "content": user_input.text}
        messages = [system_prompt] + self.history[conversation_id] + [current_user_message]

        final_speech = "Funktion deaktiviert oder Fehler."
        
        for _ in range(3):
            try:
                t = tools if tools else None
                response = await self.client.chat.completions.create(
                    model=self.model_name, messages=messages, tools=t, tool_choice="auto" if t else None
                )
                
                msg = response.choices[0].message
                tool_calls = msg.tool_calls
                
                if not tool_calls:
                    final_speech = msg.content or "Erledigt."
                    break
                
                messages.append(msg)

                for tool in tool_calls:
                    fname = tool.function.name
                    args = {} 
                    try:
                        if tool.function.arguments:
                            args = json.loads(tool.function.arguments)
                        else:
                            _LOGGER.warning(f"Tool {fname} called with empty arguments string.")
                            res = "Fehler: Leere Argumente für Tool."
                            messages.append({"role": "tool", "tool_call_id": tool.id, "content": str(res)})
                            continue 
                    except json.JSONDecodeError as e:
                        _LOGGER.error(f"Fehler beim Parsen der Argumente für Tool {fname}: {e}")
                        res = f"Fehler: Ungültige Argumente für Tool ({e})."
                        messages.append({"role": "tool", "tool_call_id": tool.id, "content": str(res)})
                        continue 
                    except AttributeError: 
                        _LOGGER.error(f"Fehler: Ungültiger Tool-Aufruf, 'function' oder 'arguments' fehlen.")
                        res = "Fehler: Ungültiger Tool-Aufruf."
                        messages.append({"role": "tool", "tool_call_id": tool.id, "content": str(res)})
                        continue

                    if not isinstance(args, dict):
                        messages.append({"role": "tool", "tool_call_id": tool.id, "content": "Fehler: Argumente müssen ein JSON-Objekt sein."})
                        continue

                    res = "Erfolg."

                    # --- ROUTING MIT HARTER SECURITY ---
                    if fname == "execute_service":
                        domain = args["domain"]
                        service = args["service"]
                        data = args.get("service_data", {})
                        allowed = True
                        denial_reason = ""

                        if domain == "homeassistant" and service in ["restart", "stop"]:
                            if not feat_system: allowed=False; denial_reason="System-Neustart deaktiviert."
                        elif domain == "update" and service == "install":
                            if not feat_updates: allowed=False; denial_reason="Update deaktiviert."
                        elif domain == "todo":
                            if not feat_todo: allowed=False; denial_reason="To-Do deaktiviert."
                        elif domain == "calendar":
                            if not feat_calendar: allowed=False; denial_reason="Kalender deaktiviert."
                        elif not (domain in ["homeassistant", "update", "todo", "calendar"]):
                            if not feat_control: allowed=False; denial_reason="Steuerung deaktiviert."

                        if allowed:
                            try:
                                await self.hass.services.async_call(domain, service, data, blocking=True)
                                res = f"Service {domain}.{service} erfolgreich."
                            except Exception as e: res = f"Fehler: {e}"
                        else: res = f"ABGELEHNT: {denial_reason}"

                    elif fname == "manage_memory":
                        if feat_proactive: res = await self._manage_memory(args["action"], args["key"], args.get("value"))
                        else: res = "ABGELEHNT"
                    elif fname == "scan_for_trouble":
                        if feat_proactive: res = await self._scan_for_trouble()
                        else: res = "ABGELEHNT"
                    elif fname == "check_system_health":
                        if feat_info: res = await self._check_system_health()
                        else: res = "ABGELEHNT."
                    elif fname == "list_todo_items":
                        if feat_todo: res = await self._list_todo_items(args["entity_id"])
                        else: res = "ABGELEHNT."
                    elif fname == "list_calendar_events":
                        if feat_calendar: res = await self._list_calendar_events(args["entity_id"], args.get("duration_hours", 168))
                        else: res = "ABGELEHNT."
                    elif fname == "get_entity_infos":
                        res = await self._get_entity_infos(args["entity_ids"])
                    elif fname == "create_dashboard_file":
                        if feat_dashboard: res = await self._save_dashboard(args["filename"], args["yaml_content"])
                        else: res = "ABGELEHNT."
                    elif fname == "list_custom_cards":
                        if feat_dashboard: res = await self._list_custom_cards()
                        else: res = "ABGELEHNT."
                    elif fname == "get_logs":
                        if feat_info: res = await self._read_logs()
                        else: res = "ABGELEHNT."
                    elif fname == "create_backup":
                        if feat_automation: 
                            if self.hass.services.has_service("backup", "create"): await self.hass.services.async_call("backup", "create", {})
                            elif self.hass.services.has_service("hassio", "backup_full"): await self.hass.services.async_call("hassio", "backup_full", {})
                            res = "Backup gestartet."
                        else: res = "ABGELEHNT."
                    elif fname == "create_automation":
                        if feat_automation: await self._save_automation(args); res = "Erstellt."
                        else: res = "ABGELEHNT."
                    elif fname == "delete_automation":
                        if feat_automation: res = await self._delete_automation(args["alias"])
                        else: res = "ABGELEHNT."
                    elif fname == "create_blueprint":
                        if feat_automation: res = await self._save_blueprint(args["filename"], args["yaml_content"])
                        else: res = "ABGELEHNT."
                    elif fname == "delete_blueprint":
                        if feat_automation: res = await self._delete_blueprint(args["filename"])
                        else: res = "ABGELEHNT."
                    elif fname == "create_script":
                        if feat_scripts: await self._save_script(args); res = "Script erstellt."
                        else: res = "ABGELEHNT."
                    elif fname == "delete_script":
                        if feat_scripts: res = await self._delete_script(args["name"])
                        else: res = "ABGELEHNT."
                    elif fname == "create_scene":
                        if feat_scenes: await self._save_scene(args); res = "Scene erstellt."
                        else: res = "ABGELEHNT."
                    elif fname == "delete_scene":
                        if feat_scenes: res = await self._delete_scene(args["name"])
                        else: res = "ABGELEHNT."
                    elif fname == "add_scheduled_task":
                        if feat_scheduling: res = await self._add_scheduled_task(args["time"], args["task"], args.get("date"), args.get("repeat", "none"))
                        else: res = "ABGELEHNT."
                    elif fname == "delete_scheduled_task":
                        if feat_scheduling: res = await self._delete_scheduled_task(args["index"])
                        else: res = "ABGELEHNT."
                    elif fname == "list_scheduled_tasks":
                        if feat_scheduling: res = await self._list_scheduled_tasks()
                        else: res = "ABGELEHNT."

                    messages.append({"role": "tool", "tool_call_id": tool.id, "content": str(res)})

            except Exception as e:
                _LOGGER.error(f"HAcoBot Error: {e}")
                final_speech = f"Fehler: {str(e)}"
                break
        
        if conversation_id:
            self.history[conversation_id].append(current_user_message)
            self.history[conversation_id].append({"role": "assistant", "content": final_speech})

        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(final_speech)
        return conversation.ConversationResult(response=intent_response, conversation_id=conversation_id)

    # --- MEMORY FUNCTIONS ---
    async def _manage_memory(self, action, key, value=None):
        # Validate memory structure
        if "user_facts" not in self._memory_data or not isinstance(self._memory_data["user_facts"], dict):
             self._memory_data["user_facts"] = {}

        if action == "save":
            self._memory_data["user_facts"][key] = value
            await self._save_memory_to_disk()
            return f"Gespeichert: {key} = {value}"
        elif action == "delete":
            if key in self._memory_data["user_facts"]:
                del self._memory_data["user_facts"][key]
                await self._save_memory_to_disk()
                return f"Gelöscht: {key}"
            return "Key nicht gefunden."
        elif action == "save_note":
            # Sicherstellen, dass die Liste existiert
            if "system_notes" not in self._memory_data: self._memory_data["system_notes"] = []
            
            # Duplikate vermeiden
            if key in self._memory_data["system_notes"]:
                return f"Notiz existiert bereits: {key}"
            
            self._memory_data["system_notes"].append(key)
            await self._save_memory_to_disk()
            return f"Notiz gespeichert: {key}"
            
        elif action == "delete_note":
            if "system_notes" in self._memory_data and key in self._memory_data["system_notes"]:
                self._memory_data["system_notes"].remove(key)
                await self._save_memory_to_disk()
                return f"Notiz gelöscht: {key}"
            return "Notiz nicht gefunden."
            
        return "Unbekannte Aktion."

    async def _save_memory_to_disk(self):
        """Speichert das Gedächtnis in die JSON-Datei."""
        def save():
            try:
                if not os.path.exists(self.root_path):
                    os.makedirs(self.root_path, exist_ok=True)
                with open(self.memory_file, "w", encoding="utf-8") as f:
                    json.dump(self._memory_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                _LOGGER.error(f"Fehler beim Speichern des Gedächtnisses: {e}")
        await self.hass.async_add_executor_job(save)

    async def _scan_for_trouble(self):
        states = self.hass.states.async_all()
        issues = []
        for state in states:
            if state.state in ["unavailable", "unknown"]:
                if "button" in state.entity_id or "scene" in state.entity_id: continue
                issues.append(f"⚠️ {state.attributes.get('friendly_name', state.entity_id)} ist nicht verfügbar.")
            if "battery" in state.attributes.get("device_class", "") or "battery" in state.entity_id:
                try:
                    val = float(state.state)
                    if val < 20: issues.append(f"🔋 {state.attributes.get('friendly_name', state.entity_id)} Batterie kritisch ({val}%)!")
                except: pass
        if not issues: return "Systemscan: Alles okay."
        msg = "\n".join(issues[:10])
        await self.hass.services.async_call("persistent_notification", "create", {"title": "HAcoBot Systemwarnung", "message": msg})
        return f"Probleme gefunden:\n{msg}"

    # --- HILFSFUNKTIONEN ---
    async def _check_system_health(self):
        log_path = self.hass.config.path("home-assistant.log")
        def analyze():
            if not os.path.exists(log_path): return "Kein Log."
            c_err, c_warn = 0, 0
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    for l in f.readlines()[-1000:]:
                        if "ERROR" in l: c_err+=1
                        elif "WARNING" in l: c_warn+=1
            except: pass
            return f"Analyse: {c_err} Fehler, {c_warn} Warnungen."
        return await self.hass.async_add_executor_job(analyze)

    # --- SCHEDULING FUNCTIONS ---
    async def _add_scheduled_task(self, time_str, task, date_str=None, repeat="none"):
        if not date_str:
            # Use local time for default date
            date_str = dt_util.now().strftime("%Y-%m-%d")
        
        self._memory_data["scheduled_tasks"].append({
            "time": time_str,
            "date": date_str,
            "repeat": repeat,
            "task": task
        })
        await self._save_memory_to_disk()
        return f"Aufgabe geplant für {date_str} um {time_str}: {task}"

    async def _delete_scheduled_task(self, index):
        try:
            if 0 <= index < len(self._memory_data["scheduled_tasks"]):
                removed = self._memory_data["scheduled_tasks"].pop(index)
                await self._save_memory_to_disk()
                return f"Gelöscht: {removed['task']}"
            return "Index ungültig."
        except: return "Fehler."

    async def _list_scheduled_tasks(self):
        tasks = self._memory_data.get("scheduled_tasks", [])
        if not tasks: return "Keine geplanten Aufgaben."
        return "\n".join([f"[{i}] {t['time']} {t.get('date','')}: {t.get('task', t.get('prompt', 'Unbekannt'))}" for i, t in enumerate(tasks)])

    async def _check_scheduled_tasks(self, now):
        """Prüft minütlich, ob Aufgaben anstehen."""
        if not self._memory_data: return
        
        tasks = self._memory_data.get("scheduled_tasks", [])
        to_execute = []
        keep = []
        
        # FIX: Use configured timezone
        now_local = dt_util.as_local(now)
        current_time = now_local.strftime("%H:%M")
        current_date = now_local.strftime("%Y-%m-%d")
        
        tasks_changed = False
        
        for t in tasks:
            task_time = t.get("time")
            task_date = t.get("date", current_date)
            task_msg = t.get("task", t.get("prompt", "Erinnerung"))
            repeat = t.get("repeat", "none")
            
            # Helper for comparison
            is_today = (task_date == current_date)
            is_past_date = (task_date < current_date)
            
            # Execute if:
            # 1. It is today and time is reached or passed (catch-up)
            # 2. It was in the past (catch-up if not too old? For now, just execute one-offs)
            
            should_execute = False
            
            if is_today and task_time <= current_time:
                should_execute = True
            elif is_past_date:
                should_execute = True
                
            if should_execute:
                to_execute.append(task_msg)
                tasks_changed = True
                
                # Handle Recurrence
                if repeat == "daily":
                    # Reschedule to tomorrow (relative to NOW, or relative to task time?)
                    # If we catch up a task from 3 days ago, we want it for tomorrow relative to TODAY.
                    next_date = (now_local + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    t["date"] = next_date
                    keep.append(t)
                else:
                    # One-off: do not keep
                    pass
            else:
                # Future task
                keep.append(t)
        
        # Update memory if changed
        if tasks_changed:
            self._memory_data["scheduled_tasks"] = keep
            await self._save_memory_to_disk()
            
        # Execute tasks
        for msg in to_execute:
             await self.hass.services.async_call(
                 "persistent_notification", "create", 
                 {"title": "HAcoBot Erinnerung", "message": f"Erinnerung: {msg}"}
             )
             # Optional: Try to execute as command?
             # For now, just notify as requested ("erinnert mich").

    async def _list_todo_items(self, eid):
        try:
            r = await self.hass.services.async_call("todo", "get_items", {"entity_id": eid}, blocking=True, return_response=True)
            if r and eid in r:
                return "Inhalt:\n" + "\n".join([f"- {i['summary']}" for i in r[eid].get('items', [])])
            return "Leer/Fehler."
        except Exception as e: return str(e)

    async def _list_calendar_events(self, eid, dur):
        try:
            s = dt_util.now(); e = s + datetime.timedelta(hours=dur)
            r = await self.hass.services.async_call("calendar", "get_events", {"entity_id": eid, "start_date_time": s.isoformat(), "end_date_time": e.isoformat()}, blocking=True, return_response=True)
            if r and eid in r:
                return "\n".join([f"- {ev['start']}: {ev['summary']} (UID: {ev.get('uid')})" for ev in r[eid].get('events', [])])
            return "Keine Termine."
        except Exception as e: return str(e)

    async def _get_entity_infos(self, eids):
        res = []
        for eid in eids:
            s = self.hass.states.get(eid)
            if s: res.append(f"{eid}: {s.state} {json.dumps(dict(s.attributes), default=str, ensure_ascii=False)}")
        return "\n".join(res)

    async def _save_dashboard(self, fn, ct):
        if not fn.endswith(".yaml"): fn+=".yaml"
        fp = os.path.join(self.dashboard_path, fn)
        
        # Sicherstellen, dass Dashboard-Ordner existiert (bereits in __init__ aber zur Sicherheit)
        if not os.path.exists(self.dashboard_path):
             os.makedirs(self.dashboard_path, exist_ok=True)

        ct = self._clean_markdown(ct)
        def w():
            with open(fp, "w", encoding="utf-8") as f: f.write(ct)
        await self.hass.async_add_executor_job(w)
        return fp

    async def _list_custom_cards(self):
        """Listet Dateien im /www/community Ordner auf."""
        path = self.hass.config.path("www", "community")
        def scan():
            if not os.path.exists(path): return "Ordner /config/www/community/ nicht gefunden."
            try:
                files = [f for f in os.listdir(path) if f.endswith(".js")]
                return "Gefundene Custom Cards:\n" + "\n".join(files)
            except Exception as e: return f"Fehler beim Lesen: {e}"
        return await self.hass.async_add_executor_job(scan)

    async def _read_logs(self):
        lp = self.hass.config.path("home-assistant.log")
        def r():
            if os.path.exists(lp):
                with open(lp, "r", encoding="utf-8", errors="ignore") as f: return "".join(f.readlines()[-20:])
            return "No Log."
        return await self.hass.async_add_executor_job(r)

    async def _delete_automation(self, alias):
        fp = self.hass.config.path("automations.yaml")
        def p():
            with open(fp,"r") as f: l=f.readlines()
            nl, buf, d = [], [], False
            for line in l:
                if line.strip().startswith("- ") and not line.startswith("  "):
                    if buf: 
                        if f"alias: '{alias}'" in "".join(buf) or f"alias: {alias}" in "".join(buf): d=True
                        else: nl.extend(buf)
                    buf=[line]
                else: buf.append(line)
            if buf:
                if f"alias: '{alias}'" in "".join(buf) or f"alias: {alias}" in "".join(buf): d=True
                else: nl.extend(buf)
            if d:
                with open(fp,"w") as f: f.writelines(nl)
                return True
            return False
        if await self.hass.async_add_executor_job(p):
            await self.hass.services.async_call("automation", "reload", {})
            return "Gelöscht."
        return "Nicht gefunden."

    async def _delete_blueprint(self, fn):
        fp = self.hass.config.path(BLUEPRINT_PATH, fn + (".yaml" if not fn.endswith(".yaml") else ""))
        def r():
            if os.path.exists(fp): os.remove(fp); return True
            return False
        if await self.hass.async_add_executor_job(r):
            await self.hass.services.async_call("automation", "reload", {})
            return "Gelöscht."
        return "Nicht gefunden."

    async def _save_automation(self, args):
        uid = ulid.ulid()
        fp = self.hass.config.path("automations.yaml")
        t, c, a = self._clean_indent(args['trigger']), self._clean_indent(args.get('condition','[]')), self._clean_indent(args['action'])
        mode_val = args.get('mode', 'single')
        b = f"- id: '{uid}'\n  alias: '{args['alias']}'\n  description: '{args.get('description','')}'\n  trigger:\n{t}\n  condition:\n{c}\n  action:\n{a}\n  mode: {mode_val}\n"
        def w():
            mode = "a"
            if os.path.exists(fp):
                with open(fp,"r") as f: 
                    if f.read().strip()=="[]": mode="w"
            with open(fp, mode) as f:
                if mode=="a" and os.path.getsize(fp)>0: f.write("\n")
                f.write(b)
        await self.hass.async_add_executor_job(w)
        await self.hass.services.async_call("automation", "reload", {})

    async def _save_blueprint(self, fn, ct):
        ct = self._clean_markdown(ct)
        if "blueprint:" in ct: ct = ct[ct.find("blueprint:"):]
        fp = self.hass.config.path(BLUEPRINT_PATH, fn + (".yaml" if not fn.endswith(".yaml") else ""))
        if not os.path.exists(os.path.dirname(fp)): os.makedirs(os.path.dirname(fp))
        def w():
            with open(fp, "w") as f: f.write(ct)
        await self.hass.async_add_executor_job(w)
        await self.hass.services.async_call("automation", "reload", {})
        return fp

    def _clean_markdown(self, t):
        t=t.strip()
        if "```" in t:
            p = t.split("```")
            if len(p)>1:
                c=p[1].strip()
                if c.lower().startswith("yaml"): c=c[4:].strip()
                return c
        return t

    def _clean_indent(self, t):
        t = self._clean_markdown(t)
        for k in ["trigger:","action:","condition:","sequence:"]:
            if t.lower().startswith(k): t=t[len(k):].strip()
        return "\n".join(["    "+l for l in t.split('\n') if l.strip()])

    # --- SCRIPT HANDLERS ---
    async def _save_script(self, args):
        """Erstellt ein HA Script."""
        script_id = args["name"].lower().replace(" ", "_").replace("-", "_")
        fp = self.hass.config.path("scripts.yaml")
        
        sequence = self._clean_indent(args['sequence'])
        
        # Script-Format:
        script_block = f"{script_id}:\n  alias: '{args['alias']}'\n  description: '{args.get('description', '')}'\n  sequence:\n{sequence}\n"
        
        def write():
            mode = "a"
            if os.path.exists(fp):
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content == "{}" or content == "":
                        mode = "w"
            with open(fp, mode, encoding="utf-8") as f:
                if mode == "a" and os.path.exists(fp) and os.path.getsize(fp) > 0:
                    f.write("\n")
                f.write(script_block)
        
        await self.hass.async_add_executor_job(write)
        await self.hass.services.async_call("script", "reload", {})

    async def _delete_script(self, name):
        """Löscht ein HA Script."""
        script_id = name.lower().replace(" ", "_").replace("-", "_")
        fp = self.hass.config.path("scripts.yaml")
        
        def parse():
            if not os.path.exists(fp):
                return False
                
            with open(fp, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines, buffer, deleted = [], [], False
            current_script = None
            
            for line in lines:
                # Neues Script beginnt (keine Einrückung, enthält :)
                if line and not line.startswith(" ") and ":" in line:
                    if buffer:
                        # Vorherigen Buffer prüfen
                        if current_script == script_id:
                            deleted = True
                        else:
                            new_lines.extend(buffer)
                    buffer = [line]
                    current_script = line.split(":")[0].strip()
                else:
                    buffer.append(line)
            
            # Letzten Buffer verarbeiten
            if buffer:
                if current_script == script_id:
                    deleted = True
                else:
                    new_lines.extend(buffer)
            
            if deleted:
                with open(fp, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                return True
            return False
        
        if await self.hass.async_add_executor_job(parse):
            await self.hass.services.async_call("script", "reload", {})
            return "Script gelöscht."
        return "Script nicht gefunden."

    # --- SCENE HANDLERS ---
    async def _save_scene(self, args):
        """Erstellt eine HA Scene."""
        scene_id = args["name"].lower().replace(" ", "_").replace("-", "_")
        fp = self.hass.config.path("scenes.yaml")
        
        entities = self._clean_indent(args['entities'])
        
        # Scene-Format:
        scene_block = f"- id: '{scene_id}'\n  name: '{args['name']}'\n  entities:\n{entities}\n"
        
        def write():
            mode = "a"
            if os.path.exists(fp):
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content == "[]" or content == "":
                        mode = "w"
            with open(fp, mode, encoding="utf-8") as f:
                if mode == "a" and os.path.exists(fp) and os.path.getsize(fp) > 0:
                    f.write("\n")
                f.write(scene_block)
        
        await self.hass.async_add_executor_job(write)
        await self.hass.services.async_call("scene", "reload", {})

    async def _delete_scene(self, name):
        """Löscht eine HA Scene."""
        scene_id = name.lower().replace(" ", "_").replace("-", "_")
        fp = self.hass.config.path("scenes.yaml")
        
        def parse():
            if not os.path.exists(fp):
                return False
                
            with open(fp, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines, buffer, deleted = [], [], False
            in_scene = False
            
            for line in lines:
                # Neue Scene beginnt mit "- id:" oder "- name:"
                if line.strip().startswith("- "):
                    if buffer:
                        # Vorherigen Buffer prüfen
                        buffer_str = "".join(buffer)
                        if f"id: '{scene_id}'" in buffer_str or f"name: '{name}'" in buffer_str:
                            deleted = True
                        else:
                            new_lines.extend(buffer)
                    buffer = [line]
                    in_scene = True
                elif in_scene:
                    buffer.append(line)
            
            # Letzten Buffer verarbeiten
            if buffer:
                buffer_str = "".join(buffer)
                if f"id: '{scene_id}'" in buffer_str or f"name: '{name}'" in buffer_str:
                    deleted = True
                else:
                    new_lines.extend(buffer)
            
            if deleted:
                with open(fp, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                return True
            return False
        
        if await self.hass.async_add_executor_job(parse):
            await self.hass.services.async_call("scene", "reload", {})
            return "Scene gelöscht."
        return "Scene nicht gefunden."
        