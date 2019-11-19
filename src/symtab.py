class SymTabEntry:
    '''
    This class is entry for symbol table.
    id denotes name of variable.
    type denotes type and other properties of variable.
    assigned denotes whether it is assigned or not. It can be only true when used by interpreter.
    '''
    def __init__(self, id: str, type):
        self.id = id
        self.type = type
        self.assigned = False

    '''
    This function checks whether two entry has same type.
    '''
    def type_eq(self, other):
        raise NotImplementedError


class SymTabBlock:
    '''
    This is a symbol table block. It works as dict.
    '''
    def __init__(self, prev, next = None):
        self.prev = prev
        if next is None:
            self.next = []
        self.table = {}

    def insert(self, symbol):
        if symbol.id in self.table.keys():
            # TODO : Need to implement (maybe try-except?)
            pass
        else:
            self.table[symbol.id] = symbol

    def remove(self, id):
        if id not in self.table.keys():
            # TODO : Need to implement (maybe try-except?)
            pass
        else:
            self.table.pop(id)

    def get(self, id):
        try:
            return self.table[id]
        except KeyError:
            # TODO : Need to implement
            pass


class SymTab:
    def __init__(self):
        global_table = SymTabBlock(None)
        self.cur = global_table

    def insert_block_table(self, block_table):
        self.cur.next.append(block_table)
        block_table.prev = self.cur
        self.cur = block_table

    def insert(self, symbol):
        self.cur.insert(symbol)

    def remove(self, id):
        self.cur.remove(id)

    def get(self, id):
        table = self.cur
        while table != None:
            entry = table.get(id)
            if entry != None:
                table = table.prev
            else:
                return entry
        return None

    def rise(self):
        if self.cur.prev is None:
            raise RuntimeError("This is root block")
        self.cur = self.cur.prev
