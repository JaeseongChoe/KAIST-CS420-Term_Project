class Node:
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
