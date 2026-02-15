import os
import sys
import re
import json

def parse_issue_body(body):
    """Parses the issue body from the GitHub Issue Form."""
    data = {}
    
    # Simple parsing logic for the issue form format
    # Expecting headers like "### Heading" followed by content
    # This is rough but works for standard issue forms
    
    # Regex to capture sections
    # Matches ### Header \n Content
    pattern = r"###\s+(.*?)\s*\n\s*(.*?)(?=\n###|$)"
    matches = re.findall(pattern, body, re.DOTALL)
    
    for header, content in matches:
        header = header.strip()
        content = content.strip()
        
        # Map headers to internal keys based on the issue template
        if "Betroffene Funktion" in header:
            # Extract function name (e.g., "get_base_rules (Basis-Regeln)" -> "get_base_rules")
            data["function"] = content.split(" ")[0].strip()
        elif "Der neue Code/Text" in header:
            data["content"] = content
            
    return data

def update_prompts_file(file_path, target_function, new_content):
    """Updates the prompts.py file with the new content."""
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File {file_path} not found.")
        return False
        
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Locate the function and its return list
    start_line = -1
    return_line = -1
    end_line = -1
    
    # 1. Find the function definition
    for i, line in enumerate(lines):
        if f"def {target_function}(" in line:
            start_line = i
            break
            
    if start_line == -1:
        print(f"[ERROR] Function '{target_function}' not found in {file_path}.")
        return False
        
    # 2. Find the return statement and the list start
    for i in range(start_line, len(lines)):
        if "return [" in lines[i]:
            return_line = i
            break
            
    if return_line == -1:
        print(f"[ERROR] 'return [' not found for function '{target_function}'.")
        return False
        
    # 3. Find the end of the list ']'
    # We look for the matching closing bracket with correct indentation
    # Assuming standard formatting (indentation of function body + 4 spaces usually)
    # But safer to just look for the first ']' on a new line that matches the return indent?
    # Or just scan forward.
    
    # Let's count brackets to be safe, or just look for the indentation level of 'return'
    # The 'return' line indentation
    return_indent = len(lines[return_line]) - len(lines[return_line].lstrip())
    
    insertion_index = -1
    
    for i in range(return_line + 1, len(lines)):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("]"):
            # Found the closing bracket
            insertion_index = i
            break
    
    if insertion_index == -1:
         print(f"[ERROR] Closing ']' not found for function '{target_function}'.")
         return False

    # Check if the last item is an empty string line (common in this file), if so, insert before it
    if '""' in lines[insertion_index - 1] or "''" in lines[insertion_index - 1]:
        insertion_index -= 1

    # Prepare the new content lines
    # Split by newlines and format each line as a string in the list
    new_lines = []
    # Indentation for the list items (usually return_indent + 4)
    item_indent = " " * (return_indent + 4)
    
    # Clean up the input content - remove marked code blocks if present
    clean_content = new_content.replace("```python", "").replace("```", "").strip()
    
    for line in clean_content.splitlines():
        # Escape quotes if necessary
        escaped_line = line.replace('"', '\\"')
        new_lines.append(f'{item_indent}"{escaped_line}",\n')
        
    # If there are lines to add
    if new_lines:
        # Insert them
        for line in reversed(new_lines):
            lines.insert(insertion_index, line)
            
        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
            
        print(f"[SUCCESS] Successfully added new prompt to '{target_function}'.")
        return True
    else:
         print("[WARN] No content to add.")
         return False

def main():
    # Only run if we have an event path (GitHub Actions) or a manual test file
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    
    if not event_path:
        # Fallback for local testing (optional)
        print("[INFO] No GITHUB_EVENT_PATH found. Waiting for manual input or exit.")
        # For now, just exit or mock if we want.
        # Let's mock for development if a specific file exists
        if os.path.exists("test_issue.json"):
            event_path = "test_issue.json"
        else:
            print("[ERROR] Not running in GitHub Actions and no test file found.")
            sys.exit(1)
            
    with open(event_path, "r", encoding="utf-8") as f:
        event_data = json.load(f)
        
    # Extract issue body
    # Event structure depends on the trigger. For 'issues', it's event['issue']['body']
    issue = event_data.get("issue", {})
    body = issue.get("body", "")
    
    if not body:
        print("[ERROR] No issue body found.")
        sys.exit(1)
        
    parsed = parse_issue_body(body)
    
    target_function = parsed.get("function")
    content = parsed.get("content")
    
    if not target_function or not content:
        print("[ERROR] Could not parse 'Target Function' or 'Content' from issue body.")
        print(f"Debug: Parsed data: {parsed}")
        sys.exit(1)
        
    print(f"[INFO] Processing change for function: {target_function}")
    
    # Allow mapping of "SONSTIGES" or custom inputs if needed, 
    # but for now we expect strict function names from the dropdown.
    
    file_path = "custom_components/prompts.py"
    success = update_prompts_file(file_path, target_function, content)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
