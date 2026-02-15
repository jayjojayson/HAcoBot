"""Schalter für HAcoBot Funktionen."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, FEATURE_SWITCHES

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Erstellt die Funktions-Schalter."""
    switches = []
    for key, label in FEATURE_SWITCHES.items():
        # Überspringe Kategorie-Header (beginnen mit "_cat_")
        if key.startswith("_cat_"):
            continue
        switches.append(HAcoBotFeatureSwitch(entry, key, label))
    
    async_add_entities(switches)

class HAcoBotFeatureSwitch(SwitchEntity, RestoreEntity):
    """Ein Schalter um eine HAcoBot Funktion zu aktivieren/deaktivieren."""

    def __init__(self, entry, feature_key, feature_label):
        self._entry_id = entry.entry_id
        self._feature_key = feature_key
        self._attr_has_entity_name = True
        self._attr_name = feature_label
        self._attr_unique_id = f"{entry.entry_id}_{feature_key}"
        self._is_on = True # Standardmäßig an

        # Verknüpfung zum Gerät
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "HAcoBot",
        }

    @property
    def is_on(self):
        return self._is_on

    async def async_added_to_hass(self):
        """Zustand wiederherstellen nach Neustart."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state:
            self._is_on = last_state.state == "on"

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        self.async_write_ha_state()
        