# -----------------------------------------------------------------------------
# syntax_analyzer.py
#
# A syntax analyzer for ANSI C (C89 / C90). Based on ANSI/ISO 9899-1990
# -----------------------------------------------------------------------------

import sys
import lexical_analyzer
import ply.yacc as yacc
import node


class SyntaxAnalyzerError(Exception):
    pass


class UnsupFeatureError(SyntaxAnalyzerError):
    pass


# Get the token map
tokens = lexical_analyzer.tokens

# Starting grammar rule
start = 'statement'


# constant
def p_constant(p):
    '''
        constant : ICONST
                 | FCONST
                 | CCONST
    '''
    p[0] = ast.Const(p.slice[1].type, p[1], p.lineno(1))


# primary-expression
def p_primary_expression(p):
    '''
        primary_expression : ID
                           | constant
                           | STR_LITER
                           | LPAREN expression RPAREN
    '''
    if len(p) == 2:
        if p.slice[1].type == 'ID':
            p[0] = ast.ID(p[1], p.lineno(1))
        elif isinstance(p[1], ast.Const):
            p[0] = p[1]
        else:
            p[0] = ast.Const(p.slice[1].type, p[1], p.lineno(1))
    elif len(p) == 4:
        p[0] = p[2]
    else:
        raise SyntaxAnalyzerError


# postfix-expression
def p_postfix_expression(p):
    '''
        postfix_expression : primary_expression
                           | postfix_expression LBRACKET expression RBRACKET
                           | postfix_expression LPAREN argument_expression_list RPAREN
                           | postfix_expression PERIOD ID
                           | postfix_expression ARROW ID
                           | postfix_expression INCREMENT
                           | postfix_expression DECREMENT
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        if p[2] == '[' and p[4] == ']':
            p[0] = ast.Subscript(p[1], p[3], p.lineno(2))
        elif p[2] == '(' and p[4] == ')':
            ast.FunCall(p[1], p[3], p.lineno(2))
        else:
            raise SyntaxAnalyzerError
    elif len(p) == 4:
        raise UnsupFeatureError
    elif len(p) == 3:
        if p[2] == '++':
            p[0] = ast.UnaOp(ast.ArithOp.POS_INC, p[1], p.lineno(2))
        elif p[2] == '--':
            p[0] = ast.UnaOp(ast.ArithOp.POS_DEC, p[1], p.lineno(2))
        else:
            raise SyntaxAnalyzerError
    else:
        raise SyntaxAnalyzerError


# argument-expression-list:
def p_argument_expression_list(p):
    '''
        argument_expression_list : assignment_expression
                                 | argument_expression_list COMMA assignment_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.Args(p[1], p[3], p.lineno(3))
    else:
        raise SyntaxAnalyzerError


# unary-expression
def p_unary_expression(p):
    '''
        unary_expression : postfix_expression
                         | INCREMENT unary_expression
                         | DECREMENT unary_expression
                         | unary_operator cast_expression
                         | SIZEOF unary_expression
                         | SIZEOF LPAREN type_name RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == '++':
            p[0] = ast.UnaOp(ast.ArithOp.PRE_INC, p[2], p.lineno(2))
        elif p[1] == '--':
            p[0] = ast.UnaOp(ast.ArithOp.PRE_DEC, p[2], p.lineno(2))
        elif p[1] == 'sizeof':
            p[0] = ast.UnaOp(ast.Operator.SIZEOF, p[2], p.lineno(1))
        else:
            p[0] = ast.UnaOp(p[1], p[2], p.lineno(1))
    elif len(p) == 5:
        # ??? UnsupFeatureError?
        p[0] = ast.UnaOp(ast.Operator.SIZEOF, p[3], p.lineno(1))
    else:
        raise SyntaxAnalyzerError


# unary-operator
def p_unary_operator(p):
    '''
        unary_operator : AMPERSAND
                       | ASTERISK
                       | PLUS
                       | MINUS
                       | B_NOT
                       | L_NOT
    '''
    if p[1] == '&':
        p[0] = ast.MemPoinOp.ADDRS
    elif p[1] == '*':
        p[0] = ast.MemPoinOp.INDIR
    elif p[1] == '+':
        p[0] = ast.ArithOp.UNA_PLUS
    elif p[1] == '-':
        p[0] = ast.ArithOp.UNA_MINUS
    elif p[1] == '~':
        p[0] = ast.BitwiseOp.B_NOT
    else:
        p[0] = ast.LogicalOp.L_NOT


# cast-expression
def p_cast_expression(p):
    '''
        cast_expression : unary_expression
                        | LPAREN type_name RPAREN cast_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = ast.Cast(p[2], p[4], p.lineno(1))
    else:
        raise SyntaxAnalyzerError


