# -----------------------------------------------------------------------------
# intermediate_code_generator.py
#
# An intermediate code generator for ANSI C (C89 / C90).
# -----------------------------------------------------------------------------
_CAL_EXP_SET = set("MUL_EXPR", "ADD_EXPR", "SHIFT_EXPR",
                   "REL_EXPR", "EQ_EXPR", "AND_EXPR",
                   "XOR_EXPR", "OR_EXPR", "L_AND_EXPR",
                   "L_OR_EXPR")
_LIST_EXP_SET = set("COMP_STMT", "DECLARATION_LIST", "STMT_LIST", "TRSL_UNIT")

import node
import symtab

def new_var():
    y = 0
    while True:
        yield y
        y = y + 1

def new_label():
    l = 0
    while True:
        yield l
        l = l + 1

def IRgenerate(node, output):
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
    output goto l_2
    output label l_1
    t_4 = IRgenerate(e_2)
    output t_2 <- t_4
    output label l_2
    '''
    if node.type == "ARRAY":
        reg1 = IRgenerate(node.children[0], output)
        reg2 = IRgenerate(node.children[1], output)
        reg_result = new_var()
        output("r%d = r%d [ r%d ]".format(reg_result, reg1, reg2))
        return reg_result
    elif node.type == "FUNCTION":
        reg1 = IRgenerate(node.children[0], output)
        IRgenerate(node.children[1], output)
        reg_result = new_var()
        n = len(node.children[1].children)
        output("r%d = CALL r%d %d".format(reg_result, reg1, n))
        return reg_result
    elif node.type == "POSTINC":
        reg1 = IRgenerate(node.children[0], output)
        TODO()
    elif node.type == "POSTDEC":
        TODO()
    elif node.type == "ARG_EXPR_LIST":
        TODO()
        # Store argument using
        # PARAM r%n
    elif node.type == "PREINC":
        TODO()
    elif node.type == "PREDEC":
        TODO()
    elif node.type == "UNARY":
        reg1 = IRgenerate(node.children[1], output)
        reg_result = new_var()
        output("r%d = %s r%d".format(reg_result, node.children[0].value, reg1))
    elif node.type == "SIZEOF":
        TODO("differentiate two sizeof call")
    elif node.type == "UNA_OP":
        raise ValueError("UNA_OP should not called in IRgenerate")
    elif node.type == "CAST":
        reg = IRgenerate(node.children[1], output)
        reg_result = new_var()
        output("r%d = CAST %s r%d".format(TODO(), reg))
        return reg_result
    elif node.type in _CAL_EXP_SET:
        reg1 = IRgenerate(node.children[0], output)
        reg2 = IRgenerate(node.children[1], output)
        reg3 = new_var()
        output("r%d = r%d %s r%d".format(reg3, reg1, node.get_value(), reg2))
        return reg3
    elif node.type == "TERNARY":
        reg1 = IRgenerate(node.children[0], output)
        l1 = new_label()
        l2 = new_label()
        reg_result = new_var()
        output("BFALSE l%d r%d".format(l1, reg1))
        reg2 = IRgenerate(node.children[1], output)
        output("r%d = r%d".format(reg_result, reg2))
        output("GOTO l%d".format(l2))
        output("l%d : ".format(l1))
        reg3 = IRgenerate(node.children[2], output)
        output("r%d = r%d".format(reg_result, reg3))
        output("l%d : ".format(l2))
        return reg_result
    elif node.type == "ASSIGN_EXPR":
        reg1 = IRgenerate(node.children[0])
        reg2 = IRgenerate(node.children[1])
        output("r%d %s r%d".format(reg1, node.get_value(), reg2))
    elif node.type == "ASSIGN_OP":
        raise ValueError("ASSIGN_OP should not called in IRgenerate")
    elif node.type == "EXPR":
        reg1 = IRgenerate(node.children[0])
        reg2 = IRgenerate(node.children[1])
        return reg1 # Maybe not
    elif node.type == "DECLARATION":
        TODO()
    elif node.type == "DECL_SPEC_LIST":
        TODO()
    elif node.type == "INIT_DECL_LIST":
        for line in node.children:
            IRgenerate(line)
    elif node.type == "DECL_W/O_INIT":
        TODO()
    elif node.type == "DECL_W_INIT":
        TODO()
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
        TODO()
    elif node.type == "POINTER":
        raise ValueError("POINTER should not called in IRgenerate")
    elif node.type == "TYPE_QUAL_LIST":
        raise ValueError("TYPE_QUAL_LIST should not called in IRgenerate")
    elif node.type == "PARAM_LIST":
        TODO()
    elif node.type == "PARAM_DECLARATION":
        TODO()
    elif node.type == "ID_LIST":
        TODO()
    elif node.type == "TYPE_NAME":
        raise ValueError("TYPE_NAME should not called in IRgenerate")
    elif node.type == "TYPEDEF_NAME":
        raise ValueError("TYPEDEF_NAME should not called in IRgenerate")
    elif node.type == "INIT":
        return IRgenerate(node.children[0], output)
    elif node.type == "INIT_LIST":
        for init in node.children:
            IRgenerate(init, output)
    elif node.type == "LABEL":
        output("l%s".format(node.get_value()))
        return IRgenerate(node.children[0], output)
    elif node.type == "CASE":
        reg1 = IRgenerate(node.children[0], output)
        TODO("Check reg1 equals match value")
        l_next = new_label()
        output("BNE l%d r%d r%d".format(l_next, reg_match, reg1))
        reg_result = IRgenerate(node.children[1], output)
        output("l%d : ".format(l_next))
    elif node.type == "DEFAULT":
        return IRgenerate(node.children[0], output)
    elif node.type in _LIST_EXP_SET:
        reg_result = 0
        for child in node.children:
            reg_result = IRgenerate(child, output)
        return reg_result
    elif node.type == "EXPR_STMT":
        return IRgenerate(node.children[0], output)
        # interpret CONST_EXP
        # If given value matches result
        # statement
        # else GOTO next label
    elif node.type == "IF":
        if len(node.children) == 2:
            reg1 = IRgenerate(node.children[0], output)
            l1 = new_label()
            output("BFALSE l%d r%d".format(l1, reg1))
            IRgenerate(node.children[1], output)
            output("l%d : ".format(l1))
        else:
            reg1 = IRgenerate(node.children[0], output)
            l1 = new_label()
            l2 = new_label()
            output("BFALSE l%d r%d".format(l1, reg1))
            IRgenerate(node.children[1], output)
            output("GOTO l%d".format(l2))
            output("l%d : ".format(l1))
            IRgenerate(node.children[2], output)
            output("l%d : ".format(l2))
    elif node.type == "SWITCH":
        reg1 = IRgenerate(node.children[0], output)
        TODO()
    elif node.type == "WHILE":
        l1 = new_label()
        l2 = new_label()
        output("l%d : ".format(l1))
        reg1 = IRgenerate(node.children[0], output)
        output("BFALSE l%d r%d".format(l2, reg1))
        IRgenerate(node.children[1], output)
        output("GOTO l%d".format(l1))
        output("l%d : ".format(l2))
    elif node.type == "DO_WHILE":
        l1 = new_label()
        output("l%d : ".format(l1))
        IRgenerate(node.children[0], output)
        reg1 = IRgenerate(node.children[1], output)
        output("BTRUE l%d r%d".format(l1, reg1))
    elif node.type == "FOR":
        IRgenerate(node.children[0], output)
        l1 = new_label()
        l2 = new_label()
        output("l%d : ".format(l1))
        reg2 = IRgenerate(node.children[1], output)
        output("BFALSE l%d r%d".format(l2, reg2))
        IRgenerate(node.children[3], output)
        IRgenerate(node.children[2], output)
        output("GOTO l%d".format(l1))
        output("l%d : ".format(l2))
    elif node.type == "GOTO":
        TODO()
        # Create GOTO table
    elif node.type == "CONTINUE":
        TODO()
        # create loop_start_label globally
    elif node.type == "BREAK":
        TODO()
        # create loop_end_label globally
    elif node.type == "RETURN":
        TODO()
         # ISSUE : why node value ㅠㅠㅠ
    elif node.type == "FUNC_DEF":
        TODO()
    elif node.type == "EMPTY":
        pass
    elif node.type == "EXPR_OPT":
        pass



if __name__ == "__main__":
    IRgenerate(ast, print)
    file = open("output.txt", 'a')
    IRgenerate(ast, file.write)
