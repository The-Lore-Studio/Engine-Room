# Unit 3: Gamepad System Architecture

## The Situation
To write a proper gamepad fetcher, you must first understand the environment it runs in. In Chromium, the Gamepad API spans two processes:
1. **The Browser Process (Privileged)**: Runs device fetchers (like `GameControllerDataFetcherMac`) and writes the updated gamepad state into a shared memory buffer.
2. **The Renderer Process (Sandboxed)**: Renders the web page and calls `navigator.getGamepads()` to read the state from the shared memory buffer.

To achieve low-latency (250Hz updates) without freezing the UI thread, Chromium uses a shared memory segment containing a version number and a dictionary of gamepad states.

In this predicament, the communication channel is broken: gamepad state updates are either causing race conditions or not syncing to the renderer process.

Your job is in `browser_engine/gamepad_ipc.py`. You must:
- Complete `BrowserGamepadProvider.write_gamepad_state()` to thread-safely copy gamepad data and increment the shared memory version number.
- Complete `RendererGamepadAPI.get_gamepads()` to retrieve the data from shared memory using a read-caching pattern (i.e. only copy new data if the version number has changed) to keep CPU overhead minimal.

---

## Technical Specifications
1. **Thread Safety**: Use the shared memory's lock to protect reads and writes.
2. **Low Overhead**: If the version in shared memory has not changed since the last poll, `get_gamepads()` must return the local cached dictionary directly without acquiring locks or copying data.
3. **Atomic Writes**: Increment the version number only *after* the data has been copied.

---

## How to Test
Run the Level 3 mechanical checkpoint to verify the data flows correctly:
```bash
python3 replay.py checkpoint
```

Once passed, type `/checkpoint` to trigger the conceptual oral examination.
