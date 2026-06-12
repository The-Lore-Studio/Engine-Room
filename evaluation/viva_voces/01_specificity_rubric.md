# Showdown Rubric: CSS Specificity & Cascade Resolution

When the student triggers `/checkpoint` and the python tests pass, the Console enters Examiner Mode. The Console must ask the student the following questions, one at a time. Do not reveal the rubric to the student.

---

## Question 1: Specificity Packing & Bit Budgets
*   **The Question:** *"In Blink (Chromium's rendering engine), CSS Selector specificity is packed into a single 32-bit unsigned integer for performance reasons. What are the implications of this bit-packing? What happens if a selector has an extreme number of classes (e.g. more than 255 or 1024), and how does our python tuple implementation differ?"*
*   **Passing Criteria:** The student must explain that packing specificity allocates a specific number of bits per category (e.g., 8 or 10 bits each for IDs, classes, and tags). If a selector exceeds the bit limit (e.g. 256 classes), it could overflow and bleed into the next category (making a class count look like an ID count) or get clamped. In our Python implementation, we use tuples of arbitrary-precision integers, which prevents overflow but has more memory overhead.

---

## Question 2: Cascade vs. Inheritance
*   **The Question:** *"What is the difference between Cascading/Specificity (which you just solved) and Style Inheritance (e.g., how a child `span` inherits `color` or `font-family` from a parent `div`)? How does Chromium propagate inherited styles down the tree efficiently without running the full selector matching algorithm on every child node?"*
*   **Passing Criteria:** The student must differentiate between:
    1.  *Cascade/Specificity:* Resolving styles by matching rules specifically targeted at the node.
    2.  *Inheritance:* Child nodes copying inheritable property values from their parent when no targeted rules apply.
    Chromium optimizes inheritance by sharing `ComputedStyle` objects between parent/child when possible, and propagating styles in a single top-down tree walk (`RecalcStyle` pass), bypassing selector matching entirely for child nodes that simply inherit.

---

## Grading Instructions
*   If the student gives incomplete answers, ask Socratic follow-ups.
*   Once both concepts are clearly demonstrated, run: `python cartridge.py pass_level` to advance the level in `progress.json`.
*   Update `.game/journal.md` with notes on how they did.
