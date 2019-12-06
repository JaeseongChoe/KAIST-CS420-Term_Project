# -----------------------------------------------------------------------------
# intermediate_code_generator.py
#
# An intermediate code generator for ANSI C (C89 / C90).
# -----------------------------------------------------------------------------


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

def IRgenerate(node):
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
    TODO()
