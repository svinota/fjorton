# Function arguments fetched from stack

## Description

Normally, if one pushes a function name to the stack, the
function is being called with the reference to the stack.
The value returned from the function is not pushed to the
stack, it has to do it explicitly:
```python
@fjorton
def add(stack):
    stack.append(stack.pop() + stack.pop())


@fjorton
def f():
    2,
    3,
    add

print(f())
```

The goal of the spec is to provide a way to map the last stack
cells to the function arguments.

## Solution

The solution was to introduce a separate decorator, that would
perform the mapping:
```python
@map_stack      # → map the stack
def plain_add(a, b):
    '''
    A function with normal Python syntax.
    To be used in `@map_stack`, has to return
    a list, that would be merged into the stack.
    '''
    return [a + b]


@map_stack      # → map the stack
@fjorton        # → enable fjorton syntax
def add(a, b):
    '''
    stack[-1] → a
    stack[-2] → b
    '''
    a + b       # push the sum to the stack


@fjorton
def f():
    2,
    3,
    add         # produces add(stack), [2, 3] → [5]
    4,
    plain_add   # produces plain_add(stack), [5, 4] → [9]

print(f())      # None → [9]
```

The new decorator may be used with normal function to map the
stack to args as well as with fjorton-enabled function. The order
of decorators does matter: `@fjorton` must be the closest to the
function.

## Alternatives

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
