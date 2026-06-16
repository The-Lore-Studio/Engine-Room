# Showdown Rubric: Gamepad System Architecture (Level 3)

Once the student passes the mechanical verification suite, switch your persona to **Examiner** and ask the following conceptual questions. Evaluate their responses against the criteria below. Do not assist the student.

---

## 1. Questions

### Question 1: Polling vs Event-Driven IPC
> *"In Chromium, the JavaScript `navigator.getGamepads()` API is a polling-based API. Why does the browser engine use a shared memory segment to transfer gamepad states rather than sending an IPC message (such as a Mojo message) from the Renderer to the Browser every time JavaScript polls?"*

### Question 2: Sandboxing and Hardware Permissions
> *"Why can't the Renderer process (where Blink runs) talk directly to the OS USB/Bluetooth APIs to query gamepad state? What security principle does this boundary protect?"*

### Question 3: The Version-Caching Pattern
> *"Walk me through how you implemented caching in `RendererGamepadAPI.get_gamepads()`. What would be the performance impact if we omitted the version check and always copied data from the shared memory segment?"*

---

## 2. Evaluation Criteria

### PASS Criteria:
*   **For Q1**: The student understands that polling at 60Hz or 250Hz via standard IPC would flood the IPC channel with messages, causing high latency, CPU context switches, and thread blocking. Shared memory enables lock-free/low-latency reads (O(1) memory copies).
*   **For Q2**: The student explains that the Renderer is untrusted/sandboxed to prevent compromised websites from gaining raw hardware/driver access. Restricting hardware access to the Browser process maintains the "Principle of Least Privilege".
*   **For Q3**: The student explains that the version check avoids acquiring locks and copying dictionaries on every single poll. Without it, the Renderer would constantly waste CPU cycles on locks and memory allocation even when the gamepad state is completely idle.

### FAIL Criteria:
*   The student does not understand the difference between shared memory and message-passing IPC.
*   The student cannot explain why the Renderer process is sandboxed.
*   The student's explanation of the caching logic is incorrect or indicates they don't understand how version numbers gate updates.
