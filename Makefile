MAKEAUXFLAGS?=-s
MAKE=make ${MAKEAUXFLAGS}

JUVIX?=juvix
JUVIX_FILES_TO_ISABELLE := \
   ./docs/prelude.juvix.md \
   ./docs/arch/node/types/engine_behaviour.juvix.md \


JUVIX_TO_ISABELLE := $(JUVIX) --log-level error isabelle
ISABELLE_OUTPUT_DIR := ./docs/theories

art.bib:
	@curl -s -o docs/references/art.bib https://art.anoma.net/art.bib || echo "[!] Failed to download art.bib"

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

.phony: theories
theories:
	@echo "Converting Juvix files to Isabelle..."
	@for file in $(JUVIX_FILES_TO_ISABELLE); do \
	    echo "Processing $$file..."; \
		outdir=$$(dirname $$file); \
		$(JUVIX_TO_ISABELLE) $$file --output-dir=$$outdir || true; \
	done