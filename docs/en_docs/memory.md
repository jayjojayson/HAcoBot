# Long-Term Memory

HAcoBot has a **persistent memory**.  
This means it does not forget information when you close the chat window or restart Home Assistant.

## How does it work?

The bot stores facts in a JSON file: `/config/HAcoBot/hacobot_memory.json`

This file is:
- **Readable** for you
- **Editable** (in FileExplorer)
- Permanently stored

## What is stored?

### User Facts
- Your name, if you tell HAcoBot
- Personal preferences  
  e.g. "I don't want a briefing notification in the sidebar (HA)"
  e.g. "I don't like updates on weekends"

### System Notes
- Information the bot has learned about your installation
- Relevant context for better decisions

## Privacy

- All data remains **local** on your Home Assistant server
- If you delete the integration, this folder will also be automatically cleaned up
