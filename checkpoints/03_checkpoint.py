# checkpoints/03_checkpoint.py
# Verification test script for Level 3: Gamepad IPC.

import sys
import os

# Ensure browser_engine is in the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from browser_engine.gamepad_ipc import GamepadState, SharedMemoryBuffer, BrowserGamepadProvider, RendererGamepadAPI
except ImportError as e:
    print(f"[FAIL] Could not import gamepad_ipc module: {e}")
    sys.exit(1)

def run_tests():
    print(">>> Executing mechanical validation test suite for Level 3...")
    
    shm = SharedMemoryBuffer()
    provider = BrowserGamepadProvider(shm)
    api = RendererGamepadAPI(shm)

    # Check 1: Initial State is empty
    initial_pads = api.get_gamepads()
    if not isinstance(initial_pads, dict):
        print("[FAIL] get_gamepads() must return a dictionary of gamepad states.")
        sys.exit(1)
    if len(initial_pads) != 0:
        print(f"[FAIL] Expected 0 initial gamepads, got {len(initial_pads)}.")
        sys.exit(1)

    # Check 2: Browser writes, version updates
    state = GamepadState(index=0, connected=True, timestamp=123.45)
    state.axes = [0.12, -0.34]
    state.buttons = [1.0, 0.0]
    
    provider.write_gamepad_state(0, state)
    
    if shm.version <= 0:
        print("[FAIL] write_gamepad_state() must increment the shared memory version number.")
        sys.exit(1)
        
    if 0 not in shm.buffer:
        print("[FAIL] write_gamepad_state() failed to write to the shared memory buffer.")
        sys.exit(1)

    # Check 3: Renderer reads new data
    rendered_pads = api.get_gamepads()
    if 0 not in rendered_pads:
        print("[FAIL] get_gamepads() failed to retrieve gamepad state from buffer.")
        sys.exit(1)
        
    p0 = rendered_pads[0]
    if not p0.connected or p0.axes != [0.12, -0.34] or p0.buttons != [1.0, 0.0]:
        print("[FAIL] get_gamepads() returned corrupted or incomplete gamepad data.")
        sys.exit(1)

    # Check 4: Caching behavior
    # If the version does not change, get_gamepads() must serve from cached_states
    # and NOT re-read from shared memory.
    # We test this by modifying the shared memory raw buffer directly without incrementing version.
    shm.buffer[0].axes = [0.99, 0.99]
    cached_pads = api.get_gamepads()
    if cached_pads[0].axes == [0.99, 0.99]:
        print("[FAIL] get_gamepads() served fresh data even though version did not change (caching is broken).")
        sys.exit(1)

    # If version increments, it should fetch new data
    shm.version += 1
    fresh_pads = api.get_gamepads()
    if fresh_pads[0].axes != [0.99, 0.99]:
        print("[FAIL] get_gamepads() served stale data after version was incremented.")
        sys.exit(1)

    print("\n[PASS] Gamepad IPC mechanical validation passed!")
    sys.exit(0)

if __name__ == '__main__':
    run_tests()
