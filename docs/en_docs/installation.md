# Installation

### HACS

1. Simply follow the link to add this repository to HACS:
 [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jayjojayson&repository=hass-victron-vrm-api&category=integration)
2. Go to `Settings -> Devices & Services -> Integrations`
3. Click on `Add Integration`
4. Search for `HAcoBot`
5. Install the integration
6. Restart Home Assistant

### Manual via HACS (not recommended)

1. Install HACS in Home Assistant
2. Go to **HACS → Integrations → Custom repositories**
3. Add the repository URL: `https://github.com/jayjojayson/HAcoBot`
4. Install the integration

### Manual (not recommended)

1. Download the repository
2. Copy the folder
   `custom_components/hacobot`
   to
   `/config/custom_components/`
3. Restart Home Assistant
4. Go to `Settings -> Devices & Services -> Integrations`
5. Click on `Add Integration`
6. Search for `HAcoBot`
7. Install the integration
8. Restart Home Assistant

## Important: Clear Browser Cache

Since HAcoBot comes with its own dashboard card, **you must clear the browser cache after restarting**, so that the JavaScript files are loaded correctly.

- Key combination: **CTRL + F5**

> **Note:**
> If the integration does not appear in the list, clear the browser cache again and reload the page.
