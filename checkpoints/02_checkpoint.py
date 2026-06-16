# checkpoints/02_checkpoint.py
# Verification test script for Level 2: DOM Parser.

import sys
import os

# Ensure browser_engine is in the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from browser_engine.dom_parser import HTMLParser, Node
except ImportError as e:
    print(f"[FAIL] Could not import dom_parser module: {e}")
    sys.exit(1)

def run_tests():
    print(">>> Executing mechanical validation test suite for Level 2...")
    
    # Test 1: Simple HTML Node
    html1 = "<div>Hello World</div>"
    parser1 = HTMLParser(html1)
    root1 = parser1.parse()
    if not root1 or root1.tag_name != "div":
        print("[FAIL] Failed to parse basic HTML tag name.")
        sys.exit(1)
    if len(root1.children) != 1 or root1.children[0].text != "Hello World":
        print("[FAIL] Failed to parse basic text child node.")
        sys.exit(1)

    # Test 2: Basic Attribute
    html2 = '<div class="container">Hello</div>'
    parser2 = HTMLParser(html2)
    root2 = parser2.parse()
    if not root2 or root2.attributes.get("class") != "container":
        print("[FAIL] Failed to parse single tag attribute.")
        sys.exit(1)

    # Test 3: Multiple Attributes & Attribute Values with Spaces (The Predicament)
    html3 = '<div id="main" class="container active">Hello</div>'
    parser3 = HTMLParser(html3)
    root3 = parser3.parse()
    if not root3:
        print("[FAIL] Parser crashed or returned None on multiple attributes.")
        sys.exit(1)
        
    if root3.attributes.get("id") != "main":
        print(f"[FAIL] Expected id='main', got {root3.attributes.get('id')}.")
        sys.exit(1)
        
    if root3.attributes.get("class") != "container active":
        print(f"[FAIL] Expected class='container active', got {root3.attributes.get('class')}. (Attribute values containing spaces failed to parse).")
        sys.exit(1)

    # Test 4: Nested HTML Nodes
    html4 = '<div class="wrapper"><span class="highlight">Inner</span></div>'
    parser4 = HTMLParser(html4)
    root4 = parser4.parse()
    if not root4 or len(root4.children) != 1:
        print("[FAIL] Failed to parse nested children structure.")
        sys.exit(1)
        
    span = root4.children[0]
    if span.tag_name != "span" or span.attributes.get("class") != "highlight":
        print("[FAIL] Nested child node tag or attributes parsed incorrectly.")
        sys.exit(1)
    if len(span.children) != 1 or span.children[0].text != "Inner":
        print("[FAIL] Nested child's text node parsed incorrectly.")
        sys.exit(1)

    print("\n[PASS] DOM Tree Parser mechanical validation passed!")
    sys.exit(0)

if __name__ == '__main__':
    run_tests()
