class SymTabEntry:
    def __init__(self, id, type, scope):
        self.id = id
        self.type = type
        self.scope = scope


class SymTabBlock:
    def __init__(self, prev, next = None):
        self.prev = prev
        self.next = next
        self.table = {}

    def insert(self, symbol):
        if symbol.id in self.table.keys():
            # Need to implement (maybe try-except?)
            pass
        else:
            self.table[symbol.id] = symbol

    def remove(self, id):
        if not id in self.table.keys():
            # Need to implement (maybe try-except?)
            pass
        else:
            self.table.pop(id)

    def get(slef, id):
        try:
            return self.table[id]
        except KeyError:
            # Need to implement
            pass


class SymTab:
    def __init__(self):
        global_table = SymTabBlock(None)
        self.cur = global_table

    def insert_block_table(self, block_table):
        self.cur.next = block_table
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
