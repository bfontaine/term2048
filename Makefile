# M1Algo project's Makefile
#
COVERFILE=.coverage
COVERAGE_REPORT=report -m

.DEFAULT: check-versions
.PHONY: check check-versions covercheck

deps:
	pip install -qr requirements.txt

check:
	python tests/test.py

check-versions:
	tox

covercheck:
	coverage run --source=term2048 tests/test.py
	coverage $(COVERAGE_REPORT)

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

publish: check-versions
	python setup.py sdist upload
