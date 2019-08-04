# Contributing to `term2048`

## Bugs
If you find a bug, you can either (1) make a pull-request with a fix or (2)
open an issue. In the latter case, please describe how to reproduce the bug.

I don’t have access to a Windows machine, so my ability to reproduce (and fix)
issues on that OS is very limited.

## New features
I consider `term2048` to be stable; please don’t add new features.

## Make a release

1. Ensure tests pass. CI should be green. Run `python3 tests/test.py` and
   `python2 tests/test.py`
2. Add an entry in the changelog; bump the version in `term2048/__init__.py`;
   commit; tag; push.
2. `rm -rf dist` to remove old distribution files
3. `python3 setup.py sdist bdist_wheel`
4. `twine check dist/*`. Fix any warning.
5. `twine upload dist/*`