# multiplicative-expression
def p_multiplicative_expression(p):
    '''
        multiplicative_expression : cast_expression
                                  | multiplicative_expression ASTERISK cast_expression
                                  | multiplicative_expression DIV cast_expression
                                  | multiplicative_expression MOD cast_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] == '*':
            p[0] = ast.BinOp(p[1], ast.ArithOp.MUL , p[3], p.lineno(2))
        elif p[2] == '/':
            p[0] = ast.BinOp(p[1], ast.ArithOp.DIV , p[3], p.lineno(2))
        elif p[2] == '%':
            p[0] = ast.BinOp(p[1], ast.ArithOp.MOD , p[3], p.lineno(2))
        else:
            raise SyntaxAnalyzerError
    else:
        raise SyntaxAnalyzerError


# additive-expression
def p_additive_expression(p):
    '''
        additive_expression : multiplicative_expression
                            | additive_expression PLUS multiplicative_expression
                            | additive_expression MINUS multiplicative_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] == '+':
            p[0] = ast.BinOp(p[1], ast.ArithOp.ADD, p[3], p.lineno(2))
        elif p[2] == '-':
            p[0] = ast.BinOp(p[1], ast.ArithOp.SUB, p[3], p.lineno(2))
        else:
            raise SyntaxAnalyzerError
    else:
        raise SyntaxAnalyzerError


# shift-expression
def p_shift_expression(p):
    '''
        shift_expression : additive_expression
                         | shift_expression B_LSHIFT additive_expression
                         | shift_expression B_RSHIFT additive_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] == '<<':
            p[0] = ast.BinOp(p[1], ast.BitwiseOp.B_LSHIFT, p[3], p.lineno(2))
        elif p[2] == '>>':
            p[0] = ast.BinOp(p[1], ast.BitwiseOp.B_RSHIFT, p[3], p.lineno(2))
        else:
            raise SyntaxAnalyzerError
    else:
        raise SyntaxAnalyzerError


# relational-expression
def p_relational_expression(p):
    '''
        relational_expression : shift_expression
                              | relational_expression LT shift_expression
                              | relational_expression GT shift_expression
                              | relational_expression LE shift_expression
                              | relational_expression GE shift_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] == '<':
            p[0] = ast.BinOp(p[1], ast.ComRelOp.LT, p[3], p.lineno(2))
        elif p[2] == '>':
            p[0] = ast.BinOp(p[1], ast.ComRelOp.GT, p[3], p.lineno(2))
        elif p[2] == '<=':
            p[0] = ast.BinOp(p[1], ast.ComRelOp.LE, p[3], p.lineno(2))
        elif p[2] == '>=':
            p[0] = ast.BinOp(p[1], ast.ComRelOp.GE, p[3], p.lineno(2))
        else:
            raise SyntaxAnalyzerError
    else:
        raise SyntaxAnalyzerError


# equality-expression
def p_equality_expression(p):
    '''
        equality_expression : relational_expression
                            | equality_expression EQ relational_expression
                            | equality_expression NE relational_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[2] == '==':
            p[0] = ast.BinOp(p[1], ast.ComRelOp.EQ, p[3], p.lineno(2))
        elif p[2] == '!=':
            p[0] = ast.BinOp(p[1], ast.ComRelOp.NE, p[3], p.lineno(2))
        else:
            raise SyntaxAnalyzerError
    else:
        raise SyntaxAnalyzerError


# AND-expression
def p_AND_expression(p):
    '''
        AND_expression : equality_expression
                       | AND_expression AMPERSAND equality_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.BinOp(p[1], ast.BitwiseOp.B_AND, p[3], p.lineno(2))
    else:
        raise SyntaxAnalyzerError


# exclusive-OR-expression
def p_exclusive_OR_expression(p):
    '''
        exclusive_OR_expression : AND_expression
                                | exclusive_OR_expression B_XOR AND_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.BinOp(p[1], ast.BitwiseOp.B_XOR, p[3], p.lineno(2))
    else:
        raise SyntaxAnalyzerError


# inclusive-OR-expression
def p_inclusive_OR_expression(p):
    '''
        inclusive_OR_expression : exclusive_OR_expression
                                | inclusive_OR_expression B_OR exclusive_OR_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.BinOp(p[1], ast.BitwiseOp.B_OR, p[3], p.lineno(2))
    else:
        raise SyntaxAnalyzerError


