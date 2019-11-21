# -----------------------------------------------------------------------------
# syntax_analyzer.py
#
# A syntax analyzer for ANSI C.  Based on the grammar in K&R, 2nd Ed.
# -----------------------------------------------------------------------------

import sys
import lexical_analyzer
import ply.yacc as yacc
from node import Node

# Get the token map
tokens = lexical_analyzer.tokens

# modify token to node
def to_node(node_list):
    result = []
    for item in node_list:
        if isinstance(item, Node):
            result.append(item)
        elif isinstance(item, str):
            result.append(Node(item, (None, None), None))
        else:
            result.append(Node((item[0], (item[2], item[2]), item[1])))
    return result

def union_line_range(token):
    begin = None
    end = None
    for item in token[1:]:
        if item.data[1][0] is not None:
            begin = item.data[1][0]
            break
    for item in reversed(token[1:]):
        if item.data[1][1] is not None:
            end = item.data[1][1]
            break
    return begin, end
# translation-unit:


def p_translation_unit_1(t):
    'translation_unit : external_declaration'
    children = to_node(t[1:])
    t[0] = Node(("translation_unit", union_line_range(children)), children)


def p_translation_unit_2(t):
    'translation_unit : translation_unit external_declaration'
    children = to_node(t[1:])
    t[0] = Node(("translation_unit", union_line_range(children)), children)


# external-declaration:


def p_external_declaration_1(t):
    'external_declaration : function_definition'
    children = to_node(t[1:])
    t[0] = Node(("external_declaration", union_line_range(children)), children)


def p_external_declaration_2(t):
    'external_declaration : declaration'
    children = to_node(t[1:])
    t[0] = Node(("external_declaration", union_line_range(children)), children)


# function-definition:


def p_function_definition_1(t):
    'function_definition : declaration_specifiers declarator declaration_list compound_statement'
    children = to_node(t[1:])
    t[0] = Node(("function_definition", union_line_range(children)), children)


def p_function_definition_2(t):
    'function_definition : declarator declaration_list compound_statement'
    children = to_node(t[1:])
    t[0] = Node(("function_definition", union_line_range(children)), children)


def p_function_definition_3(t):
    'function_definition : declarator compound_statement'
    children = to_node(t[1:])
    t[0] = Node(("function_definition", union_line_range(children)), children)


def p_function_definition_4(t):
    'function_definition : declaration_specifiers declarator compound_statement'
    children = to_node(t[1:])
    t[0] = Node(("function_definition", union_line_range(children)), children)

# declaration:


def p_declaration_1(t):
    'declaration : declaration_specifiers init_declarator_list SEMI'
    children = to_node(t[1:])
    t[0] = Node(("declaration", union_line_range(children)), children)


def p_declaration_2(t):
    'declaration : declaration_specifiers SEMI'
    children = to_node(t[1:])
    t[0] = Node(("declaration", union_line_range(children)), children)

# declaration-list:


def p_declaration_list_1(t):
    'declaration_list : declaration'
    children = to_node(t[1:])
    t[0] = Node(("declaration_list", union_line_range(children)), children)


def p_declaration_list_2(t):
    'declaration_list : declaration_list declaration'
    children = to_node(t[1:])
    t[0] = Node(("declaration_list", union_line_range(children)), children)

# declaration-specifiers


def p_declaration_specifiers_1(t):
    'declaration_specifiers : storage_class_specifier declaration_specifiers'
    children = to_node(t[1:])
    t[0] = Node(("declaration_specifiers", union_line_range(children)), children)


def p_declaration_specifiers_2(t):
    'declaration_specifiers : type_specifier declaration_specifiers'
    children = to_node(t[1:])
    t[0] = Node(("declaration_specifiers", union_line_range(children)), children)


def p_declaration_specifiers_3(t):
    'declaration_specifiers : type_qualifier declaration_specifiers'
    children = to_node(t[1:])
    t[0] = Node(("declaration_specifiers", union_line_range(children)), children)


def p_declaration_specifiers_4(t):
    'declaration_specifiers : storage_class_specifier'
    children = to_node(t[1:])
    t[0] = Node(("declaration_specifiers", union_line_range(children)), children)


def p_declaration_specifiers_5(t):
    'declaration_specifiers : type_specifier'
    children = to_node(t[1:])
    t[0] = Node(("declaration_specifiers", union_line_range(children)), children)


def p_declaration_specifiers_6(t):
    'declaration_specifiers : type_qualifier'
    children = to_node(t[1:])
    t[0] = Node(("declaration_specifiers", union_line_range(children)), children)

