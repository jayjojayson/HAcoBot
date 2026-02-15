# Dashboard Designer

HAcoBot can generate YAML code for Lovelace dashboards.  
The generated files are saved under the following path: `/config/HAcoBot/Dashboard-Cards/`

## Commands

Examples of voice or chat commands:

- "Create a card for my office with light and heating."
- "Create a sun-position-card."

## Features

### Stacks
- Automatically uses `vertical-stack` or `horizontal-stack` for groupings

### Custom Cards
- Supports cards from HACS  
  e.g. `mini-graph-card`

### Intelligence
- Independently searches for suitable entities from your system
- Takes room and device names into account

## The HAcoBot Card (Frontend)

The integration comes with a special **Chat Card** for your dashboard.

### Adding

1. **Dashboard → Edit → Add Card**
2. Search for **"HAcoBot Chat"**

If the card is not found:
- Clear browser cache (**CTRL + F5**)
- or add manually with:

```yaml
type: custom:hacobot-card
```
