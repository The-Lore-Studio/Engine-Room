import re

class Node:
    def __init__(self, tag, attributes=None, text=""):
        self.tag = tag
        self.attributes = attributes or {}
        self.text = text
        self.computed_style = {}
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        id_str = f"#{self.attributes['id']}" if 'id' in self.attributes else ""
        class_str = f".{self.attributes['class']}" if 'class' in self.attributes else ""
        return f"[DOM Node {self.tag}{id_str}{class_str}] text='{self.text}'"

class Rule:
    def __init__(self, selector, declarations):
        self.selector = selector
        self.declarations = declarations

    def __repr__(self):
        return f"Rule({self.selector} -> {self.declarations})"

def match_selector(node, selector):
    """
    Matches a single compound selector (e.g. 'div', '.container', '#title', 'div.container')
    against a DOM node. Returns True if matching.
    """
    # Tokenize the selector into parts: tag, classes, and id
    # e.g., 'div.container#title' -> ['div', '.container', '#title']
    tokens = re.findall(r'^[a-zA-Z0-9]+|\.[a-zA-Z0-9_-]+|#[a-zA-Z0-9_-]+', selector)
    if not tokens:
        return False

    for token in tokens:
        if token.startswith("#"):
            if node.attributes.get("id") != token[1:]:
                return False
        elif token.startswith("."):
            classes = node.attributes.get("class", "").split()
            if token[1:] not in classes:
                return False
        else:
            if node.tag != token:
                return False
    return True

def compute_specificity(selector):
    """
    TO THE STUDENT:
    Compute specificity of a selector string and return a 3-part tuple: (IDs, Classes, Tags).
    
    Examples:
      '#title'          -> (1, 0, 0)
      '.container'      -> (0, 1, 0)
      'div'             -> (0, 0, 1)
      'div.container'   -> (0, 1, 1)
    
    Currently returns (0, 0, 0) for all. Implement the correct counts!
    """
    return (0, 0, 0)

class StyleResolver:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def resolve_styles(self, node):
        """
        TO THE STUDENT:
        This resolves styles for a node by applying declarations of matching rules.
        
        Currently, it applies matching rules in stylesheet order (sequential override).
        You must sort matched rules by specificity (using compute_specificity) before
        applying them, so that higher specificity rules override lower ones.
        """
        matched_rules = []
        for rule in self.rules:
            if match_selector(node, rule.selector):
                matched_rules.append(rule)
        
        # TODO: Sort matched_rules by specificity.
        # Python compares tuples element-by-element: (1, 0, 0) > (0, 1, 0) > (0, 0, 1)
        # We want higher specificity rules to be applied LATER (so they overwrite preceding styles).
        
        # Apply style declarations in sorted order
        for rule in matched_rules:
            node.computed_style.update(rule.declarations)

        # Recursively resolve styles for children
        for child in node.children:
            self.resolve_styles(child)

if __name__ == '__main__':
    # Simulation Setup
    resolver = StyleResolver()
    
    # stylesheet parsed in order:
    # 1. Class selector (should have lower specificity than ID)
    resolver.add_rule(Rule(".container", {"color": "green", "font-weight": "bold"}))
    # 2. ID selector (should override class color to blue)
    resolver.add_rule(Rule("#title", {"color": "blue"}))
    # 3. Tag selector (lowest specificity, should be overridden by both class and id)
    resolver.add_rule(Rule("div", {"color": "red", "margin": "10px"}))
    
    # DOM Tree Creation
    root = Node("div", {"class": "container", "id": "title"}, text="Hello World")
    
    print("Parsing CSS Stylesheet & Resolving Style Tree...")
    resolver.resolve_styles(root)
    
    print("-" * 60)
    print("Computed Style Result:")
    print(f"Node        : {root}")
    print(f"Styles      : {root.computed_style}")
    print("-" * 60)
    
    # Diagnostics
    color = root.computed_style.get("color")
    if color == "red":
        print("[FAIL] Cascade priority failed! The tag selector override incorrectly won.")
    elif color == "green":
        print("[FAIL] Specificity resolution failed! Class selector (.container) overrode ID selector (#title) due to parsing order.")
    elif color == "blue":
        print("[SUCCESS] Style Resolved correctly! 'color' is blue (ID specificity won).")
    else:
        print("[FAIL] Style not applied.")
