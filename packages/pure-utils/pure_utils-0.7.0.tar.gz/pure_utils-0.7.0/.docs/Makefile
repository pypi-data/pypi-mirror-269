.PHONY: help docs Makefile

SPHINXOPTS  ?= -c .
SPHINXBUILD ?= sphinx-build
SOURCEDIR    = source
BUILDDIR     = build
REFERENCEDIR = $(SOURCEDIR)/refs
DOCSDIR      = ../docs

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

docs:
	rm -rf build
	make html
	find $(REFERENCEDIR) -type f -name *.rst ! -name index.rst -exec rm -f {} \;
	mkdir -p $(DOCSDIR) && rm -rf $(DOCSDIR)/*
	cp -r build/html/{_static,refs,*.html} $(DOCSDIR)

push:
	git add $(DOCSDIR)/
	git commit -m "Update pages"
	git push origin gh-pages
