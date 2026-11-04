"""Compact exact-choice constraints for Outlines' regex decoder."""

import re


def choices_to_regex(choices):
    """Accept exactly the supplied labels, sharing common character prefixes.

    Outlines 0.1's generate.choice constructs a flat regex alternation. A prefix
    tree describes the same finite language with smaller intermediate automata.
    No labels are retrieved, ranked, or removed here.
    """
    labels = sorted(set(choices))
    if not labels or any(not isinstance(label, str) or not label for label in labels):
        raise ValueError("Provide at least one nonempty string label.")
    root = {}
    for label in labels:
        node = root
        for character in label:
            node = node.setdefault(character, {})
        node[None] = None

    def pattern(node):
        branches = [re.escape(char) + pattern(child) for char, child in node.items() if char is not None]
        if not branches:
            return ""
        result = branches[0] if len(branches) == 1 else "(?:" + "|".join(branches) + ")"
        return "(?:" + result + ")?" if None in node else result

    return pattern(root)
