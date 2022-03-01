# Contributing to `term2048`

## Bugs
If you find a bug, you can either (1) make a pull-request with a fix or (2)
open an issue. In the latter case, please describe how to reproduce the bug.

I don’t have access to a Windows machine, so my ability to reproduce (and fix)
issues on that OS is very limited.

## New features
I consider `term2048` to be stable; please don’t add new features.

## Make a release

1. Update the CHANGELOG
2. Update the version in `pyproject.toml` and in `term2048/__init__.py`
3. Commit
4. Push and wait for the CI job to succeed
5. Tag with `v` followed by the version (e.g. `git tag v1.0.0`)
6. Push the tag
7. Wait for the [CI job][ci] to finish

[ci]: https://github.com/bfontaine/term2048/actions/workflows/publish.yml