# storage-class-specifier


def p_storage_class_specifier(t):
    '''storage_class_specifier : AUTO
                               | REGISTER
                               | STATIC
                               | EXTERN
                               | TYPEDEF
                               '''
    children = to_node(t[1:])
    t[0] = Node(("storage_class_specifier", union_line_range(children)), children)

# type-specifier:


def p_type_specifier(t):
    '''type_specifier : VOID
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
                      | TYPEID
                      '''

    children = to_node(t[1:])
    t[0] = Node(("type_specifier", union_line_range(children)), children)

# type-qualifier:


def p_type_qualifier(t):
    '''type_qualifier : CONST
                      | VOLATILE'''

    children = to_node(t[1:])
    t[0] = Node(("type_qualifier", union_line_range(children)), children)

# struct-or-union-specifier


def p_struct_or_union_specifier_1(t):
    'struct_or_union_specifier : struct_or_union ID LBRACE struct_declaration_list RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("struct_or_union_specifier", union_line_range(children)), children)


def p_struct_or_union_specifier_2(t):
    'struct_or_union_specifier : struct_or_union LBRACE struct_declaration_list RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("struct_or_union_specifier", union_line_range(children)), children)


def p_struct_or_union_specifier_3(t):
    'struct_or_union_specifier : struct_or_union ID'
    children = to_node(t[1:])
    t[0] = Node(("struct_or_union_specifier", union_line_range(children)), children)

# struct-or-union:


def p_struct_or_union(t):
    '''struct_or_union : STRUCT
                       | UNION
                       '''
    children = to_node(t[1:])
    t[0] = Node(("struct_or_union", union_line_range(children)), children)

# struct-declaration-list:


def p_struct_declaration_list_1(t):
    'struct_declaration_list : struct_declaration'
    children = to_node(t[1:])
    t[0] = Node(("struct_declaration_list", union_line_range(children)), children)


def p_struct_declaration_list_2(t):
    'struct_declaration_list : struct_declaration_list struct_declaration'
    children = to_node(t[1:])
    t[0] = Node(("struct_declaration_list", union_line_range(children)), children)

# init-declarator-list:


def p_init_declarator_list_1(t):
    'init_declarator_list : init_declarator'
    children = to_node(t[1:])
    t[0] = Node(("init_declarator_list", union_line_range(children)), children)


def p_init_declarator_list_2(t):
    'init_declarator_list : init_declarator_list COMMA init_declarator'
    children = to_node(t[1:])
    t[0] = Node(("init_declarator_list", union_line_range(children)), children)

# init-declarator


def p_init_declarator_1(t):
    'init_declarator : declarator'
    children = to_node(t[1:])
    t[0] = Node(("init_declarator", union_line_range(children)), children)


def p_init_declarator_2(t):
    'init_declarator : declarator EQUALS initializer'
    children = to_node(t[1:])
    t[0] = Node(("init_declarator", union_line_range(children)), children)

# struct-declaration:


def p_struct_declaration(t):
    'struct_declaration : specifier_qualifier_list struct_declarator_list SEMI'
    children = to_node(t[1:])
    t[0] = Node(("struct_declaration", union_line_range(children)), children)

# specifier-qualifier-list:


def p_specifier_qualifier_list_1(t):
    'specifier_qualifier_list : type_specifier specifier_qualifier_list'
    children = to_node(t[1:])
    t[0] = Node(("specifier_qualifier_list", union_line_range(children)), children)


def p_specifier_qualifier_list_2(t):
    'specifier_qualifier_list : type_specifier'
    children = to_node(t[1:])
    t[0] = Node(("specifier_qualifier_list", union_line_range(children)), children)


def p_specifier_qualifier_list_3(t):
    'specifier_qualifier_list : type_qualifier specifier_qualifier_list'
    children = to_node(t[1:])
    t[0] = Node(("specifier_qualifier_list", union_line_range(children)), children)


def p_specifier_qualifier_list_4(t):
    'specifier_qualifier_list : type_qualifier'
    children = to_node(t[1:])
    t[0] = Node(("specifier_qualifier_list", union_line_range(children)), children)

# struct-declarator-list:


def p_struct_declarator_list_1(t):
    'struct_declarator_list : struct_declarator'
    children = to_node(t[1:])
    t[0] = Node(("struct_declarator_list", union_line_range(children)), children)