# logical-and-expression
def p_logical_AND_expression(p):
    '''
        logical_AND_expression : inclusive_OR_expression
                               | logical_AND_expression L_AND inclusive_OR_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.BinOp(p[1], ast.LogicalOp.L_AND, p[3], p.lineno(2))
    else:
        raise SyntaxAnalyzerError


# logical-or-expression
def p_logical_OR_expression(p):
    '''
        logical_OR_expression : logical_AND_expression
                              | logical_OR_expression L_OR logical_AND_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.BinOp(p[1], ast.LogicalOp.L_OR, p[3], p.lineno(2))
    else:
        raise SyntaxAnalyzerError


# conditional-expression
def p_conditional_expression(p):
    '''
        conditional_expression : logical_OR_expression
                               | logical_OR_expression TERNARY expression COLON conditional_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 6:
        p[0] = ast.TerOp(p[1], p[3], p[5], p.lineno(2))
    else:
        raise SyntaxAnalyzerError


# assignment-expression
def p_assignment_expression(p):
    '''
        assignment_expression : conditional_expression
                              | unary_expression assignment_operator assignment_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.Assign(p[1], p[2], p[3], p.lineno(2))
    else:
        raise SyntaxAnalyzerError


# assignment-operator
def p_assignment_operator(p):
    '''
        assignment_operator : ASSIGN
                            | MUL_ASSIGN
                            | DIV_ASSIGN
                            | MOD_ASSIGN
                            | ADD_ASSIGN
                            | SUB_ASSIGN
                            | B_LSHIFT_ASSIGN
                            | B_RSHIFT_ASSIGN
                            | B_AND_ASSIGN
                            | B_XOR_ASSIGN
                            | B_OR_ASSIGN
    '''
    if p[1] == '=':
        p[0] = ast.AssignOp.ASSIGN
    elif p[1] == '*=':
        p[0] = ast.AssignOp.MUL_ASSIGN
    elif p[1] == '/=':
        p[0] = ast.AssignOp.DIV_ASSIGN
    elif p[1] == '%=':
        p[0] = ast.AssignOp.MOD_ASSIGN
    elif p[1] == '+=':
        p[0] = ast.AssignOp.ADD_ASSIGN
    elif p[1] == '-=':
        p[0] = ast.AssignOp.SUB_ASSIGN
    elif p[1] == '<<=':
        p[0] = ast.AssignOp.B_LSHIFT_ASSIGN
    elif p[1] == '>>=':
        p[0] = ast.AssignOp.B_RSHIFT_ASSIGN
    elif p[1] == '&=':
        p[0] = ast.AssignOp.B_AND_ASSIGN
    elif p[1] == '^=':
        p[0] = ast.AssignOp.B_XOR_ASSIGN
    elif p[1] == '|=':
        p[0] = ast.AssignOp.B_OR_ASSIGN
    else:
        raise SyntaxAnalyzerError


