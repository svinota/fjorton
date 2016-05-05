from fjorton import fjorton


def add(stack):
    while len(stack) > 1:
        stack[0] += stack.pop()
    return stack[0]


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
