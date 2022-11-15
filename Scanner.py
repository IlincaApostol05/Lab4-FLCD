from SymbolTable import SymbolTable
from FiniteAutomata import FiniteAutomaton
import re

reserved_words = ["for", "while", "if", "else", "SHOW", "input_number", "input_string", "@", "input_char", "elif",
                  "set_nth", "get_nth", "length","stop"]
reserved_operators = ["+", "-", "*", "/", "=", "====", "!=", "<", "<=", ">", ">=", "||", "&&", "[", "]", ";", ":", "(", ")",",","->","+="]
integer_const_verify = FiniteAutomaton("finite_automata_integer_constant.json")
const_name_verify = FiniteAutomaton("finite_automata_constant_name.json")

class PIF:
    def __init__(self):
        self.__data = []

    def __setitem__(self, key, pos):
        self.__data.append((key, pos))

    def __str__(self):
        return "\n".join(map(str, self.__data))

    def tokens(self):
        return list(map(lambda x: x[0], self.__data))

def is_constant(token):
    global integer_const_verify, const_name_verify
    if integer_const_verify.check(token) or const_name_verify.check(token):
        return True
    else:
        return re.match(r"^([0-9])", token) is not None

def is_identifier(token):
    global integer_const_verify, const_name_verify
    if integer_const_verify.check(token) or const_name_verify.check(token):
        return True
    else:
        return re.match(r'^[a-z]([a-zA-Z]|[0-9]|[-_])*$', token) is not None or re.match(r"^'.+'$", token) is not None

def scanner(file):
    pif = PIF()
    symbolTableConstants = SymbolTable()
    symbolTableIdentifiers = SymbolTable()
    with open(file) as f:
        line_index = 1
        line = f.readline()
        while line:
            #print(line)
            split = re.findall(r'`.+`|".+"|\'.\'|[:;()\[\]\.\+\-\*/=!<>%@|&\(\)]|[^:;()\s\[\]\.\+\-\*/=!<>%@|&\(\)]+', line)
            split = list(filter(lambda x: x is not None and x != '', map(lambda x: x.strip(), split)))
            #print("split",split)

            i = 0
            while i < len(split) - 1:
                if split[i] == ';' and split[i + 1] != ']':
                    print("Lexical error. Invalid token: '{}' on line {}".format(split[i+1], line_index))
                    return None
                #if split[i] == ']' and split[i + 1] != ' ':
                #    print("Lexical error. Invalid token: '{}' on line {}".format(split[i+1], line_index))
                #    return None
                if split[i] == ')' and split[i + 1] != ';':
                    print("Lexical error. Invalid token: '{}' on line {}".format(split[i+1], line_index))
                    return None
                if split[i] in ('!', '<', '>', '+', '-', '*', '/'):
                    if split[i + 1] == '=':
                        split[i] += '='
                if split[i] == '=' and split[i + 1] == '=' and split[i + 2] == '=' and split[i + 3] == '=':
                    split[i] = '===='
                    del split[i + 1]
                    del split[i+2]
                    del split[i+3]
                if split[i] == '|' and split[i + 1] == '|':
                    split[i] = '||'
                    del split[i + 1]
                if split[i] == '-' and split[i + 1] == '>':
                    split[i] = '->'
                    del split[i + 1]
                if split[i] == '&' and split[i + 1] == '&':
                    split[i] = '&&'
                    del split[i + 1]
                i += 1

            for token in split:
                #print("token:",token)
                if token in reserved_words or token in reserved_operators:
                    pif[token] = 0
                elif is_identifier(token):
                    index = symbolTableIdentifiers.add(token)
                    pif[token] = index
                elif is_constant(token):
                    index = symbolTableConstants.add(token)
                    pif[token] = index
                else:
                    print("Lexical error. Invalid token: '{}' on line {}".format(token, line_index))
                    return None
            line = f.readline()
            line_index += 1
    return symbolTableConstants,symbolTableIdentifiers, pif


if __name__ == "__main__":
        symbolTableConstants,symbolTableIdentifiers, pif = scanner("files/p1.txt")
        print("Symbol Table Constants:")
        print(symbolTableConstants, "\n")
        print("Symbol Table Identifiers:")
        print(symbolTableIdentifiers, "\n")
        print("PIF:")
        print(pif)
        with open("files/pif.out", "w+") as f:
            f.write('\n'.join(pif.tokens()))
        print("Valid program!")