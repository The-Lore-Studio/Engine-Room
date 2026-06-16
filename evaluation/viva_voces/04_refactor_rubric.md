# Showdown Rubric: Gamepad Platform Refactor - Finale (Level 4)

Once the student passes the Level 4 mechanical verification, switch your persona to **Examiner** and conduct the final oral exam. Evaluate their answers against the criteria below. Do not assist the student.

---

## 1. Questions

### Question 1: Max Index vs Array Count
> *"In Apple's GameController framework, Apple defines the maximum player index as `GCControllerPlayerIndex4` which has the integer value of 3. Why must our `kMaxPlayerIndex` constant be set to 4, and why do we assert against `GCControllerPlayerIndex4 + 1` rather than just `GCControllerPlayerIndex4`?"*

### Question 2: Decoupling and Static Assertions
> *"Why did we define `kMaxPlayerIndex` locally inside the macOS fetcher instead of keeping the include to `gamepad.h` and referencing a global macOS cap? And what role does the static assertion play in this design?"*

### Question 3: The Signed/Unsigned Compiler Trap
> *"If we declare our local constant as a signed `int` (matching Apple's framework enums) but the loop counter in our update checks is `size_t` (unsigned), what compiler warning is generated, and why does the Chromium build system treat this warning as a fatal error?"*

---

## 2. Evaluation Criteria

### PASS Criteria:
*   **For Q1**: The student explains that array sizing is 1-based (count of elements), while index enums are 0-based. Because the maximum slot index is 3 (Index4), we need 4 slots (0, 1, 2, 3) to prevent out-of-bounds writes.
*   **For Q2**: The student explains that local definitions decouple the fetcher from the generic subsystem, preventing compile-time dependencies on gamepad.h. The static assertion anchors the hardcoded local constant back to the platform framework, ensuring that if Apple ever updates the SDK player count, the build fails immediately rather than causing silent runtime buffer overflows.
*   **For Q3**: The student identifies the `-Wsign-compare` warning. They explain that comparing signed and unsigned values can lead to unexpected behavior (due to implicit conversion of negative numbers to very large unsigned numbers). Chromium uses `-Werror` to turn all warnings into build-blocking errors to enforce maximum safety and correctness.

### FAIL Criteria:
*   The student does not understand why an array needs 4 slots when the maximum index is 3.
*   The student cannot explain the purpose of a compile-time static assertion.
*   The student does not understand why signed vs unsigned comparisons are risky or why Chromium compiles with `-Werror`.
