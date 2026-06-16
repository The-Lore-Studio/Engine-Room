# Unit 4: Gamepad System Platform Refactor (Finale)

## The Situation
Now that you understand the gamepad IPC subsystem, you are ready for the finale. 

In `browser_engine/game_controller_data_fetcher_mac.py`, the macOS GameController data fetcher uses a global constant `gamepad.kItemsLengthCap` to size its local `connected_` player slots array:
```python
self.connected_ = [False] * gamepad.kItemsLengthCap
```

This represents a **tight architectural coupling**. The macOS data fetcher's array size should be determined by macOS/iOS framework capabilities (specifically Apple's `GCControllerPlayerIndex4`), not by a generic global cap in the parent gamepad subsystem. If another platform demands 8 or 16 slots and we increase `gamepad.kItemsLengthCap`, the Mac fetcher would waste resources allocating unused slots.

Additionally, the file has a redundant local constant `kGCControllerPlayerIndexCount = 4` that duplicates the player limit, creating two sources of truth.

Your job in `browser_engine/game_controller_data_fetcher_mac.py` is to:
1. Define a class/module-level constant `kMaxPlayerIndex = 4` representing the fetcher's local capability.
2. In the initialization, add an assertion (simulating C++ `static_assert`) to ensure your constant stays in sync with Apple's framework index:
   ```python
   assert kMaxPlayerIndex == GCControllerPlayerIndex4 + 1, "kMaxPlayerIndex must match Apple index4 + 1"
   ```
3. Remove the redundant `kGCControllerPlayerIndexCount = 4` and point `next_unused_player_index` to your new constant instead.
4. Subevery reference of `gamepad.kItemsLengthCap` inside the macOS fetcher with `kMaxPlayerIndex`.
5. Remove the import `from . import gamepad` entirely from `game_controller_data_fetcher_mac.py` to prove they are decoupled!

---

## How to Test
Run the Level 4 mechanical validation tests:
```bash
python3 replay.py checkpoint
```

Once passed, run `/checkpoint` to trigger the final conceptual oral exam.
