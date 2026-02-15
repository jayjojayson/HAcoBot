"""Config flow für die HAcoBot Integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN, 
    CONF_API_KEY, 
    CONF_MODEL, 
    CONF_PROVIDER,
    CONF_URL,
    PROVIDER_GOOGLE,
    PROVIDER_OPENAI,
    PROVIDER_GROQ,
    PROVIDER_DEEPSEEK,
    PROVIDER_OLLAMA,
    PROVIDER_OPENROUTER,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER
)

class HAcoBotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handhabt den Config Flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Ersteinrichtung."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="HAcoBot", 
                data=user_input
            )

        # Schema: Labels kommen jetzt automatisch aus translations/de.json!
        data_schema = vol.Schema({
            vol.Required(CONF_PROVIDER, default=DEFAULT_PROVIDER): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        PROVIDER_GOOGLE, 
                        PROVIDER_OPENAI,
                        PROVIDER_GROQ,
                        PROVIDER_DEEPSEEK,
                        PROVIDER_OLLAMA,
                        PROVIDER_OPENROUTER
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN
                )
            ),
            # API Key Optional machen (für Ollama), Label kommt aus JSON
            vol.Optional(CONF_API_KEY): str,
            vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): str,
            # URL Feld: Placeholder entfernt, da von HA Selector Config nicht unterstützt
            vol.Optional(CONF_URL): selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.URL)
            ),
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )

    async def async_step_reconfigure(self, user_input=None):
        """Menüpunkt: Neu konfigurieren."""
        errors = {}
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])

        if user_input is not None:
            return self.async_update_reload_and_abort(
                entry,
                data={**entry.data, **user_input},
            )

        current_provider = entry.data.get(CONF_PROVIDER, DEFAULT_PROVIDER)
        current_key = entry.data.get(CONF_API_KEY, "")
        current_model = entry.data.get(CONF_MODEL, DEFAULT_MODEL)
        current_url = entry.data.get(CONF_URL, "")

        data_schema = vol.Schema({
            vol.Required(CONF_PROVIDER, default=current_provider): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        PROVIDER_GOOGLE, 
                        PROVIDER_OPENAI,
                        PROVIDER_GROQ,
                        PROVIDER_DEEPSEEK,
                        PROVIDER_OLLAMA,
                        PROVIDER_OPENROUTER
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN
                )
            ),
            vol.Optional(CONF_API_KEY, description={"suggested_value": current_key}): str,
            vol.Optional(CONF_MODEL, default=current_model): str,
            vol.Optional(CONF_URL, description={"suggested_value": current_url}): selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.URL)
            ),
        })

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=data_schema,
            errors=errors,
        )
        