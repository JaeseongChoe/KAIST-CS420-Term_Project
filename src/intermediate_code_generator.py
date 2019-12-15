# -----------------------------------------------------------------------------
# intermediate_code_generator.py
#
# An intermediate code generator for ANSI C (C89 / C90).
# -----------------------------------------------------------------------------
_CAL_EXP_SET = set(["MUL_EXPR", "ADD_EXPR", "SHIFT_EXPR",
                   "REL_EXPR", "EQ_EXPR", "AND_EXPR",
                   "XOR_EXPR", "OR_EXPR", "L_AND_EXPR",
                   "L_OR_EXPR"])
_LIST_EXP_SET = set(["DECLARATION_LIST", "STMT_LIST", "TRSL_UNIT"])

import node
import symtab
import semantic_analyzer

class intermediate_code_generator:
    
    def __init__(self):
        self.symtab = symtab.SymTab()
        self.gototab = dict()
        self.looplabelstack = list()
        self.var = self.new_var_generator()
        self.label = self.new_label_generator()
    
    def new_var_generator(self):
        y = 0
        while True:
            yield y
            y = y + 1

    def new_label_generator(self):
        l = 0
        while True:
            yield l
            l = l + 1

    def new_var(self):
        return next(self.var)

    def new_label(self):
        return next(self.label)

    def IRgenerate(self, node, output):
        '''
        This function generates intermediate code for node.
        It will generate ic for each subnodes recursively.
        Then after the job is done, with the results from each subnodes, it outputs
        ic for this node itself.
        Then it returns resulting temp_var containing result of this node.
        Ex1:
           +
          / \
        n_1 n_2

        t_1 = IRgenerate(n_1)
        t_2 = IRgenerate(n_2)
        t_3 = new_var()
        output t_3 = t_1 + t_2
        return t_3

        Ex2:
        funcall(f, a_1, a_2, ... a_n)

        t_1 = IRgenerate(f)
        for i in 1..n:
            t_i = IRgenerate(a_i)
            output param t_i
        t_3 = new_var()
        output t_3 = call t_1 n
        return t_3

        Ex3:
        IfThenElse(b, e_1, e_2)
        t_1 = IRgenerate(b)
        l_1 = new_label()
        l_2 = new_label()
        t_2 = new_var()
        output beq t_1 0 l_1
        t_3 = IRgenerate(e_1)
        output t_2 <- t_3
        output GOTO l_2
        output label l_1
        t_4 = IRgenerate(e_2)
        output t_2 <- t_4
        output label l_2
        '''
        if node.type == "ARRAY":
            reg1 = self.IRgenerate(node.children[0].get_value(), output)
            reg2 = self.IRgenerate(node.children[1].get_value(), output)
            reg_result = self.new_var()
            output("\tr{} = r{} [ r{} ]".format(reg_result, reg1, reg2))
            return reg_result
        elif node.type == "FUNCTION":
            reg1 = self.new_var()
            func_name = node.children[0].get_value().get_value()
            output("\tr{} = {}".format(reg1, func_name))
            self.IRgenerate(node.children[1].get_value(), output)
            reg_result = self.new_var()
            n = len(node.children[1].get_value().children)
            output("\tr{} = CALL r{} {}".format(reg_result, reg1, n))
            return reg_result
        elif node.type == "ID":
            return self.symtab.get(node.get_value()).type
        elif node.type == "ICONST" or node.type == "FCONST" or node.type == "CCONST" or node.type == "STR_LITER":
            reg = self.new_var()
            output("\tr{} = {}".format(reg, node.get_value()))
            return reg
        elif node.type == "POSTINC":
            reg1 = self.IRgenerate(node.get_value(), output)
            temp_reg = self.new_var()
            reg_result = self.new_var()
            output("\tr{} = r{}".format(reg_result, reg1))
            output("\tr{} = 1".format(temp_reg))
            output("\tr{} = r{} + r{}".format(reg1, reg1, temp_reg))
            return reg_result
        elif node.type == "POSTDEC":
            reg1 = self.IRgenerate(node.get_value(), output)
            temp_reg = self.new_var()
            reg_result = self.new_var()
            output("\tr{} = r{}".format(reg_result, reg1))
            output("\tr{} = 1".format(temp_reg))
            output("\tr{} = r{} - r{}".format(reg1, reg1, temp_reg))
            return reg_result
        elif node.type == "ARG_EXPR_LIST":
            for child in node.children:
                reg = self.IRgenerate(child, output)
                output("\tPARAM r{}".format(reg))
        elif node.type == "PREINC":
            reg1 = self.IRgenerate(node.children[0], output)
            temp_reg = self.new_var()
            output("\tr{} = 1".format(temp_reg))
            output("\tr{} = r{} + r{}".format(reg1, reg1, temp_reg))
            return reg1
        elif node.type == "PREDEC":
            reg1 = self.IRgenerate(node.children[0], output)
            temp_reg = self.new_var()
            output("\tr{} = 1".format(temp_reg))
            output("\tr{} = r{} - r{}".format(reg1, reg1, temp_reg))
            return reg1
        elif node.type == "UNARY":
            reg1 = self.IRgenerate(node.children[1], output)
            reg_result = self.new_var()
            output("\tr{} = {} r{}".format(reg_result, node.children[0].value, reg1))
        elif node.type == "SIZEOF":
            # TODO : differentiate two sizeof call
            pass
        elif node.type == "UNA_OP":
            raise ValueError("UNA_OP should not called in IRgenerate")
        elif node.type == "CAST":
            reg = self.IRgenerate(node.children[1], output)
            reg_result = self.new_var()
            output("\tr{} = CAST {} r{}".format(reg_result, node.children[0].children[0].children[0].get_value(), reg))
            return reg_result
        elif node.type in _CAL_EXP_SET:
            reg1 = self.IRgenerate(node.children[0], output)
            reg2 = self.IRgenerate(node.children[1], output)
            reg3 = self.new_var()
            output("\tr{} = r{} {} r{}".format(reg3, reg1, node.get_value(), reg2))
            return reg3
        elif node.type == "TERNARY":
            reg1 = self.IRgenerate(node.children[0], output)
            l1 = self.new_label()
            l2 = self.new_label()
            reg_result = self.new_var()
            output("\tBFALSE l{} r{}".format(l1, reg1))
            reg2 = self.IRgenerate(node.children[1], output)
            output("\tr{} = r{}".format(reg_result, reg2))
            output("\tGOTO l{}".format(l2))
            output("l{} : ".format(l1))
            reg3 = self.IRgenerate(node.children[2], output)
            output("\tr{} = r{}".format(reg_result, reg3))
            output("l{} : ".format(l2))
            return reg_result
        elif node.type == "ASSIGN_EXPR":
            reg1 = self.IRgenerate(node.children[0], output)
            reg2 = self.IRgenerate(node.children[1], output)
            output("\tr{} {} r{}".format(reg1, node.get_value(), reg2))
        elif node.type == "ASSIGN_OP":
            raise ValueError("ASSIGN_OP should not called in IRgenerate")
        elif node.type == "EXPR":
            reg1 = self.IRgenerate(node.children[0], output)
            reg2 = self.IRgenerate(node.children[1], output)
            return reg1 # Maybe not
        elif node.type == "DECLARATION_LIST":
            for child in node.children:
                self.IRgenerate(child, output)
        elif node.type == "DECLARATION":
            self.IRgenerate(node.children[1], output)
        elif node.type == "DECL_SPEC_LIST":
            raise ValueError("DECL_SPEC_LIST should not called in IRgenerate")
        elif node.type == "INIT_DECL_LIST":
            reg_result = []
            for line in node.children:
                reg_result.append(self.IRgenerate(line, output))
            return reg_result
        elif node.type == "DECL_W/O_INIT":
            dest_reg = self.new_var()
            index = 0
            if len(node.children[0].children) == 2:
                index = 1
            child = node.children[0].children[index]
            if child.type == "ID":
                self.symtab.insert(symtab.SymTabEntry(child.get_value(), dest_reg))
            elif child.type == "ARR_DECL":
                self.symtab.insert(symtab.SymTabEntry(child.children[0].get_value(), dest_reg))
            return dest_reg
        elif node.type == "DECL_W_INIT":
            dest_reg = self.new_var()
            src_reg = self.IRgenerate(node.children[1].children[0], output)
            index = 0
            if len(node.children[0].children) == 2:
                index = 1
            child = node.children[0].children[index]
            if child.type == "ID":
                self.symtab.insert(SymTabEntry(child.get_value(), dest_reg))
            elif child.type == "ARR_DECL":
                self.symtab.insert(SymTabEntry(child.children[0].get_value(), dest_reg))
            output("\tr{} = r{}".format(dest_reg, src_reg))
            return dest_reg
        elif node.type == "STORAGE_SPEC":
            raise ValueError("STORAGE_SPEC should not called in IRgenerate")
        elif node.type == "TYPE_SPEC":
            raise ValueError("TYPE_SPEC should not called in IRgenerate")
        elif node.type == "SPEC_QUAL":
            raise ValueError("SPEC_QUAL should not called in IRgenerate")
        elif node.type == "ENUM_LIST":
            raise ValueError("ENUM_LIST should not called in IRgenerate")
        elif node.type == "TYPE_QUAL":
            raise ValueError("TYPE_QUAL should not called in IRgenerate")
        elif node.type == "DECL":
            raise ValueError("DECL should not called in IRgenerate")
        elif node.type == "POINTER":
            raise ValueError("POINTER should not called in IRgenerate")
        elif node.type == "TYPE_QUAL_LIST":
            raise ValueError("TYPE_QUAL_LIST should not called in IRgenerate")
        elif node.type == "PARAM_LIST":
            raise ValueError("PARAM_LIST should not called in IRgenerate")
        elif node.type == "PARAM_DECLARATION":
            raise ValueError("PARAM_DECLARATION should not called in IRgenerate")
        elif node.type == "ID_LIST":
            raise ValueError("ID_LIST should not called in IRgenerate")
        elif node.type == "TYPE_NAME":
            raise ValueError("TYPE_NAME should not called in IRgenerate")
        elif node.type == "TYPEDEF_NAME":
            raise ValueError("TYPEDEF_NAME should not called in IRgenerate")
        elif node.type == "INIT":
            return self.IRgenerate(node.children[0], output)
        elif node.type == "INIT_LIST":
            for init in node.children:
                self.IRgenerate(init, output)
        elif node.type == "LABEL":
            v1 = node.get_value()
            output("l{}".format(v1))
            self.gototab[node.children[0]] = v1
            return self.IRgenerate(node.children[0], output)
        elif node.type == "CASE":
            reg1 = self.IRgenerate(node.children[0], output)
            # TODO : Check reg1 equals match value
            l_next = self.new_label()
            output("\nBNE l{} r{} r{}".format(l_next, reg_match, reg1))
            reg_result = self.IRgenerate(node.children[1], output)
            output("l{} : ".format(l_next))
        elif node.type == "DEFAULT":
            return self.IRgenerate(node.children[0], output)
        elif node.type == "STMT_LIST":
            for child in node.children:
                self.IRgenerate(child, output)
        elif node.type == "COMP_STMT":
            self.symtab.insert_block_table(symtab.SymTabBlock(None))
            for child in node.children:
                reg_result = self.IRgenerate(child, output)
            self.symtab.remove_block_table()
            return reg_result
        elif node.type in _LIST_EXP_SET:
            reg_result = 0
            for child in node.children:
                reg_result = self.IRgenerate(child, output)
            return reg_result
        elif node.type == "EXPR_STMT":
            return self.IRgenerate(node.children[0], output)
            # interpret CONST_EXP
            # If given value matches result
            # statement
            # else \tGOTO next label
        elif node.type == "IF":
            if len(node.children) == 2:
                reg1 = self.IRgenerate(node.children[0], output)
                l1 = self.new_label()
                output("\tBFALSE l{} r{}".format(l1, reg1))
                self.IRgenerate(node.children[1], output)
                output("l{} : ".format(l1))
            else:
                reg1 = self.IRgenerate(node.children[0], output)
                l1 = self.new_label()
                l2 = self.new_label()
                output("\tBFALSE l{} r{}".format(l1, reg1))
                self.IRgenerate(node.children[1], output)
                output("\tGOTO l{}".format(l2))
                output("l{} : ".format(l1))
                self.IRgenerate(node.children[2], output)
                output("l{} : ".format(l2))
        elif node.type == "SWITCH":
            reg1 = self.IRgenerate(node.children[0], output)
            TODO()
        elif node.type == "WHILE":
            l1 = self.new_label()
            l2 = self.new_label()
            self.looplabelstack.append((l1, l2))
            output("l{} : ".format(l1))
            reg1 = self.IRgenerate(node.children[0], output)
            output("\tBFALSE l{} r{}".format(l2, reg1))
            self.IRgenerate(node.children[1], output)
            output("\tGOTO l{}".format(l1))
            output("l{} : ".format(l2))
            self.looplabelstack.pop()
        elif node.type == "DO_WHILE":
            l1 = self.new_label()
            l2 = self.new_label()
            self.looplabelstack.append((l1, l2))
            output("l{} : ".format(l1))
            self.IRgenerate(node.children[0], output)
            reg1 = self.IRgenerate(node.children[1], output)
            output("\tBTRUE l{} r{}".format(l1, reg1))
            output("l{} : ".format(l2))
            self.looplabelstack.pop()
        elif node.type == "FOR":
            l1 = self.new_label()
            l2 = self.new_label()
            self.looplabelstack.append((l1, l2))
            self.IRgenerate(node.children[0], output)
            output("l{} : ".format(l1))
            reg2 = self.IRgenerate(node.children[1], output)
            output("\tBFALSE l{} r{}".format(l2, reg2))
            self.IRgenerate(node.children[3], output)
            self.IRgenerate(node.children[2], output)
            output("\tGOTO l{}".format(l1))
            output("l{} : ".format(l2))
            self.looplabelstack.pop()
        elif node.type == "\tGOTO":
            output("\tGOTO l{}".format(self.gototab[node.children[0]]))
            # Create \tGOTO table
        elif node.type == "CONTINUE":
            output("\tGOTO l{}".format(self.looplabelstack[-1][0]))
            # create loop_start_label globally
        elif node.type == "BREAK":
            output("\tGOTO l{}".format(self.looplabelstack[-1][1]))
            self.looplabelstack.pop()
            # create loop_end_label globally
        elif node.type == "RETURN":
            if len(node.children) == 1:
                reg_result = self.IRgenerate(node.children[0], output)
                output("\tRET r{}".format(reg_result))
            else:
                output("\tRET")
        elif node.type == "TRSL_UNIT":
            self.symtab.insert_block_table(symtab.SymTabBlock(None))
            for child in cursor.children:
                self.IRgenerate(child)
            self.symtab.remove_block_table()
            output("start : ")
            output("\tGOTO l{}".format(self.gototab['main']))
        elif node.type == "FUNC_DEF":
            l_func = self.new_label()
            output("l{} : ".format(l_func))
            node_func = node.children[1].children[0]
            name_func = node_func.children[0].get_value()
            self.gototab[name_func] = l_func
            self.symtab.insert_block_table(symtab.SymTabBlock(None))
            arg_list = []
            if len(node_func.children) == 2:
                for param in node_func.children[1].children:
                    if len(param.children) == 2:
                        param_name = param.children[1].children[-1].get_value()
                        dest_reg = self.new_var()
                        self.symtab.insert(symtab.SymTabEntry(param_name, dest_reg))
            result = self.IRgenerate(node.children[-1], output)
            self.symtab.remove_block_table()
            return result
        elif node.type == "EMPTY":
            pass
        elif node.type == "EXPR_OPT":
            pass


if __name__ == "__main__":
    ast = semantic_analyzer.checked_ast
    intermediate_code_generator = intermediate_code_generator()
    intermediate_code_generator.IRgenerate(ast, print)
    # file = open("output.txt", 'a')
    # intermediate_code_generator.IRgenerate(ast, file.write)
    # file.close()
