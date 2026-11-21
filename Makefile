# Build the manuscript from manuscript/*.md.
# docx: for co-author comments; tex/pdf: Springer Nature LaTeX class (sn-jnl);
# si: the Supplementary Information as a separate PDF with its own reference list.
PANDOC   ?= pandoc
TECTONIC ?= tectonic

META     := manuscript/metadata.yaml
SECTIONS := $(sort $(wildcard manuscript/[0-9]*.md))
BIB      := references.bib data/dataset_citations.bib
OUT      := build/qpx-paper
FIGS     := $(wildcard figures/*)
SI       := manuscript/supplementary-information.md

.PHONY: all docx tex pdf si clean
all: docx pdf si
docx: $(OUT).docx
tex: $(OUT).tex
pdf: $(OUT).pdf
si: $(OUT)-si.pdf

$(OUT).docx: $(META) $(SECTIONS) $(BIB) $(FIGS) templates/nature.csl
	@mkdir -p build
	$(PANDOC) $(META) $(SECTIONS) --resource-path=.:figures --citeproc \
		--default-image-extension=png \
		$(addprefix --bibliography=,$(BIB)) --csl=templates/nature.csl -o $@

$(OUT).tex: $(META) $(SECTIONS) $(BIB) templates/sn-template.tex
	@mkdir -p build
	$(PANDOC) $(META) $(SECTIONS) --natbib $(addprefix --bibliography=,$(BIB)) \
		--default-image-extension=pdf \
		--template=templates/sn-template.tex -s -o $@

$(OUT).pdf: $(OUT).tex $(FIGS) templates/sn-jnl.cls templates/sn-nature.bst
	cp templates/sn-jnl.cls templates/sn-nature.bst $(BIB) build/
	cp -r figures build/
	cd build && $(TECTONIC) --keep-logs qpx-paper.tex

$(OUT)-si.pdf: $(SI) $(BIB) $(FIGS) templates/nature.csl
	@mkdir -p build
	$(PANDOC) $(SI) --resource-path=.:figures --default-image-extension=pdf --citeproc \
		$(addprefix --bibliography=,$(BIB)) --csl=templates/nature.csl --toc \
		--pdf-engine=$(TECTONIC) -o $@

clean:
	rm -rf build
