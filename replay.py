import sys
import json
import os
import subprocess
from datetime import datetime

STATE_FILE = '.game/progress.json'
JOURNAL_FILE = '.game/journal.md'

def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "active_level": 1,
            "completed_levels": [],
            "calibration": {
                "c_experience": None,
                "kernel_experience": None
            },
            "learning_journal": {
                "misconceptions_identified": [],
                "concepts_mastered": []
            }
        }
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def append_to_journal(entry_type, text):
    os.makedirs(os.path.dirname(JOURNAL_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(JOURNAL_FILE, 'a') as f:
        f.write(f"\n### {entry_type} [{timestamp}]\n{text}\n")

def status():
    state = load_state()
    print("=" * 50)
    print(f"          REPLAY STATUS - LEVEL {state['active_level']}")
    print("=" * 50)
    print(f"Active Level      : {state['active_level']}")
    print(f"Completed Levels  : {', '.join(map(str, state['completed_levels'])) or 'None'}")
    print(f"Mastered Concepts : {', '.join(state['learning_journal']['concepts_mastered']) or 'None'}")
    print(f"Misconceptions    : {', '.join(state['learning_journal']['misconceptions_identified']) or 'None'}")
    print(f"Calibration C     : {state['calibration']['c_experience'] or 'Not Calibrated'}")
    print(f"Calibration Kernel: {state['calibration']['kernel_experience'] or 'Not Calibrated'}")
    print("=" * 50)

def doctor():
    print("=" * 50)
    print("        REPLAY DIAGNOSTIC REPORT (DOCTOR)")
    print("=" * 50)
    
    # Check 1: Python Version
    py_version = sys.version_info
    print(f"[-] Python Version : {py_version.major}.{py_version.minor}.{py_version.micro} -> PASS")
    
    # Check 2: Save State File
    if os.path.exists(STATE_FILE):
        print(f"[-] Save State      : Found (.game/progress.json) -> PASS")
    else:
        print(f"[x] Save State      : Missing! (Run onboarding first) -> WARNING")
        
    # Check 3: Codebase Import
    try:
        sys.path.append(os.path.abspath('browser_engine'))
        import css_resolver
        print(f"[-] CSS Engine      : Loaded successfully -> PASS")
    except Exception as e:
        print(f"[x] CSS Engine      : Load Failed! Error: {e} -> FAIL")
        
    # Check 4: Git integration
    try:
        devnull = open(os.devnull, 'w')
        subprocess.run(["git", "status"], stdout=devnull, stderr=devnull, check=True)
        print(f"[-] Git Repository  : Detected -> PASS")
    except Exception:
        print(f"[x] Git Repository  : Not initialized or not in path -> WARNING")
        
    print("=" * 50)

def start():
    state = load_state()
    level = state['active_level']
    
    # Determine the brief based on active level
    brief_path = f"journey/{level:02d}_css_specificity.md"
    if level == 1:
        brief_path = "journey/01_css_specificity.md"
    else:
        brief_path = f"journey/{level:02d}_next_predicament.md"
        
    if os.path.exists(brief_path):
        print(f"--- LOADING PREDICAMENT BRIEF (LEVEL {level}) ---")
        with open(brief_path, 'r') as f:
            print(f.read())
        print("-" * 50)
    else:
        if level == 2:
            print(f"--- LOADING PREDICAMENT BRIEF (LEVEL 2) ---")
            print("# Unit 2: The DOM Tree Parser")
            print("\nYou have successfully unlocked Unit 2. The HTML/DOM parsing lab environment is ready.")
            print("To proceed, you would fix a tokenization bug in our custom HTML parser.")
            print("-" * 50)
        else:
            print(f"[ERROR] Could not find predicament brief at {brief_path}")

def checkpoint():
    state = load_state()
    level = state['active_level']
    
    test_script = f"checkpoints/{level:02d}_checkpoint.py"
    if level == 1:
        test_script = "checkpoints/01_checkpoint.py"
        
    if not os.path.exists(test_script):
        print(f"[ERROR] No checkpoint validation test found for level {level} at {test_script}")
        sys.exit(1)
        
    print(">>> Executing mechanical validation test suite...")
    result = subprocess.run([sys.executable, test_script])
    
    if result.returncode != 0:
        print("\n[FAIL] Mechanical test failed. Fix the implementation in browser_engine/ and try again.")
        sys.exit(1)
        
    print("\n[PASS] Mechanical validation passed!")
    print("=" * 60)
    print("CONSOLE ACTIONS REQUIRED:")
    print("1. Switch your persona from COLLABORATOR to EXAMINER.")
    print("2. Ask the student the oral questions defined in evaluation/viva_voces/01_specificity_rubric.md.")
    print("3. Listen to the student's explanations without assisting them.")
    print("4. If they answer correctly, run: python replay.py pass_level")
    print("=" * 60)

def pass_level():
    state = load_state()
    level = state['active_level']
    
    if level == 1:
        state['completed_levels'].append(1)
        state['learning_journal']['concepts_mastered'].extend(["CSS Specificity", "Style Resolution"])
        state['active_level'] = 2
        save_state(state)
        
        # Write to journal
        append_to_journal(
            "Level Completion",
            "- **Level 1: CSS Specificity & Cascade Resolution** has been successfully cleared.\n"
            "- Mastered concepts: *CSS Specificity*, *Style Resolution*.\n"
            "- Passed mechanical tests and oral examination."
        )
        
        print("=" * 50)
        print(f"[CHECKPOINT PASSED] Level {level} successfully cleared.")
        print("progress.json has been updated. Level 2 is now unlocked!")
        
        # Git Save State Mechanism
        try:
            # Check if git is initialized
            devnull = open(os.devnull, 'w')
            subprocess.run(["git", "status"], stdout=devnull, stderr=devnull, check=True)
            
            # Stage changed files
            subprocess.run(["git", "add", "browser_engine/", ".game/"], check=True)
            # Commit changes
            subprocess.run(["git", "commit", "-m", "checkpoint: level-01 CSS specificity cascade resolved"], check=True)
            print("[SAVE STATE] Git commit successfully created: 'checkpoint: level-01 CSS specificity cascade resolved'.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[SAVE STATE] Git repository not detected or git not installed. Skipping automatic commit.")
            
        print("=" * 50)
    else:
        print(f"No logic defined to pass Level {level} in this prototype.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python replay.py [status|start|checkpoint|pass_level|doctor]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == 'status':
        status()
    elif cmd == 'start':
        start()
    elif cmd == 'checkpoint':
        checkpoint()
    elif cmd == 'pass_level':
        pass_level()
    elif cmd == 'doctor':
        doctor()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
