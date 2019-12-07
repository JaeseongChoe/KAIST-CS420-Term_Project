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
