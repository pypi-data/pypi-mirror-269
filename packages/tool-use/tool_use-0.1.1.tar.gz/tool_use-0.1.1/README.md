# Promptflow-Tool-Use

- promptflow custom llm tool package for function calling mode and newer version of openai/azure deployment

## Pypi Installation

```bash
pip install tool-use
```

link : https://pypi.org/project/tool-use/0.1.0/

## Contribution Guideline

### setup environment

```bash
pyenv install 3.11
pyenv virtualenv 3.11 tool-use
pyenv activate tool-use
pip install poetry
poetry install --with dev

# test
pytest tests
```

### push to PYPI

```bash
make pre-commit
pip install wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
```
