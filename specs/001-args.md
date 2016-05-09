# Function arguments fetched from stack

## Description

```python

# @... ?
def add(a, b):
    '''
    a ← stack[-1]
    b ← stack[-2]
    '''
    a + b


@fjorton
def f():
    2,
    5,
    add
```

The idea is to map the last stack cells to the function arguments.

## Variants

### 1. The injected call.

On the injected function call [1] check function arguments.

* `args[0] == 'stack'` → pass the stack reference.
* `not args or args[0] != 'stack'` → map the stack cells

…
* **+** : transparent
* **+** : all the logic is incapsulated in one code piece
* **-** : seriosly slows down the code with excessive checks

Example:
```python

@fjorton
def test(stack):
    pass


@fjorton
def add(a, b):
    a + b


@fjorton
def f(c, d):
    c
    d
    add          # → produces add(*stack[-2:])
    test         # → produces test(stack)

f(2, 5)

```

### 2. The @fjorton decorator

Check the function signature in the `@fjorton` decorator.

* **+** : one decorator name for all functions
* **-** : unclear logic: how to handle cases with calls from different contexts

Example:
```python

@fjorton
def test(stack):
    pass


@fjorton         # → maps stack[-2:] to a, b
def add(a, b):
    a + b


@fjorton         # → does not affect args?
def f(c, d):
    c
    d
    add          # → produces add(stack)
    test         # → produces test(stack) — uniform calls

f(2, 5)
```

### 3. Two decorators

Make two different decorators — one for the «normal» calls, and one for the fjorton calls.

* **+** : explicit logic
* **+** : no checks → fast calls
* **-** : two different decorators for the same fjorton functions

`@on_stack` → for functions, implicitly called by fjorton
`@fjorton` → for functions called via normal calls (like `f(a, b)`)

Example:
```python

@fjorton
def test(stack):
    pass


@on_stack         # → explicitly maps stack[-len(args):] to args
def add(a, b):
    a + b


@fjorton         # → does not affect args
def f(c, d):
    c
    d
    add          # → produces add(stack)
    test         # → produces test(stack) — uniform calls

f(2, 5)
```

[1] https://github.com/svinota/fjorton/blob/0.1/fjorton/__init__.py#L37
