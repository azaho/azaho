---
name: azaho-cv
description: Maintain Andrii Zahorodnii's data-driven CV and use its canonical structured data for tasks that need current biographical or professional information. Use when editing or rebuilding the CV, selecting optional CV material, updating matching website facts, or answering and drafting from Andrii's education, experience, publications, honors, teaching, leadership, or public contact details.
---

# Azaho CV

Use the repository data rather than reconstructing the CV from memory or from the generated PDF.

## Locate the CV

Resolve paths from the repository root (`git rev-parse --show-toplevel`). The usual canonical clone on Andrii's laptop is `/Users/andrii/utils/azaho`.

- `cv/cv.json`: canonical structured content, including current and optional entries.
- `cv/build.py`: JSON-to-LaTeX generator and selection CLI.
- `cv/template.tex`: LaTeX layout and macros.
- `cv/andrii-zahorodnii-cv.tex`: generated; do not edit by hand.
- `cv/andrii-zahorodnii-cv.pdf`: generated public PDF.
- `cv/test_build.py`: generator and content invariants.
- `Makefile`: local build commands.
- `.github/workflows/build-cv.yml`: automatic build on `main`.
- `index.html`: website bio, publication cards, and the stable CV link.

Public locations:

- Website: `https://azaho.org`
- Current PDF: `https://azaho.org/cv/andrii-zahorodnii-cv.pdf`
- Repository: `https://github.com/azaho/azaho`

The Overleaf project and `source_file` recorded in `cv/cv.json` are historical provenance. They are not the current editing surface.

## Use CV information in another task

1. Read `cv/cv.json` first. Treat it as the canonical CV superset.
2. Use entries with `include_by_default: true` for claims about the current public CV. Entries marked `false` are real historical or optional material, but do not imply that they appear in the published PDF.
3. For website-specific summaries, links, or publication statuses, also inspect `index.html`.
4. Prefer information supplied by Andrii in the current request when it is newer or more specific. If a time-sensitive fact may have changed, verify it with the authoritative source or flag the uncertainty; do not silently invent an update.
5. Use each item's `sources` field for provenance when relevant. Do not treat the `document.default_profile` label as a last-updated timestamp; the current default is determined by the flags and present data.
6. Select only facts relevant to the requested artifact. Do not dump the entire CV into bios, forms, nominations, or applications.

Public contact information is intentionally limited to `zaho [at] mit [dot] edu` and `https://azaho.org`. Do not add or disclose a personal phone number, home address, birth date, member ID, receipt/order number, IP address, or other private administrative data.

## Update the public CV

1. Inspect `git status` and preserve unrelated or untracked user files.
2. Edit content in `cv/cv.json`. Do not hand-edit the generated `.tex` or PDF. Edit `cv/template.tex` or `cv/build.py` only for layout or generator behavior.
3. Give every new section item a unique stable `id`, `type`, `include_by_default`, and useful `sources`. Set the flag to `false` when retaining an item only for future or targeted versions.
4. Update `index.html` when the same fact is presented on the website, especially roles, honors, publication authors, statuses, and links.
5. Run:

   ```bash
   python3 -m unittest cv/test_build.py
   python3 cv/build.py
   make cv
   ```

6. When the PDF changes, extract text for content checks and render every page to images for visual review. Check wrapping, clipping, overlaps, section transitions, page count, and the contact line.
7. Confirm `git diff --check`, inspect the focused diff, and verify that generated `.tex` and PDF match the JSON.
8. Commit the JSON, tests, generated `.tex`, generated PDF, and any intentional website or workflow changes together. Push only when the user asks to publish.
9. After a push, verify the `Build CV` and Pages workflows and check both public URLs. Git history is public: if sensitive information appeared in an unpublished intermediate commit, clean that history before pushing.

## Build targeted versions

List selectable entries with:

```bash
python3 cv/build.py --list
```

Use `--include ITEM_ID`, `--exclude ITEM_ID`, or `--all` for targeted versions. Write experiments to a temporary or explicitly requested output path. Do not replace the stable public PDF unless the user intends to change the default public CV.

The local Makefile expects TeX Live 2024 at `/Users/andrii/texlive/2024/bin/universal-darwin`; override `TEXBIN` if that installation moves.
