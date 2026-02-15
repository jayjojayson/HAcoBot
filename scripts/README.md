# Helper Scripts

Diese Skripte unterstützen die Entwicklung und Automatisierung von HAcoBot.

## `validate_prompts.py`
Prüft `custom_components/prompts.py` auf Python-Syntaxfehler und das Vorhandensein wichtiger Kern-Funktionen. Wird in CI/CD genutzt.

## `process_issue_prompt.py`
Wird von der GitHub Action `issue_to_pr.yml` genutzt.
- Liest den Body eines Issues (aus `GITHUB_EVENT_PATH`)
- Extrahiert die Ziel-Funktion und den neuen Prompt-Inhalt
- Fügt den neuen Inhalt automatisch in `custom_components/prompts.py` ein
