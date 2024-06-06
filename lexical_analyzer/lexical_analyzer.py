from enum import Enum
import json


# Token types enum
class TokenType(Enum):
    END = "END"

    ERROR = "ERROR"

    BREAK = "T_BREAK"
    BOOL = "T_BOOL"
    CHAR = "T_CHAR"
    CONTINUE = "T_CONTINUE"
    FOR = "T_FOR"
    FALSE = "T_FALSE"
    IF = "T_IF"
    ELSE = "T_ELSE"
    INT = "T_INT"
    PRINT = "T_PRINT"
    RETURN = "T_RETURN"
    TRUE = "T_TRUE"
    VOID = "T_VOID"

    ASSIGN = "T_ASSIGN"
    ROP_S = "T_ROP_S"
    ROP_G = "T_ROP_G"
    ROP_SE = "T_ROP_SE"
    ROP_GE = "T_ROP_GE"
    ROP_EQ = "T_ROP_EQ"
    ROP_NE = "T_ROP_NE"

    LOP_AND = "T_LOP_AND"
    LOP_OR = "T_LOP_OR"
    LOP_NOT = "T_LOP_NOT"

    AOP_PL = "T_AOP_PL"
    AOP_MN = "T_AOP_MN"
    AOP_MP = "T_AOP_MP"
    AOP_DV = "T_AOP_DV"
    AOP_MOD = "T_AOP_MOD"

    LP = "T_LP"
    RP = "T_RP"
    LSB = "T_LSB"
    RSB = "T_RSB"
    LB = "T_LB"
    RB = "T_RB"

    COMMA = "T_COMMA"
    SEMICOLON = "T_SEMICOLON"

    DECIMAL = "T_DECIMAL"
    HEXADECIMAL = "T_HEXADECIMAL"

    ID = "T_ID"
    CHARACTER = "T_CHARACTER"
    STRING = "T_STRING"
    COMMENT = "T_COMMENT"
    WHITESPACE = "T_WHITESPACE"


#Token structure
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value


