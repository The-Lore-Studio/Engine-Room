# Unit 2: The DOM Tree Parser

## The Situation
In Unit 1, you resolved style specificity calculations. Now we move up the rendering pipeline to the **HTML / DOM Parser**.

The engine contains a custom recursive descent parser in `browser_engine/dom_parser.py` designed to convert HTML strings into a tree of `Node` objects. However, there is a major tokenization bug:
When parsing tags with spaces in their attribute values (like `<div class="container active">`), the parser fails to extract the attributes and leaves them empty.

### Why it happens:
Look at how the parser extracts tag names and attributes from the raw tag contents:
```python
parts = [p for p in tag_content.split(' ') if p]
tag_name = parts[0]
for part in parts[1:]:
    # parses class="container"
```
Because the parser naively splits the entire tag content by spaces (`' '`), it breaks a single attribute with space-separated values (like `class="container active"`) into multiple parts:
*   Part 1: `class="container`
*   Part 2: `active"`

Neither of these matches the regex `(\w+)="([^"]*)"`, so the parser drops the classes completely!

Your job is to fix `browser_engine/dom_parser.py` so that it correctly extracts all attributes (including those with spaces in their values).

---

## Technical Specifications
1. **Blink Connection**: In Chromium, the Blink layout engine uses `HTMLTokenizer` and `HTMLDocumentParser` to scan characters and extract attributes sequentially, matching quoted boundaries rather than splitting naively.
2. **Implementation**: Modify the tokenization/regex logic in `browser_engine/dom_parser.py` so that it parses multi-attribute tags and matches quoted attributes with spaces correctly.
   * *Tip*: Standard regular expressions like `re.findall` can extract key-value pairs matching a pattern.

---

## How to Test
Run the Level 2 mechanical checkpoint to verify:
```bash
python3 replay.py checkpoint
```

Once passed, type `/checkpoint` to trigger the conceptual oral exam.
