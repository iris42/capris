all:
	@echo "tasks:"
	@echo "  audit      Runs pep8 on library"
	@echo "  clean      Clean up all pyc and pyo files"
	@echo "  setup      Setup the local environment"
	@echo "  tests      Runs the tests for capris"
	@echo "  optimized  Optimized tests for IO time"

tests:
	python  -m capris.tests
	python3 -m capris.tests

optimized:
	python  -OO -m capris.tests
	python3 -OO -m capris.tests


setup:
	pip install --editable .
	easy_install sphinx-pypi-upload

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

audit:
	pep8 capris
