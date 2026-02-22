# To-Do Lists & Calendar

HAcoBot has access to your Home Assistant To-Do lists and calendar.

## To-Do Lists

The bot distinguishes precisely between **Completing (Checking off)** and **Deleting (Removing)**.

### Viewing
- "What's on the shopping list?"

### Adding
- "Add butter to the shopping list."

### Checking off
- "Cross milk off the list."  
  (marks the entry as done)

### Deleting
- "Delete bread from the list."  
  (removes the entry completely)

## Calendar

### Querying
- "Do I have appointments today?"

### Deleting
- "Delete the dentist appointment."

> **Note:**  
> The bot first searches for the matching appointment to determine the internal ID, and then deletes it specifically.
