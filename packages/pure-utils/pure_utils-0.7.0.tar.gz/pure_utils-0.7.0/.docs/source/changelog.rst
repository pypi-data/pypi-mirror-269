Changelog
=========

v0.7.0 - [2024-04-22]
---------------------
* Add new module - ``repeaters`` (utilities for repeat functions).
* Update development dependencies.

v0.6.0 - [2024-03-01]
---------------------
* Add ``unpack`` utility in ``containers`` module.
* Add function synopsis in README short descriptions.
* Fix examples in docstrings.
* Fix tests for ``debug.caller``.
* Fix ``containers`` function signatures.
* Fix README links for ``containers`` utilities.
* Change development status to Beta.
* Rename ``datetime`` module to ``times``.

v0.5.0 - [2024-02-25]
---------------------
* Add new module - ``containers`` (utilities for working with data containers).
* Update versions build and dev dependencies.

v0.4.1 - [2024-02-20]
---------------------
* Add ``_internal`` subpackage (with "private" modules).
* Rename ``dt`` module to ``datetime``.
* Refactor imports into tests.
* Refactor variables into ``debug``, ``profiler`` and ``_internal/*`` modules.

v0.4.0 - [2024-02-19]
---------------------
* Add support Python3.12 into ci scenario.
* Add several tests (for ``dt`` module) for python3.10 only.
* Add new module - ``debug`` (utilities for debugging and development).
* Add new module - ``profiler`` (helper classes for working with the cProfile).
* Refactor .docs/Makefile.
* Use flake8 explicitly into Makefile and ci scenario.
* Remove ``pyproject-flake8`` optional dependencies, because it's orphaned on github.

v0.3.0 - [2024-02-04]
---------------------
* Add new module - ``dt`` (utilities for working with datetime objects).

v0.2.0 - [2024-02-02]
---------------------
* Add new string utilities module.
* Add short utilities description in README.
* Add new make commands (``tests-cov-json``, ``tests-cov-html``).
* Fix coverage settings.
* Remove ``run_tests.sh``.
* Rename github workflow scenario.

v0.1.1 - [2024-02-01]
---------------------
* Add badges for gh-repo.
* Add new make-command: ``upload`` (for upload built packages to PyPI).
* Fix Makefile.
* Fix Sphinx docs.
* Fix package name in README.

v0.1.0 - [2024-02-01]
---------------------
* Create project repository with infrastructure:
  python project, github actions, makefile automations, docs, etc).
* Add a first general-purpose utility - metaclass for creating the singletons.
