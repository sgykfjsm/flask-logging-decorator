LANG = LANG=en_US.UTF-8
PIPENV_RUN = $(LANG) pipenv run

init:
	pip install pipenv --upgrade
	$(LANG) pipenv install --dev --skip-lock

lint:
	@# E501	line too long (82 > 79 characters)
	@# F401	module imported but unused
	@# E128	continuation line under-indented for visual indent
	@# E402	module level import not at top of file
	$(PIPENV_RUN) flake8 --ignore=E501,F401,E128,E402, flask_logging_decorator
	$(PIPENV_RUN) mypy flask_logging_decorator --follow-imports=skip --disallow-untyped-defs --disallow-incomplete-defs --check-untyped-defs --no-implicit-optional --strict-optional --show-error-context --ignore-missing-imports

test:
	$(PIPENV_RUN) pipenv run python -m pytest -v

publish:
	$(PIPENV_RUN) pip install twine wheel --upgrade
	$(PIPENV_RUN) python setup.py sdist bdist_wheel
	@#$(PIPENV_RUN) twine upload --repository pypitest dist/*
	$(PIPENV_RUN) twine upload dist/*
	$(RM) -r build dist .egg flask_logging_decorator.egg-info

clean:
	$(RM) -r build dist .egg flask_logging_decorator.egg-info
