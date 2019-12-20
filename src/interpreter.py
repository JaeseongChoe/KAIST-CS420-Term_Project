# -----------------------------------------------------------------------------
# interpreter.py
#
# An interpreter for ANSI C (C89 / C90).
# -----------------------------------------------------------------------------

import node
import symtab
import lexical_analyzer
import syntax_analyzer
import semantic_analyzer
import intermediate_code_generator
import symtab

class RuntimeError(Exception):
    """Base class for exceptions in Interpreter

    Attributes:
        expr -- input expression in which the error occurred
        mgs -- explanation of the error
    """

    def __init__(self, msg, lineno):
        print("Run-time error : line " + str(lineno))
        self.msg = msg + " at " + str(lineno) 

class interpreter_class:

    def __init__(self, ast, size):
        self.ast = ast
        self.size = size
        self.ic_generator = intermediate_code_generator.intermediate_code_generator()
        self.ic_output = []
        self.ic_generator.IRgenerate(self.ast, self.ic_output.append)
        self.gototab = self.ic_generator.gototab
        self.functab = self.ic_generator.functab
        self.linetab = self.ic_generator.linetab
        self.symtab = symtab.SymTab()
        self.varlist = []
        self.gotolist = dict()
        for i in range(len(self.ic_output)):
            if self.ic_output[i].split()[0][0] == 'l':
                self.gotolist[self.ic_output[i].split()[0]] = i + 1
        self.memory = dict()
        self.history = dict()
        self.paramlist = []
        self.ret_line = None
        self.ret_addr = None
        self.ret_val = None
        self.ret_symtab = self.symtab
        self.global_symtab = [None] * 32
        self.scope_level = 0
        self.code_line = 0
        self.pc = 0
        for i in range(len(self.ic_output)):
            if self.ic_output[i].split()[0] == "start":
                self.pc = i + 1
                self.pc = self.gotolist[self.ic_output[self.pc].split()[1]]
                self.code_line = self.functab["main"][1]

    def is_type(self, str, type):
        try:
            type(str)
            return True
        except ValueError:
            return False

    def index_parser(self, index):
        if self.is_type(index, int):
            return int(index)
        elif self.is_type(index, float):
            return int(float(index))
        elif self.isalpha(index[0]):
            return self.memory[self.symtab.get(index).type]
        else:
            raise RuntimeError("Index format is wrong", self.code_line)

    def find_line(self, pc):
        current_pc = pc
        ir_line = self.ic_output[current_pc].split()
        while ir_line[0][0] == "<" or ir_line[0][0] == "l" or ir_line[0] == "start":
            current_pc += 1
            ir_line = self.ic_output[current_pc].split()
        if current_pc >= len(self.ic_output):
            return self.linetab[pc] - 1
        return self.linetab[current_pc] - 1

    def interp(self, target_line):
        # When program counter is out of bound
        if self.pc >= len(self.ic_output):
            raise RuntimeError("Program counter out of bound", self.code_line)

        # Interpret until it meets target line
        while self.code_line < target_line:
            self.code_line += 1

            while self.linetab[self.pc] <= self.code_line: 
                current_line = self.ic_output[self.pc].split()

                if current_line[0] == "RET":
                    if len(current_line) >= 2:
                        src_addr = current_line[1]
                        self.ret_val = self.memory[src_addr]
                    self.pc = self.ret_addr
                    self.code_line = self.ret_line
                    self.symtab = self.ret_symtab
                    if self.scope_level > 0:
                        self.scope_level -= 1
                    return

                elif current_line[0] == "PARAM":
                    src_addr = current_line[1]
                    self.paramlist.append(self.memory[src_addr])

                elif current_line[0] == "GOTO":
                    branch_addr = current_line[1]
                    self.pc = self.gotolist[branch_addr]
                    self.code_line = self.find_line(self.pc)
                    self.interp(target_line)
                    return

                elif current_line[0] == "BFALSE":
                    branch_addr = current_line[1]
                    src_addr = current_line[2]
                    if self.memory[src_addr] == 0:
                        self.pc = self.gotolist[branch_addr]
                        self.code_line = self.find_line(self.pc)
                        self.interp(target_line)
                        return

                elif current_line[0] == "BTRUE":
                    branch_addr = current_line[1]
                    src_addr = current_line[2]
                    if self.memory[src_addr] == 1:
                        self.pc = self.gotolist[branch_addr]
                        self.code_line = self.find_line(self.pc)
                        self.interp(target_line)
                        return

                elif current_line[0] == "<SCOPE>":
                    self.symtab.insert_block_table(symtab.SymTabBlock(None))

                elif current_line[0] == "<\\SCOPE>":
                    self.symtab.remove_block_table()

                elif current_line[0][0] == 'r':
                    if current_line[1] == '=':
                        dest_addr = current_line[0]
                        src_value = None
                        if current_line[2][0] == 'r':
                            if len(current_line) == 4:
                                unary_value = self.memory[current_line[3]]
                                if current_line[2] == '&':
                                    src_value = int(current_line[3][1:])
                                elif current_line[2] == '*':
                                    src_value = self.memory["r" + str(unary_value)]
                                elif current_line[2] == '+':
                                    src_value = + unary_value
                                elif current_line[2] == '-':
                                    src_value = - unary_value
                                elif current_line[2] == '!':
                                    src_value = not unary_value
                                elif current_line[2] == '~':
                                    src_value = ~ unary_value
                                else:
                                    raise RuntimeError("Unknown unary operator", self.code_line)
                            elif len(current_line) > 4:
                                lhs_value = self.memory[current_line[2]]
                                rhs_value = self.memory[current_line[4]]
                                if current_line[3] == '[':
                                    src_value = lhs_value[rhs_value]
                                elif current_line[3] == '*':
                                    src_value = lhs_value * rhs_value
                                elif current_line[3] == '/':
                                    src_value = lhs_value / rhs_value
                                elif current_line[3] == '+':
                                    src_value = lhs_value + rhs_value
                                elif current_line[3] == '-':
                                    src_value = lhs_value - rhs_value
                                elif current_line[3] == '>>':
                                    src_value = lhs_value >> rhs_value
                                elif current_line[3] == '<<':
                                    src_value = lhs_value << rhs_value
                                elif current_line[3] == '>':
                                    src_value = int(lhs_value > rhs_value)
                                elif current_line[3] == '<':
                                    src_value = int(lhs_value < rhs_value)
                                elif current_line[3] == '>=':
                                    src_value = int(lhs_value >= rhs_value)
                                elif current_line[3] == '<=':
                                    src_value = int(lhs_value <= rhs_value)
                                elif current_line[3] == '==':
                                    src_value = int(lhs_value == rhs_value)
                                elif current_line[3] == '&':
                                    src_value = int(lhs_value & rhs_value)
                                elif current_line[3] == '^':
                                    src_value = int(lhs_value ^ rhs_value)
                                elif current_line[3] == '|':
                                    src_value = int(lhs_value | rhs_value)
                                elif current_line[3] == '&&':
                                    src_value = int(lhs_value and rhs_value)
                                elif current_line[3] == '||':
                                    src_value = int(lhs_value or rhs_value)
                                else:
                                    raise RuntimeError("Unknown binary operator", self.code_line)
                            else:
                                src_value = self.memory[current_line[2]]
                        elif current_line[2] == "CALL":
                            func_name = self.memory[current_line[3]]
                            if func_name == "printf":
                                if isinstance(self.paramlist[0], str):
                                    str_literal = self.paramlist[0]
                                    if len(self.paramlist) > 1:
                                        str_param_list = []
                                        for i in range(len(str_literal)):
                                            if str_literal[i] == '%' and i < len(str_literal) - 1:
                                                str_param_list.append(str_literal[i + 1])
                                        if len(str_param_list) != len(self.paramlist) - 1:
                                            raise RuntimeError("Wrong parameters for printf", self.code_line)
                                        for i in range(len(str_param_list)):
                                            if str_param_list[i] == 'd':
                                                print(int(self.paramlist[i + 1]))
                                            elif str_param_list[i] == 'f':
                                                print(float(self.paramlist[i + 1]))
                                            else:
                                                raise RuntimeError("Unknown string literal", self.code_line)
                                    else:
                                    	result_str_list = str_literal.split("\\n")
                                    	for i in range(len(result_str_list)):
                                    		if i == len(result_str_list) - 1:
                                    			print(result_str_list[i], end = "")
                                    		else:
                                    			print(result_str_list[i])
                                else:
                                    try:
                                        print(self.paramlist[0])
                                    except:
                                        raise RuntimeError("Unknown string literal", self.code_line)
                                self.paramlist = []
                            else:
                                try:
                                    param_list = self.functab[func_name][0]
                                    func_line = self.functab[func_name][1]
                                    if len(self.paramlist) != int(current_line[4]):
                                        raise RuntimeError("Wrong parameters for function call", self.code_line)
                                except:
                                    raise RuntimeError("Wrong function call", self.code_line)
                                self.ret_line = self.code_line
                                self.ret_addr = self.pc
                                self.ret_symtab = self.symtab
                                self.symtab = symtab.SymTab()
                                self.scope_level += 1
                                self.pc = self.gototab[func_name]
                                self.code_line = func_line
                                for i in range(len(param_list)):
                                    self.symtab.insert(symtab.SymTabEntry(param_list[i][0], param_list[i][1]))
                                    self.varlist.append(param_list[i][1])
                                    self.memory[param_list[i][1]] = self.paramlist[i]
                                    self.history[param_list[i][1]] = [[func_line, self.paramlist[i]]]
                                import sys
                                self.interp(sys.maxsize)
                                src_value = self.ret_val
                                self.paramlist = []
                        elif current_line[2] == "CAST":
                            cast_type = current_line[3]
                            src_before_value = self.memory[current_line[4]]
                            if cast_type == "int":
                                src_value = int(src_before_value)
                            elif cast_type == "float":
                                src_value = float(src_before_value)
                            elif cast_type == "char":
                                src_value = chr(int(src_before_value))
                            else:
                                src_value = src_before_value
                        elif self.is_type(current_line[2], int):
                            src_value = int(current_line[2])
                        elif self.is_type(current_line[2], float):
                            src_value = float(current_line[2])
                        elif current_line[2][0] == '\'':
                            src_value = current_line[2][1:-1]
                        elif current_line[2][0] == '\"':
                            str_value = ""
                            for i in range(2, len(current_line)):
                                str_value += current_line[i] + " "
                            src_value = str_value[1:-2]
                        elif current_line[2][0].isalpha():
                            src_value = current_line[2]
                        self.memory[dest_addr] = src_value
                        if dest_addr in self.varlist:
                            self.history[dest_addr].append([self.code_line, src_value])
                    elif current_line[1] == ":=":
                        dest_addr = current_line[0]
                        self.symtab.insert(symtab.SymTabEntry(current_line[2], dest_addr))
                        self.varlist.append(dest_addr)
                        if len(current_line) < 4:
                            self.memory[dest_addr] = None
                            self.history[dest_addr] = [[self.code_line, None]]
                        else:
                            index = self.index_parser(current_line[4])
                            self.memory[dest_addr] = [None] * index
                            self.history[dest_addr] = [[self.code_line, [None] * index]]
                        self.global_symtab[self.scope_level] = self.symtab.cur
                    elif len(current_line) > 3 and current_line[1] == '[':
                        index = self.memory[current_line[2]]
                        dest_addr = current_line[0]
                        src_value = self.memory[current_line[5]]
                        if self.memory[dest_addr][0] == None:
                            self.memory[dest_addr] = [0] * len(self.memory[dest_addr])
                        self.memory[dest_addr][index] = src_value
                        self.history[dest_addr].append([self.code_line, self.memory[dest_addr]])
                    else:
                        raise RuntimeError("Wrong IR representation at assignment", self.code_line)

                elif not (current_line[0][0] == 'l' or current_line[0] == "start"):
                    raise RuntimeError("Wrong IR representation", self.code_line)

                self.pc += 1

    def run(self, offset):
        self.interp(self.code_line + offset)
        if self.code_line + offset >= self.size:
            self.symtab.cur = self.global_symtab[0]
            print("End of program")


