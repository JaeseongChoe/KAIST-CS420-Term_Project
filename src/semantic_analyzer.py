# ----------------------------------------------------------------------
# semantic_analyzer.py
#
# A semantic analyzer for ANSI C.
# ----------------------------------------------------------------------

import sys
import lexical_analyzer
import syntax_analyzer
import symtab

# Basic class for type
class Type:
	"""
    Attributes:
        type -- type of current node
        input_type -- input type when it is function
        output_type -- output type when it is function
    """
	def __init__(self, current_type, input_type = None, output_type = None, children = None):
		self.type = current_type
		self.input_type = input_type
		self.output_type = output_type
		self.children = children

	def get_type(self):
		return self.type

# Exception raised for type errors
class TypeError(Exception):
    """
    Attributes:
        node -- input node's position and name 
        		in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, node, message):
        self.node = node
        self.message = message

# Class for semantic analyzer
class semantic_analyzer:
	def __init__(self, ast, symtab):
		# Cursor for original AST, symbol table
		self.ast = ast
		self.cursor = ast
		self.symtab = symtab

	def binary_same(self, left, right):
		# TODO : Check two types are compatible (i.e. int and float)
		if left.current_type != right.current_type:
			raise TypeError(None, "Current type is wrong.")
		else:
			return left

	def find_type(self, cursor, name_list):
		# Recursive function for finding type
		def helper_function(cur):
			for name in name_list:
				if cur.data[0] == name:
					return cur, name
			if not cur.children:
				raise TypeError(cur, "Target type not found.")
			else:
				return helper_function(cur.children[0])

		# Check invalid attributes
		if not name_list or not cursor:
			raise TypeError(cursor, "Attributes are empty.")
		return helper_function(cursor)

	def lookup(self, name):
		# TODO : Implement lookup
		pass

	def lookup_array(self, name):
		# TODO : Implement lookup for array
		pass

	def lookup_function(self, name):
		# TODO : Implement lookup for function
		pass

	def type_check(self, cursor):
		# AST type of current cursor
		cursor_type = cursor.type

		if cursor_type == 'ICONST':
			return Type('int')

		elif cursor_type == 'FCONST':
			return Type('float')

		elif cursor_type == 'CCONST':
			return Type('char')

		elif cursor_type == 'ID':
			return self.lookup(cursor.get_value())

		elif cursor_type == 'STR_LITER':
			return Type('string')

		elif cursor_type == 'ARRAY':
			return self.lookup_array(cursor.children[0], cursor.children[1])

		elif cursor_type == 'FUNCTION':
			return self.lookup_function(cursor.children[0], cursor.children[1])

		elif cursor_type == 'POSTINC':
			return self.type_check(cursor.get_value())

		elif cursor_type == 'POSTDEC':
			return self.type_check(cursor.get_value())

		elif cursor_type == 'ARG_EXPR_LIST':
			# TODO
			pass

		elif cursor_type == 'PREINC' or cursor_type == 'PREDEC':
			return self.type_check(cursor.children[0])
		
		elif cursor_type == 'UNARY':
			if cursor.children[0].get_value() == '*':
				return Type('pointer', children = [self.type_check(cursor.children[1])])
			else:
				return self.type_check(cursor.children[1])

		elif cursor_type == 'SIZEOF':
			return Type('int')

		elif cursor_type == 'CAST':
			# TODO
			pass

		elif cursor_type == 'MUL_EXPR' or cursor_type == 'ADD_EXPR':
			return self.binary_same(self.type_check(cursor.children[0]), self.type_check(cursor.children[1]))

		elif cursor_type == 'SHIFT_EXPR':
			self.type_check(cursor.children[1])
			return self.type_check(cursor.children[0])

		elif cursor_type == 'REL_EXPR' or cursor_type == 'EQ_EXPR':
			self.binary_same(self.type_check(cursor.children[0]), self.type_check(cursor.children[1]))
			return Type('int')

		elif cursor_type == 'AND_EXPR' or cursor_type == 'XOR_EXPR' or cursor_type == 'OR_EXPR' or cursor_type == 'L_AND_EXPR' or cursor_type == 'L_OR_EXPR':
			self.binary_same(self.type_check(cursor.children[1]), Type('int'))
			self.binary_same(self.type_check(cursor.children[0]), Type('int'))
			return Type('int')

		elif cursor_type == 'TERNARY':
			self.binary_same(self.type_check(cursor.children[0]), Type('int'))
			return self.binary_same(self.type_check(cursor.children[1]), self.type_check(cursor.children[2]))

		elif cursor_type == 'ASSIGN_EXPR':
			self.binary_same(self.type_check(cursor.children[0]), self.type_check(cursor.children[1]))
			return None

		elif cursor_type == 'EXPR':
			prec_type = self.type_check(cursor.children[0])
			post_type = self.type_check(cursor.children[1])
			if not post_type:
				return prec_type
			else:
				post_type

		else:
			pass


	def type_convert(self, node):
		pass

# Open the source code
f = open("../test/mandatory_example.c", 'r')
s = f.read()
f.close()

# Get tokens from lexical_analyzer
lexer = lexical_analyzer.lexical_analyzer
lexer.input(s)
# while True:
# 	tok = lexer.token()
# 	if not tok: 
#   		break
# 	print(tok)

# Get AST from syntax analyzer
parser = syntax_analyzer.parser
ast = parser.parse(s, lexer = lexer)

# Print out all AST nodes
def print_ast(cursor, depth):
	indent = " " * depth
	print(f"{indent}{cursor.type}")
	for child in cursor.children:
		print_ast(child, depth + 1)

if ast:
	print_ast(ast, 0)