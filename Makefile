# term2048's Makefile
#
SRC=term2048

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

PY_VERSION:=$(subst ., ,$(shell python --version 2>&1 | cut -d' ' -f2))
PY_VERSION_MAJOR:=$(word 1,$(PY_VERSION))
PY_VERSION_MINOR:=$(word 2,$(PY_VERSION))
PY_VERSION_SHORT:=$(PY_VERSION_MAJOR).$(PY_VERSION_MINOR)

ifdef TRAVIS_PYTHON_VERSION
PY_VERSION_SHORT:=$(TRAVIS_PYTHON_VERSION)
endif

.DEFAULT: check-versions
.PHONY: check check-versions stylecheck covercheck

deps:
	pip install -qr requirements.txt
ifeq ($(PY_VERSION_SHORT),2.6)
	pip install -qr py26-requirements.txt
endif
ifneq ($(PY_VERSION_SHORT),3.3)
	pip install -q wsgiref==0.1.2
endif

check:
	python tests/test.py

check-versions:
	tox

stylecheck:
	pep8 $(SRC)

covercheck:
	coverage run --source=term2048 tests/test.py
	coverage $(COVERAGE_REPORT)

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

publish: check-versions
	python setup.py sdist upload