# expression
def p_expression(p):
    '''
        expression : assignment_expression
                   | expression COMMA assignment_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ast.Expr(p[1], p[3], p.lineno(3))
    else:
        raise SyntaxAnalyzerError


# constant-expression
def p_constant_expression(p):
    'constant_expression : conditional_expression'
    p[0] = p[1]


# declaration
def p_declaration(p):
    '''
        declaration : declaration_specifiers SEMI_COLON
                    | declaration_specifiers init_declarator_list SEMI_COLON
    '''
    pass


# declaration-specifiers
def p_declaration_specifiers(p):
    '''
        declaration_specifiers : storage_class_specifier
                               | storage_class_specifier declaration_specifiers
                               | type_specifier
                               | type_specifier declaration_specifiers
                               | type_qualifier
                               | type_qualifier declaration_specifiers
    '''
    pass


# init-declarator-list:
def p_init_declarator_list(p):
    '''
        init_declarator_list : init_declarator
                             | init_declarator_list COMMA init_declarator
    '''
    pass


# init-declarator
def p_init_declarator(p):
    '''
        init_declarator : declarator
                        | declarator ASSIGN initializer
    '''
    pass


# storage-class-specifier
def p_storage_class_specifier(p):
    '''
        storage_class_specifier : TYPEDEF
                                | EXTERN
                                | STATIC
                                | AUTO
                                | REGISTER
    '''
    pass


# type-specifier
def p_type_specifier(p):
    '''
        type_specifier : VOID
                       | CHAR
                       | SHORT
                       | INT
                       | LONG
                       | FLOAT
                       | DOUBLE
                       | SIGNED
                       | UNSIGNED
                       | struct_or_union_specifier
                       | enum_specifier
                       | typedef_name
    '''
    pass


# struct-or-union-specifier
def p_struct_or_union_specifier(p):
    '''
        struct_or_union_specifier : struct_or_union ID
                                  | struct_or_union LBRACE struct_declaration_list RBRACE
                                  | struct_or_union ID LBRACE struct_declaration_list RBRACE

    '''
    pass


# struct-or-union
def p_struct_or_union(p):
    '''
        struct_or_union : STRUCT
                        | UNION
    '''
    pass


# struct-declaration-list
def p_struct_declaration_list(p):
    '''
        struct_declaration_list : struct_declaration
                                | struct_declaration_list struct_declaration
    '''
    pass


# struct-declaration
def p_struct_declaration(p):
    'struct_declaration : specifier_qualifier_list struct_declarator_list SEMI_COLON'
    pass


# specifier-qualifier-list
def p_specifier_qualifier_list(p):
    '''
        specifier_qualifier_list : type_specifier
                                 | type_specifier specifier_qualifier_list
                                 | type_qualifier
                                 | type_qualifier specifier_qualifier_list
    '''
    pass


# struct-declarator-list
def p_struct_declarator_list(p):
    '''
        struct_declarator_list : struct_declarator
                               | struct_declarator_list COMMA struct_declarator
    '''
    pass


# struct-declarator
def p_struct_declarator(p):
    '''
        struct_declarator : declarator
                          | COLON constant_expression
                          | declarator COLON constant_expression
    '''
    pass


# enum-specifier
def p_enum_specifier(p):
    '''
        enum_specifier : ENUM LBRACE enumerator_list RBRACE
                       | ENUM ID LBRACE enumerator_list RBRACE
                       | ENUM ID
    '''
    pass


# enumerator-list:
def p_enumerator_list(p):
    '''
        enumerator_list : enumerator
                        | enumerator_list COMMA enumerator
    '''
    pass


# enumerator
def p_enumerator(p):
    '''
        enumerator : ECONST
                   | ECONST ASSIGN constant_expression
    '''
    pass


# type-qualifier
def p_type_qualifier(p):
    '''
        type_qualifier : CONST
                       | VOLATILE
    '''
    pass


# declarator
def p_declarator(p):
    '''
        declarator : direct_declarator
                   | pointer direct_declarator
    '''
    pass


# direct-declarator
def p_direct_declarator(p):
    '''
        direct_declarator : ID
                          | LPAREN declarator RPAREN
                          | direct_declarator LPAREN RPAREN
                          | direct_declarator LBRACKET constant_expression RBRACKET
                          | direct_declarator LPAREN parameter_type_list RPAREN
                          | direct_declarator LPAREN identifier_list RPAREN
    '''
    pass


# pointer
def p_pointer(p):
    '''
        pointer : ASTERISK
                | ASTERISK type_qualifier_list
                | ASTERISK pointer
                | ASTERISK type_qualifier_list pointer
    '''
    pass


# type-qualifier-list
def p_type_qualifier_list(p):
    '''
        type_qualifier_list : type_qualifier
                            | type_qualifier_list type_qualifier
    '''
    pass


# parameter-type-list
def p_parameter_type_list(p):
    '''
        parameter_type_list : parameter_list
                            | parameter_list COMMA ELLIPSIS
    '''
    pass


# parameter-list
def p_parameter_list(p):
    '''
        parameter_list : parameter_declaration
                       | parameter_list COMMA parameter_declaration
    '''
    pass


# parameter-declaration
def p_parameter_declaration(p):
    '''
        parameter_declaration : declaration_specifiers declarator
                              | declaration_specifiers
                              | declaration_specifiers abstract_declarator
    '''
    pass


# identifier-list
def p_identifier_list(p):
    '''
        identifier_list : ID
                        | identifier_list COMMA ID
    '''
    pass


# type-name
def p_type_name(p):
    '''
        type_name : specifier_qualifier_list
                  | specifier_qualifier_list abstract_declarator
    '''
    pass


# abstract-declaration
def p_abstract_declarator(p):
    '''
        abstract_declarator : pointer
                             | direct_abstract_declarator
                             | pointer direct_abstract_declarator
    '''
    pass


# direct-abstract-declaration
def p_direct_abstract_declarator(p):
    '''
        direct_abstract_declarator : LPAREN abstract_declarator RPAREN
                                   | LBRACKET RBRACKET
                                   | LBRACKET constant_expression RBRACKET
                                   | direct_abstract_declarator LBRACKET RBRACKET
                                   | direct_abstract_declarator LBRACKET constant_expression RBRACKET
                                   | LPAREN RPAREN
                                   | LPAREN parameter_type_list RPAREN
                                   | direct_abstract_declarator LPAREN RPAREN
                                   | direct_abstract_declarator LPAREN parameter_type_list RPAREN
    '''
    pass


# typedef-name
def p_typedef_name(p):
    'typedef_name : ID'
    pass


# initializer
def p_initializer(p):
    '''
        initializer : assignment_expression
                    | LBRACE initializer_list RBRACE
                    | LBRACE initializer_list COMMA RBRACE
    '''
    pass


# initializer-list
def p_initializer_list(p):
    '''
        initializer_list : initializer
                         | initializer_list COMMA initializer
    '''
    pass


# statement
def p_statement(p):
    '''
        statement : labeled_statement
                  | compound_statement
                  | expression_statement
                  | selection_statement
                  | iteration_statement
                  | jump_statement
    '''
    pass


# labeled-statement
def p_labeled_statement(p):
    '''
        labeled_statement : ID COLON statement
                          | CASE constant_expression COLON statement
                          | DEFAULT COLON statement
    '''
    pass


# compound-statement
def p_compound_statement(p):
    '''
        compound_statement : LBRACE RBRACE
                           | LBRACE declaration_list RBRACE
                           | LBRACE statement_list RBRACE
                           | LBRACE declaration_list statement_list RBRACE
    '''
    pass


# declaration-list
def p_declaration_list(p):
    '''
        declaration_list : declaration
                         | declaration_list declaration
    '''
    pass


# statement-list
def p_statement_list(p):
    '''
        statement_list : statement
                       | statement_list statement
    '''
    pass


# expression-statement
def p_expression_statement(p):
    '''
        expression_statement : SEMI_COLON
                             | expression SEMI_COLON
    '''
    pass


# selection-statement
def p_selection_statement(p):
    '''
        selection_statement : IF LPAREN expression RPAREN statement
                            | IF LPAREN expression RPAREN statement ELSE statement
                            | SWITCH LPAREN expression RPAREN statement
    '''
    pass


# iteration_statement
def p_iteration_statement(p):
    '''
        iteration_statement : WHILE LPAREN expression RPAREN statement
                            | DO statement WHILE LPAREN expression RPAREN SEMI_COLON
                            | FOR LPAREN expression_opt SEMI_COLON expression_opt SEMI_COLON expression_opt RPAREN statement
    '''
    pass


# jump_statement
def p_jump_statement(p):
    '''
        jump_statement : GOTO ID SEMI_COLON
                       | CONTINUE SEMI_COLON
                       | BREAK SEMI_COLON
                       | RETURN SEMI_COLON
                       | RETURN expression SEMI_COLON
    '''
    pass


# translation-unit
def p_translation_unit(p):
    '''
        translation_unit : external_declaration
                         | translation_unit external_declaration
    '''
    pass


# external-declaration
def p_external_declaration(p):
    '''
        external_declaration : function_definition
                             | declaration
    '''
    pass


# function-definition
def p_function_definition(p):
    '''
        function_definition : declarator compound_statement
                            | declaration_specifiers declarator compound_statement
                            | declarator declaration_list compound_statement
                            | declaration_specifiers declarator declaration_list compound_statement
    '''
    pass


# empty
def p_empty(p):
    'empty : '
    pass


# opts
def p_expression_opt(p):
    '''
        expression_opt : expression
                       | empty
    '''
    pass


def p_error(p):
    print("Whoa. We're hosed")


import profile
# Build the grammar

yacc.yacc()

while 1:
    try:
        s = input('expr > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)

#yacc.yacc(method='LALR',write_tables=False,debug=False)

#profile.run("yacc.yacc(method='LALR')")
