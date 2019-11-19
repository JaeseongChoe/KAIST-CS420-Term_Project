class Node:
    '''
    This node forms abstract syntax tree for syntax analyzer.py.
    The data contains 4 informations, name of node, value of node(option), starting line number of subtree, ending line number of subtree.
    Type of data is either Tuple[str, Tuple[int, int]] or Tuple[str, Tuple[int, int], str] as (name_node, (start_line, end_line), value_node) where value_node is optional.

    The node is leaf node when it is token analyzed by lexical_analyzer.
    In this case, data is type of (name_node, (start_line, end_line), value_node).
    Value of name_node is name of token, start_line and end_line are both line number of that token, and value_node is token value.

    The node is internal node when it is not token.
    In this case, data is type of (name_node, (start_line, end_line)).
    Value of name_node is name of nonterminal in lhs of production rule, start_line and end_line is defined as union of start-end range of its children.
    '''
    def __init__(self, data = None, child_list = []):
        self.data = data
        self.children = []
        for child in child_list:
            self.children.append(child)

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def add_children(self, child_list):
        for child in child_list:
            self.add_child(child)

    def remove_children(self, child_list):
        for child in child_list:
            self.remove_child(child)
