# ----------------------------------------------------------------------
# semantic_analyzer.py
#
# A semantic analyzer for ANSI C.
# ----------------------------------------------------------------------

import sys
import lexical_analyzer
import syntax_analyzer
import symtab
import node

# Basic class for type
class Type:
	"""
    Attributes:
        type -- type of current node
        input_type -- input type when it is function
        output_type -- output type when it is function
    """
	def __init__(self, current_type, input_type = None, output_type = None, pointer = 0, children = None):
		self.type = current_type
		self.input_type = input_type
		self.output_type = output_type
		self.pointer = pointer
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
    def __init__(self, message, lineno):
        self.message = message
        self.lineno = lineno

# Class for semantic analyzer
class semantic_analyzer:
	def __init__(self, ast, symtab):
		# Cursor for original AST, symbol table
		self.ast = ast
		self.cursor = ast
		self.symtab = symtab
		self.lineno = 0

	def binary_compat(self, src, dest, line, fixed = False):
		# Check two types are compatible (i.e. int and float)
		src_type = self.type_check(src)
		dest_type = self.type_check(dest)

		if not src_type or not dest_type:
			raise TypeError("Empty attributes", line)
		elif src_type.pointer != dest_type.pointer:
			raise TypeError("Wrong dereferencing type", line)

		import copy
		if src_type.type == dest_type.type:
			return src_type

		elif src_type.type == 'int' and dest_type.type == 'float':
			child_node = copy.deepcopy(src)
			type_spec_node = node.Node('TYPE_SPEC', 'float', line)
			spec_qual_node = node.Node('SPEC_QUAL', None, line, [type_spec_node])
			type_name_node = node.Node('TYPE_NAME', None, line, [spec_qual_node])
			src.type = 'CAST'
			src.set_value(None)
			src.children = [type_name_node, child_node]
			print(f'Type \'int\' has been automatically casted to \'float\' at line {line}')
			return dest_type

		elif src_type.type == 'float' and dest_type.type == 'int' and fixed:
			child_node = copy.deepcopy(src)
			type_spec_node = node.Node('TYPE_SPEC', 'int', line)
			spec_qual_node = node.Node('SPEC_QUAL', None, line, [type_spec_node])
			type_name_node = node.Node('TYPE_NAME', None, line, [spec_qual_node])
			src.type = 'CAST'
			src.set_value(None)
			src.children = [type_name_node, child_node]
			print(f'Type \'float\' has been automatically casted to \'int\' at line {line}')
			return dest_type

		elif src_type.type == 'float' and dest_type.type == 'int' and not fixed:
			child_node = copy.deepcopy(dest)
			type_spec_node = node.Node('TYPE_SPEC', 'float', line)
			spec_qual_node = node.Node('SPEC_QUAL', None, line, [type_spec_node])
			type_name_node = node.Node('TYPE_NAME', None, line, [spec_qual_node])
			dest.type = 'CAST'
			dest.set_value(None)
			dest.children = [type_name_node, child_node]
			print(f'Type \'int\' has been automatically casted to \'float\' at line {line}')
			return src_type

		else:
			raise TypeError("Different type", line)

	def binary_same(self, left, right, line):
		# Check two types are same 
		if left.type != right.type or left.pointer != right.pointer:
			raise TypeError("Different type", line)
		else:
			return left

	def find_type(self, cursor, name_list, line):
		# Recursive function for finding type
		def helper_function(cur):
			for name in name_list:
				if cur.data[0] == name:
					return cur, name
			if not cur.children:
				raise TypeError("Cannot find type", line)
			else:
				return helper_function(cur.children[0])

		# Check invalid attributes
		if not name_list or not cursor:
			raise TypeError("Empty attributes", line)
		return helper_function(cursor)

	def insert_symbol(self, spec_type, cursor, line):
		# Insert symbol
		index = 0

		import copy
		result_type = copy.deepcopy(spec_type)

		if len(cursor.children) == 2:
			index = 1
			result_type.pointer = len(cursor.children[0].children)

		if cursor.children[index].type == 'ID':
			self.symtab.insert(symtab.SymTabEntry(cursor.children[index].get_value(), result_type))
		
		elif cursor.children[index].type == 'ARR_DECL':
			result_type.pointer += 1
			self.binary_compat(cursor.children[index].children[1], Type('int'), line, True)
			self.symtab.insert(symtab.SymTabEntry(cursor.children[index].children[0].get_value(), result_type))

	def lookup(self, name, line):
		try:
			lookup_type = self.symtab.get(name)
		except:
			raise TypeError('Free identifier', line)

		if not lookup_type:
			raise TypeError('Free identifier', line)
		else:
			return lookup_type.type

	def lookup_array(self, array_node, id_node, line):
		self.binary_compat(id_node, Type('int'), line, True)
		name = array_node.get_value().get_value()

		try:
			lookup_type = self.symtab.get(name)
		except:
			raise TypeError('Free identifier', line)

		if not lookup_type:
			raise TypeError('Free identifier', line)

		import copy
		lookup_type = copy.deepcopy(lookup_type.type)

		if lookup_type.type == 'function' or lookup_type.pointer < 1:
			raise TypeError('Undefined type', line)
		else:
			lookup_type.pointer -= 1
			return lookup_type

	def lookup_function(self, function_node, arg_node, line):
		name = function_node.get_value().get_value()
		if name == 'printf':
			return None

		try:
			lookup_type = self.symtab.get(name)
		except:
			raise TypeError('Free identifier', line)

		if not lookup_type:
			raise TypeError('Free identifier', line)
		lookup_type = lookup_type.type

		if lookup_type.type != 'function' or len(lookup_type.input_type) != len(arg_node.children):
			raise TypeError('Undefined type', line)
		else:
			for i in range(len(arg_node.children)):
				self.binary_compat(arg_node.children[i], lookup_type.input_type[i], line, True)
		
		return lookup_type.output_type

	def type_check(self, cursor):
		# Omit the base cases
		if not cursor:
			return None
		elif isinstance(cursor, Type):
			return cursor

		# AST type of current cursor
		cursor_type = cursor.type
		self.lineno = cursor.lineno

		if cursor_type == 'ICONST':
			return Type('int')

		elif cursor_type == 'FCONST':
			return Type('float')

		elif cursor_type == 'CCONST':
			return Type('char')

		elif cursor_type == 'ID':
			return self.lookup(cursor.get_value(), self.lineno)

		elif cursor_type == 'STR_LITER':
			return Type('string')

		elif cursor_type == 'ARRAY':
			return self.lookup_array(cursor.children[0], cursor.children[1], self.lineno)

		elif cursor_type == 'FUNCTION':
			return self.lookup_function(cursor.children[0], cursor.children[1].get_value(), self.lineno)

		elif cursor_type == 'INDEX':
			return self.type_check(cursor.get_value())

		elif cursor_type == 'POSTINC':
			return self.type_check(cursor.get_value())

		elif cursor_type == 'POSTDEC':
			return self.type_check(cursor.get_value())

		elif cursor_type == 'ARG_EXPR_LIST':
			type_list = []
			for child in cursor.children:
				type_list.append(self.type_check(child))
			return Type('arg_list', None, children = type_list)

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
			return self.type_check(cursor.children[0].children[0])

		elif cursor_type == 'MUL_EXPR' or cursor_type == 'ADD_EXPR':
			return self.binary_compat(cursor.children[0], cursor.children[1], self.lineno)

		elif cursor_type == 'SHIFT_EXPR':
			self.type_check(cursor.children[1])
			return self.type_check(cursor.children[0])

		elif cursor_type == 'REL_EXPR' or cursor_type == 'EQ_EXPR':
			self.binary_compat(cursor.children[0], cursor.children[1], self.lineno)
			return Type('int')

		elif cursor_type == 'AND_EXPR' or cursor_type == 'XOR_EXPR' or cursor_type == 'OR_EXPR' or cursor_type == 'L_AND_EXPR' or cursor_type == 'L_OR_EXPR':
			self.binary_compat(cursor.children[1], Type('int'), self.lineno, True)
			self.binary_compat(cursor.children[0], Type('int'), self.lineno, True)
			return Type('int')

		elif cursor_type == 'TERNARY':
			self.binary_compat(cursor.children[0], Type('int'), self.lineno, True)
			return self.binary_compat(cursor.children[1], cursor.children[2], self.lineno)

		elif cursor_type == 'ASSIGN_EXPR':
			self.binary_compat(cursor.children[1], cursor.children[0], self.lineno, True)
			return None

		elif cursor_type == 'EXPR':
			prec_type = self.type_check(cursor.children[0])
			post_type = self.type_check(cursor.children[1])
			if not post_type:
				return prec_type
			else:
				return post_type

		elif cursor_type == 'CONST_EXP':
			return  self.type_check(cursor.children[0])

		elif cursor_type == 'DECLARATION':
			if len(cursor.children) == 2:
				spec_type = self.type_check(cursor.children[0])
				init_type = self.type_check(cursor.children[1])

				if spec_type and init_type:
					for init_child in init_type.children:
						if init_child.type:
							self.binary_compat(cursor.children[1], cursor.children[0], self.lineno, True)
						self.insert_symbol(spec_type, init_child.children[0], self.lineno)

			return None

		elif cursor_type == 'DECL_SPEC_LIST':
			spec_type = None
			for child in cursor.children:
				if child.type == 'TYPE_SPEC':
					spec_type = self.type_check(child)
			return spec_type

		elif cursor_type == 'INIT_DECL_LIST':
			type_list = []
			for child in cursor.children:
				type_list.append(self.type_check(child))
			return Type(None, None, children = type_list)

		elif cursor_type == 'DECL_W/O_INIT':
			return Type(None, None, children = [cursor.children[0]])

		elif cursor_type == 'DECL_W_INIT':
			init_type = self.type_check(cursor.children[1])
			return Type(init_type, None, children = [cursor.children[0]])

		elif cursor_type == 'TYPE_SPEC':
			return Type(cursor.get_value())

		elif cursor_type == 'SPEC_QUAL':
			if len(cursor.children) == 1:
				return Type(cursor.children[0].get_value())
			return None

		elif cursor_type == 'DECL':
			if len(cursor.children) == 1:
				child_type = None
				if cursor.children[0].type == 'ID':
					child_type = Type('id', cursor.children[0].get_value())
				
				elif cursor.children[0].type == 'ARR_DECL':
					child_type = Type('array', cursor.children[0].children[0].get_value())
					self.binary_compat(cursor.children[0].children[1], Type('int'), self.lineno, True)

				else:
					raise TypeError('Different type', self.lineno)
				
				return child_type
			
			else:
				child_type = None
				if cursor.children[1].type == 'ID':
					child_type = Type('id', cursor.children[1].get_value())
				
				elif cursor.children[1].type == 'ARR_DECL':
					child_type = Type('array', cursor.children[1].children[0].get_value())
					self.binary_compat(cursor.children[1].children[1], Type('int'), self.lineno, True)

				if not child_type:
					raise TypeError('Different type', self.lineno)
				
				if isinstance(child_type, Type):
					child_type.pointer = len(cursor.children[0].children)

				return child_type

		elif cursor_type == 'INIT':
			self.type_check(cursor.children[0])
			return None

		elif cursor_type == 'INIT_LIST':
			for child in cursor.children:
				self.type_check(child)
			return None

		elif cursor_type == 'LABEL':
			return self.type_check(cursor.get_value())

		elif cursor_type == 'CASE':
			return Type('case', None, children = [self.type_check(cursor.children[0]), self.type_check(cursor.get_value())])

		elif cursor_type == 'DEFAULT':
			return self.type_check(cursor.get_value())

		elif cursor_type == 'COMP_STMT':
			self.symtab.insert_block_table(symtab.SymTabBlock(None))

			result_type = None
			if len(cursor.children) == 2:
				self.type_check(cursor.children[0])
				result_type = self.type_check(cursor.children[1])
			elif len(cursor.children) == 1:
				result_type = self.type_check(cursor.children[0])

			self.symtab.remove_block_table()
			return result_type

		elif cursor_type == 'DECLARATION_LIST':
			for child in cursor.children:
				self.type_check(child)
			return None

		elif cursor_type == 'STMT_LIST':
			child_type_list = []
			for child in cursor.children:
				child_type = self.type_check(child)
				if not child_type:
					continue
				if child_type.type == 'stmt_list':
					child_type_list += child_type.children
				else:
					child_type_list.append(child_type)
			return Type('stmt_list', None, children = child_type_list)

		elif cursor_type == 'IF' or cursor_type == 'WHILE' or cursor_type == 'DO_WHILE':
			self.binary_compat(cursor.children[0], Type('int'), self.lineno, True)
			child_type_list = []
			for child in cursor.children:
				child_type = self.type_check(child)
				if child_type.type == 'stmt_list':
					child_type_list += child_type.children
				else:
					child_type_list.append(child_type)
			return Type('stmt_list', None, children = child_type_list)

		elif cursor_type == 'SWITCH':
			switch_type = self.type_check(cursor.children[0])
			case_type = self.type_check(cursor.children[1])

			def case_type_check(cur_type, result):
				if cur_type.type == 'case':
					self.binary_same(cur_type.children[0], switch_type, self.lineno)
					return case_type_check(cur_type.children[1], result)
				elif cur_type.type == 'stmt_list':
					for child in cur_type.children:
						result.append(case_type_check(child))
					return result
				else:
					result.append(cur_type)
					return result

			child_type_list = case_type_check(case_type, [])
			return Type('stmt_list', None, children = child_type_list)

		elif cursor_type == 'FOR':
			for i in range(len(cursor.children)):
				if cursor.children[i].type != 'EXPR_OPT':
					self.type_check(cursor.children[i])
					if i == 1:
						self.binary_compat(cursor.children[i], Type('int'), self.lineno, True)
			return self.type_check(cursor.get_value())

		elif cursor_type == 'RETURN':
			if not cursor.children[0]:
				return Type('void')
			return self.type_check(cursor.children[0])

		elif cursor_type == 'TRSL_UNIT':
			self.symtab.insert_block_table(symtab.SymTabBlock(None))

			for child in cursor.children:
				self.type_check(child)

			self.symtab.remove_block_table()
			return None

		elif cursor_type == 'FUNC_DEF':
			return_type = self.type_check(cursor.children[0])
			param_environment = {}

			if cursor.children[1].type == 'DECL' and cursor.children[1].children[0].type == 'FUN_DECL':
				function_node = cursor.children[1].children[0]
				function_name = function_node.children[0].get_value()

				arg_list = []
				if len(function_node.children) == 2:
					for param in function_node.children[1].children:
						if len(param.children) == 2:
							param_type = self.type_check(param.children[0])
							id_type = self.type_check(param.children[1])
							param_type.pointer = id_type.pointer
							arg_list.append(param_type)
							param_environment[id_type.input_type] = param_type

				function_type = Type('function', input_type = arg_list, output_type = return_type)
				self.symtab.insert(symtab.SymTabEntry(function_name, function_type))

			if cursor.children[-1].type == 'COMP_STMT':
				
				def stmt_type_check(cur_type):
					if not cur_type:
						return 
					elif cur_type.type == 'stmt_list':
						for child in cur_type.children:
							stmt_type_check(child)
					else:
						self.binary_same(cur_type, return_type, self.lineno)
						return
				
				self.symtab.insert_block_table(symtab.SymTabBlock(None))
				for key in param_environment:
					self.symtab.insert(symtab.SymTabEntry(key, param_environment[key]))

				stmt_type_check(self.type_check(cursor.children[-1]))
				self.symtab.remove_block_table()

			return None

		else:
			raise TypeError('Undefined type', self.lineno)

	def check(self):
		self.type_check(self.cursor)
		return self.cursor

# Open the source code
f = open("../test/mandatory_example.c", 'r')
s = f.read()
f.close()

# Get tokens from lexical_analyzer
lexer = lexical_analyzer.lexical_analyzer

# Get AST from syntax analyzer
parser = syntax_analyzer.parser
ast = parser.parse(s, lexer = lexer)

# Initialize semantic analyer
semantic_analyzer = semantic_analyzer(ast, symtab.SymTab())
checked_ast = semantic_analyzer.check()

# Print out all AST nodes
def print_ast(cursor, depth):
	indent = " " * depth
	print(f"{indent}{cursor.type} {cursor.value}")
	if isinstance(cursor.value, node.Node):
		print_ast(cursor.value, depth + 1)
	if not cursor.children:
		return
	for child in cursor.children:
		print_ast(child, depth + 1)

# Check
# if checked_ast:
# 	print_ast(checked_ast, 0)