import dataclasses
import typing


NodeType = typing.NewType('NodeType', object)


@dataclass(frozen=False)
class Node:
    value: StringType


@dataclass(frozen=False)
class UnaOp(Node):
    operator: NodeType
    operand: NodeType


@dataclass(frozen=False)
class BinOp(Node):
    operator: NodeType
    left: NodeType
    right: NodeType


@dataclass(frozen=False)
class IfThenElse(Node):
    condition: NodeType
    then_body: NodeType
    else_body: NodeType


@dataclass(frozen=False)
class WhileLoop(Node):
    condition: NodeType
    body: NodeType


@dataclass(frozen=False)
class ForLoop(Node):
    initialization: NodeType
    condition: NodeType
    after_thought: NodeType
    body: NodeType


@dataclass(frozen=False)
class FunDef(Node):
    fun_name: str
    params: List[(Type, StringType)] = field(default_factory = list)
    body: NodeType


@dataclass(frozen=False)
class FunCall(Node):
    fun_name: StringType
    args: List[NodeType] = field(default_factory = list)


@dataclass(frozen=False)
class ArrayAssign(Node):
    id: NodeType
    index: NodeType
    value: NodeType


@dataclass(frozen=False)
class ArrayAccess(Node):
    id: NodeType
    index: NodeType


@dataclass(frozen=False)
class Block(Node):
    statements: List[NodeType] = field(default_factory = list)


@dataclass(frozen=False)
class Printf(Node):
    format_string: NodeType
    args: List[NodeType] = field(default_factory = list)
