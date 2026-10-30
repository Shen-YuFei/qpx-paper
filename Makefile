# Build the manuscript from manuscript/*.md.
# docx: for co-author comments; tex/pdf: Springer Nature LaTeX class (sn-jnl).
PANDOC   ?= pandoc
TECTONIC ?= tectonic

META     := manuscript/metadata.yaml
SECTIONS := $(sort $(wildcard manuscript/[0-9]*.md))
BIB      := references.bib
OUT      := build/qpx-paper

.PHONY: all docx tex pdf clean
all: docx pdf
docx: $(OUT).docx
tex: $(OUT).tex
pdf: $(OUT).pdf

$(OUT).docx: $(META) $(SECTIONS) $(BIB) templates/nature.csl
	@mkdir -p build
	$(PANDOC) $(META) $(SECTIONS) --resource-path=.:figures --citeproc \
		--bibliography=$(BIB) --csl=templates/nature.csl -o $@

$(OUT).tex: $(META) $(SECTIONS) $(BIB) templates/sn-template.tex
	@mkdir -p build
	$(PANDOC) $(META) $(SECTIONS) --natbib --bibliography=$(BIB) \
		--template=templates/sn-template.tex -s -o $@

$(OUT).pdf: $(OUT).tex templates/sn-jnl.cls templates/sn-nature.bst
	cp templates/sn-jnl.cls templates/sn-nature.bst $(BIB) build/
	cd build && $(TECTONIC) --keep-logs qpx-paper.tex

clean:
	rm -rf build
