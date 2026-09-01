.PHONY: cv cv-tex cv-clean

TEXBIN ?= $(HOME)/texlive/2024/bin/universal-darwin
LATEXMK := PATH="$(TEXBIN):$(PATH)" latexmk

cv-tex:
	python3 cv/build.py

cv: cv-tex
	cd cv && $(LATEXMK) -pdf -file-line-error -halt-on-error -interaction=nonstopmode andrii-zahorodnii-cv.tex

cv-clean:
	cd cv && $(LATEXMK) -c andrii-zahorodnii-cv.tex
