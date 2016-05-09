import byteplay
import inspect


def ___cstack():
    try:
        ___stack___ = stack
    except NameError:
        ___stack___ = []
    return ___stack___

___stack_code = list(filter(lambda x: x[0] != byteplay.SetLineno,
                            (byteplay
                             .Code
                             .from_code(___cstack.func_code)
                             .code)))[:-2]


def show_stack(stack):
    print(stack)


def apply(stack):
    stack.append(stack.pop()(stack.pop()))


def map_stack(f):
    args = inspect.getargspec(f).args
    def wrapped(s):
        l = len(args)
        if len(s) < l:
            raise TypeError("%s() takes %i arguments (%i in the stack)" %
                            (f.func_name, l, len(s)))
        new_args = []
        while l:
            new_args.append(s.pop())
            l -= 1
        s.extend(f(*new_args))
    return wrapped


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

    def to_call(ret):
            ret.pop()
            ret.extend([(byteplay.LOAD_GLOBAL, 'locals'),
                        (byteplay.CALL_FUNCTION, 0),
                        (byteplay.LOAD_CONST, '___stack___'),
                        (byteplay.BINARY_SUBSCR, None),
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
            if hasattr(f.func_globals[ret[-2][1]], '__call__'):
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
