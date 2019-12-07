# ----------------------------------------------------------------------
# ast.py
#
# A module for abstract syntax tree for ANSI C (C89 / C90).
# ----------------------------------------------------------------------

import enum


class Type(enum.Enum):
    VOID = 0
    INT = 1
    FLOAT = 2
    CHAR = 3


class Operator(enum.Enum):
    SIZEOF = 0


class ArithOp(enum.Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    UNA_PLUS = 5
    UNA_MINUS = 6
    PRE_INC = 7
    PRE_DEC = 8
    POS_INC = 9
    POS_DEC = 10


class ComRelOp(enum.Enum):
    EQ = 0
    NE = 1
    GT = 2
    LT = 3
    GE = 4
    LE = 5


class LogicalOp(enum.Enum):
    L_NOT = 0
    L_AND = 1
    L_OR = 2


class BitwiseOp(enum.Enum):
    B_NOT = 0
    B_AND = 1
    B_OR = 2
    B_XOR = 3
    B_LSHIFT = 4
    B_RSHIFT = 5


class AssignOp(enum.Enum):
    ASSIGN = 0
    ADD_ASSIGN = 1
    SUB_ASSIGN = 2
    MUL_ASSIGN = 3
    DIV_ASSIGN = 4
    MOD_ASSIGN = 5
    B_AND_ASSIGN = 6
    B_OR_ASSIGN = 7
    B_XOR_ASSIGN = 8
    B_LSHIFT_ASSIGN = 9
    B_RSHIFT_ASSIGN = 10


class MemPoinOp(enum.Enum):
    INDIR = 0
    ADDRS = 1
    DEREF = 2
    REFEN = 3


class Node(object):
    pass


class Const(Node):
    def __init__(self, type, value, lineno):
        self.type = type
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return '<%s, %s>' % (self.type, self.value)


class ID(Node):
    def __init__(self, id, lineno):
        self.id = id
        self.lineno = lineno

    def __repr__(self):
        return '<ID, %s>' % self.id


class Subscript(Node):
    def __init__(self, id, index, lineno):
        self.id = id
        self.index = index
        self.lineno = lineno

    def __repr__(self):
        return '<%s[%s]>' % (self.id, self.index)


class FunCall(Node):
    def __init__(self, id, args, lineno):
        self.id = id
        self.args = args
        self.lineno = lineno

    def __repr__(self):
        return '<%s(%s)>' % (self.id, self.args)


class Args(Node):
    def __init__(self, args, arg, lineno):
        self.args = args
        self.arg = arg
        self.lineno = lineno

    def __repr__(self):
        if self.args == None:
            return '%s' % self.arg
        else:
            return '%s, %s' % (self.args, self.arg)


class UnaOp(Node):
    def __init__(self, operator, operand, lineno):
        self.operator = operator
        self.operand = operand
        self.lineno = lineno

    def __repr__(self):
        return '<%s(%s)>' % (self.operator, self.operand)


class BinOp(Node):
    def __init__(self, left, op, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return '<%s(%s, %s)>' % (self.op, self.left, self.right)


class TerOp(Node):
    def __init__(self, condition, then_body, else_body, lineno):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
        self.linno = lineno

    def __repr__(self):
        return '<%s ? %s : %s>' % (self.condition, self.then_body, self.else_body)


class Assign(Node):
    def __init__(self, dst, op, src, lineno):
        self.op = op
        self.dst = dst
        self.src = src
        self.lineno = lineno

    def __repr__(self):
        return '<%s(%s, %s)>' % (self.op, self.dst, self.src)


class Cast(Node):
    def __init__(self, type, expr, lineno):
        self.type = type
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return '<CAST(%s, %s)>' % (self.type, self.expr)


class Expr(Node):
    def __init__(self, expr, assign_expr, lineno):
        self.expr = expr
        self.assign_expr = assign_expr
        self.lineno = lineno

    def __repr__(self):
        if self.expr == None:
            return '%s' % self.assign_expr
        else:
            return '%s, %s' % (self.expr, self.assign_expr)
