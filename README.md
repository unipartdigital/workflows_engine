# Installation

```bash
git clone git@gitlab.unipart.digital:mcosta/workflows.git
cd workflows
pip install -r pip-requirements.txt --user
pip install . --user
```

## Pipenv

```
pipenv --three && pipenv run pip install -r pip-requirements.txt && pipenv shell
```

# Docs

## Building

### Local

To build the documentation

```bash
pip install .[doc] --user
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
