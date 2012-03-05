all: diginorm.pdf abstract.pdf

clean:
	rm -fr *.log *.aux diginorm.pdf

diginorm.pdf: diginorm.tex diginorm.bib
	pdflatex diginorm
	bibtex diginorm
	pdflatex diginorm
	pdflatex diginorm

abstract.pdf: abstract.tex
	pdflatex abstract
	pdflatex abstract