def p_struct_declarator_list_2(t):
    'struct_declarator_list : struct_declarator_list COMMA struct_declarator'
    children = to_node(t[1:])
    t[0] = Node(("struct_declarator_list", union_line_range(children)), children)

# struct-declarator:


def p_struct_declarator_1(t):
    'struct_declarator : declarator'
    children = to_node(t[1:])
    t[0] = Node(("struct_declarator", union_line_range(children)), children)


def p_struct_declarator_2(t):
    'struct_declarator : declarator COLON constant_expression'
    children = to_node(t[1:])
    t[0] = Node(("struct_declarator", union_line_range(children)), children)


def p_struct_declarator_3(t):
    'struct_declarator : COLON constant_expression'
    children = to_node(t[1:])
    t[0] = Node(("struct_declarator", union_line_range(children)), children)

# enum-specifier:


def p_enum_specifier_1(t):
    'enum_specifier : ENUM ID LBRACE enumerator_list RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("enum_specifier", union_line_range(children)), children)


def p_enum_specifier_2(t):
    'enum_specifier : ENUM LBRACE enumerator_list RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("enum_specifier", union_line_range(children)), children)


def p_enum_specifier_3(t):
    'enum_specifier : ENUM ID'
    children = to_node(t[1:])
    t[0] = Node(("enum_specifier", union_line_range(children)), children)

# enumerator_list:


def p_enumerator_list_1(t):
    'enumerator_list : enumerator'
    children = to_node(t[1:])
    t[0] = Node(("enumerator_list", union_line_range(children)), children)


def p_enumerator_list_2(t):
    'enumerator_list : enumerator_list COMMA enumerator'
    children = to_node(t[1:])
    t[0] = Node(("enumerator_list", union_line_range(children)), children)

# enumerator:


def p_enumerator_1(t):
    'enumerator : ID'
    children = to_node(t[1:])
    t[0] = Node(("enumerator", union_line_range(children)), children)


def p_enumerator_2(t):
    'enumerator : ID EQUALS constant_expression'
    children = to_node(t[1:])
    t[0] = Node(("enumerator", union_line_range(children)), children)

# declarator:


def p_declarator_1(t):
    'declarator : pointer direct_declarator'
    children = to_node(t[1:])
    t[0] = Node(("declarator", union_line_range(children)), children)


def p_declarator_2(t):
    'declarator : direct_declarator'
    children = to_node(t[1:])
    t[0] = Node(("declarator", union_line_range(children)), children)

# direct-declarator:


def p_direct_declarator_1(t):
    'direct_declarator : ID'
    children = to_node(t[1:])
    t[0] = Node(("direct_declarator", union_line_range(children)), children)


def p_direct_declarator_2(t):
    'direct_declarator : LPAREN declarator RPAREN'
    children = to_node(t[1:])
    t[0] = Node(("direct_declarator", union_line_range(children)), children)


def p_direct_declarator_3(t):
    'direct_declarator : direct_declarator LBRACKET constant_expression_opt RBRACKET'
    children = to_node(t[1:])
    t[0] = Node(("direct_declarator", union_line_range(children)), children)


def p_direct_declarator_4(t):
    'direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN '
    children = to_node(t[1:])
    t[0] = Node(("direct_declarator", union_line_range(children)), children)


def p_direct_declarator_5(t):
    'direct_declarator : direct_declarator LPAREN identifier_list RPAREN '
    children = to_node(t[1:])
    t[0] = Node(("direct_declarator", union_line_range(children)), children)


def p_direct_declarator_6(t):
    'direct_declarator : direct_declarator LPAREN RPAREN '
    children = to_node(t[1:])
    t[0] = Node(("direct_declarator", union_line_range(children)), children)

# pointer:


def p_pointer_1(t):
    'pointer : TIMES type_qualifier_list'
    children = to_node(t[1:])
    t[0] = Node(("pointer", union_line_range(children)), children)


def p_pointer_2(t):
    'pointer : TIMES'
    children = to_node(t[1:])
    t[0] = Node(("pointer", union_line_range(children)), children)


def p_pointer_3(t):
    'pointer : TIMES type_qualifier_list pointer'
    children = to_node(t[1:])
    t[0] = Node(("pointer", union_line_range(children)), children)


def p_pointer_4(t):
    'pointer : TIMES pointer'
    children = to_node(t[1:])
    t[0] = Node(("pointer", union_line_range(children)), children)

# type-qualifier-list:


