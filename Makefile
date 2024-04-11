PORT?=8000
VERSION?=$(shell cat VERSION)
ALIAS?=latest
MKDOCSCONFIG?=mkdocs.yml
PIP?=pip3
MKDOCSFLAGS?=

DEV?=true
DEVALIAS?="dev"

PWD=$(CURDIR)

MAKEAUXFLAGS?=-s
MAKE=make ${MAKEAUXFLAGS}

MKDOCSCONFIG?=mkdocs.yml
MIKEFLAGS?=--push  \
	--remote origin  \
	--branch gh-pages  \
	--config-file ${MKDOCSCONFIG}

build:
	mkdocs build --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}


.PHONY: test-build
test-build: export MKDOCSFLAGS=--clean
test-build: export REPORT_TODOS=true
test-build: export REPORT_BROKEN_LINKS=true
test-build:
	@mkdocs build --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}
assets:
	@curl -s -o art.bib https://art.anoma.net/art.bib || echo "[!] Failed to download art.bib"

serve: assets
	mkdocs serve --dev-addr localhost:${PORT} --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}

.PHONY : mike
mike: assets
	@git fetch --all
	@git checkout gh-pages
	@git pull origin gh-pages --rebase
	@git checkout main
	mike deploy ${VERSION} ${MIKEFLAGS}

mike-serve: docs
	mike serve --dev-addr localhost:${PORT} --config-file ${MKDOCSCONFIG}

.PHONY: dev
dev: assets
	export DEV=true
	mike delete ${DEVALIAS} ${MIKEFLAGS} > /dev/null 2>&1 || true
	VERSION=${DEVALIAS} ${MAKE} mike

.PHONY: latest
latest: assets
	mike delete ${VERSION} ${MIKEFLAGS} > /dev/null 2>&1 || true
	${MAKE} mike
	mike alias ${VERSION} latest -u ${MIKEFLAGS}
	mike set-default ${MIKEFLAGS} ${VERSION}
	git tag -d v${VERSION} > /dev/null 2>&1 || true
	git tag -a v${VERSION} -m "Release v${VERSION}"


install:
	@echo "[!] Use a Python virtual environment if you are not using one."
	${PIP} install -r requirements.txt

.PHONY : pre-commit
pre-commit :
	@pre-commit run --all-files

clean:
	@rm -rf site \
			.juvix-mkdocs \
			.juvix-build \
			.cache \
			.mypy_cache \
			__pycache__
	@find . -type d -name "site" -exec rm -rf {} \;
