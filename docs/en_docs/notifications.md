# Notifications & Alerts

HAcoBot can send notifications via various services - via chat, voice, or automatically for important events.

## Available Services

HAcoBot supports all Home Assistant `notify` services:

- **Mobile Apps** (`notify.mobile_app_*`)  
  Notifications to your smartphone (Home Assistant App)
  
- **Persistent Notification** (`notify.persistent_notification`)  
  Notifications in the Home Assistant Frontend

- **Other Services**  
  Telegram, Pushover, E-Mail, etc. (if configured)

## Sending Notifications

### Via Chat/Voice

Simply say:

> "Send me a notification: Living room window is still open"

> "Remind me in 30 minutes: Hang up laundry"

> "Notify me when the washing machine is finished"

HAcoBot automatically uses the appropriate notify service.

### Manual Notification

You can also explicitly specify a service:

> "Send a persistent notification: System update available"

> "Send me a push notification on my phone"

## Parameters

Notifications support the following parameters:

- **message** (Required): The message text
- **title** (Optional): Title of the message
- **data** (Optional): Additional data (e.g. priority, tag, actions)

**Example with Title:**
> "Send notification with title 'Warning': Server room temperature too high"

## Proactive Notifications

If the feature **"HAcoBot thinks ahead"** is enabled, HAcoBot sends **automatic** notifications for:

- **Critical Batteries** (below 20%)
- **Unavailable Entities** (except buttons, scenes)
- **Security Warnings** (e.g. window open when user leaves house)
- **Faulty Automations**
- **Critical System Problems**

### Example: Security Monitoring

If HAcoBot detects that the user has left the house but windows or doors are still open, it sends a notification **immediately**:

**HAcoBot detects:**
- `person.jan` = `not_home`
- `binary_sensor.living_room_window` = `on` (open)

**HAcoBot sends:**
> 🚨 **Security Warning**  
> You have left the house, but the window in the living room is still open.  
> Do you want to return to close it?

## Integration with Automations

You can also include notifications in automations:

> "Create an automation: When the washing machine is finished, send me a notification"

> "When the temperature drops below 5°C, notify me"

## Technical Details

- Notifications are sent via `execute_service` with domain `notify`
- HAcoBot automatically uses the appropriate service (e.g. `notify.mobile_app_iphone`)
- For security warnings, **persistent_notification** or the Mobile App service is used

## Examples

### Simple Notification
**User:** "Send me a notification: Test"

**HAcoBot executes:**
```yaml
service: notify.mobile_app_iphone
data:
  message: "Test"
```

### Notification with Title
**User:** "Send notification with title 'Reminder': Take out trash"

**HAcoBot executes:**
```yaml
service: notify.mobile_app_iphone
data:
  title: "Reminder"
  message: "Take out trash"
```

### Proactive Security Warning
**HAcoBot detects problem and sends:**
```yaml
service: notify.mobile_app_iphone
data:
  title: "🚨 Security Warning"
  message: "You have left the house, but the window in the living room is still open. Do you want to return?"
  data:
    priority: high
```

## Best Practices

✅ **Use clear messages**: "Washing machine finished" instead of "WaMa done"  
✅ **Use titles for important messages**: `title: "Warning"` or `title: "Reminder"`  
✅ **Enable Proactive Learning**: For automatic security warnings  
❌ **Avoid Spam**: Too many notifications will be ignored