# Generate AST
def preprocess(code_dir):

    # Read line number
    line_number = 0
    f = open(code_dir, 'r')
    while True:
        line = f.readline()
        if not line: break
        line_number += 1
    f.close()

    # Open the source code
    f = open(code_dir, 'r')
    s = f.read()
    f.close()

    # Get tokens from lexical_analyzer
    lexer = lexical_analyzer.lexical_analyzer

    # Get AST from syntax analyzer
    parser = syntax_analyzer.parser
    ast = parser.parse(s, lexer = lexer)

    # Initialize semantic analyzer
    type_checker = semantic_analyzer.semantic_analyzer(ast, symtab.SymTab())
    return interpreter_class(type_checker.check(), line_number)

if __name__ == "__main__":

    # Code directory
    code_dir = "../test/mandatory_example.c"

    # Start console
    instruction = """[Command List]
    \trun : execute the whole code
    \tcode [code's directory] : change the target code at [code's directory]
    \texit : terminate the interpreter
    \t\tIf you do not set your code, target code becomes ../test/mandatory_example.c in default.
    \tnext, print, trace as explained in project document"""
    print(instruction)

    # Initialize interpreter
    interpreter = preprocess(code_dir)

    while True:
        command = str(input("> "))
        command_list = command.split()
        if command_list[0] == "run":
            import sys
            interpreter.run(sys.maxsize)
            break
        elif command_list[0] == "code":
            from os import path
            if len(command_list) < 2:
                print("given input is empty")
                continue
            if not path.isfile(command_list[1]):
                print("given input is not a file")
                continue
            interpreter = preprocess(command_list[1])
        elif command_list[0] == "next":
            if len(command_list) < 2:
                interpreter.run(1)
            elif interpreter.is_type(command_list[1], int):
                interpreter.run(int(command_list[1]))
            else:
                print("Incorrect command usage : try 'next [lines]'")
        elif command_list[0] == "print":
            if len(command_list) < 2:
                print("Incorrect command usage : try 'print [variable]'")
            elif not command_list[1][0].isalpha():
            	print("Invalid typing of the variable name")
            else:
                id_input = command_list[1]
                if id_input[0] == '&':
                    id_input = id_input[1:]
                    try:
                        src_reg = interpreter.symtab.get(id_input).type
                        print(src_reg[1:])
                    except:
                        print("Invisible variable")
                if id_input[0] == '*':
                    id_input = id_input[1:]
                    try:
                        src_reg = interpreter.symtab.get(id_input).type
                        val_addr = interpreter.memory[src_reg]
                        src_addr = "r" + str(int(val_addr))
                        print_val = interpreter.memory[src_addr]
                        if print_val == None: 
                            print("N/A")
                        else:
                            print(print_val)
                    except:
                        print("Invisible variable")
                else:
                    try:
                        src_reg = interpreter.symtab.get(id_input).type
                        print_val = interpreter.memory[src_reg]
                        if print_val == None:
                            print("N/A")
                        else:
                            print(print_val)
                    except:
                        print("given identifier does not exist")
        elif command_list[0] == "trace":
            if len(command_list) < 2:
                print("Incorrect command usage : try 'trace [variable]'")
            elif not command_list[1][0].isalpha():
            	print("Invalid typing of the variable name")
            else:
                id_input = command_list[1]
                try:
                    src_reg = interpreter.symtab.get(id_input).type
                    history_list = interpreter.history[src_reg]
                    for history in history_list:
                        if not history[1]:
                            print("{} = N/A at line {}".format(id_input, history[0]))
                        elif isinstance(history[1], list) and history[1][0] == None:
                            print("{} = N/A at line {}".format(id_input, history[0]))
                        else:
                            print("{} = {} at line {}".format(id_input, history[1], history[0]))
                except:
                    print("Invisible variable")
        elif command_list[0] == "exit":
            break
        else:
            print("Unknown command")
