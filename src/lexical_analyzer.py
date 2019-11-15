# ----------------------------------------------------------------------
# lexical_analyzer.py
#
# A lexical analyzer for ANSI C.
# ----------------------------------------------------------------------

import sys
sys.path.insert(0, "../lib")

import ply.lex as lex


# Keywords
keyowrd = (
    'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO',
    'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF',
    'INT', 'LONG', 'REGISTER', 'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC',
    'STRUCT', 'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE'
)

# Constants
constant = (
    'FCONST',        # floating-constant
    'ICONST',        # integer-constant
    'ECONST',        # enumeration-constant
    'CCONST'         # character-constant
)

# String Literals
string_literals = (
    '"S-CHAR-SEQUENCE"'
    'L"S-CHAR-SEQUENCE"'
)

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
    'B_NOT', 'AMPERSAND', 'B_OR', 'B_XOR', 'B_LSHIFT', 'B_RSHIFT'

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
    'SIZEOF'
)

# Punctuators
punctuators = (
    'LBRACKET', 'RBRACKET',    # [, ]
    'LPAREN', 'RPAREN',        # (, )
    'LBRACE', 'RBRACE',        # {, }
    'SEMI_COLON',              # ;
    'ELLIPSIS'                 # ...
)

# Tokens
tokens = keyword + constant + string_literals + operators + punctuators + (
    'ID', 'TYPEID',
    'SCONST',
)

# Completely ignored characters
t_ignore = ' \t\x0c'

# Newlines


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Assignment operators

t_EQUALS = r'='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_LSHIFTEQUAL = r'<<='
t_RSHIFTEQUAL = r'>>='
t_ANDEQUAL = r'&='
t_OREQUAL = r'\|='
t_XOREQUAL = r'\^='

# Increment/decrement
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

# ->
t_ARROW = r'->'

# ?
t_CONDOP = r'\?'

# Delimeters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'
t_ELLIPSIS = r'\.\.\.'

# Identifiers and reserved words

keyowrd_map = {}
for k in keyword:
    keyword_map[k.lower()] = k


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = keyword_map.get(t.value, "ID")
    return t

# Integer literal
t_ICONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
t_FCONST = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'c' or L'c'
t_CCONST = r'(L)?\'([^\\\n]|(\\.))*?\''

# Comments


def t_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Preprocessor directive (ignored)


def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

lexical_analyzer = lex.lex()
if __name__ == "__main__":
    lex.runmain(lexical_analyzer)
