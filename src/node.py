class Node:
    def __init__(self, type=None, value=None, lineno=None, child_list=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.children = child_list or []

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_child(self, child, ind = None):
        if ind is None:
            self.children.append(child)
        else:
            self.children.insert(ind, child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_at(self, ind):
        return self.children.pop(ind)

    def add_children(self, child_list):
        for child in child_list:
            self.add_child(child)

    def remove_children(self, child_list):
        for child in child_list:
            self.remove_child(child)
