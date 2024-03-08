PORT?=8000
VERSION?=v0.1.0
ALIAS?=latest
MKDOCSCONFIG?=mkdocs.insiders.yml
PIP?=pip3
MKDOPCSFLAGS?=

build:
	mkdocs build --config-file ${MKDOCSCONFIG}

serve:
	mkdocs serve --dev-addr localhost:${PORT} --config-file ${MKDOCSCONFIG} ${MKDOCSFLAGS}

PRECOMMIT := $(shell command -v pre-commit 2> /dev/null)

install:
	${PIP} install -r requirements.txt

.PHONY : install-pre-commit
install-pre-commit :
	@$(if $(PRECOMMIT),, pip install pre-commit)

.PHONY : pre-commit
pre-commit :
	@pre-commit run --all-files

clean:
	@rm -rf site
	@find . -type d -name "site" -exec rm -rf {} \;
