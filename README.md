[![Build Status](https://travis-ci.org/Jackevansevo/Interpreter.svg?branch=master)](https://travis-ci.org/Jackevansevo/Interpreter)
[![Coverage Status](https://coveralls.io/repos/github/Jackevansevo/Interpreter/badge.svg?branch=master)](https://coveralls.io/github/Jackevansevo/Interpreter?branch=master)

# --C Interpreter

Interpreter for a simplified C like language

## Installation

It's recommended to use a virtual environment to encapsulate dependencies.

    python -m venv env

    source env/bin/activate

    pip install -e .

## Example Usage

Inside the projects virtual environment run:

    mmci examples/operators.cmm

## Features

See more programs in `\examples`

--C has a c like syntax:

```c
/* Answer: 4 */

int main() {
  return ((1 + 2) * 4) / 3;
}

```

**Conditionals**

```c
/* Answer: 2 */

int main() {
  int x = 30;
  if (x < 25) {
    return 1;
  } else if(x < 50) {
    return 2;
  } else {
    return 3;
  }
}
```

**Functions**

```c
/* Answer: 16 */

int square(int x) {
  return x * x;
}

int main() {
  return square(5- 1);
}
```

**Recursion**


```c
/* Answer: 21 */

int fib(int n) {
  if (n < 2) return n;
  return (fib(n - 1) + fib(n - 2));
}

int main() {
  int x = 8;
  return fib(x);
}
```

**Closures**

```c
/* Answer: 16 */

int square(int a) {
  return a * a;
}

function twice(function f) {
  int g(int x) { return f(f(x)); }
  return g;
}

int main() {
  int cube = twice(square);
  return cube(2);
}
```




## Running Tests

Inside the projects virtual environment run:

### Quick Way

    python setup.py test

### Recommended Way

    pip install -e ."[test]"

    pytest
