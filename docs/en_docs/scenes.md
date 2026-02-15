# Scene Manager

HAcoBot can create and manage Home Assistant Scenes directly via chat or voice.

## What are Scenes?

Scenes are **snapshots of entity states**. They store the desired states of lights, switches, air conditioners, etc. and restore them at the push of a button.

**Examples:**
- "Cinema Mode" (Light off, TV on, Soundbar loud)
- "Relax" (Light dimmed, soft colors, quiet music)
- "Work" (Light bright, desk lamp on, distractions off)
- "Romantic" (Candles on, main light off, quiet music)

## Creating Scenes

### Via Chat/Voice

Simply say:

> "Create a scene for Cinema Mode"

> "Create a scene 'Relax': Living room light at 30%, color warm white"

HAcoBot automatically creates the scene and uses the appropriate entities from your system.

### Detailed Scene

You can also define multiple entities at once:

> "Scene 'Work': Desk lamp 100%, living room light off, floor lamp 80%"

## Deleting Scenes

You can delete individual scenes:

> "Delete the scene 'Cinema Mode'"

**Important:** Individual scenes are deleted IMMEDIATELY without confirmation.

If you want to delete ALL scenes, HAcoBot will MANDATORILY ask for confirmation beforehand.

## Activating Scenes

After creation, you can activate your scenes at any time:

> "Activate Cinema Mode"

> "Turn on scene Relax"

## Technical Details

- Scenes are stored in `/config/scenes.yaml`
- After creation, `scene.reload` is called automatically
- Scenes appear as `scene.scene_name` entities
- They can be used in automations, dashboards, or via service calls

## Example

**User:** "Create a scene for Romantic Evening"

**HAcoBot creates:**
```yaml
- id: 'romantic_evening'
  name: 'Romantic Evening'
  entities:
    light.living_room:
      state: off
    light.candles:
      state: on
      brightness: 180
      color_temp: 400
    media_player.sonos:
      state: playing
      volume_level: 0.3
```

**Usage:**
After creation, you can activate the scene with:
- Dashboard button
- Voice command: "Activate Romantic Evening"
- Automation
- Service Call: `scene.turn_on` with `entity_id: scene.romantic_evening`

## Difference to Scripts

| Feature | Scene | Script |
| :--- | :--- | :--- |
| **Purpose** | Restore states | Execute actions |
| **Structure** | Entity states | Action sequence |
| **Example** | Light at 50%, color blue | Turn on light, wait 5s, turn off light |
| **Usage** | Fixed state | Dynamic flows |

**Rule of thumb:** Use Scenes for "static states" and Scripts for "dynamic flows".
