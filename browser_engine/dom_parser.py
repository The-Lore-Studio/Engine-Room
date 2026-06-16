# dom_parser.py
# Simulated HTML/DOM Tree Parser for Unit 2.
# Parses HTML strings into a tree of Node objects.

import re

class Node:
    def __init__(self, tag_name="", attributes=None, children=None, text=""):
        self.tag_name = tag_name
        self.attributes = attributes or {}
        self.children = children or []
        self.text = text

    def __repr__(self):
        if self.text:
            return f"Node(text='{self.text}')"
        return f"Node(tag='{self.tag_name}', attrs={self.attributes}, children={len(self.children)})"

class HTMLParser:
    def __init__(self, html):
        self.html = html
        self.pos = 0

    def peek(self):
        if self.pos >= len(self.html):
            return None
        return self.html[self.pos]

    def consume(self):
        char = self.peek()
        if char:
            self.pos += 1
        return char

    def parse(self):
        while self.pos < len(self.html):
            if self.peek() == '<':
                self.consume() # consume '<'
                if self.peek() == '/':
                    self.consume() # consume '/'
                    # End tag
                    tag_name = ""
                    while self.peek() and self.peek() != '>':
                        tag_name += self.consume()
                    self.consume() # consume '>'
                    return tag_name.strip()
                else:
                    # Start tag
                    tag_content = ""
                    while self.peek() and self.peek() != '>':
                        tag_content += self.consume()
                    self.consume() # consume '>'
                    
                    # Tokenize tag name and attributes
                    # BUG: Naive split by space breaks when attribute values have spaces (e.g. class="container active")
                    # parts = tag_content.split(' ') for <div class="container active"> returns:
                    # ['div', 'class="container', 'active"']
                    # Splitting this way drops the attributes or parses them incorrectly.
                    parts = [p for p in tag_content.split(' ') if p]
                    if not parts:
                        continue
                    tag_name = parts[0]
                    
                    attributes = {}
                    for part in parts[1:]:
                        attr_match = re.match(r'(\w+)="([^"]*)"', part)
                        if attr_match:
                            attributes[attr_match.group(1)] = attr_match.group(2)
                            
                    # Parse children
                    children = []
                    while self.pos < len(self.html):
                        # Peek if it's the matching end tag
                        if self.peek() == '<' and self.pos + 1 < len(self.html) and self.html[self.pos + 1] == '/':
                            # Parse end tag and verify
                            end_tag = self.parse()
                            if end_tag != tag_name:
                                raise ValueError(f"Tag mismatch: expected </{tag_name}>, got </{end_tag}>")
                            break
                        else:
                            child = self.parse()
                            if child:
                                if isinstance(child, str):
                                    # Text node
                                    children.append(Node(text=child))
                                else:
                                    children.append(child)
                    
                    return Node(tag_name=tag_name, attributes=attributes, children=children)
            else:
                # Text node
                text = ""
                while self.pos < len(self.html) and self.peek() != '<':
                    text += self.consume()
                return text.strip()
        return None
