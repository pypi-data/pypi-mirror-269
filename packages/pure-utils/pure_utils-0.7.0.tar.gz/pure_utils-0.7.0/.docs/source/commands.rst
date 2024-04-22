Make commands
=============

Actual for contributors only.

Dependencies
------------
- ``make deps-dev`` - Install only development dependencies.
- ``make deps-docs`` - Install only documentation dependencies.
- ``make deps-build`` - Install only build system dependencies.
- ``make deps`` - Install all dependencies.

Distributing
------------
- ``make build-sdist`` - Build a source distrib.
- ``make build-wheel`` - Build a pure python wheel distrib.
- ``make build`` - Build both distribs (source and wheel).
- ``make upload`` - Upload built packages to PyPI..

Development
-----------
- ``make cleanup`` - Clean up python temporary files and caches.
- ``make format`` - Fromat the code (by black and isort).
- ``make lint`` - Check code style and types (by flake8, pydocstyle and mypy).
- ``make tests`` - Run tests with coverage measure (output to terminal).
- ``make tests-cov-json`` - Run tests with coverage measure (output to json [coverage.json]).
- ``make tests-cov-html`` - Run tests with coverage measure (output to html [coverage_report/]).
