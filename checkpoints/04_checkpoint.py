# checkpoints/04_checkpoint.py
# Verification test script for Level 4 (Finale): Gamepad Refactor.

import sys
import os

# Ensure browser_engine is in the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    print(">>> Executing mechanical validation test suite for Level 4 (Finale)...")
    
    # 1. Read source code to verify static-assert and decoupling rules
    fetcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../browser_engine/game_controller_data_fetcher_mac.py'))
    if not os.path.exists(fetcher_path):
        print(f"[FAIL] Could not find fetcher file at {fetcher_path}")
        sys.exit(1)
        
    with open(fetcher_path, 'r') as f:
        src = f.read()

    # Rule: Decoupling check
    if "import gamepad" in src or "from . import gamepad" in src:
        print("[FAIL] Code smell detected: macOS fetcher still imports/references 'gamepad'. They must be fully decoupled!")
        sys.exit(1)
        
    if "kItemsLengthCap" in src:
        print("[FAIL] 'kItemsLengthCap' is still referenced. You must replace it with your local constant.")
        sys.exit(1)

    # Rule: Redundancy check
    if "kGCControllerPlayerIndexCount" in src:
        print("[FAIL] Redundant constant 'kGCControllerPlayerIndexCount' should be removed and consolidated.")
        sys.exit(1)

    # Rule: Local constant exists
    if "kMaxPlayerIndex" not in src:
        print("[FAIL] You must define 'kMaxPlayerIndex' inside the fetcher module.")
        sys.exit(1)

    # Rule: Static assertion exists
    if "GCControllerPlayerIndex4 + 1" not in src and "GCControllerPlayerIndex4+1" not in src:
        print("[FAIL] You must assert that your local constant is in sync with 'GCControllerPlayerIndex4 + 1'.")
        sys.exit(1)

    # 2. Runtime Behavior check
    try:
        from browser_engine.game_controller_data_fetcher_mac import GameControllerDataFetcherMac, kMaxPlayerIndex, GCControllerPlayerIndexUnassigned
    except ImportError as e:
        print(f"[FAIL] Could not import refactored fetcher: {e}")
        sys.exit(1)

    if kMaxPlayerIndex != 4:
        print(f"[FAIL] Expected kMaxPlayerIndex to be 4, got {kMaxPlayerIndex}")
        sys.exit(1)

    fetcher = GameControllerDataFetcherMac()
    connected = fetcher.get_connected_players()
    if len(connected) != 4:
        print(f"[FAIL] connected_ array should be of size 4, got size {len(connected)}")
        sys.exit(1)

    # Check next_unused_player_index works
    fetcher.update_connection(0, True)
    fetcher.update_connection(1, True)
    if fetcher.next_unused_player_index() != 2:
        print("[FAIL] next_unused_player_index returned incorrect slot.")
        sys.exit(1)

    fetcher.update_connection(2, True)
    fetcher.update_connection(3, True)
    if fetcher.next_unused_player_index() != GCControllerPlayerIndexUnassigned:
        print("[FAIL] next_unused_player_index should return unassigned when all slots are full.")
        sys.exit(1)

    print("\n[PASS] Gamepad platform refactor mechanical validation passed!")
    sys.exit(0)

if __name__ == '__main__':
    run_tests()