def p_type_qualifier_list_1(t):
    'type_qualifier_list : type_qualifier'
    children = to_node(t[1:])
    t[0] = Node(("type_qualifier_list", union_line_range(children)), children)


def p_type_qualifier_list_2(t):
    'type_qualifier_list : type_qualifier_list type_qualifier'
    children = to_node(t[1:])
    t[0] = Node(("type_qualifier_list", union_line_range(children)), children)

# parameter-type-list:


def p_parameter_type_list_1(t):
    'parameter_type_list : parameter_list'
    children = to_node(t[1:])
    t[0] = Node(("parameter_type_list", union_line_range(children)), children)


def p_parameter_type_list_2(t):
    'parameter_type_list : parameter_list COMMA ELLIPSIS'
    children = to_node(t[1:])
    t[0] = Node(("parameter_type_list", union_line_range(children)), children)

# parameter-list:


def p_parameter_list_1(t):
    'parameter_list : parameter_declaration'
    children = to_node(t[1:])
    t[0] = Node(("parameter_list", union_line_range(children)), children)


def p_parameter_list_2(t):
    'parameter_list : parameter_list COMMA parameter_declaration'
    children = to_node(t[1:])
    t[0] = Node(("parameter_list", union_line_range(children)), children)

# parameter-declaration:


def p_parameter_declaration_1(t):
    'parameter_declaration : declaration_specifiers declarator'
    children = to_node(t[1:])
    t[0] = Node(("parameter_declaration", union_line_range(children)), children)


def p_parameter_declaration_2(t):
    'parameter_declaration : declaration_specifiers abstract_declarator_opt'
    children = to_node(t[1:])
    t[0] = Node(("parameter_declaration", union_line_range(children)), children)

# identifier-list:


def p_identifier_list_1(t):
    'identifier_list : ID'
    children = to_node(t[1:])
    t[0] = Node(("identifier_list", union_line_range(children)), children)


def p_identifier_list_2(t):
    'identifier_list : identifier_list COMMA ID'
    children = to_node(t[1:])
    t[0] = Node(("identifier_list", union_line_range(children)), children)

# initializer:


def p_initializer_1(t):
    'initializer : assignment_expression'
    children = to_node(t[1:])
    t[0] = Node(("initializer", union_line_range(children)), children)


def p_initializer_2(t):
    '''initializer : LBRACE initializer_list RBRACE
                   | LBRACE initializer_list COMMA RBRACE'''
    children = to_node(t[1:])
    t[0] = Node(("initializer", union_line_range(children)), children)

# initializer-list:


def p_initializer_list_1(t):
    'initializer_list : initializer'
    children = to_node(t[1:])
    t[0] = Node(("initializer_list", union_line_range(children)), children)

def p_initializer_list_2(t):
    'initializer_list : initializer_list COMMA initializer'
    children = to_node(t[1:])
    t[0] = Node(("initializer_list", union_line_range(children)), children)

# type-name:


def p_type_name(t):
    'type_name : specifier_qualifier_list abstract_declarator_opt'
    children = to_node(t[1:])
    t[0] = Node(("type_name", union_line_range(children)), children)


def p_abstract_declarator_opt_1(t):
    'abstract_declarator_opt : empty'
    children = to_node(t[1:])
    t[0] = Node(("abstract_declarator_opt", union_line_range(children)), children)


def p_abstract_declarator_opt_2(t):
    'abstract_declarator_opt : abstract_declarator'
    children = to_node(t[1:])
    t[0] = Node(("abstract_declarator_opt", union_line_range(children)), children)

# abstract-declarator:


def p_abstract_declarator_1(t):
    'abstract_declarator : pointer '
    children = to_node(t[1:])
    t[0] = Node(("abstract_declarator", union_line_range(children)), children)


def p_abstract_declarator_2(t):
    'abstract_declarator : pointer direct_abstract_declarator'
    children = to_node(t[1:])
    t[0] = Node(("abstract_declarator", union_line_range(children)), children)


def p_abstract_declarator_3(t):
    'abstract_declarator : direct_abstract_declarator'
    children = to_node(t[1:])
    t[0] = Node(("abstract_declarator", union_line_range(children)), children)

# direct-abstract-declarator:


def p_direct_abstract_declarator_1(t):
    'direct_abstract_declarator : LPAREN abstract_declarator RPAREN'
    children = to_node(t[1:])
    t[0] = Node(("direct_abstract_declarator", union_line_range(children)), children)


