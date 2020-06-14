# Installation

```bash
git clone git@gitlab.unipart.digital:mcosta/workflows.git
cd workflows
pip install . --user
```

# Docs

## Building

### Local

To build the documentation

```bash
pip install sphinx recommonmark --user
cd docs
make html
```

### Docker

It is possible to build and serve the html in a docker container

```bash
docker build -t workflow_docs -f ./docs/Dockerfile .
docker run -p 80:8080 workflow_docs
```

Then just visit [`http://localhost:8080/`](http://localhost:8080/).

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
