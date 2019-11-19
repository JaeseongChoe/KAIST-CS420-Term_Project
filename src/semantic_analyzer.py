# ----------------------------------------------------------------------
# semantic_analyzer.py
#
# A semantic analyzer for ANSI C.
# ----------------------------------------------------------------------

import sys
import syntax_analyzer

# Get AST from syntax analyzer
# TODO

# Class for semantic analyzer
class semantic_analyzer:
	def __init__(self, ast):
		# Cursor for original AST
		self.ast = ast

	def binary_same(self, left, right):


	def ternary_same(self, left, mid, right):


	def type_check(self, cursor):
		# AST type of current cursor
		name_node = cursor.get_data[0]

		if name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		elif name_node == "statement":

		else:


	def type_convert(self, node):


	def run(self):
