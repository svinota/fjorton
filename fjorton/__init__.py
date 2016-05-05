import byteplay


def ___cstack():
    try:
        ___stack___ = argv
    except NameError:
        ___stack___ = []
    return ___stack___

___stack_code = list(filter(lambda x: x[0] != byteplay.SetLineno,
                            (byteplay
                             .Code
                             .from_code(___cstack.func_code)
                             .code)))[:-2]


def fjorton(f):

    def to_stack(ret):
        ret.pop()
        ret.extend([(byteplay.LOAD_GLOBAL, 'locals'),
                    (byteplay.CALL_FUNCTION, 0),
                    (byteplay.LOAD_CONST, '___stack___'),
                    (byteplay.BINARY_SUBSCR, None),
                    (byteplay.LOAD_ATTR, 'append'),
                    (byteplay.ROT_TWO, None),
                    (byteplay.CALL_FUNCTION, 1),
                    (byteplay.POP_TOP, None)])

    global ___stack_code
    c = byteplay.Code.from_code(f.func_code)
    simple = (byteplay.LOAD_FAST,
              byteplay.LOAD_CONST,
              byteplay.LOAD_DEREF,
              byteplay.LOAD_ATTR,
              byteplay.BUILD_LIST)
    ret = []
    more = -1
    more_trigger = None
    ret.extend(___stack_code)
    for code, value in c.code:
        if code == byteplay.LOAD_CONST:
            if isinstance(value, tuple) and len(value) == 1:
                value = value[0]
        ret.append((code, value))

        if code in simple:
            more = 0
            continue
        elif more == 0 and code == byteplay.POP_TOP:
            to_stack(ret)
        elif code == byteplay.POP_TOP and \
                ret[-2][0] == byteplay.LOAD_GLOBAL:
            # is it a variable or a function?
            if hasattr(f.func_globals[ret[-2][1]], '__call__'):
                ret.pop()
                ret.extend([(byteplay.LOAD_GLOBAL, 'locals'),
                            (byteplay.CALL_FUNCTION, 0),
                            (byteplay.LOAD_CONST, '___stack___'),
                            (byteplay.BINARY_SUBSCR, None),
                            (byteplay.CALL_FUNCTION, 1),
                            (byteplay.POP_TOP, None)])
            else:
                to_stack(ret)
        elif code == byteplay.RETURN_VALUE and \
                ret[-2] == (byteplay.LOAD_CONST, None):
            ret.pop()
            ret.pop()
            ret.extend([(byteplay.LOAD_GLOBAL, 'locals'),
                        (byteplay.CALL_FUNCTION, 0),
                        (byteplay.LOAD_CONST, '___stack___'),
                        (byteplay.BINARY_SUBSCR, None),
                        (byteplay.RETURN_VALUE, None)])

        if more >= 0:
            if more_trigger and code == more_trigger:
                more -= 1
            elif more_trigger is None:
                more -= 1

    c.code = ret
    f.func_code = c.to_code()
    #
    return f
