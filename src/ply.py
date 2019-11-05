import dataclasses
import typing

@dataclass
class node:
  line:int

@dataclass
class binary_operation(node):
  op:node
  lvalue:node
  rvalue:node

@dataclass
class array_assignment(node):
  array:node
  index:node
  value:node

@dataclass
class assignment(node):
  id:node
  value:node

@dataclass
class unary_operation(node):
  operator:node
  operand:node

@dataclass
class call(node):
  fun_name:str
  params:List[node]

@dataclass
class fun_def(node):
  fun_name:str
  params:List[(Type, str)]
  body:node

@dataclass
class array_access(node):
  array:node
  index:node

@dataclass
class printf(node):
  string:node
  others:List[node]

@dataclass
class cond_while(node):
  cond:node
  body:node

@dataclass
class cond_for(node):
  init:node
  cond:node
  body:node
  after:node

class if_then_else(node):
  cond:node
  then_body:node
  else_body:node
