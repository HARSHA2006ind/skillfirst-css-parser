
import json
import sys
from pathlib import Path
import tinycss2


def parse_css(css_text):
    # Parse the CSS file, ignoring comments and whitespace
    stylesheet = tinycss2.parse_stylesheet(
        css_text,
        skip_comments=True,
        skip_whitespace=True
    )

    rules = []
    warnings = []

    # Process each CSS rule
    for index, rule in enumerate(stylesheet, start=1):

        # Handle CSS syntax errors detected by tinycss2
        if rule.type == "error":
            warnings.append({
                "rule": index,
                "message": rule.message
            })
            continue

        # Process only standard selector-based CSS rules
        if rule.type != "qualified-rule":
            continue

        # Extract the selector
        selector = tinycss2.serialize(rule.prelude).strip()

        # Parse declarations inside the rule
        declarations = tinycss2.parse_declaration_list(
            rule.content,
            skip_comments=True,
            skip_whitespace=True
        )

        properties = []

        for declaration in declarations:

            # Handle malformed declarations detected by tinycss2
            if declaration.type == "error":
                warnings.append({
                    "rule": index,
                    "selector": selector,
                    "message": declaration.message
                })
                continue

            # Ignore items that are not declarations
            if declaration.type != "declaration":
                continue

            # Extract the property's value
            value = tinycss2.serialize(
                declaration.value
            ).strip()

            # Detect empty values, such as: padding:;
            if not value:
                warnings.append({
                    "rule": index,
                    "selector": selector,
                    "property": declaration.name,
                    "message": "Empty CSS property value"
                })
                continue

            # Store the property, value, and !important status
            properties.append({
                "property": declaration.name,
                "value": value,
                "important": bool(declaration.important)
            })

        # Store the selector and its declarations
        rules.append({
            "selector": selector,
            "declarations": properties
        })

    return {
        "rules": rules,
        "warnings": warnings
    }


def main():
    # Check whether the CSS file was provided
    if len(sys.argv) != 2:
        print(
            "Usage: python parser.py <css-file>",
            file=sys.stderr
        )
        sys.exit(2)

    css_file = Path(sys.argv[1])

    # Read the CSS file
    try:
        css_text = css_file.read_text(encoding="utf-8")
    except OSError as error:
        print(
            f"Error reading file: {error}",
            file=sys.stderr
        )
        sys.exit(1)

    # Parse the CSS and print the result as JSON
    result = parse_css(css_text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
