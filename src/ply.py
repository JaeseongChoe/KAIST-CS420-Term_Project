import dataclasses
import typing

node = typing.NewType('node', object)

@dataclass(frozen=False)
class node:
  line:int

@dataclass(frozen=False)
class binary_operation(node):
  op:node
  lvalue:node
  rvalue:node

@dataclass(frozen=False)
class array_assignment(node):
  array:node
  index:node
  value:node

@dataclass(frozen=False)
class assignment(node):
  id:node
  value:node

@dataclass(frozen=False)
class unary_operation(node):
  operator:node
  operand:node

@dataclass(frozen=False)
class call(node):
  fun_name:str
  params:List[node] = field(default_factory = list)

@dataclass(frozen=False)
class fun_def(node):
  fun_name:str
  params:List[(Type, str)] = field(default_factory = list)
  body:node

@dataclass(frozen=False)
class array_access(node):
  array:node
  index:node

@dataclass(frozen=False)
class printf(node):
  string:node
  others:List[node] = field(default_factory = list)

@dataclass(frozen=False)
class cond_while(node):
  cond:node
  body:node

@dataclass(frozen=False)
class cond_for(node):
  init:node
  cond:node
  body:node
  after:node

@dataclass(frozen=False)
class if_then_else(node):
  cond:node
  then_body:node
  else_body:node