# Function to get the next token
def get_next_token(expr):
    if not expr:
        symbol_table[count].append((TokenType.END.value, 'end'))
        return Token(TokenType.END), expr

    # Check for single character tokens
    ###########################################################
    if ord(expr[0]) == ord("\t") or ord(expr[0]) == ord("\n"):
        expr = expr[1:]
        return Token(TokenType.WHITESPACE), expr
    elif expr.startswith(' '):
        expr = expr[1:]
        return Token(TokenType.WHITESPACE), expr
    ###########################################################

    elif expr[0:5] == 'break':
        expr = expr[5:]
        symbol_table[count].append((TokenType.BREAK.value, 'break'))
        lexis_list.append((TokenType.BREAK.value, 'break'))
        return Token(TokenType.BREAK), expr
    elif expr[0:4] == 'bool':
        symbol_table[count].append((TokenType.BOOL.value, 'bool'))
        lexis_list.append((TokenType.BOOL.value, 'BOOL'))
        expr = expr[4:]
        return Token(TokenType.BOOL), expr
    elif expr[0:4] == 'char':
        symbol_table[count].append((TokenType.CHAR.value, 'char'))
        lexis_list.append((TokenType.CHAR.value, 'char'))
        expr = expr[4:]
        return Token(TokenType.CHAR), expr
    elif expr[0:8] == 'continue':
        symbol_table[count].append((TokenType.CONTINUE.value, 'continue'))
        lexis_list.append((TokenType.CONTINUE.value, 'continue'))
        expr = expr[8:]
        return Token(TokenType.CONTINUE), expr
    elif expr[0:3] == 'for':
        symbol_table[count].append((TokenType.FOR.value, 'for'))
        lexis_list.append((TokenType.FOR.value, 'for'))
        expr = expr[3:]
        return Token(TokenType.FOR), expr
    elif expr[0:5] == 'false':
        symbol_table[count].append((TokenType.FALSE.value, 'false'))
        lexis_list.append((TokenType.FALSE.value, 'false'))
        expr = expr[5:]
        return Token(TokenType.FALSE), expr
    elif expr[0:2] == 'if':
        symbol_table[count].append((TokenType.IF.value, 'if'))
        lexis_list.append((TokenType.IF.value, 'if'))
        expr = expr[2:]
        return Token(TokenType.IF), expr
    elif expr[0:4] == 'else':
        symbol_table[count].append((TokenType.ELSE.value, 'else'))
        lexis_list.append((TokenType.ELSE.value, 'else'))
        expr = expr[4:]
        return Token(TokenType.ELSE), expr
    elif expr[0:3] == 'int':
        symbol_table[count].append((TokenType.INT.value, 'int'))
        lexis_list.append((TokenType.INT.value, 'int'))
        expr = expr[3:]
        return Token(TokenType.INT), expr
    elif expr[0:5] == 'print':
        symbol_table[count].append((TokenType.PRINT.value, 'print'))
        lexis_list.append((TokenType.PRINT.value, 'print'))
        expr = expr[5:]
        return Token(TokenType.PRINT), expr
    elif expr[0:6] == 'return':
        symbol_table[count].append((TokenType.RETURN.value, 'return'))
        lexis_list.append((TokenType.RETURN.value, 'return'))
        expr = expr[6:]
        return Token(TokenType.RETURN), expr
    elif expr[0:4] == 'true':
        symbol_table[count].append((TokenType.TRUE.value, 'true'))
        lexis_list.append((TokenType.TRUE.value, 'true'))
        expr = expr[4:]
        return Token(TokenType.TRUE), expr
    elif expr[0:4] == 'void':
        symbol_table[count].append((TokenType.VOID.value, 'void'))
        lexis_list.append((TokenType.VOID.value, 'void'))
        expr = expr[4:]
        return Token(TokenType.VOID), expr
    ###########################################################
    elif expr[0] == '<':
        symbol_table[count].append((TokenType.ROP_S.value, '<'))
        lexis_list.append((TokenType.ROP_S.value, '<'))
        expr = expr[1:]
        return Token(TokenType.ROP_S), expr
    elif expr[0] == '>':
        symbol_table[count].append((TokenType.ROP_G.value, '>'))
        lexis_list.append((TokenType.ROP_G.value, '>'))
        expr = expr[1:]
        return Token(TokenType.ROP_G), expr
    elif expr[0:2] == '<=':
        symbol_table[count].append((TokenType.ROP_SE.value, '<='))
        lexis_list.append((TokenType.ROP_SE.value, '<='))
        expr = expr[2:]
        return Token(TokenType.ROP_SE), expr
    elif expr[0:2] == '>=':
        symbol_table[count].append((TokenType.ROP_GE.value, '>='))
        lexis_list.append((TokenType.ROP_GE.value, '>='))
        expr = expr[2:]
        return Token(TokenType.ROP_GE), expr
    elif expr[0:2] == '==':
        symbol_table[count].append((TokenType.ROP_EQ.value, '=='))
        lexis_list.append((TokenType.ROP_EQ.value, '=='))
        expr = expr[2:]
        return Token(TokenType.ROP_EQ), expr
    elif expr[0:2] == '!=':
        symbol_table[count].append((TokenType.ROP_NE.value, '!='))
        lexis_list.append((TokenType.ROP_NE.value, '!='))
        expr = expr[2:]
        return Token(TokenType.ROP_NE), expr
    ###########################################################
    elif expr[0] == '=':
        symbol_table[count].append((TokenType.ASSIGN.value, '='))
        lexis_list.append((TokenType.ASSIGN.value, '='))
        expr = expr[1:]
        return Token(TokenType.ASSIGN), expr
    ###########################################################
    elif expr[0:2] == '&&':
        symbol_table[count].append((TokenType.LOP_AND.value, '&&'))
        lexis_list.append((TokenType.LOP_AND.value, '&&'))
        expr = expr[2:]
        return Token(TokenType.LOP_AND), expr
    elif expr[0:2] == '||':
        symbol_table[count].append((TokenType.LOP_OR.value, '||'))
        lexis_list.append((TokenType.LOP_OR.value, '||'))
        expr = expr[2:]
        return Token(TokenType.LOP_OR), expr
    elif expr[0] == '!':
        symbol_table[count].append((TokenType.LOP_NOT.value, '!'))
        lexis_list.append((TokenType.LOP_NOT.value, '!'))
        expr = expr[1:]
        return Token(TokenType.LOP_NOT), expr
    ###########################################################
    elif expr[0] == '(':
        symbol_table[count].append((TokenType.LP.value, '('))
        lexis_list.append((TokenType.LP.value, '('))
        expr = expr[1:]
        return Token(TokenType.LP), expr
    elif expr[0] == ')':
        symbol_table[count].append((TokenType.RP.value, ')'))
        lexis_list.append((TokenType.RP.value, ')'))
        expr = expr[1:]
        return Token(TokenType.RP), expr
    elif expr[0] == '[':
        symbol_table[count].append((TokenType.LSB.value, '['))
        lexis_list.append((TokenType.LSB.value, '['))
        expr = expr[1:]
        return Token(TokenType.LSB), expr
    elif expr[0] == ']':
        symbol_table[count].append((TokenType.RSB.value, ']'))
        lexis_list.append((TokenType.RSB.value, ']'))
        expr = expr[1:]
        return Token(TokenType.RSB), expr
    elif expr[0] == '{':
        symbol_table[count].append((TokenType.LB.value, '{'))
        lexis_list.append((TokenType.LB.value, '{'))
        expr = expr[1:]
        return Token(TokenType.LB), expr
    elif expr[0] == '}':
        symbol_table[count].append((TokenType.RB.value, '}'))
        lexis_list.append((TokenType.RB.value, '}'))
        expr = expr[1:]
        return Token(TokenType.RB), expr
    ###########################################################
    elif expr[0] == ',':
        symbol_table[count].append((TokenType.COMMA.value, ','))
        lexis_list.append((TokenType.COMMA.value, ','))
        expr = expr[1:]
        return Token(TokenType.COMMA), expr
    elif expr[0] == ';':
        symbol_table[count].append((TokenType.SEMICOLON.value, ';'))
        lexis_list.append((TokenType.SEMICOLON.value, ';'))
        expr = expr[1:]
        return Token(TokenType.SEMICOLON), expr
    ###########################################################
    validop = '{}[]()&|,-+=*/;'
    hexadecimal_str = ''
    hexadecimal_char = 'ABCDEFabcdef'
    if expr.startswith('0x') or expr.startswith('0X'):
        hexadecimal_str += '0x'
        for char in expr[2:]:
            if char.isdigit() or char in hexadecimal_char:
                hexadecimal_str += char
            else:
                if char != '\\t' and char != '\\n' and char != ' ' and char not in validop:
                    symbol_table[count].append((TokenType.ERROR.value, hexadecimal_str))
                    return Token(TokenType.ERROR), expr[len(hexadecimal_str):]
                break

    if hexadecimal_str:
        expr = expr[len(hexadecimal_str):]
        symbol_table[count].append((TokenType.HEXADECIMAL.value, hexadecimal_str))
        lexis_list.append((TokenType.HEXADECIMAL.value, hexadecimal_str))
        return Token(TokenType.HEXADECIMAL, hexadecimal_str), expr
    ###########################################################

    # Check for numbers

    decimal_str = ''
    if expr[0].isdigit():
        for char in expr:
            if char.isdigit():
                decimal_str += char
            else:
                if char != '\\t' and char != '\\n' and char != ' ' and char not in validop:
                    return Token(TokenType.ERROR), expr
                break

    if decimal_str:
        expr = expr[len(decimal_str):]
        symbol_table[count].append((TokenType.DECIMAL.value, decimal_str))
        lexis_list.append((TokenType.DECIMAL.value, decimal_str))
        return Token(TokenType.DECIMAL, decimal_str), expr
    ###########################################################
    alphabet = ''.join(chr(i) for i in range(65, 91))
    alphabet += ''.join(chr(i) for i in range(97, 123))
    id = ''

    if expr[0] in alphabet or expr[0] == '_':
        for char in expr:
            if char.isdigit() or char in alphabet or char == '_':
                id += char
            else:
                break

    if id:
        expr = expr[len(id):]
        symbol_table[count].append((TokenType.ID.value, id))
        lexis_list.append((TokenType.ID.value, id))
        return Token(TokenType.ID, id), expr

    ###########################################################
    any = ''.join(chr(i) for i in range(128))

    any.replace('\\', '')
    any.replace("'", '')
    any.replace('"', '')

    character = ''

    if expr[0] == "'":
        if expr[1:3] == '\\\'' or expr[1:3] == '\\\\':
            character += expr[0:4]
        elif expr[1] in any or expr[1:3] == '\\\n' or expr[1:3] == '\\\t':
            character += expr[0:3]
        else:
            character = None

    if character and expr[len(character) - 1] == "'":
        expr = expr[len(character):]
        symbol_table[count].append((TokenType.CHARACTER.value, character))
        lexis_list.append((TokenType.CHARACTER.value, character))
        return Token(TokenType.CHARACTER, character), expr
    ###########################################################
    any_2 = any.replace('"', '')
    any_2 = any_2.replace('\\', '')
    str = ''
    if expr[0] == '"':
        str += '"'
        for i in range(1, len(expr)):
            if expr[i] in any_2 or expr[i] == '\n' or expr[i] == '\t':
                str += expr[i]
            else:
                if expr[i:i + 2] == '\\\"':
                    str += expr[i:i + 2]
                    expr = expr[:i] + expr[i + 2:]
                    i += 2
                elif expr[i] == '\\':
                    str += expr[i]
                    expr = expr[:i] + expr[i:]
                    i += 1
                elif ord(expr[i]) == ord('"'):
                    break
                else:
                    str = None
                    break

    if str:
        str += '"'
        expr = expr[len(str):]
        symbol_table[count].append((TokenType.STRING.value, str))
        lexis_list.append((TokenType.STRING.value, str))
        return Token(TokenType.STRING, str), expr
    ###########################################################

    comment = ''
    if expr.startswith('//') and expr.endswith('\n'):
        for char in expr:
            if char in any or char == '\\t' or char == "'" or char == '"' or char == '\\':
                comment += char
            else:
                comment = None
                break

    if comment:
        expr = expr[len(comment):]
        symbol_table[count].append((TokenType.COMMENT.value, comment))
        lexis_list.append((TokenType.COMMENT.value, comment))
        return Token(TokenType.COMMENT, comment), expr
    ###########################################################
    if expr[0] in '+-*/%':
        expr2 = expr[0]
        expr = expr[1:]
        if expr2 == '+':
            symbol_table[count].append((TokenType.AOP_PL.value, '+'))
            lexis_list.append((TokenType.AOP_PL.value, '+'))
            return Token(TokenType.AOP_PL), expr
        elif expr2 == '-':
            symbol_table[count].append((TokenType.AOP_MN.value, '-'))
            lexis_list.append((TokenType.AOP_MN.value, '-'))
            return Token(TokenType.AOP_MN), expr
        elif expr2 == '*':
            symbol_table[count].append((TokenType.AOP_MP.value, '*'))
            lexis_list.append((TokenType.AOP_MP.value, '*'))
            return Token(TokenType.AOP_MP), expr
        elif expr2 == '/':
            symbol_table[count].append((TokenType.AOP_DV.value, '/'))
            lexis_list.append((TokenType.AOP_DV.value, '/'))
            return Token(TokenType.AOP_DV), expr
        elif expr2 == '%':
            symbol_table[count].append((TokenType.AOP_MOD.value, '%'))
            lexis_list.append((TokenType.AOP_MOD.value, '%'))
            return Token(TokenType.AOP_MOD), expr
    ###########################################################
    # Error: invalid token
    i = 1
    for ch in expr:
        if ch != ' ':
            i += 1
        else:
            break

    symbol_table[count].append((TokenType.ERROR.value, expr[:i]))
    return Token(TokenType.ERROR), expr[i:]


count = 0
symbol_table = {}
reader = open("../program.txt", "r")
file_path = '../symbol_table.json'
file_path2 = '../tokens.json'
lexis_list = []

for expr in reader:
    count += 1
    symbol_table[count] = []
    # expr = input("Enter an arithmetic expression: ")
    while True:
        token, expr = get_next_token(expr)
        if token.type == TokenType.END:
            break
        elif token.type == TokenType.ERROR:
            print("Error: Invalid token")
            break
        else:
            if token.value:
                print(count, ' ', token.value, "-> ", token.type.value)
            else:
                print(count, ' ', token.type.value)

with open(file_path, 'w') as json_file:
    json.dump(symbol_table, json_file, indent=4)

with open(file_path2, 'w') as json_file2:
    json.dump(lexis_list, json_file2, indent=4)
