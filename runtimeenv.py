def type_to_size(ty):
    ty_map = {"int":4, "float":4}
    TODO()

class CallStackFrame:
    '''
    This class is data class for stack frame in function call.
    '''
    def __init__(self, params, ret_add, ret_ty, bef = None):
        self.params = params or []
        self.ret_add = ret_add
        self.ret_val = None
        self.size = sum(type_to_size(i.type) for i in self.params) + type_to_size(ret_ty) + 4
        # 4 is pointer of ret_add
        # TODO : Register storing?


class Stackframe:
    '''
    This class is data class for stack frame.
    '''

    def __init__(self, locals, bef=None):
        self.locals = locals
        self.size = sum(type_to_size(i.type) for i in self.params)
        if bef is None:
            self.bef = bef
            self.start_add = 0
        else:
            self.bef = bef
            self.start_add = self.bef.start_add + self.bef.size

class RuntimeEnviroment:

    def __init__(self, global_variables, fun_table):
        self.global_frame = StackFrame(global_variables)
        self.fun_table = fun_table
