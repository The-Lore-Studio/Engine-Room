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
        
    rubric_file = f"evaluation/viva_voces/{level:02d}_rubric.md"
    if level == 1:
        rubric_file = "evaluation/viva_voces/01_specificity_rubric.md"
    elif level == 3:
        rubric_file = "evaluation/viva_voces/03_architecture_rubric.md"
    elif level == 4:
        rubric_file = "evaluation/viva_voces/04_refactor_rubric.md"

    print("\n[PASS] Mechanical validation passed!")
    print("=" * 60)
    print("CONSOLE ACTIONS REQUIRED:")
    print("1. Switch your persona from COLLABORATOR to EXAMINER.")
    print(f"2. Ask the student the oral questions defined in {rubric_file}.")
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
    elif level == 2:
        state['completed_levels'].append(2)
        state['learning_journal']['concepts_mastered'].extend(["DOM Parser", "Tokenization"])
        state['active_level'] = 3
        save_state(state)
        
        append_to_journal(
            "Level Completion",
            "- **Level 2: DOM Tree Parser** has been successfully cleared.\n"
            "- Mastered concepts: *DOM Parser*, *Tokenization*.\n"
            "- Passed mechanical tests."
        )
        
        print("=" * 50)
        print(f"[CHECKPOINT PASSED] Level {level} successfully cleared.")
        print("progress.json has been updated. Level 3 is now unlocked!")
        
        try:
            subprocess.run(["git", "add", "browser_engine/", ".game/"], check=True)
            subprocess.run(["git", "commit", "-m", "checkpoint: level-02 DOM tree parser resolved"], check=True)
            print("[SAVE STATE] Git commit successfully created: 'checkpoint: level-02 DOM tree parser resolved'.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        print("=" * 50)
    elif level == 3:
        state['completed_levels'].append(3)
        state['learning_journal']['concepts_mastered'].extend(["Gamepad System Architecture", "Low-Latency IPC", "Version-based Caching"])
        state['active_level'] = 4
        save_state(state)
        
        append_to_journal(
            "Level Completion",
            "- **Level 3: Gamepad System Architecture** has been successfully cleared.\n"
            "- Mastered concepts: *Gamepad System Architecture*, *Low-Latency IPC*, *Version-based Caching*.\n"
            "- Passed mechanical tests and oral examination."
        )
        
        print("=" * 50)
        print(f"[CHECKPOINT PASSED] Level {level} successfully cleared.")
        print("progress.json has been updated. Level 4 (Finale) is now unlocked!")
        
        try:
            subprocess.run(["git", "add", "browser_engine/", ".game/"], check=True)
            subprocess.run(["git", "commit", "-m", "checkpoint: level-03 gamepad system architecture resolved"], check=True)
            print("[SAVE STATE] Git commit successfully created: 'checkpoint: level-03 gamepad system architecture resolved'.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        print("=" * 50)
    elif level == 4:
        state['completed_levels'].append(4)
        state['learning_journal']['concepts_mastered'].extend(["Gamepad Platform Refactor", "Decoupling Constants", "Compile-Time Assertions"])
        save_state(state)
        
        append_to_journal(
            "Level Completion",
            "- **Level 4: Gamepad Platform Refactor (Finale)** has been successfully cleared.\n"
            "- Mastered concepts: *Gamepad Platform Refactor*, *Decoupling Constants*, *Compile-Time Assertions*.\n"
            "- Passed mechanical tests and oral examination."
        )
        
        print("=" * 60)
        print("🎉 CONGRATULATIONS! You have completed all levels in the Replay! 🎉")
        print("You have mastered CSS Specificity, DOM Parsing, Gamepad IPC, and Platform Refactoring.")
        print("=" * 60)
        
        try:
            subprocess.run(["git", "add", "browser_engine/", ".game/"], check=True)
            subprocess.run(["git", "commit", "-m", "checkpoint: level-04 gamepad platform refactor completed (finale)"], check=True)
            print("[SAVE STATE] Git commit successfully created: 'checkpoint: level-04 gamepad platform refactor completed (finale)'.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    else:
        print(f"No logic defined to pass Level {level} in this prototype.")

def calibrate(c_exp, kernel_exp):
    state = load_state()
    state['calibration']['c_experience'] = c_exp
    state['calibration']['kernel_experience'] = kernel_exp
    save_state(state)
    print(f"[CALIBRATION] Saved: C++={c_exp}, Kernel={kernel_exp}")

def show_map():
    state = load_state()
    level = state['active_level']
    
    def get_status_str(lvl):
        if lvl < level:
            return "✅ Done"
        elif lvl == level:
            return "📍 Active"
        else:
            return "Locked"

    def get_status_marker(lvl):
        if lvl < level:
            return "✅ cleared"
        elif lvl == level:
            return "📍 YOU ARE HERE"
        else:
            return "🔒 locked"

    def color_status(lvl, text):
        if lvl < level:
            return f"\033[32m{text}\033[0m"
        elif lvl == level:
            return f"\033[1;33m{text}\033[0m"
        else:
            return f"\033[90m{text}\033[0m"

    active_file = "css_resolver.py" if level == 1 else "dom_parser.py" if level == 2 else "gamepad_ipc.py" if level == 3 else "game_controller_data_fetcher_mac.py"
    
    done_str = "None"
    if level == 2:
        done_str = "Level 1 done"
    elif level == 3:
        done_str = "Levels 1–2 done"
    elif level >= 4:
        done_str = "Levels 1–3 done"
        
    print("\n\033[1mEngine Room — Replay Map\033[0m")
    print(f"You are here: Level {level} active · {done_str} · Lab seeded ({active_file})")
    print()

    def show_subsystem_map():
        interior_width = 66
        border = "       +" + "-" * interior_width + "+"
        arrow = " " * 40 + "|"
        arrow_v = " " * 40 + "v"

        def draw_box(prefix, content, suffix=""):
            left_part = f"{prefix}{content}"
            if suffix:
                space_needed = interior_width - len(suffix)
                line_content = f"{left_part:<{space_needed}}{suffix}"
            else:
                line_content = left_part.center(interior_width)
            return f"       |{line_content}|"

        l2_box = draw_box("[*] ", "HTML / DOM Tree Parser (Level 2)", "  <-- [YOU ARE HERE]") if level == 2 else (
            draw_box("[PASS] ", "HTML / DOM Tree Parser (Level 2)") if level > 2 else
            draw_box("[ ] ", "HTML / DOM Tree Parser (Level 2)")
        )

        l1_box = draw_box("[*] ", "CSS Specificity & Style Resolver (Level 1)", "  <-- [YOU ARE HERE]") if level == 1 else (
            draw_box("[PASS] ", "CSS Specificity & Style Resolver (Level 1)") if level > 1 else
            draw_box("[ ] ", "CSS Specificity & Style Resolver (Level 1)")
        )

        l4_box = draw_box("[*] ", "macOS GameController Fetcher (Level 4 - Finale)", "  <-- [YOU ARE HERE]") if level == 4 else (
            draw_box("[PASS] ", "macOS GameController Fetcher (Level 4 - Finale)") if level > 4 else
            draw_box("[ ] ", "macOS GameController Fetcher (Level 4 - Finale)")
        )

        l3_box = draw_box("[*] ", "Shared Memory IPC Boundary (Level 3)", "  <-- [YOU ARE HERE]") if level == 3 else (
            draw_box("[PASS] ", "Shared Memory IPC Boundary (Level 3)") if level > 3 else
            draw_box("[ ] ", "Shared Memory IPC Boundary (Level 3)")
        )

        print("=" * 80)
        print("                 🎮 BROWSER REPLAY SUB-SYSTEM MAP 🎮".center(80))
        print("=" * 80)
        print()
        print("   [ RENDERING PIPELINE ]")
        print()
        print(border)
        print(draw_box("", "HTML Source Code String"))
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(l2_box)
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(draw_box("", "Document Object Model (DOM) Tree"))
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(l1_box)
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(draw_box("", "Compositor & Layout Tree"))
        print(border)
        print()
        print("   [ HARDWARE INPUT PIPELINE ]")
        print()
        print(border)
        print(draw_box("", "OS Game Controller Events"))
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(l4_box)
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(draw_box("", "Gamepad Provider / Manager"))
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(l3_box)
        print(border)
        print(arrow)
        print(arrow_v)
        print(border)
        print(draw_box("", "Blink WebGamepad API"))
        print(border)
        print("=" * 80)
        print()

    show_subsystem_map()
    
    print("\033[1m1. Level progression\033[0m")
    print(f"   {get_status_marker(1):<18} Level 1: CSS Specificity")
    print(f"   {get_status_marker(2):<18} Level 2: DOM Parser")
    print(f"   {get_status_marker(3):<18} Level 3: Gamepad IPC")
    print(f"   {get_status_marker(4):<18} Level 4: Mac Refactor (Finale)")
    print()
    
    print(f"\033[1m{'Level':<6}{'Unit':<30}{'File you edit':<36}{'Checkpoint':<20}{'Viva rubric':<28}{'Your status'}\033[0m")
    
    def print_table_row(lvl, unit, filename, check, rubric):
        status_text = get_status_str(lvl)
        if lvl < level:
            color = "\033[32m"
        elif lvl == level:
            color = "\033[1;33m"
        else:
            color = "\033[90m"
            
        print(f"{color}{lvl:<6}{unit:<30}{filename:<36}{check:<20}{rubric:<28}{status_text}\033[0m")

    print_table_row(1, "CSS specificity & cascade", "css_resolver.py", "01_checkpoint.py", "01_specificity_rubric.md")
    print_table_row(2, "DOM tree parser", "dom_parser.py", "02_checkpoint.py", "02_rubric.md")
    print_table_row(3, "Gamepad shared-memory IPC", "gamepad_ipc.py", "03_checkpoint.py", "03_architecture_rubric.md")
    print_table_row(4, "Mac fetcher decoupling", "game_controller_data_fetcher_mac.py", "04_checkpoint.py", "04_refactor_rubric.md")
    print()

    print("\033[1m2. Rendering pipeline (toy engine → Blink)\033[0m")
    print("   parallel track")
    print("   HTML string")
    print(f"       │  ({color_status(2, 'Level 2: dom_parser.py')} ↔ HTMLTokenizer / HTMLTreeBuilder)")
    print("       ▼")
    print("   DOM tree (Node)")
    print(f"       │  ({color_status(1, 'Level 1: css_resolver.py')} ↔ StyleResolver / ElementRuleCollector)")
    print("       ▼")
    print("   computed_style per node")
    print("       │")
    print("       ▼")
    print("   Layout (not in Replay yet)")
    print("       │")
    print("       ▼")
    print("   Paint / pixels")
    print()
    print("   \033[1mParallel Track (Levels 3–4: gamepad_*.py ↔ separate Chromium subsystem)\033[0m")
    print("   Browser process ↔ Renderer")
    print("   (Levels 1–2 = URL → styled DOM. Levels 3–4 = Chromium gamepad architecture (Issue 40275102), not the layout path.)")
    print()

    print("   \033[1mChromium Engine Reference (Process vs. Dependency Axes):\033[0m")
    print("   Chromium is best understood along two axes at once:")
    print("   how it splits at runtime (into OS processes) and how its code is layered (a dependency stack).")
    print()
    print("   \033[1mA. Runtime Axis (Process Split - The Major Subsystems):\033[0m")
    print("      ┌────────────────────────────────────────────────────────┐")
    print("      │                   Browser Process (Host UI/IO)         │")
    print("      └───────────────────────────┬────────────────────────────┘")
    print("                                  │ (Mojo IPC)")
    print("            ┌─────────────────────┼─────────────────────┐")
    print("            ▼                     ▼                     ▼")
    print("      ┌───────────┐         ┌───────────┐         ┌───────────┐")
    print("      │ Renderer  │         │    GPU    │         │  Device   │")
    print("      │ Process   │         │  Process  │         │  Service  │")
    print("      │ (Blink/V8)│         │(Compositing)        │ (Gamepad) │")
    print("      └─────┬─────┘         └───────────┘         └─────┬─────┘")
    print("            │                                           │")
    print("            └───────────[ Direct Shared Memory ]────────┘")
    print()
    print("   \033[1mB. Code Dependency Stack (Layering Axis):\033[0m")
    print("      //chrome      (The actual product: UI, settings, branding)")
    print("         │")
    print("         ▼ (embeds)")
    print("      //components  (Reusable browser features: Sync, Autofill)")
    print("         │")
    print("         ▼")
    print("      //content     (Multi-process browser engine embedding Blink/V8)")
    print("         │")
    print("         ├──────────────────────────┐")
    print("         ▼                          ▼")
    print("      //third_party/blink       //services (Device, Audio, etc.)")
    print("      (DOM parsing, style)          │")
    print("         │                          │")
    print("         └─────────────┬────────────┘")
    print("                       ▼")
    print("                     //mojo (IPC framework)")
    print("                       │")
    print("                       ▼")
    print("                     //base (Core utilities, threading primitives)")
    print()
    print("   * Note: The dependency rule is strictly one-directional — nothing lower")
    print("     in the stack may depend on anything higher — which is why //content")
    print("     is \"the engine\".")
    print()

    print(f"\033[1m3. Level {level} predicament (current task)\033[0m")
    if level == 1:
        print("   Input stylesheets:")
        print("     .container { color: green; }")
        print("     #title { color: blue; }")
        print("   Result:")
        print("     Naive resolver applies last stylesheet rule (green) instead of higher specificity (blue).")
        print("   Fix zone: browser_engine/css_resolver.py")
        print("   Blink analogue: StyleResolver / ElementRuleCollector calculates class vs ID specificity.")
    elif level == 2:
        print("   your fix")
        print('   <div id="main" class="container active">')
        print('            │')
        print('            ▼')
        print('     tag_content.split(\' \')   ← breaks inside quotes')
        print('            │')
        print('            ▼')
        print('     class="container" + active"  → regex fails → attrs lost')
        print()
        print('   Your fix:')
        print('     regex / quoted scan ✅ class="container active"')
        print('     Node with correct attributes')
        print()
        print("   Bug location: dom_parser.py ~lines 54–68 — naive tag_content.split(' ') breaks quoted values with spaces.")
        print()
        print("   Blink analogue: HTMLTokenizer respects quote boundaries; it does not split on spaces inside \"...\".")
    elif level == 3:
        print("   Browser (GamepadProvider) ──[Shared Memory]──> Renderer (GamepadAPI)")
        print("   Task:")
        print("     Implement write_gamepad_state() (Browser) and get_gamepads() (Renderer) with version-based read caching.")
        print("   Fix zone: browser_engine/gamepad_ipc.py")
        print("   Blink analogue: navigator.getGamepads() reads lock-free from the shared memory buffer.")
    elif level >= 4:
        print("   macOS Fetcher connected_[kItemsLengthCap]  <-- COUPLED")
        print("   Task:")
        print("     Declare kMaxPlayerIndex = 4 locally, assert against GCControllerPlayerIndex4 + 1, and remove gamepad.py dependencies.")
        print("   Fix zone: browser_engine/game_controller_data_fetcher_mac.py")
        print("   Blink analogue: GameControllerDataFetcherMac uses Apple's native player enums.")
    print()

    print("\033[1m4. Repo file map\033[0m")
    def get_tree_marker(lvl):
        if lvl < level:
            return "✅"
        elif lvl == level:
            return "📍"
        else:
            return "  "

    print("   Engine-Room/")
    print("   ├── replay.py                    ← status | start | checkpoint | pass_level")
    print("   ├── .game/")
    print(f"   │   ├── progress.json            ← save slot (active_level: {level})")
    print("   │   └── journal.md               ← tutor memory")
    print("   │")
    print("   ├── journey/")
    print(f"   │   ├── 01_css_specificity.md    {get_tree_marker(1)}")
    print(f"   │   ├── 02_next_predicament.md   {get_tree_marker(2)} DOM parser brief")
    print(f"   │   ├── 03_next_predicament.md   {get_tree_marker(3)} Gamepad IPC brief")
    print(f"   │   └── 04_next_predicament.md   {get_tree_marker(4)} Mac refactor brief")
    print("   │")
    print("   ├── browser_engine/")
    if level == 2:
        print(f"   │   ├── dom_parser.py            📍 FIX THIS (Level 2)")
        print(f"   │   ├── css_resolver.py          ✅ (Level 1)")
        print(f"   │   ├── gamepad_ipc.py               Level 3")
        print(f"   │   ├── gamepad.py                   Level 3–4 shared constants")
        print(f"   │   └── game_controller_data_fetcher_mac.py  Level 4")
    elif level == 1:
        print(f"   │   ├── dom_parser.py                Level 2")
        print(f"   │   ├── css_resolver.py          📍 FIX THIS (Level 1)")
        print(f"   │   ├── gamepad_ipc.py               Level 3")
        print(f"   │   ├── gamepad.py                   Level 3–4 shared constants")
        print(f"   │   └── game_controller_data_fetcher_mac.py  Level 4")
    elif level == 3:
        print(f"   │   ├── dom_parser.py            ✅ (Level 2)")
        print(f"   │   ├── css_resolver.py          ✅ (Level 1)")
        print(f"   │   ├── gamepad_ipc.py           📍 FIX THIS (Level 3)")
        print(f"   │   ├── gamepad.py                   Level 3–4 shared constants")
        print(f"   │   └── game_controller_data_fetcher_mac.py  Level 4")
    else: # level >= 4
        print(f"   │   ├── dom_parser.py            ✅ (Level 2)")
        print(f"   │   ├── css_resolver.py          ✅ (Level 1)")
        print(f"   │   ├── gamepad_ipc.py           ✅ (Level 3)")
        print(f"   │   ├── gamepad.py                   Level 3–4 shared constants")
        print(f"   │   └── game_controller_data_fetcher_mac.py  📍 FIX THIS (Level 4)")
    print("   │")
    print("   ├── checkpoints/")
    print("   │   ├── 01_checkpoint.py … 04_checkpoint.py")
    print("   │")
    print("   ├── evaluation/viva_voces/")
    print("   │   ├── 01_specificity_rubric.md … 04_refactor_rubric.md")
    print("   │")
    print("   └── context/")
    print("       ├── gamepad_system.md        ← grounding for Levels 3–4")
    print("       └── chromium_architecture.md ← general Chromium architecture guide")
    print()

    print("\033[1m5. Command loop (every level)\033[0m")
    print("   python3 replay.py start        → read predicament brief")
    print("           ↓")
    print(f"   edit browser_engine/{active_file}  → fix the bug")
    print("           ↓")
    print("   python3 replay.py checkpoint   → mechanical tests")
    print("           ↓")
    print("   /checkpoint (chat)             → viva voce oral exam")
    print("           ↓")
    print("   python3 replay.py pass_level   → unlock next level")
    print()

    print("\033[1m6. Your next step\033[0m")
    if level == 1:
        print("   Open browser_engine/css_resolver.py")
        print("   Implement compute_specificity() and resolve_styles()")
        print("   Run python3 replay.py checkpoint")
        print("   When green, say /checkpoint for the oral exam")
    elif level == 2:
        print("   Open browser_engine/dom_parser.py (cursor is already there)")
        print("   Fix attribute tokenization around line 59")
        print("   Run python3 replay.py checkpoint")
        print("   When green, say /checkpoint for the oral exam")
        print("   Want a hint on how to fix the tokenizer without writing the patch for you?")
    elif level == 3:
        print("   Open browser_engine/gamepad_ipc.py")
        print("   Complete BrowserGamepadProvider.write_gamepad_state() and RendererGamepadAPI.get_gamepads()")
        print("   Run python3 replay.py checkpoint")
        print("   When green, say /checkpoint for the oral exam")
    elif level >= 4:
        print("   Open browser_engine/game_controller_data_fetcher_mac.py")
        print("   Decouple the macOS fetcher from gamepad.py and add compile-time checks")
        print("   Run python3 replay.py checkpoint")
        print("   When green, say /checkpoint for the final oral exam")
    print("=" * 70)
    print("\033[96m💡 Tip: You can ask the Socratic tutor in the chat for additional resources, references, or deep-dives on any of these concepts!\033[0m")

def show_resources(concept=None):
    resources = {
        "specificity": {
            "title": "CSS Specificity & Cascade",
            "links": [
                ("W3C CSS Cascade Spec", "https://www.w3.org/TR/css-cascade-4/"),
                ("MDN Web Docs: CSS Specificity", "https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity")
            ],
            "chromium_source": [
                ("third_party/blink/renderer/core/css/resolver/style_resolver.h", "Calculates element computed style from rule list"),
                ("third_party/blink/renderer/core/css/element_rule_collector.h", "Collects style rules matching a DOM element")
            ]
        },
        "dom": {
            "title": "HTML / DOM Parser & Tokenization",
            "links": [
                ("HTML Living Standard: Parsing Section", "https://html.spec.whatwg.org/multipage/parsing.html")
            ],
            "chromium_source": [
                ("third_party/blink/renderer/core/html/parser/html_tokenizer.h", "Splits raw HTML characters into tokens"),
                ("third_party/blink/renderer/core/html/parser/html_tree_builder.h", "Maintains state machine to build DOM tree from tokens")
            ]
        },
        "ipc": {
            "title": "Shared Memory & Mojo IPC",
            "links": [
                ("Mojo IPC Introduction", "https://chromium.googlesource.com/chromium/src/+/main/mojo/README.md"),
                ("Chromium Multi-Process Process Model Docs", "https://www.chromium.org/developers/design-documents/multi-process-architecture/")
            ],
            "chromium_source": [
                ("device/gamepad/gamepad_provider.h", "Polls gamepad hardware and coordinates thread-safe shared memory writes"),
                ("device/gamepad/public/mojom/gamepad.mojom", "Defines the gamepad IPC Mojo service interfaces and shared memory structs")
            ]
        },
        "mac": {
            "title": "macOS Fetcher Decoupling & Game Controller Framework",
            "links": [
                ("Chromium Issue 40275102", "https://issues.chromium.org/issues/40275102"),
                ("Apple Game Controller API Reference", "https://developer.apple.com/documentation/gamecontroller")
            ],
            "chromium_source": [
                ("device/gamepad/game_controller_data_fetcher_mac.mm", "macOS gamepad fetcher implementation utilizing Apple GCController APIs")
            ]
        }
    }

    if not concept:
        print("=" * 60)
        print("          AVAILABLE REPLAY CONCEPTS & LEARNING RESOURCES")
        print("=" * 60)
        print("Run 'python replay.py resources [concept]' to see reference resources.")
        print()
        print("Available concepts:")
        for key, info in resources.items():
            print(f"  - {key:<14} : {info['title']}")
        print("=" * 60)
        return

    key = concept.lower().strip()
    if key in ["css", "specificity", "cascade"]:
        key = "specificity"
    elif key in ["dom", "parser", "tokenizer"]:
        key = "dom"
    elif key in ["ipc", "mojo", "shared_memory", "gamepad_ipc"]:
        key = "ipc"
    elif key in ["mac", "fetcher", "macos", "refactor"]:
        key = "mac"

    if key not in resources:
        print(f"[ERROR] Unknown concept '{concept}'. Available concepts: css, dom, ipc, mac.")
        return

    info = resources[key]
    print("=" * 60)
    print(f" LEARNING RESOURCES: {info['title'].upper()}")
    print("=" * 60)
    print()
    print("📚 Specifications & References:")
    for title, url in info['links']:
        print(f"  - {title}:")
        print(f"    {url}")
    print()
    print("🏛️ Blink / Chromium Source Code:")
    for filepath, desc in info['chromium_source']:
        print(f"  - {filepath}")
        print(f"    ({desc})")
    print("=" * 60)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python replay.py [status|start|checkpoint|pass_level|doctor|calibrate|map|resources]")
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
    elif cmd == 'calibrate':
        if len(sys.argv) < 4:
            print("Usage: python replay.py calibrate [c_experience] [kernel_experience]")
            sys.exit(1)
        calibrate(sys.argv[2], sys.argv[3])
    elif cmd == 'map':
        show_map()
    elif cmd == 'resources':
        concept = sys.argv[2] if len(sys.argv) > 2 else None
        show_resources(concept)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
