# Feature Switches (Security)

After installation, a **HAcoBot** device is created in Home Assistant.  
There you will find switches (entities) that allow you to specifically **revoke or allow rights** to the bot.

This is for security:  
You can, for example, allow the bot to build dashboards, but forbid it from switching devices or restarting the system.

## Overview of Switches

### Updates & Maintenance
- May list updates
- May install updates on command

### System Restart
- May execute `homeassistant.restart`
- **Critical!** Should only be activated when needed

### Live Control
- May control devices, e.g.:
  - `light`
  - `switch`
  - `cover`
  - `climate`
  - other entities

### To-Do List Manager
- May read To-Do lists
- May add, check off, and delete entries

### Calendar Manager
- May read calendar entries
- May delete appointments

### Dashboard Designer
- May create YAML files for dashboards

### Automation & Blueprints
- May create automations
- May delete automations and blueprints

### Diagnostics & Briefing
- May read logs
- May analyze system status

### HAcoBot Thinks Ahead
- Activates long-term memory
- Activates proactive background scans
