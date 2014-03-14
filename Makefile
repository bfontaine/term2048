# M1Algo project's Makefile
#
COVERFILE=.coverage

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
	coverage report -m

clean:
	rm -f *~ */*~
	rm -f $(COVERFILE)

publish: check-versions
	@echo === DEPRECATED ===
	@echo Releases are now published through Travis-CI.
	@echo Tag the commit and push, and Travis will take care of the rest.
