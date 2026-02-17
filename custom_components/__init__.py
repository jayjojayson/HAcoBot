"""Die HAcoBot Integration."""
import logging
import os
import shutil
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.helpers import config_validation as cv, device_registry as dr, storage
from homeassistant.components import conversation
from homeassistant.components.http import StaticPathConfig
from homeassistant.util import ulid
import voluptuous as vol

from .const import DOMAIN, CONF_API_KEY, CONF_MODEL, DEFAULT_MODEL, FEATURE_SWITCHES
from .agent import HAcoBotAgent

_LOGGER = logging.getLogger(__name__)

# WICHTIG: Nur 'switch' laden. 'conversation' machen wir manuell.
PLATFORMS = ["switch"]
# Name des Hauptordners im Config-Verzeichnis
DATA_DIR = "HAcoBot"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Richtet die Integration über einen Config Entry ein."""
    
    api_key = entry.data[CONF_API_KEY]
    model = entry.options.get(CONF_MODEL, entry.data.get(CONF_MODEL, DEFAULT_MODEL))

    # 1. Agent initialisieren
    agent = HAcoBotAgent(hass, entry, api_key, model)
    # WICHTIG: Asynchrone Initialisierung abwarten (löst den Blocking Call Fehler)
    await agent.async_initialize()
    
    conversation.async_set_agent(hass, entry, agent)
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = agent

    # 2. Statischen Web-Pfad registrieren
    component_path = os.path.dirname(__file__)
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            "/hacobot",
            os.path.join(component_path, "www"),
            cache_headers=False
        )
    ])

    # 3. Gerät in der Registry anlegen
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name="HAcoBot",
        manufacturer="Jayjojayson",
        model="HAcoBot",
        sw_version="2.7.0",
    )

    # 4. Plattformen (Schalter) laden
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # 5. Service registrieren
    async def handle_process_prompt(call: ServiceCall) -> dict:
        prompt = call.data.get("prompt")
        # ConversationInput benötigt zwingend alle Argumente (auch satellite_id seit 2024.x)
        fake_input = conversation.ConversationInput(
            text=prompt,
            context=call.context,
            conversation_id=ulid.ulid(),
            device_id=None,
            language="de",
            agent_id=entry.entry_id,
            #  satellite_id muss übergeben werden (None ist ok), sonst gibt es den __init__ Fehler
            satellite_id=None 
        )
        result = await agent.async_process(fake_input)
        response_text = result.response.speech.get('plain', {}).get('speech', '')
        
        return {
            "response": response_text
        }
        
    hass.services.async_register(
        DOMAIN, 
        "process_prompt", 
        handle_process_prompt, 
        schema=vol.Schema({vol.Required("prompt"): cv.string}),
        supports_response=SupportsResponse.ONLY
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entlädt die Integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        conversation.async_unset_agent(hass, entry)
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Wird aufgerufen, wenn die Integration vom User gelöscht wird."""
    def remove_data_dir():
        dir_path = hass.config.path(DATA_DIR)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                _LOGGER.info(f"HAcoBot Ordner erfolgreich gelöscht: {dir_path}")
            except Exception as e:
                _LOGGER.error(f"Fehler beim Löschen des HAcoBot Ordners: {e}")

    await hass.async_add_executor_job(remove_data_dir)
    