from fjorton import fjorton

a = 2
b = 4


def add(stack):
    while len(stack) > 1:
        stack[0] += stack.pop()


class TestSupportedTypes(object):

    def test_list(self):

        @fjorton
        def f():
            [2, 3, 4]
            [5, 6, 7]
            add

        assert f() == [[2, 3, 4, 5, 6, 7]]

    def test_numbers(self):

        @fjorton
        def f():
            2,
            6,
            add

        assert f() == [8]

    def test_deref(self):
        a = 2
        b = 3

        @fjorton
        def f():
            a
            b
            add

        assert f() == [5]

    def test_globals(self):

        @fjorton
        def f():
            a
            b
            add

        assert f() == [6]

    def test_object_attrs(self):

        class TA(object):
            attr = 56

        class TB(object):
            attr = 67

        @fjorton
        def f():
            TA().attr
            TB().attr
            add

        assert f() == [123]
