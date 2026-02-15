# Setting up Voice Control

To speak with HAcoBot (instead of just typing), you must link it to Home Assistant's Voice services.

## Prerequisites

- A microphone  
  e.g.:
  - Smartphone
  - ESP32-S3 Box
  - Browser (via HTTPS / SSL)

## Setup

1. Go to **Settings → Voice Assistants**
2. Click on your existing assistant  
   or create a new one (**"HAcoBot Voice"**)
3. **Conversation Agent**:  
   Select **HAcoBot** here

### Speech-to-Text (STT)

**Recommended:**
- **Whisper**  
  (local via add-on **"Wyoming Whisper"**)

**Alternative:**
- Home Assistant Cloud

### Text-to-Speech (TTS)

**Recommended:**
- **Piper**  
  (local via add-on **"Wyoming Piper"**)

**Alternative:**
- Google Translate

## Done 🎤

Now you can speak with HAcoBot via the **microphone icon on the dashboard** or on your **mobile phone**.
