# Installation

```bash
git clone git@gitlab.unipart.digital:mcosta/workflows.git
cd workflows
pip install . --user
```

# Docs

## Building

To build the documentation

```bash
pip install sphinx recommonmark --user
cd docs
make html
```

## Extentions

We probably should look at these

- https://www.sphinx-doc.org/en/master/usage/extensions/index.html

  - Nice plots and graphs
    https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html

  - Autocreate stuff from source code
    https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html

  - Support for NumPy and Google style docstrings:
    https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

- https://github.com/yoloseem/awesome-sphinxdoc

  - Auto creating for JS
    https://github.com/lunant/sphinxcontrib-autojs

  - display JSONSchema
    https://github.com/lnoor/sphinx-jsonschema

  - Turn git log into change log
    https://github.com/OddBloke/sphinx-git
