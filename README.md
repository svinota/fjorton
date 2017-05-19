fjorton
=======

The `fjorton` library is a proof-of-concept to bring some
Forth features to the Python world.

The idea is quite simple. Python silently drops every
reference, left on the stack without use. E.g. this code::

    def f():
        (2, 3, 4)
        do_something


normally will be translated by Python2 into that bytecode::
    ...
    (LOAD_CONST, (2, 3, 4)),        # put the symbol on the stack
    (POP_TOP, None),                # dismiss it
    (LOAD_GLOBAL, "do_something"),  # again...
    (POP_TOP, None),                # ... and dismiss
    ...

The `fjorton` library changes the bytecode, so the referenced
symbols aren't dropped, but either saved to the implicit stack,
or called as a function.

If the object is callable Python object -- a function, an object
with `.__call__()` method -- `fjorton` will call it, otherwise the
reference will be pushed onto the stack.

There known limitations:

* The library doesn't recognise object methods/attributes as callable
  (yet; that will be fixed later)
* The library doesn't handle built-in or C methods, since it's
  impossible to get their signature and properly map the stack to
  the arguments.

The code sample::

    import fjorton

    @fjorton.func
    def add(a, b):
        a + b


    @fjorton.func
    def test():
        56,
        67,
        add

    assert test() == [123]


Short Q'n'A:

* *Why `56,` not `56`?* -- 'Cause Python optimizes out all simple literals
  to be dropped by `POP_TOP`, so they simply disappear from the bytecode.
  The `56,` statement creates a tuple, and it will remain in the bytecode,
  so we have a chance to work with it. The library translates one-cell tuples
  into simple references.
* *Why `[123]`, not `123`?* -- 'Cause it's a stack, it's a list.
* *May the function body contain normal Python code?* -- Sure. The library
  just extends the code a bit in a compatible (I hope so) way.
* *Why should I use the library?* -- You should **not**. It's made just for
  fun, it is against all the Python rules, so please avoid to use it in the
  production.
* *Will Python3 be supported?* -- Maybe.