def p_direct_abstract_declarator_2(t):
    'direct_abstract_declarator : direct_abstract_declarator LBRACKET constant_expression_opt RBRACKET'
    children = to_node(t[1:])
    t[0] = Node(("direct_abstract_declarator", union_line_range(children)), children)


def p_direct_abstract_declarator_3(t):
    'direct_abstract_declarator : LBRACKET constant_expression_opt RBRACKET'
    children = to_node(t[1:])
    t[0] = Node(("direct_abstract_declarator", union_line_range(children)), children)


def p_direct_abstract_declarator_4(t):
    'direct_abstract_declarator : direct_abstract_declarator LPAREN parameter_type_list_opt RPAREN'
    children = to_node(t[1:])
    t[0] = Node(("direct_abstract_declarator", union_line_range(children)), children)


def p_direct_abstract_declarator_5(t):
    'direct_abstract_declarator : LPAREN parameter_type_list_opt RPAREN'
    children = to_node(t[1:])
    t[0] = Node(("direct_abstract_declarator", union_line_range(children)), children)

# Optional fields in abstract declarators


def p_constant_expression_opt_1(t):
    'constant_expression_opt : empty'
    children = to_node(t[1:])
    t[0] = Node(("constant_expression_opt", union_line_range(children)), children)


def p_constant_expression_opt_2(t):
    'constant_expression_opt : constant_expression'
    children = to_node(t[1:])
    t[0] = Node(("constant_expression_opt", union_line_range(children)), children)


def p_parameter_type_list_opt_1(t):
    'parameter_type_list_opt : empty'
    children = to_node(t[1:])
    t[0] = Node(("parameter_type_list_opt", union_line_range(children)), children)


def p_parameter_type_list_opt_2(t):
    'parameter_type_list_opt : parameter_type_list'
    children = to_node(t[1:])
    t[0] = Node(("parameter_type_list_opt", union_line_range(children)), children)

# statement:


def p_statement(t):
    '''
    statement : labeled_statement
              | expression_statement
              | compound_statement
              | selection_statement
              | iteration_statement
              | jump_statement
              '''
    children = to_node(t[1:])
    t[0] = Node(("statement", union_line_range(children)), children)

# labeled-statement:


def p_labeled_statement_1(t):
    'labeled_statement : ID COLON statement'
    children = to_node(t[1:])
    t[0] = Node(("labeled_statement", union_line_range(children)), children)


def p_labeled_statement_2(t):
    'labeled_statement : CASE constant_expression COLON statement'
    children = to_node(t[1:])
    t[0] = Node(("labeled_statement", union_line_range(children)), children)


def p_labeled_statement_3(t):
    'labeled_statement : DEFAULT COLON statement'
    children = to_node(t[1:])
    t[0] = Node(("labeled_statement", union_line_range(children)), children)

# expression-statement:


def p_expression_statement(t):
    'expression_statement : expression_opt SEMI'
    children = to_node(t[1:])
    t[0] = Node(("expression_statement", union_line_range(children)), children)

# compound-statement:


def p_compound_statement_1(t):
    'compound_statement : LBRACE declaration_list statement_list RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("compound_statement", union_line_range(children)), children)


def p_compound_statement_2(t):
    'compound_statement : LBRACE statement_list RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("compound_statement", union_line_range(children)), children)


def p_compound_statement_3(t):
    'compound_statement : LBRACE declaration_list RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("compound_statement", union_line_range(children)), children)


def p_compound_statement_4(t):
    'compound_statement : LBRACE RBRACE'
    children = to_node(t[1:])
    t[0] = Node(("compound_statement", union_line_range(children)), children)

# statement-list:


def p_statement_list_1(t):
    'statement_list : statement'
    children = to_node(t[1:])
    t[0] = Node(("statement_list", union_line_range(children)), children)


def p_statement_list_2(t):
    'statement_list : statement_list statement'
    children = to_node(t[1:])
    t[0] = Node(("statement_list", union_line_range(children)), children)

# selection-statement


def p_selection_statement_1(t):
    'selection_statement : IF LPAREN expression RPAREN statement'
    children = to_node(t[1:])
    t[0] = Node(("selection_statement", union_line_range(children)), children)


def p_selection_statement_2(t):
    'selection_statement : IF LPAREN expression RPAREN statement ELSE statement '
    children = to_node(t[1:])
    t[0] = Node(("selection_statement", union_line_range(children)), children)


def p_selection_statement_3(t):
    'selection_statement : SWITCH LPAREN expression RPAREN statement '
    children = to_node(t[1:])
    t[0] = Node(("selection_statement", union_line_range(children)), children)

