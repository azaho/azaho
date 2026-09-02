#!/usr/bin/env python3
"""Generate the canonical LaTeX CV from cv.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CV_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = CV_DIR / "cv.json"
DEFAULT_TEMPLATE = CV_DIR / "template.tex"
TEMPLATE_MARKER = "%% CV_CONTENT %%"


def latex_escape(value: str) -> str:
    """Escape plain text for use inside LaTeX commands."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    escaped = re.sub(r"[\\&%$#_{}~^]", lambda match: replacements[match.group()], value)
    return (
        escaped.replace("->", r"$\rightarrow$")
        .replace("—", "---")
        .replace("–", "--")
        .replace("’", "'")
        .replace("“", "``")
        .replace("”", "''")
    )


def load_data(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    validate_data(data)
    return data


def validate_data(data: dict[str, Any]) -> None:
    if data.get("schema_version") != 1:
        raise ValueError("cv.json must use schema_version 1")
    if not isinstance(data.get("document"), dict):
        raise ValueError("cv.json is missing the document object")
    if not isinstance(data.get("sections"), list):
        raise ValueError("cv.json is missing the sections array")

    seen: set[str] = set()
    for section in data["sections"]:
        section_id = section.get("id")
        if not section_id or section_id in seen:
            raise ValueError(f"Missing or duplicate section id: {section_id!r}")
        seen.add(section_id)
        for item in section.get("items", []):
            item_id = item.get("id")
            if not item_id or item_id in seen:
                raise ValueError(f"Missing or duplicate item id: {item_id!r}")
            seen.add(item_id)
            if "include_by_default" not in item:
                raise ValueError(f"{item_id} is missing include_by_default")


def is_selected(item: dict[str, Any], args: argparse.Namespace) -> bool:
    item_id = item["id"]
    if item_id in args.exclude:
        return False
    return args.all or item["include_by_default"] or item_id in args.include


def selected_bullets(item: dict[str, Any], include_all: bool) -> list[dict[str, Any]]:
    return [
        bullet
        for bullet in item.get("bullets", [])
        if include_all or bullet.get("include_by_default", True)
    ]


def render_bullets(item: dict[str, Any], include_all: bool) -> list[str]:
    bullets = selected_bullets(item, include_all)
    if not bullets:
        return []
    lines = [r"      \resumeItemListStart"]
    lines.extend(f"        \\resumeItem{{{latex_escape(bullet['text'])}}}" for bullet in bullets)
    lines.append(r"      \resumeItemListEnd")
    return lines


def render_subheading(item: dict[str, Any], include_all: bool) -> list[str]:
    lines = [
        r"    \resumeSubheading",
        f"      {{{latex_escape(item['title'])}}}{{{latex_escape(item['date'])}}}",
        f"      {{{latex_escape(item['subtitle'])}}}{{{latex_escape(item['location'])}}}",
    ]
    lines.extend(render_bullets(item, include_all))
    return lines


def render_multi_subheading(item: dict[str, Any], include_all: bool) -> list[str]:
    affiliations = item.get("affiliations", [])
    if not affiliations:
        raise ValueError(f"{item['id']} needs at least one affiliation")

    first = affiliations[0]
    first_org = (
        f"{latex_escape(first['organization'])} "
        f"{{\\color{{dark-grey}} \\small ({latex_escape(first['date'])})}}"
    )
    lines = [
        r"    \resumeSubheading",
        f"      {{{latex_escape(item['title'])}}}{{}}",
        f"      {{{first_org}}}{{{latex_escape(first['location'])}}}",
    ]

    continuation_macros = [
        "resumeSubheadingPrime",
        "resumeSubheadingPrimePrime",
        "resumeSubheadingPrimePrimePrime",
    ]
    for index, affiliation in enumerate(affiliations[1:]):
        macro = continuation_macros[min(index, len(continuation_macros) - 1)]
        org = (
            f"{latex_escape(affiliation['organization'])} "
            f"{{\\color{{dark-grey}} \\small ({latex_escape(affiliation['date'])})}}"
        )
        lines.extend(
            [
                f"    \\{macro}",
                f"      {{{org}}}{{{latex_escape(affiliation['location'])}}}",
            ]
        )
    lines.extend(render_bullets(item, include_all))
    return lines


def render_publication(item: dict[str, Any]) -> str:
    suffix = item.get("suffix", "").strip()
    suffix_latex = f" {latex_escape(suffix)}." if suffix else ""
    title_punctuation = "" if item["title"].rstrip().endswith((".", "?", "!")) else "."
    return (
        r"  \resumeItem{"
        + item["authors_latex"]
        + f" ({latex_escape(item['year_venue'])}). "
        + r"\textit{"
        + latex_escape(item["title"])
        + title_punctuation
        + "}"
        + suffix_latex
        + "}"
    )


def render_awards(items: list[dict[str, Any]]) -> list[str]:
    lines = [r"{\small", r"\begin{tabularx}{\textwidth}{@{}Xr@{}}"]
    for index, item in enumerate(items):
        organization = item.get("organization", "").strip()
        organization_latex = f" --- {latex_escape(organization)}" if organization else ""
        spacing = r"\\" if index == len(items) - 1 else r"\\[2pt]"
        lines.append(
            f"    \\textbf{{{latex_escape(item['name'])}}}{organization_latex} "
            f"& {{\\color{{dark-grey}} {latex_escape(item['date'])}}}{spacing}"
        )
    lines.extend([r"\end{tabularx}", "}"])
    return lines


def render_skills(item: dict[str, Any]) -> list[str]:
    lines = [r"\begin{itemize}[leftmargin=0in,label={}]", r"  \small{\item{"]
    for index, line in enumerate(item.get("lines", [])):
        ending = "\\vspace{2pt}\\\\" if index < len(item["lines"]) - 1 else ""
        lines.append(
            f"    \\textbf{{{latex_escape(line['label'])}}}: "
            f"{latex_escape(line['text'])}{ending}"
        )
    lines.extend(["  }}", r"\end{itemize}"])
    return lines


def render_standard_section(items: list[dict[str, Any]], include_all: bool) -> list[str]:
    lines = [r"\resumeSubHeadingListStart"]
    for item in items:
        if item["type"] == "subheading":
            lines.extend(render_subheading(item, include_all))
        elif item["type"] == "multi_subheading":
            lines.extend(render_multi_subheading(item, include_all))
        elif item["type"] == "publication":
            lines.append(render_publication(item))
        else:
            raise ValueError(f"Unsupported standard item type: {item['type']}")
        lines.append("")
    lines.append(r"\resumeSubHeadingListEnd")
    return lines


def render_document(data: dict[str, Any], args: argparse.Namespace) -> str:
    document = data["document"]
    contact_line = (
        f"  \\small {latex_escape(document['email'])} \\hspace{{1pt}} $|$ "
        f"\\hspace{{1pt}} \\href{{{document['website']}}}"
        f"{{{latex_escape(document['website'])}}} \\\\"
    )
    lines = [
        "% This file is generated by cv/build.py. Edit cv/cv.json instead.",
        f"% Profile: {document['default_profile']}{' + all optional items' if args.all else ''}",
        "",
        r"\begin{center}",
        f"  \\textbf{{\\Large {latex_escape(document['name'])}}} \\\\ \\vspace{{5pt}}",
        contact_line,
        r"  \vspace{-3pt}",
        r"\end{center}",
        "",
    ]

    for section in data["sections"]:
        items = [item for item in section["items"] if is_selected(item, args)]
        if not items:
            continue
        if section.get("page_break_before"):
            lines.extend([r"\newpage", ""])
        lines.extend([f"\\section{{{latex_escape(section['title'])}}}"])
        item_types = {item["type"] for item in items}
        if item_types == {"award"}:
            lines.extend(render_awards(items))
        elif item_types == {"skills"}:
            for item in items:
                lines.extend(render_skills(item))
        else:
            lines.extend(render_standard_section(items, args.all))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def list_items(data: dict[str, Any]) -> None:
    for section in data["sections"]:
        print(f"{section['title']} ({section['id']})")
        for item in section["items"]:
            marker = "x" if item["include_by_default"] else " "
            label = item.get("title") or item.get("name") or item["id"]
            print(f"  [{marker}] {item['id']}: {label}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--all", action="store_true", help="include every optional item and bullet")
    parser.add_argument("--include", action="append", default=[], metavar="ITEM_ID")
    parser.add_argument("--exclude", action="append", default=[], metavar="ITEM_ID")
    parser.add_argument("--list", action="store_true", help="list item IDs and exit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.include = set(args.include)
    args.exclude = set(args.exclude)
    data = load_data(args.data)

    if args.list:
        list_items(data)
        return

    known_ids = {item["id"] for section in data["sections"] for item in section["items"]}
    unknown_ids = (args.include | args.exclude) - known_ids
    if unknown_ids:
        raise ValueError(f"Unknown item IDs: {', '.join(sorted(unknown_ids))}")

    output = args.output or CV_DIR / f"{data['document']['output_basename']}.tex"
    template = args.template.read_text(encoding="utf-8")
    if template.count(TEMPLATE_MARKER) != 1:
        raise ValueError(f"template must contain exactly one {TEMPLATE_MARKER!r} marker")
    generated = template.replace(TEMPLATE_MARKER, render_document(data, args))
    output.parent.mkdir(parents=True, exist_ok=True)
    if not output.exists() or output.read_text(encoding="utf-8") != generated:
        output.write_text(generated, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
