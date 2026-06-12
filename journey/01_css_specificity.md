# Unit 1: The Cascading Selector Bug (CSS Specificity)

## The Predicament
We are building a lightweight layout and rendering engine. When rendering a mock document:
```html
<div class="container" id="title">Hello World</div>
```
With the stylesheet:
```css
.container { color: green; }
#title { color: blue; }
```
The text is rendered in **green** instead of **blue**! 

Open `browser_engine/css_resolver.py` and run `python browser_engine/css_resolver.py` to see the rendering pipeline fail in real time.

In CSS standards—and in Blink (Chromium's rendering engine)—rules must be resolved using **Selector Specificity**. Currently, our engine's `StyleResolver` simply applies matching rules in the order they appear in the file, ignoring specificity completely.

Your mission is to modify `browser_engine/css_resolver.py` to calculate selector specificity correctly and apply the styles based on the CSS Cascade hierarchy.

---

## The Specificity Formula
In Blink's `CSSSelector`, specificity is calculated as a 3-part score:
*   **A (IDs):** Count the number of ID selectors in the selector (e.g., `#title` = 1, 0, 0).
*   **B (Classes/Attributes):** Count the number of class selectors, attribute selectors, and pseudo-classes (e.g., `.container` = 0, 1, 0).
*   **C (Elements):** Count the number of element names and pseudo-elements (e.g., `div` = 0, 0, 1).

A combined selector like `div.container #title` has a specificity of `(1, 1, 1)`. 

---

## Showdown Criteria
1. Run `python browser_engine/css_resolver.py` and ensure the rendering engine outputs:
   `[DOM Node div#title] text='Hello World' -> computed_style={'color': 'blue'}`
2. Type `/checkpoint` to trigger the adversarial test runner and begin the Socratic Viva Voce.