# iteration_statement:


def p_iteration_statement_1(t):
    'iteration_statement : WHILE LPAREN expression RPAREN statement'
    children = to_node(t[1:])
    t[0] = Node(("iteration_statement", union_line_range(children)), children)


def p_iteration_statement_2(t):
    'iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement '
    children = to_node(t[1:])
    t[0] = Node(("iteration_statement", union_line_range(children)), children)


def p_iteration_statement_3(t):
    'iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI'
    children = to_node(t[1:])
    t[0] = Node(("iteration_statement", union_line_range(children)), children)

# jump_statement:


def p_jump_statement_1(t):
    'jump_statement : GOTO ID SEMI'
    children = to_node(t[1:])
    t[0] = Node(("jump_statement", union_line_range(children)), children)


def p_jump_statement_2(t):
    'jump_statement : CONTINUE SEMI'
    children = to_node(t[1:])
    t[0] = Node(("jump_statement", union_line_range(children)), children)


def p_jump_statement_3(t):
    'jump_statement : BREAK SEMI'
    children = to_node(t[1:])
    t[0] = Node(("jump_statement", union_line_range(children)), children)


def p_jump_statement_4(t):
    'jump_statement : RETURN expression_opt SEMI'
    children = to_node(t[1:])
    t[0] = Node(("jump_statement", union_line_range(children)), children)


def p_expression_opt_1(t):
    'expression_opt : empty'
    children = to_node(t[1:])
    t[0] = Node(("expression_opt", union_line_range(children)), children)


def p_expression_opt_2(t):
    'expression_opt : expression'
    children = to_node(t[1:])
    t[0] = Node(("expression_opt", union_line_range(children)), children)

# expression:


def p_expression_1(t):
    'expression : assignment_expression'
    children = to_node(t[1:])
    t[0] = Node(("expression", union_line_range(children)), children)


def p_expression_2(t):
    'expression : expression COMMA assignment_expression'
    children = to_node(t[1:])
    t[0] = Node(("expression", union_line_range(children)), children)

# assigment_expression:


def p_assignment_expression_1(t):
    'assignment_expression : conditional_expression'
    children = to_node(t[1:])
    t[0] = Node(("assignment_expression", union_line_range(children)), children)


def p_assignment_expression_2(t):
    'assignment_expression : unary_expression assignment_operator assignment_expression'
    children = to_node(t[1:])
    t[0] = Node(("assignment_expression", union_line_range(children)), children)

# assignment_operator:


def p_assignment_operator(t):
    '''
    assignment_operator : EQUALS
                        | TIMESEQUAL
                        | DIVEQUAL
                        | MODEQUAL
                        | PLUSEQUAL
                        | MINUSEQUAL
                        | LSHIFTEQUAL
                        | RSHIFTEQUAL
                        | ANDEQUAL
                        | OREQUAL
                        | XOREQUAL
                        '''
    children = to_node(t[1:])
    t[0] = Node(("assignment_operator", union_line_range(children)), children)

# conditional-expression


def p_conditional_expression_1(t):
    'conditional_expression : logical_or_expression'
    children = to_node(t[1:])
    t[0] = Node(("conditional_expression", union_line_range(children)), children)


def p_conditional_expression_2(t):
    'conditional_expression : logical_or_expression CONDOP expression COLON conditional_expression '
    children = to_node(t[1:])
    t[0] = Node(("conditional_expression", union_line_range(children)), children)

# constant-expression


def p_constant_expression(t):
    'constant_expression : conditional_expression'
    children = to_node(t[1:])
    t[0] = Node(("constant_expression", union_line_range(children)), children)

# logical-or-expression


def p_logical_or_expression_1(t):
    'logical_or_expression : logical_and_expression'
    children = to_node(t[1:])
    t[0] = Node(("logical_or_expression", union_line_range(children)), children)


def p_logical_or_expression_2(t):
    'logical_or_expression : logical_or_expression LOR logical_and_expression'
    children = to_node(t[1:])
    t[0] = Node(("logical_or_expression", union_line_range(children)), children)

# logical-and-expression


def p_logical_and_expression_1(t):
    'logical_and_expression : inclusive_or_expression'
    children = to_node(t[1:])
    t[0] = Node(("logical_and_expression", union_line_range(children)), children)


def p_logical_and_expression_2(t):
    'logical_and_expression : logical_and_expression LAND inclusive_or_expression'
    children = to_node(t[1:])
    t[0] = Node(("logical_and_expression", union_line_range(children)), children)

