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
	coverage run --omit='tests/**,venv/**' tests/test.py
	coverage report -m

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

publish: check
	python setup.py sdist upload
