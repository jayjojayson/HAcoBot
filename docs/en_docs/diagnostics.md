# Diagnostics & Briefing

HAcoBot acts as your personal **System Administrator** for Home Assistant.

## The Briefing

Simply ask for:

- "What's the status?"
- "Briefing"
- "Report"

The bot generates a compact overview consisting of:

### Weather
- Current condition
- Temperature  
  (directly from entity attributes)

### Updates
- List of available updates:
  - Home Assistant Core
  - Add-ons
  - HACS

### System Status
- Analysis of `home-assistant.log`
- Detection of:
  - Errors
  - Warnings

## Proactive Warnings

When the mode **"HAcoBot thinks ahead"** is activated, the bot scans in the background for:

- "Dead" devices  
  (Status `unavailable`)
- Empty batteries  
  (< 20 %)

In case of critical problems, HAcoBot can automatically create a **Notification in Home Assistant**.
