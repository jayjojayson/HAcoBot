# Benachrichtigungen & Alerts

HAcoBot kann Benachrichtigungen über verschiedene Dienste senden – per Chat, Sprache oder automatisch bei wichtigen Ereignissen.

## Verfügbare Dienste

HAcoBot unterstützt alle Home Assistant `notify` Services:

- **Mobile Apps** (`notify.mobile_app_*`)  
  Benachrichtigungen an dein Smartphone (Home Assistant App)
  
- **Persistent Notification** (`notify.persistent_notification`)  
  Benachrichtigungen im Home Assistant Frontend

- **Weitere Services**  
  Telegram, Pushover, E-Mail, etc. (falls konfiguriert)

## Benachrichtigungen senden

### Via Chat/Sprache

Sage einfach:

> "Sende mir eine Benachrichtigung: Fenster im Wohnzimmer ist noch offen"

> "Erinnere mich in 30 Minuten: Wäsche aufhängen"

> "Benachrichtige mich, wenn die Waschmaschine fertig ist"

HAcoBot nutzt automatisch den passenden Notify-Service.

### Manuelle Benachrichtigung

Du kannst auch explizit einen Service angeben:

> "Sende eine persistente Benachrichtigung: System-Update verfügbar"

> "Sende mir eine Push-Benachrichtigung auf mein Handy"

## Parameter

Benachrichtigungen unterstützen folgende Parameter:

- **message** (Pflicht): Der Nachrichtentext
- **title** (Optional): Titel der Nachricht
- **data** (Optional): Zusätzliche Daten (z.B. priority, tag, actions)

**Beispiel mit Titel:**
> "Sende Benachrichtigung mit Titel 'Warnung': Temperatur im Serverraum zu hoch"

## Proaktive Benachrichtigungen

Wenn das Feature **"HAcoBot denkt mit"** aktiviert ist, sendet HAcoBot **automatisch** Benachrichtigungen bei:

- **Kritischen Batterien** (unter 20%)
- **Nicht verfügbaren Entities** (außer buttons, scenes)
- **Sicherheitswarnungen** (z.B. Fenster offen, wenn User das Haus verlässt)
- **Fehlerhaften Automationen**
- **Kritischen Systemproblemen**

### Beispiel: Sicherheits-Monitoring

Wenn HAcoBot erkennt, dass der User das Haus verlassen hat, aber Fenster oder Türen noch offen sind, sendet er **sofort** eine Benachrichtigung:

**HAcoBot erkennt:**
- `person.jan` = `not_home`
- `binary_sensor.fenster_wohnzimmer` = `on` (offen)

**HAcoBot sendet:**
> 🚨 **Sicherheitswarnung**  
> Du hast das Haus verlassen, aber das Fenster im Wohnzimmer ist noch offen.  
> Möchtest du zurückkehren, um es zu schließen?

## Integration mit Automationen

Du kannst Benachrichtigungen auch in Automationen einbauen:

> "Erstelle eine Automation: Wenn die Waschmaschine fertig ist, sende mir eine Benachrichtigung"

> "Wenn die Temperatur unter 5°C fällt, benachrichtige mich"

## Technische Details

- Benachrichtigungen werden via `execute_service` mit domain `notify` gesendet
- HAcoBot nutzt automatisch den passenden Service (z.B. `notify.mobile_app_iphone`)
- Bei Sicherheitswarnungen wird **persistent_notification** oder der Mobile-App-Service verwendet

## Beispiele

### Einfache Benachrichtigung
**User:** "Sende mir eine Benachrichtigung: Test"

**HAcoBot führt aus:**
```yaml
service: notify.mobile_app_iphone
data:
  message: "Test"
```

### Benachrichtigung mit Titel
**User:** "Sende Benachrichtigung mit Titel 'Erinnerung': Müll rausbringen"

**HAcoBot führt aus:**
```yaml
service: notify.mobile_app_iphone
data:
  title: "Erinnerung"
  message: "Müll rausbringen"
```

### Proaktive Sicherheitswarnung
**HAcoBot erkennt Problem und sendet:**
```yaml
service: notify.mobile_app_iphone
data:
  title: "🚨 Sicherheitswarnung"
  message: "Du hast das Haus verlassen, aber das Fenster im Wohnzimmer ist noch offen. Möchtest du zurückkehren?"
  data:
    priority: high
```

## Best Practices

✅ **Nutze klare Nachrichten**: "Waschmaschine fertig" statt "WaMa done"  
✅ **Nutze Titel bei wichtigen Meldungen**: `title: "Warnung"` oder `title: "Erinnerung"`  
✅ **Aktiviere Proaktives Lernen**: Für automatische Sicherheitswarnungen  
❌ **Vermeide Spam**: Zu viele Benachrichtigungen werden ignoriert
