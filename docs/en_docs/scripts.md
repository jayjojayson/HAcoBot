# Script Manager

HAcoBot can create and manage Home Assistant Scripts directly via chat or voice.

## What are Scripts?

Scripts are **action sequences without triggers or conditions**. They are ideal for manual actions that you want to execute at the push of a button or via voice command.

**Examples:**
- "Good Night Routine" (Lights off, shutters down, alarm armed)
- "Make Coffee" (Coffee machine on, light in kitchen on)
- "Movie Night" (TV on, dim light, turn on soundbar)

## Creating Scripts

### Via Chat/Voice

Simply say:

> "Create a script for my good night routine"

> "Create a script: Turn off the living room light and lower the shutters"

HAcoBot automatically creates the script with valid YAML syntax and uses the appropriate entities from your system.

### Manual Creation

You can also describe a script yourself:

> "Script 'Morning Routine': Light in kitchen to 80%, coffee machine on, shutters to 100%"

## Deleting Scripts

You can delete individual scripts:

> "Delete the script 'Good Night'"

**Important:** Individual scripts are deleted IMMEDIATELY without confirmation.

If you want to delete ALL scripts, HAcoBot will MANDATORILY ask for confirmation beforehand.

## Technical Details

- Scripts are stored in `/config/scripts.yaml`
- After creation, `script.reload` is called automatically
- Scripts appear as `script.script_name` entities
- They can be used in automations, dashboards, or via service calls

## Example

**User:** "Create a script for Movie Night"

**HAcoBot creates:**
```yaml
movie_night:
  alias: 'Movie Night'
  description: 'Starts the perfect movie night'
  sequence:
    - service: light.turn_off
      target:
        entity_id: light.living_room
    - service: media_player.turn_on
      target:
        entity_id: media_player.tv_living_room
    - service: light.turn_on
      target:
        entity_id: light.ambient
      data:
        brightness_pct: 20
```

**Usage:**
After creation, you can execute the script with:
- Dashboard button
- Voice command: "Start Movie Night"
- Automation
- Service Call: `script.movie_night`