# inclusive-or-expression:


def p_inclusive_or_expression_1(t):
    'inclusive_or_expression : exclusive_or_expression'
    children = to_node(t[1:])
    t[0] = Node(("inclusive_or_expression", union_line_range(children)), children)


def p_inclusive_or_expression_2(t):
    'inclusive_or_expression : inclusive_or_expression OR exclusive_or_expression'
    children = to_node(t[1:])
    t[0] = Node(("inclusive_or_expression", union_line_range(children)), children)

# exclusive-or-expression:


def p_exclusive_or_expression_1(t):
    'exclusive_or_expression :  and_expression'
    children = to_node(t[1:])
    t[0] = Node(("exclusive_or_expression", union_line_range(children)), children)


def p_exclusive_or_expression_2(t):
    'exclusive_or_expression :  exclusive_or_expression XOR and_expression'
    children = to_node(t[1:])
    t[0] = Node(("exclusive_or_expression", union_line_range(children)), children)

# AND-expression


def p_and_expression_1(t):
    'and_expression : equality_expression'
    children = to_node(t[1:])
    t[0] = Node(("and_expression", union_line_range(children)), children)


def p_and_expression_2(t):
    'and_expression : and_expression AND equality_expression'
    children = to_node(t[1:])
    t[0] = Node(("and_expression", union_line_range(children)), children)


# equality-expression:
def p_equality_expression_1(t):
    'equality_expression : relational_expression'
    children = to_node(t[1:])
    t[0] = Node(("equality_expression", union_line_range(children)), children)


def p_equality_expression_2(t):
    'equality_expression : equality_expression EQ relational_expression'
    children = to_node(t[1:])
    t[0] = Node(("equality_expression", union_line_range(children)), children)


def p_equality_expression_3(t):
    'equality_expression : equality_expression NE relational_expression'
    children = to_node(t[1:])
    t[0] = Node(("equality_expression", union_line_range(children)), children)


# relational-expression:
def p_relational_expression_1(t):
    'relational_expression : shift_expression'
    children = to_node(t[1:])
    t[0] = Node(("relational_expression", union_line_range(children)), children)


def p_relational_expression_2(t):
    'relational_expression : relational_expression LT shift_expression'
    children = to_node(t[1:])
    t[0] = Node(("relational_expression", union_line_range(children)), children)


def p_relational_expression_3(t):
    'relational_expression : relational_expression GT shift_expression'
    children = to_node(t[1:])
    t[0] = Node(("relational_expression", union_line_range(children)), children)


def p_relational_expression_4(t):
    'relational_expression : relational_expression LE shift_expression'
    children = to_node(t[1:])
    t[0] = Node(("relational_expression", union_line_range(children)), children)


def p_relational_expression_5(t):
    'relational_expression : relational_expression GE shift_expression'
    children = to_node(t[1:])
    t[0] = Node(("relational_expression", union_line_range(children)), children)

# shift-expression


def p_shift_expression_1(t):
    'shift_expression : additive_expression'
    children = to_node(t[1:])
    t[0] = Node(("shift_expression", union_line_range(children)), children)


def p_shift_expression_2(t):
    'shift_expression : shift_expression LSHIFT additive_expression'
    children = to_node(t[1:])
    t[0] = Node(("shift_expression", union_line_range(children)), children)


def p_shift_expression_3(t):
    'shift_expression : shift_expression RSHIFT additive_expression'
    children = to_node(t[1:])
    t[0] = Node(("shift_expression", union_line_range(children)), children)

# additive-expression


def p_additive_expression_1(t):
    'additive_expression : multiplicative_expression'
    children = to_node(t[1:])
    t[0] = Node(("additive_expression", union_line_range(children)), children)


def p_additive_expression_2(t):
    'additive_expression : additive_expression PLUS multiplicative_expression'
    children = to_node(t[1:])
    t[0] = Node(("additive_expression", union_line_range(children)), children)


def p_additive_expression_3(t):
    'additive_expression : additive_expression MINUS multiplicative_expression'
    children = to_node(t[1:])
    t[0] = Node(("additive_expression", union_line_range(children)), children)

# multiplicative-expression


def p_multiplicative_expression_1(t):
    'multiplicative_expression : cast_expression'
    children = to_node(t[1:])
    t[0] = Node(("multiplicative_expression", union_line_range(children)), children)


