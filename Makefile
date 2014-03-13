# M1Algo project's Makefile
#
COVERFILE=.coverage

SOURCEVENV=source venv/bin/activate;

.DEFAULT: check
.PHONY: check covercheck

deps:
	pip install -qr requirements.txt

check:
	$(SOURCEVENV) \
	python tests/test.py

covercheck:
	$(SOURCEVENV) \
	coverage3 run --omit='tests/**' tests/test.py
	$(SOURCEVENV) \
	coverage3 report -m

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

