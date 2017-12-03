[![Build Status](https://travis-ci.org/Jackevansevo/Interpreter.svg?branch=master)](https://travis-ci.org/Jackevansevo/Interpreter)
[![Coverage Status](https://coveralls.io/repos/github/Jackevansevo/Interpreter/badge.svg?branch=master)](https://coveralls.io/github/Jackevansevo/Interpreter?branch=master)

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
