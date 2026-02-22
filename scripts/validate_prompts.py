import sys
import os

def validate_python_syntax():
    # Dein Pfad zur Datei
    file_path = "custom_components/prompts.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Fehler: Datei {file_path} wurde nicht gefunden.")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Prüft die gesamte Datei auf Python-Syntaxfehler
        compile(content, file_path, 'exec')
        
        # Zusätzlicher Check: Existieren die Basis-Funktionen noch?
        # Das verhindert versehentliches Löschen von Kern-Funktionen
        essential_functions = ["get_base_rules", "get_system_prompt", "get_tool_definitions"]
        for func in essential_functions:
            if func not in content:
                print(f"⚠️ Warnung: Kern-Funktion '{func}' wurde im Code nicht gefunden!")
        
        print(f"✅ Syntax-Check für {file_path} erfolgreich bestanden.")
        
    except SyntaxError as e:
        print(f"❌ Syntax-Fehler in der prompts.py:")
        print(f"Zeile {e.lineno}: {e.msg}")
        print(f"Code: {e.text.strip() if e.text else 'N/A'}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unerwarteter Fehler beim Prüfen: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate_python_syntax()
    