# fjorton

The `fjorton` library is a proof-of-concept to bring some
Forth features to the Python world.

The idea is quite simple. Python silently drops every
reference, left on the stack without use. E.g. this code:
```python

def f():
    (2, 3, 4)
    do_something

```

normally will be translated by Python2 into that bytecode:
```
    ...
    (LOAD_CONST, (2, 3, 4)),  # put the symbol on the stack
    (POP_TOP, None),          # dismiss it
    (LOAD_GLOBAL, "do_something"),  # again...
    (POP_TOP, None),                # ... and dismiss
    ...
```

Basicall, the `fjorton` library changes the bytecode, so the
referenced symbols aren't dropped, but either saved to the
implicit stack, or called as a function.

More precise, tha `@fjorton` decorator does following steps:

1. Tries to load `stack` variable from arguments; if there is
   no `stack` argument, creates an empty `___stack___`.
2. Pushes every object, that is being dropped by `POP_TOP` and
   has no `__call__` attribute, to the `___stack___`.
3. Every object, that is being dropped by `POP_TOP` and has
   `__call__` attribute, instead is being called with
   `___stack___` as the only positional argument.
4. Every `return` or `return None` is being replaced with
   `return locals()['___stack___']`.

E.g.:
```python

from fjorton import fjorton


def add(stack):
    # pushes to the stack the sum of two
    # last stack cells
    stack.append(stack.pop() + stack.pop())


@fjorton
def f():
    #     # here the stack is being created
    56,   # 56 is pushed to the stack
    67,   # 67 is pushed to the stack
    add   # `add()` is being called as `add(locals()['___stack___'])`
    #     # here the function returns the stack

f() == [123]
```

Short Q'n'A:

* *Why `56,` not `56`?* -- 'Cause Python optimizes out all simple literals
  to be dropped by `POP_TOP`, so they simply disappear from the bytecode.
  The `56,` statement creates a tuple, and it will remain in the bytecode,
  so we have a chance to work with it. The library translates one-cell tuples
  into simple references.
* *Why `[123]`, not `123`?* -- 'Cause it's a stack, it's a list. In that case
  it contains only one cell. But that's not the rule.
* *May the function body contain normal Python code?* -- Sure. The library
  just extends the code a bit in a compatible (I hope so) way.
* *Why should I use the library?* -- You should **not**. It's made just for
  fun, it is against all the Python rules, so please avoid to use it in the
  production.
* *Will Python3 be supported?* -- Maybe.
