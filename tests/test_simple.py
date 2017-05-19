import fjorton

a = 2
b = 4


@fjorton.func
def add(a, b):
    a + b


class TestSupportedTypes(object):

    def test_list(self):

        @fjorton.func
        def f():
            [2, 3, 4]
            [5, 6, 7]
            add

        assert f() == [[2, 3, 4, 5, 6, 7]]

    def test_numbers(self):

        @fjorton.func
        def f():
            2,
            6,
            add

        assert f() == [8]

    def test_deref(self):
        a = 2
        b = 3

        def c(stack):
            stack[-1] += 7

        @fjorton.func
        def f():
            a
            b
            c
            add

        assert f() == [12]

    def test_globals(self):

        @fjorton.func
        def f():
            a
            b
            add

        assert f() == [6]

    def test_const_str(self):

        @fjorton.func
        def f():
            "bala",
            "dala",
            add

        assert f() == ["baladala"]

    def test_dict(self):

        RTM_NEWLINK = 16
        RTM_DELLINK = 17

        @fjorton.func
        def get_interfaces(stack):
            ops = stack.pop()
            events = stack.pop()
            ret = set()
            for event in events:
                nlas = event[1].get('attrs', [])
                ifname = None
                for nla in nlas:
                    if nla[0] == 'IFLA_IFNAME':
                        ifname = nla[1]
                        break
                if ifname is not None:
                    ops[event[0]](ret, ifname)
            stack.append(ret)

        @fjorton.func
        def f():
            [[RTM_NEWLINK, {'attrs': [['IFLA_IFNAME', 'eth0'],
                                      ['IFLA_ADDRESS', 'c2:b3:74:94:c2:8d']]}],
             [RTM_NEWLINK, {'attrs': [['IFLA_IFNAME', 'eth1'],
                                      ['IFLA_ADDRESS', 'c2:b3:74:94:c2:8e']]}],
             [RTM_NEWLINK, {'attrs': [['IFLA_IFNAME', 'eth2'],
                                      ['IFLA_ADDRESS', 'c2:b3:74:94:c2:8f']]}],
             [RTM_DELLINK, {'attrs': [['IFLA_IFNAME', 'eth1'],
                                      ['IFLA_ADDRESS', 'c2:b3:74:94:c2:8e']]}]]
            {RTM_NEWLINK: lambda x, y: x.add(y),
             RTM_DELLINK: lambda x, y: x.remove(y)}
            get_interfaces

        assert f() == [set(('eth0', 'eth2'))]

    def test_object_attrs(self):

        class TA(object):
            attr = 56

        class TB(object):
            attr = 67

        @fjorton.func
        def f():
            TA().attr
            TB().attr
            add

        assert f() == [123]
