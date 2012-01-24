all: diginorm.pdf

clean:
	rm -fr *.log *.aux diginorm.pdf

diginorm.pdf: diginorm.tex
	pdflatex diginorm
#	bibtex diginorm
	pdflatex diginorm
#	pdflatex diginorm
