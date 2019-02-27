PDF := gp_slides.pdf

LATEX := pdflatex -interaction=batchmode -halt-on-error

.PHONY: all clean

all: $(PDF)

$(PDF): %.pdf: %.tex slides.tex aliases.tex
	@$(LATEX) $* > /dev/null && \
	$(LATEX) $* > /dev/null || \
	printf "\033[0;31mCompilation failed\033[0m\n"
	@awk '/ [W]arning[: ]/{a=1}/^$$/{a=0}a' $*.log | sed "s/.*[Ww]arning.*/\x1b[33m&\x1b[0m/"
	@awk '/^!/{a=1}/}$$/{print;a=0}a' $*.log | sed "s/^!.*/\x1b[31m&\x1b[0m/"

clean:
	@rm -fv *.aux *.toc *.out *.log *.nav *.snm \
		*.bbl *.blg *-blx.bib *.run.xml $(PDF)

