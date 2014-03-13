# M1Algo project's Makefile
#
COVERFILE=.coverage

.DEFAULT: check
.PHONY: check covercheck

deps:
	pip install -qr requirements.txt

check:
	python tests/test.py

covercheck:
	coverage3 run --omit='tests/**' tests/test.py
	coverage3 report -m

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

