# Showdown Rubric: DOM Parser (Level 2)

Once the student passes the Level 2 mechanical checkpoint, switch your persona to **Examiner** and ask the following conceptual questions. Evaluate their explanations against the criteria below. Do not assist the student.

---

## 1. Questions

### Question 1: Naive Tokenization vs State-Machine Tokenization
> *"Why did the naive implementation of splitting tag contents by spaces (`.split(' ')`) fail when parsing attributes? In real-world browsers (like Blink), how is tokenization typically structured to handle this without splitting strings?"*

### Question 2: Error Handling in HTML Parsing
> *"Unlike XML, which crashes on malformed tags, the HTML specification defines standard error-recovery behaviors. In our parser, if we encounter a tag mismatch (e.g. `<div></span>`), what does it do? How does Blink handle mismatched tags or unclosed elements?"*

---

## 2. Evaluation Criteria

### PASS Criteria:
*   **For Q1**: The student explains that naive splitting breaks attribute values that contain spaces (like `class="btn primary"`) because the space is treated as an attribute delimiter instead of part of the value. They explain that modern engines (like Blink's `HTMLTokenizer`) use a **state machine** (specifically checking if the scanner is currently inside a double-quoted string, single-quoted string, or unquoted attribute state) to decide whether to treat a space as a delimiter or as part of a literal string.
*   **For Q2**: The student notes that our simple parser throws a `ValueError("Tag mismatch...")` on error. They explain that Blink is much more forgiving: it uses a **Stack of Open Elements** and runs recovery rules (e.g., automatically closing tags, or ignoring unexpected end tags) so the page still renders (following the HTML5 parsing specification).

### FAIL Criteria:
*   The student does not understand why space-splitting breaks quoted strings with spaces.
*   The student cannot explain how state machines or scanners process characters one by one.
*   The student is unaware of HTML's error-tolerant nature compared to strict XML parsing.
