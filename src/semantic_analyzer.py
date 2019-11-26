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
	def __init__(self, current_type, input_type = None, output_type = None):
		self.type = current_type
		self.input_type = input_type
		self.output_type = output_type

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
		# TODO : Check two types are equal
		if left.current_type != right.current_type:
			raise TypeError(None, "Current type is wrong.")
		else:
			return left

	def ternary_same(self, left, mid, right):
		pass

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


	def constant_check(self, cursor):
		# Check whether it is integer
		def int_check(data):
			try:
				int(data)
				return True
			except ValueError:
				return False

		# Check whether it is float
		def float_check(data):
			try:
				float(data)
				return True
			except ValueError:
				return False

		# Check whether it is character
		def char_check(data):
			if len(data) < 2:
				return False
			elif data[0] != '\'' or data[-1] != '\'':
				return False

			# In case of ''
			if len(data) == 2 and data == "\'\'":
				return True
			# In case of '\n' or anything with \
			elif len(data) == 4 and data[1] == '\\':
				return True
			# In case of default character
			elif len(data) == 3 and data[1] != '\\':
				return True
			else:
				return False

		# Take data from AST and verify
		data = cursor.data[0]
		if int_check(data):
			return Type("int")
		elif float_check(data):
			return Type("float")
		elif char_check(data):
			return Type("char")
		else:
			raise TypeError(cursor, "Constant type is undefined.")

	def expression_check(self, cursor):
		# AST type of current cursor
		name_node = cursor.data[0]
		child_node = cursor.children

		if name_node == "primary_expression":
			
			if len(child_node) == 1: 

				child_name_node = child_node[0].data[0]
				if child_name_node == "constant":
					return self.constant_check(cursor.children[0])

				elif len(child_name_node) > 1 and child_name_node[0] == '"' and child_name_node[-1] == '"':
					return Type("const char*")

				else:
					# TODO : lookup(child_name_node)
					pass

			else:
				self.expression_check(child_node[1])

		elif name_node == "unary_expression":

			if child_node[0].data[0] == "sizeof":
				return Type("int")

			elif child_node[0].data[0] == "unary_operator":
				return self.expression_check(child_node[1])

			elif child_node[0].data[0] == "++" or child_node[0] == "--":
				return self.expression_check(child_node[1])

			else:
				return self.expression_check(child_node[0])

		elif name_node == "cast_expression":

			if child_node[0].data[0] == '(':
				# TODO : Check that two types are compatible
				return Type(child_node[1].data[0])

			else:
				return self.expression_check(child_node[0])

		elif name_node == "multiplicative_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				return self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "additive_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				return self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "shift_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				return self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "relational_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are compatible
				self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))
				return Type("int")

			else:
				return self.expression_check(child_node[0])

		elif name_node == "equality_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are compatible
				self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))
				return Type("int")

			else:
				return self.expression_check(child_node[0])

		elif name_node == "and_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				return self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "exclusive_or_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				return self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "inclusive_or_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				return self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "conditional_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				self.binary_same(self.expression_check(child_node[0]), Type("int"))
				return self.binary_same(self.expression_check(child_node[2]), self.expression_check(child_node[4]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "assignment_expression":

			if len(child_node) > 1:
				# TODO : Check that two types are value
				return self.binary_same(self.expression_check(child_node[0]), self.expression_check(child_node[2]))

			else:
				return self.expression_check(child_node[0])

		elif name_node == "expression":

			if len(child_node) > 1:
				last = None
				for child in child_node:
					last = self.expression_check(child)
				return last

			else:
				return self.expression_check(child_node[0])

		elif name_node == "empty":
			return Type("void")

		else:
			return self.expression_check(child_node[0])

	def statement_check(self, cursor):
		# AST type of current cursor
		name_node = cursor.data[0]
		child_node = cursor.children

		if name_node == "jump_statement":

			if child_node[0].data[0] == "return":
				return self.expression_check(child_node[1])

			else:
				return Type("void")

		elif name_node == "iteration_statement":

			if child_node[0].data[0] == "while":
				self.binary_same(self.expression_check(child_node[2]), Type("int"))
				return self.statement_check(child_node[4])

			elif child_node[0].data[0] == "for":
				self.expression_check(child_node[2])
				self.binary_same(self.expression_check(child_node[4]), Type("int"))
				self.expression_check(child_node[6])
				return self.statement_check(child_node[8])

			elif child_node[0].data[0] == "do":
				self.binary_same(self.expression_check(child_node[4]), Type("int"))
				return self.statement_check(child_node[1])

			else:
				TypeError(cursor, "Current statement is not iteration_statement.")

		elif name_node == "selection_statement":

			if child_node[0].data[0] == "if":
				self.binary_same(self.expression_check(child_node[2]), Type("int"))

				if len(child_node) > 5:
					return [self.statement_check(child_node[4]), self.statement_check(child_node[6])]
				else:
					return self.statement_check(child_node[4])

			elif child_node[0].data[0] == "switch":
				# TODO : Check switch statement
				pass

		elif name_node == "statement_list":
			pass

	def type_check(self, cursor):
		# AST type of current cursor
		if cursor.data[0] == "statement":
			self.statement_check(cursor.children[0])

		elif cursor.data[0] == "declarator":
			pass

		else:
			self.type_check(cursor.children[0])


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
	print(f"{indent}{cursor.data[0]}")
	for child in cursor.children:
		print_ast(child, depth + 1)

print_ast(ast, 0)