# Sprachsteuerung einrichten

Damit du mit HAcoBot sprechen kannst (statt nur zu tippen), musst du ihn mit den Voice-Diensten von Home Assistant verknüpfen.

## Voraussetzungen

- Ein Mikrofon  
  z. B.:
  - Smartphone
  - ESP32-S3 Box
  - Browser (über HTTPS / SSL)

## Einrichtung

1. Gehe zu **Einstellungen → Sprachassistenten**
2. Klicke auf deinen bestehenden Assistenten  
   oder erstelle einen neuen (**„HAcoBot Voice“**)
3. **Unterhaltungs-Agent**:  
   Wähle hier **HAcoBot** aus

### Sprache-zu-Text (STT)

**Empfohlen:**
- **Whisper**  
  (lokal über das Add-on **„Wyoming Whisper“**)

**Alternativ:**
- Home Assistant Cloud

### Text-zu-Sprache (TTS)

**Empfohlen:**
- **Piper**  
  (lokal über das Add-on **„Wyoming Piper“**)

**Alternativ:**
- Google Translate

## Fertig 🎤

Jetzt kannst du über das **Mikrofon-Symbol im Dashboard** oder auf dem **Handy** mit HAcoBot sprechen.
