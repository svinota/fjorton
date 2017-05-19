import byteplay
import inspect


def ___cstack():
    if 'stack' in locals():
        ___stack___ = list(locals()['stack'])
    else:
        ___stack___ = []
    return ___stack___


___stack_code = list(filter(lambda x: x[0] != byteplay.SetLineno,
                            (byteplay
                             .Code
                             .from_code(___cstack.func_code)
                             .code)))[:-2]


def print_stack(*stack):
    print(list(stack))
    return []


def apply(stack):
    stack.append(stack.pop()(stack.pop()))


def __call_func(f, stack):
    argspec = inspect.getargspec(f)
    l = len(argspec.args)
    if l > 0:
        if argspec.args[0] == 'stack':
            f(stack)
            return []
        else:
            argv = stack[-l:]
            for _ in range(l):
                stack.pop()
            ret = f(*argv)
            if not isinstance(ret, list):
                return [ret]
            else:
                return ret
    elif argspec.varargs == 'stack':
        return f(*stack)
    else:
        return [f()]


def func(f):

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

    def to_call(ret):
            ret.pop()
            # ret.extend([(byteplay.LOAD_GLOBAL, 'print'),
            #             (byteplay.LOAD_GLOBAL, 'globals'),
            #             (byteplay.CALL_FUNCTION, 0),
            #             (byteplay.CALL_FUNCTION, 1),
            #             (byteplay.POP_TOP, None)])

            ret.extend([(byteplay.LOAD_GLOBAL, 'fjorton'),
                        (byteplay.LOAD_ATTR, '__call_func'),
                        (byteplay.ROT_TWO, None),
                        (byteplay.LOAD_GLOBAL, 'locals'),
                        (byteplay.CALL_FUNCTION, 0),
                        (byteplay.LOAD_CONST, '___stack___'),
                        (byteplay.BINARY_SUBSCR, None),
                        (byteplay.CALL_FUNCTION, 2),
                        (byteplay.LOAD_GLOBAL, 'locals'),
                        (byteplay.CALL_FUNCTION, 0),
                        (byteplay.LOAD_CONST, '___stack___'),
                        (byteplay.BINARY_SUBSCR, None),
                        (byteplay.LOAD_ATTR, 'extend'),
                        (byteplay.ROT_TWO, None),
                        (byteplay.CALL_FUNCTION, 1),
                        (byteplay.POP_TOP, None)])

    global ___stack_code

    c = byteplay.Code.from_code(f.func_code)
    simple = (byteplay.LOAD_FAST,
              byteplay.LOAD_CONST,
              byteplay.LOAD_ATTR,
              byteplay.STORE_MAP,
              byteplay.CALL_FUNCTION,
              byteplay.BINARY_ADD,
              byteplay.BINARY_AND,
              byteplay.BINARY_DIVIDE,
              byteplay.BINARY_FLOOR_DIVIDE,
              byteplay.BINARY_LSHIFT,
              byteplay.BINARY_MODULO,
              byteplay.BINARY_MULTIPLY,
              byteplay.BINARY_OR,
              byteplay.BINARY_POWER,
              byteplay.BINARY_RSHIFT,
              byteplay.BINARY_SUBSCR,
              byteplay.BINARY_SUBTRACT,
              byteplay.BINARY_TRUE_DIVIDE,
              byteplay.BINARY_XOR,
              byteplay.UNARY_CONVERT,
              byteplay.UNARY_INVERT,
              byteplay.UNARY_NEGATIVE,
              byteplay.UNARY_NOT,
              byteplay.UNARY_POSITIVE,
              byteplay.BUILD_LIST)
    ret = []
    ret.extend(___stack_code)
    for code, value in c.code:
        if code == byteplay.LOAD_CONST:
            if isinstance(value, tuple) and len(value) == 1:
                value = value[0]
        ret.append((code, value))

        if code == byteplay.POP_TOP and \
                ret[-2][0] in simple:
            to_stack(ret)
        elif code == byteplay.POP_TOP and \
                ret[-2][0] == byteplay.LOAD_GLOBAL:
            # is it a variable or a function?
            if ret[-2][1] in f.func_globals and \
                    hasattr(f.func_globals[ret[-2][1]], '__call__'):
                to_call(ret)
            else:
                to_stack(ret)
        elif code == byteplay.POP_TOP and \
                ret[-2][0] == byteplay.LOAD_DEREF:
            for cell in f.func_closure:
                if hasattr(cell.cell_contents, '__call__') and \
                        cell.cell_contents.func_name == ret[-2][1]:
                    to_call(ret)
                    break
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

    c.code = ret
    f.func_code = c.to_code()
    #
    return f
