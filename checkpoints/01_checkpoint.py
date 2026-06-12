import sys
import os

# Ensure the browser_engine directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../browser_engine')))

try:
    from css_resolver import Node, Rule, StyleResolver, compute_specificity
except ImportError as e:
    print(f"FAILED: Could not import elements from browser_engine/css_resolver.py. Error: {e}")
    sys.exit(1)

def run_adversarial_specificity_test():
    # 1. Test Specificity Calculation Math
    test_cases = {
        "#title": (1, 0, 0),
        ".container": (0, 1, 0),
        "div": (0, 0, 1),
        "div.container": (0, 1, 1),
        "div.container#title": (1, 1, 1),
        "div.card.active": (0, 2, 1),
        "#header.active.dark": (1, 2, 0),
        "span#alert": (1, 0, 1)
    }

    for selector, expected in test_cases.items():
        res = compute_specificity(selector)
        if res != expected:
            print(f"FAILED: Specificity calculation mismatch for '{selector}'. Got {res}, expected {expected}.")
            sys.exit(1)

    print("PASS: Specificity score calculations are correct.")

    # 2. Test Cascade Ordering Resolution
    resolver = StyleResolver()
    
    # Scramble stylesheet order to ensure parsing order does not decide precedence
    resolver.add_rule(Rule("#header", {"color": "red", "font-size": "24px"}))  # High Spec: (1, 0, 0)
    resolver.add_rule(Rule("div", {"color": "green", "margin": "10px"}))       # Low Spec: (0, 0, 1)
    resolver.add_rule(Rule("div.box", {"color": "blue", "padding": "5px"}))     # Mid Spec: (0, 1, 1)

    node = Node("div", {"class": "box", "id": "header"}, text="Test Node")
    resolver.resolve_styles(node)

    # Asserts
    if node.computed_style.get("color") != "red":
        print(f"FAILED: Specificity cascade resolution failed. Expected 'color: red' (ID selector specificity win), got 'color: {node.computed_style.get('color')}'")
        sys.exit(1)

    if node.computed_style.get("margin") != "10px":
        print(f"FAILED: Preceding rule attributes were dropped. Got margin='{node.computed_style.get('margin')}', expected '10px'.")
        sys.exit(1)

    if node.computed_style.get("padding") != "5px":
        print(f"FAILED: Intermediate rule attributes were dropped. Got padding='{node.computed_style.get('padding')}', expected '5px'.")
        sys.exit(1)

    print("SUCCESS: Style resolver passed all adversarial cascade test suites.")
    sys.exit(0)

if __name__ == '__main__':
    run_adversarial_specificity_test()
