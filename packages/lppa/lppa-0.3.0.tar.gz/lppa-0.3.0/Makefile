.PHONY: clean devel check build

build: clean
	python -m build
	twine check dist/*

check:
	flake8 tests lppa
	coverage run --source=lppa -m pytest -v tests

coverage: check
	coverage report
	coverage html

devel:
	pip install -r requirements-dev.txt
	echo 'import setuptools; setuptools.setup()' > setup.py
	pip install -e .
	rm setup.py

clean:
	rm -rf *.egg-info dist build .pytest_cache */__pycache__ .coverage htmlcov

publish: build
	twine upload dist/*

set-release-version:
	sed -Ei "s/^(__version__ = '[0-9]+\.[0-9]+\.[0-9]+)\.dev[0-9]+'$$/\1'/" lppa/__init__.py
	git add lppa/__init__.py

set-devel:
	VERSION=$$(sed -En "s/__version__ = '([0-9]+\.[0-9]+\.[0-9]+)'$$/\1/p" lppa/__init__.py); \
				if [ -z "$VERSION" ]; then \
					echo 'Version is not in the expected format. Is this a release version?'; \
					exit 1; \
				fi; \
				PATCH=$$(sed -En "s/__version__ = '[0-9]+\.[0-9]+\.([0-9]+)'$$/\1/p" lppa/__init__.py); \
				PATCH=$$((PATCH + 1)); \
				sed -Ei "s/__version__ = '([0-9]+)\.([0-9]+)\.[0-9]+'$$/__version__ = '\1.\2.$${PATCH}.dev1'/" lppa/__init__.py; \
	git add lppa/__init__.py
	git commit -s -m "Set development version"

changelog:
	towncrier build --yes
	sed -i "s/ ()$$//" CHANGELOG.md
	# https://github.com/twisted/towncrier/issues/340
	sed -i "1s/).*/)/" CHANGELOG.md
	git add CHANGELOG.md

tag-release:
	VERSION=$$(sed -En "s/__version__ = '([0-9]+\.[0-9]+\.[0-9]+)'$$/\1/p" lppa/__init__.py); \
					if [ -z "$$VERSION" ]; then \
						echo 'Version is not in the expected format. Is this a release version?'; \
						exit 1; \
					fi; \
					echo tagging $$VERSION as v$$VERSION; \
					git commit -s -m "Prepare $$VERSION release"; \
					git tag v$$VERSION

release: clean set-release-version changelog tag-release publish set-devel
