# ----------------------------------------------------------------------
# lexical_analyzer.py
#
# A lexical analyzer for ANSI C (C89 / C90).
# ----------------------------------------------------------------------

import sys
sys.path.insert(0, "../lib")

import ply.lex as lex
from ply.lex import TOKEN


# Keywords
keyword = (
    'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO',
    'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF',
    'INT', 'LONG', 'REGISTER', 'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC',
    'STRUCT', 'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE',
)

# Constants
constant = (
    'FCONST',        # floating-constant
    'ICONST',        # integer-constant
    'ECONST',        # enumeration-constant
    'CCONST',        # character-constant
)

# String Literals
string_literals = ('STR_LITER',)

# Operators
operator = (
    # Arithmetic operators (+, -, *, /, %, ++, --)
    'PLUS', 'MINUS', 'ASTERISK', 'DIV', 'MOD',
    'INCREMENT', 'DECREMENT',

    # Comparison operators (==, !=, <, >, <=, >=, !, &&, ||)
    'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',

    # Logical operators
    'L_NOT', 'L_AND', 'L_OR',

    # Bitwise operators (~, &, |, ^, <<, >>)
    'B_NOT', 'AMPERSAND', 'B_OR', 'B_XOR', 'B_LSHIFT', 'B_RSHIFT',

    # Assignment operators (=, +=, -=, *=, /=, %=, &=, ^=, |=, <<=, >>=)
    'ASSIGN',
    'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN',
    'B_AND_ASSIGN', 'B_XOR_ASSIGN', 'B_OR_ASSIGN',
    'B_LSHIFT_ASSIGN', 'B_RSHIFT_ASSIGN',

    # Member and pointer operators (., ->)
    'PERIOD', 'ARROW',

    # Other operators (?, :, ,, sizeof)
    'TERNARY', 'COLON',
    'COMMA',
)

# Punctuators
punctuator = (
    'LBRACKET', 'RBRACKET',        # [, ]
    'LPAREN', 'RPAREN',            # (, )
    'LBRACE', 'RBRACE',            # {, }
    'SEMI_COLON',                  # ;
    'ELLIPSIS',                    # ...
)

# Tokens
tokens = keyword + constant + string_literals + operator + punctuator + (
    'ID', 'TYPEID',
    'SCONST',
)

# Keywords
keyword_map = {}
for k in keyword:
    keyword_map[k.lower()] = k


# Constants
def t_CCONST(t):
    r"""
        L?
        \'
        (
            [^\'\\\n]
            | \\[\'\"\?\\abfnrtv]
            | \\[0-7]{1,3}
            | \\x[0-9a-fA-f]+
        )+
        \'
     """
    return t


def t_FCONST(t):
    r'(\d*\.\d+) ((e|E)(\+|-)?\d+)? (f|l|F|L)?'
    return t


def t_ICONST(t):
    r"""
        ([1-9]\d* ([uU][lL]? | [lL][uU]?)?)
        | (0[0-7]* ([uU][lL]? | [lL][uU]?)?)
        | (0(x|X) [0-9a-fA-F]+ ([uU][lL]? | [lL][uU]?))
     """
    return t


# String Literals
def t_STR_LITER(t):
    r"""
        L?
        \"
        (
            (
                [^\"\\\n]
                | \\[\'\"\?\\abfnrtv]
                | \\[0-7]{1,3}
                | \\x[0-9a-fA-f]+
            )+
        )*
        \"
     """
    return t


# Arithmetic operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_ASTERISK = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

# Comparion operators
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='

# Logical operators
t_L_NOT = r'!'
t_L_AND = r'&&'
t_L_OR = r'\|\|'

# Bitwise operators
t_B_NOT = r'~'
t_AMPERSAND = r'&'
t_B_OR = r'\|'
t_B_XOR = r'\^'
t_B_LSHIFT = r'<<'
t_B_RSHIFT = r'>>'

# Assignment operators
t_ASSIGN = r'='
t_ADD_ASSIGN = r'\+='
t_SUB_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_B_AND_ASSIGN = r'&='
t_B_OR_ASSIGN = r'\|='
t_B_XOR_ASSIGN = r'\^='
t_B_LSHIFT_ASSIGN = r'<<='
t_B_RSHIFT_ASSIGN = r'>>='

# Member and pointer operators
t_PERIOD = r'\.'
t_ARROW = r'->'

# Other operators
t_TERNARY = r'\?'
t_COLON = r':'
t_COMMA = r','

# Punctuators
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI_COLON = r';'
t_ELLIPSIS = r'\.\.\.'

# Completely ignored characters
t_ignore = ' \t\x0c'


# Identifier
def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = keyword_map.get(t.value, "ID")
    return t


# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Comments
def t_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


# Preprocessor directive (ignored)
def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1


# Error handling
def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)


lexical_analyzer = lex.lex()
if __name__ == "__main__":
    lex.runmain(lexical_analyzer)
