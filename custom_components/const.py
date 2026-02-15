"""Konstanten für die HAcoBot Integration."""

DOMAIN = "hacobot"
CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_PROVIDER = "provider"
CONF_URL = "url"

# Anbieter Auswahl
PROVIDER_GOOGLE = "Google Gemini"
PROVIDER_OPENAI = "OpenAI ChatGPT"
PROVIDER_GROQ = "Groq (High Speed)"
PROVIDER_DEEPSEEK = "DeepSeek (Coder)"
PROVIDER_OLLAMA = "Ollama (Lokal/Kostenlos)"
PROVIDER_OPENROUTER = "OpenRouter"

# Standardwerte
DEFAULT_PROVIDER = PROVIDER_GOOGLE
DEFAULT_MODEL = "gemini-2.0-flash"

# Ordner für generierte Inhalte
BLUEPRINT_PATH = "blueprints/automation/hacobot"

# Definition der Funktionen (Key: Label)
# Keys mit "_cat_" Präfix sind Kategorie-Header (werden nicht als Switches erstellt)
FEATURE_SWITCHES = {
    # Automatisierung & Workflows
    "_cat_automation": "═══ Automatisierung & Workflows ═══",
    "automation": "Automation & Blueprints",
    "scripts": "Script Manager",
    "scenes": "Scene Manager",
    "todo": "To-Do Listen Manager",
    "calendar": "Kalender Manager",
    
    # Steuerung & Geräte
    "_cat_control": "═══ Steuerung & Geräte ═══",
    "control": "Live Steuerung (Licht, etc.)",
    "dashboard": "Dashboard Designer",
    
    # System & Wartung
    "_cat_system": "═══ System & Wartung ═══",
    "updates": "Updates & Wartung",
    "system_control": "System Neustart (Kritisch)",
    
    # Analyse & Diagnose
    "_cat_analysis": "═══ Analyse & Diagnose ═══",
    "proactive": "HAcoBot denkt mit (Gedächtnis & Anomalien)",
    "info": "Diagnose & Briefing",
    "notify": "Benachrichtigungen & Alerts",
}