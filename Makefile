SCRIPT_CMD = script -q /dev/null
LANG = LANG=en_US.UTF-8
PYTHON_SYS_PATH := $(shell $(LANG) pipenv run python -c 'import sys; print(sys.path[-1])')

init:
	pip install pipenv --upgrade
	$(LANG) pipenv install --dev --skip-lock

lint:
	@# E501	line too long (82 > 79 characters)
	@# F401	module imported but unused
	@# E128	continuation line under-indented for visual indent
	@# E402	module level import not at top of file
	$(LANG) $(SCRIPT_CMD) pipenv run flake8 --ignore=E501,F401,E128,E402, flask_logging_decorator
	MYPYPATH="$(PYTHON_SYS_PATH)" $(LANG) $(SCRIPT_CMD) pipenv run mypy flask_logging_decorator --follow-imports=skip --disallow-untyped-defs --disallow-incomplete-defs --check-untyped-defs --no-implicit-optional --strict-optional --show-error-context --ignore-missing-imports

test:
	$(LANG) $(SCRIPT_CMD) pipenv run python -m pytest -v
