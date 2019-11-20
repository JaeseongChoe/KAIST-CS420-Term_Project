class SymTabEntry:
    def __init__(self, id, type, assigned=False):
        self.id = id
        self.type = type
        self.assigned = assigned


class SymTabBlock:
    def __init__(self, prev=None, nexts=[]):
        self.prev = prev
        self.nexts = nexts
        self.table = {}

    def insert(self, symbol):
        if symbol.id in self.table:
            # Need to implement (maybe try-except?)
            pass
        else:
            self.table[symbol.id] = symbol

    def remove(self, id):
        if id not in self.table.keys():
            # Need to implement (maybe try-except?)
            pass
        else:
            self.table.pop(id)

    def get(self, id):
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
        self.cur.nexts.append(block_table)
        block_table.prev = self.cur
        self.cur = block_table

    def remove_block_table(self):
        self.cur.prev.pop(self.cur)
        self.cur = self.cur.prev
        
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
