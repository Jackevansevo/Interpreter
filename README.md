# Interpreter

## Installation

It's recommended to use a virtual environment to encapsulate dependencies.

    python -m venv env

    source env/bin/activate

    pip install -e .

## Example Usage

Inside the projects virtual environment run:

    mmci examples/operators.cmm

## Running Tests

Inside the projects virtual environment run:

### Quick Way

    python setup.py test

### Recommended Way

    pip install -e ."[test]"

    pytest