def p_multiplicative_expression_2(t):
    'multiplicative_expression : multiplicative_expression TIMES cast_expression'
    children = to_node(t[1:])
    t[0] = Node(("multiplicative_expression", union_line_range(children)), children)


def p_multiplicative_expression_3(t):
    'multiplicative_expression : multiplicative_expression DIVIDE cast_expression'
    children = to_node(t[1:])
    t[0] = Node(("multiplicative_expression", union_line_range(children)), children)


def p_multiplicative_expression_4(t):
    'multiplicative_expression : multiplicative_expression MOD cast_expression'
    children = to_node(t[1:])
    t[0] = Node(("multiplicative_expression", union_line_range(children)), children)

# cast-expression:


def p_cast_expression_1(t):
    'cast_expression : unary_expression'
    children = to_node(t[1:])
    t[0] = Node(("cast_expression", union_line_range(children)), children)


def p_cast_expression_2(t):
    'cast_expression : LPAREN type_name RPAREN cast_expression'
    children = to_node(t[1:])
    t[0] = Node(("cast_expression", union_line_range(children)), children)

# unary-expression:


def p_unary_expression_1(t):
    'unary_expression : postfix_expression'
    children = to_node(t[1:])
    t[0] = Node(("unary_expression", union_line_range(children)), children)


def p_unary_expression_2(t):
    'unary_expression : PLUSPLUS unary_expression'
    children = to_node(t[1:])
    t[0] = Node(("unary_expression", union_line_range(children)), children)


def p_unary_expression_3(t):
    'unary_expression : MINUSMINUS unary_expression'
    children = to_node(t[1:])
    t[0] = Node(("unary_expression", union_line_range(children)), children)


def p_unary_expression_4(t):
    'unary_expression : unary_operator cast_expression'
    children = to_node(t[1:])
    t[0] = Node(("unary_expression", union_line_range(children)), children)


def p_unary_expression_5(t):
    'unary_expression : SIZEOF unary_expression'
    children = to_node(t[1:])
    t[0] = Node(("unary_expression", union_line_range(children)), children)


def p_unary_expression_6(t):
    'unary_expression : SIZEOF LPAREN type_name RPAREN'
    children = to_node(t[1:])
    t[0] = Node(("unary_expression", union_line_range(children)), children)

# unary-operator


def p_unary_operator(t):
    '''unary_operator : AND
                    | TIMES
                    | PLUS
                    | MINUS
                    | NOT
                    | LNOT '''
    children = to_node(t[1:])
    t[0] = Node(("unary_operator", union_line_range(children)), children)

# postfix-expression:


def p_postfix_expression_1(t):
    'postfix_expression : primary_expression'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)


def p_postfix_expression_2(t):
    'postfix_expression : postfix_expression LBRACKET expression RBRACKET'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)


def p_postfix_expression_3(t):
    'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)


def p_postfix_expression_4(t):
    'postfix_expression : postfix_expression LPAREN RPAREN'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)


def p_postfix_expression_5(t):
    'postfix_expression : postfix_expression PERIOD ID'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)


def p_postfix_expression_6(t):
    'postfix_expression : postfix_expression ARROW ID'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)


def p_postfix_expression_7(t):
    'postfix_expression : postfix_expression PLUSPLUS'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)


def p_postfix_expression_8(t):
    'postfix_expression : postfix_expression MINUSMINUS'
    children = to_node(t[1:])
    t[0] = Node(("postfix_expression", union_line_range(children)), children)

# primary-expression:


def p_primary_expression(t):
    '''primary_expression :  ID
                        |  constant
                        |  SCONST
                        |  LPAREN expression RPAREN'''
    children = to_node(t[1:])
    t[0] = Node(("primary_expression", union_line_range(children)), children)

# argument-expression-list:


def p_argument_expression_list(t):
    '''argument_expression_list :  assignment_expression
                              |  argument_expression_list COMMA assignment_expression'''
    children = to_node(t[1:])
    t[0] = Node(("argument_expression_list", union_line_range(children)), children)

# constant:


def p_constant(t):
    '''constant : ICONST
               | FCONST
               | CCONST'''
    children = to_node(t[1:])
    t[0] = Node(("constant", union_line_range(children)), children)

def p_empty(t):
    'empty : '
    t[0] = Node(("empty", (None, None)))


def p_error(t):
    print("Whoa. We're hosed")

import profile
# Build the grammar

#yacc.yacc()
#yacc.yacc(method='LALR',write_tables=False,debug=False)

parser = yacc.yacc()

#profile.run("yacc.yacc(method='LALR')")
