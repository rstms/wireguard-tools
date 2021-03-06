# top-level Makefile 

uninstall: ## remove module from the local python environment
	pip uninstall -yqq $(project)

install: ## install to the local environment from the source directory
	pip install --upgrade .

dev: uninstall ## local install in editable mode for development
	pip install --upgrade -e .[dev]

clean: ## remove all build, test, coverage and Python artifacts
	for clean in $(call included,clean); do ${MAKE} $$clean; done

include $(wildcard make.include/*.mk)
