#!/usr/bin/env python3
"""Render the namespace and deletion protection manifests from the Jinja2 template."""

import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "namespace-protection.yaml.j2"
PLACEHOLDER = "{{ namespace_name }}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("namespace_name", help="Kubernetes namespace name")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=HERE / "namespace-protection.yaml",
        help="output YAML path (default: namespace-protection.yaml)",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", args.namespace_name):
        parser.error("namespace_name must be a lowercase DNS label (letters, digits, hyphens)")
    if len(args.namespace_name) > 63:
        parser.error("namespace_name must be 63 characters or fewer")

    template = TEMPLATE.read_text(encoding="utf-8")
    rendered = template.replace(PLACEHOLDER, args.namespace_name)
    if "{{" in rendered or "}}" in rendered:
        parser.error("template contains an unsupported or unresolved Jinja2 expression")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
