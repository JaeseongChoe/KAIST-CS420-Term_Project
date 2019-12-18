SYMTAB_ERROR_DUP_DECL = "redeclaration of {} with no linkage"
SYMTAB_ERROR_UNDEF_ID = "{} undeclared"


class SymTabError(Exception):
    """Base class for exceptions in SymTab module.

    Attributes:
        expr -- input expression in which the error occurred
        mgs -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg.format(expr)


class DupDeclError(SymTabError):
    """Exception raised for duplicated declaration error."""
    pass


class UndefIdError(SymTabError):
    """Exception raised for undefined identifier error."""
    pass


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
            raise DupDeclError(id, SYMTAB_ERROR_DUP_DECL)
        else:
            self.table[symbol.id] = symbol

    def remove(self, id):
        if id not in self.table.keys():
            raise UndefIdError(id, SYMTAB_ERROR_UNDEF_ID)
        else:
            self.table.pop(id)

    def get(self, id):
        try:
            return self.table[id]
        except KeyError:
            return None


class SymTab:
    def __init__(self):
        global_table = SymTabBlock(None)
        self.cur = global_table

    def insert_block_table(self, block_table):
        self.cur.nexts.append(block_table)
        block_table.prev = self.cur
        self.cur = block_table

    def remove_block_table(self):
        self.cur = self.cur.prev

    def insert(self, symbol):
        self.cur.insert(symbol)

    def remove(self, id):
        self.cur.remove(id)

    def get(self, id):
        table = self.cur
        while table != None:
            entry = table.get(id)
            if entry == None:
                table = table.prev
            else:
                return entry
        raise UndefIdError(id, SYMTAB_ERROR_UNDEF_ID)
