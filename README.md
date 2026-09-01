# Andrii Zahorodnii

Email: ✉️ zaho [at] mit [dot] edu

[GitHub](https://github.com/azaho) | [LinkedIn](https://www.linkedin.com/in/zaho/) | [Google Scholar](https://scholar.google.com/citations?user=je-fgs8AAAAJ&hl=en) | [Personal Website](https://azaho.org)

## About Me 👋

I am a Member of Technical Staff at [Merge Labs](https://merge.io/), working at the intersection of neuroscience and machine learning.

I completed my undergraduate and master's studies at [MIT](https://www.mit.edu/) in Computer Science and Brain and Cognitive Sciences, where my research focused on representation learning from large-scale human neural recordings. At MIT, I was advised by [Ila Fiete](https://fietelab.mit.edu/) and previously worked with [Guangyu Robert Yang](https://www.linkedin.com/in/robert-yang-41a83019).

I co-founded the [Ukraine Leadership and Technology Academy](https://ultacademy.org/) to equip brilliant young Ukrainians with the skills, knowledge, and confidence they need to rebuild Ukraine into a thriving, European nation. I also won the [Schwarzman Scholarship](https://news.mit.edu/2025/mit-students-named-schwarzman-scholars-0115) (class of 2026), and am a [Cerebras Fellow](https://cerebras.ai/blog/aibi-revolutionizing-ai-interviewing). I co-organize [TEDxMIT](https://tedx.mit.edu/team).

## Publications and Writing

Please see my [personal website](https://azaho.org) for a list of publications and writing.

## CV

The CV is generated from [`cv/cv.json`](cv/cv.json), the single source of truth for all current and optional entries. Each item has an `include_by_default` flag. The default selection reproduces the February 2026 CV; older material is retained with the flag set to `false`.

Useful commands:

```bash
# Show default and optional item IDs.
python3 cv/build.py --list

# Regenerate the default LaTeX file.
python3 cv/build.py

# Add one optional entry to a custom build.
python3 cv/build.py --include promys-europe --output /tmp/cv-with-promys.tex

# Include every optional item and optional bullet.
python3 cv/build.py --all --output /tmp/cv-complete.tex

# Build the default PDF with the existing TeX Live 2024 installation.
make cv
```

The Makefile uses `~/texlive/2024/bin/universal-darwin`, the same pinned TeX Live installation used by the SMI manuscript. Override `TEXBIN` if that installation moves.

Pushing a change to the JSON, generator, or template runs [the CV workflow](.github/workflows/build-cv.yml). It regenerates the LaTeX source, compiles `cv/andrii-zahorodnii-cv.pdf`, and commits the current generated files. The website's **CV (PDF)** navigation link always points to that stable path.
