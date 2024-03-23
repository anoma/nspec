PORT?=8000
VERSION?=$(shell cat VERSION)
ALIAS?=latest
MKDOCSCONFIG?=mkdocs.yml
PIP?=pip3
MKDOPCSFLAGS?=

DEV?=true
DEVALIAS?="dev"

PWD=$(CURDIR)

MAKEAUXFLAGS?=-s
MAKE=make ${MAKEAUXFLAGS}

PORT?=8000
MKDOCSCONFIG?=mkdocs.yml
MIKEFLAGS?=--push  \
	--remote origin  \
	--branch gh-pages  \
	--config-file ${MKDOCSCONFIG}

build:
	mkdocs build --config-file ${MKDOCSCONFIG}

serve:
	mkdocs serve --dev-addr localhost:${PORT} --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}

.PHONY : mike
mike:
	@git fetch --all
	@git checkout gh-pages
	@git pull origin gh-pages --rebase
	@git checkout main
	mike deploy ${VERSION} ${MIKEFLAGS}

mike-serve: docs
	mike serve --dev-addr localhost:${PORT} --config-file ${MKDOCSCONFIG}

.PHONY: dev
dev:
	export DEV=true
	mike delete ${DEVALIAS} ${MIKEFLAGS} > /dev/null 2>&1 || true
	VERSION=${DEVALIAS} ${MAKE} mike

.PHONY: latest
latest:
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
	@rm -rf site
	@find . -type d -name "site" -exec rm -rf {} \;
