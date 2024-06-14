PORT?=8000
VERSION?=$(shell cat VERSION)
PIP?=pip3

PWD=$(CURDIR)

MAKEAUXFLAGS?=-s
MAKE=make ${MAKEAUXFLAGS}

MKDOCSCONFIG?=mkdocs.yml
MKDOCSFLAGS?=

MIKEPUSHFLAGS?=--push
MIKEFLAGS?=${MIKEPUSHFLAGS} \
	--remote origin  \
	--branch gh-pages  \
	--allow-empty \
	--ignore-remote-status \
	--config-file ${MKDOCSCONFIG}

GITBRANCH?=$(shell git rev-parse --abbrev-ref HEAD)

build:
	mkdocs build --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}


.PHONY: test-build
test-build: export MKDOCSFLAGS=--clean
test-build: export REPORT_BROKEN_LINKS=true
test-build: export REMOVE_CACHE=true
test-build:
	@mkdocs build --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}

art.bib:
	@curl -s -o docs/references/art.bib https://art.anoma.net/art.bib || echo "[!] Failed to download art.bib"

.PHONY: serve
serve:
	mkdocs serve --dev-addr localhost:${PORT} --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}

.PHONY : mike
mike:
	@git fetch --all
	@git checkout gh-pages
	@git pull origin gh-pages --rebase
	@git checkout ${GITBRANCH}
	mike deploy ${VERSION} ${MIKEFLAGS} -t ${VERSION}

.PHONY: mike-serve
mike-serve: docs
	mike serve --dev-addr localhost:${PORT} --config-file ${MKDOCSCONFIG}

.PHONY: delete-alias
delete-alias:
	mike delete ${VERSION} ${MIKEFLAGS} > /dev/null 2>&1 || true

.PHONY: deploy
deploy:
	${MAKE} delete-alias
	${MAKE} mike
	DEFAULTVERSION=$(shell cat VERSION); \
	if [ "${VERSION}" = "${DEFAULTVERSION}" ]; then \
		mike set-default ${MIKEFLAGS} ${DEFAULTVERSION}; \
		mike alias ${VERSION} latest -u ${MIKEFLAGS}; \
	fi; \
	git tag -d ${VERSION} > /dev/null 2>&1 || true; \
	git tag -a ${VERSION} -m "Release ${VERSION}"

install:
	@echo "[!] Use a Python virtual environment if you are not using one."
	${PIP} install -r requirements.txt

.PHONY : pre-commit
pre-commit :
	@pre-commit run --all-files

clean:
	@if [ -d "env" ]; then rm -rf env; fi
	@if [ -d ".hooks" ]; then rm -rf .hooks; fi
	@rm -rf site \
			.juvix-mkdocs \
			.juvix-build \
			.cache \
			.mypy_cache \
			__pycache__
	@find . -type d -name "site" -exec rm -rf {} \;
