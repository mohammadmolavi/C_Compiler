
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.START()

    def START(self):
        while self.current_token_type() == 'T_COMMENT':
            self.COMMENT()
        funcs = self.FUNCS()
        return {'type': 'START', 'body': funcs}

    def FUNCS(self):
        funcs = []
        funcs.append(self.FUNC())
        while self.pos < len(self.tokens) and self.current_token_type() in ['T_INT', 'T_CHAR', 'T_BOOL', 'T_VOID']:
            funcs.append(self.FUNC())
        if (len(funcs) == 0):
            funcs = funcs[0]
        return funcs

    def FUNC(self):
        type_specifier = self.consume(['T_INT', 'T_CHAR', 'T_BOOL', 'T_VOID'])
        name = self.consume('T_ID')
        self.consume('T_LP')
        params = self.PARAMS()
        self.consume('T_RP')
        self.consume('T_LB')
        exp = self.EXP()
        self.consume('T_RB')
        return {
            'type': 'FUNC',
            'return_type': type_specifier[1],
            'name': name[1],
            'params': params,
            'body': exp
        }

    def PARAMS(self):
        params = []
        if self.current_token_type() in ['T_INT', 'T_CHAR', 'T_BOOL']:
            params.append(self.PARAM())
            params.extend(self.MORE_PARAMS())
            return params
        else:
            return params

    def MORE_PARAMS(self):
        more_params = []
        if self.current_token_type() == "T_COMMA":
            self.consume("T_COMMA")
            more_params.append(self.PARAM())
            more_params.extend(self.MORE_PARAMS())
            return more_params
        elif self.current_token_type() == "T_RP":
            return more_params

    def PARAM(self):
        type_specifier = self.consume(['T_INT', 'T_CHAR', 'T_BOOL'])
        name = self.consume('T_ID')
        return {'type': 'PARAM', 'param_type': type_specifier[1], 'name': name[1]}

    def EXP(self):
        exps = []
        while self.pos < len(self.tokens) and self.current_token_type() != 'T_RB':
            if self.current_token_type() in ['T_ID','T_INT', 'T_CHAR', 'T_BOOL']:
                exps.append(self.EXP1())
                self.consume('T_SEMICOLON')
            elif self.current_token_type() == 'T_FOR':
                exps.append(self.FOR())
            elif self.current_token_type() == 'T_IF':
                exps.append(self.IF())
            elif self.current_token_type() == 'T_PRINT':
                exps.append(self.PRINT())
            elif self.current_token_type() == 'T_RETURN':
                exps.append(self.RETURN())
            elif self.current_token_type() == 'T_BREAK':
                exps.append(self.BREAK())
            elif self.current_token_type() == 'T_CONTINUE':
                exps.append(self.CONTINUE())
            elif self.current_token_type() == 'T_COMMENT':
                exps.append(self.COMMENT())
            elif self.current_token_type() == 'T_SEMICOLON':
                self.consume('T_SEMICOLON')
            else:
                # self.consume('T_SEMICOLON')
                print(SyntaxError(f'Unexpected token {self.current_token()}'))
                del self.tokens[self.pos]


        return exps

    def EXP1(self):
        left = self.OPERAND()
        while self.current_token_type() in ['T_ASSIGN', 'T_AOP_PL', 'T_AOP_MN', 'T_AOP_MP', 'T_AOP_DV', 'T_AOP_MOD']:
            op = self.consume(['T_ASSIGN', 'T_AOP_PL', 'T_AOP_MN', 'T_AOP_MP', 'T_AOP_DV', 'T_AOP_MOD','T_AOP_MOD'])
            right = self.EXP1()
            left = {'operator': op[1], 'left': left, 'right': right}
        return left

    def OPERAND(self):
        token = self.current_token()
        if token[0] in ['T_DECIMAL', 'T_HEXADECIMAL', 'T_STRING', 'T_CHARACTER', 'T_TRUE', "T_FALSE"]:
            self.pos += 1
            return {'value': token[1]}
        elif token[0] == 'T_ID':
            return self.CALL_FUNC()
        elif token[0] == 'T_LP':
            self.consume('T_LP')
            expr = self.EXP1()
            self.consume('T_RP')
            return expr
        elif token[0] in ['T_INT', 'T_BOOL', 'T_CHAR']:
            return_dic = {'type': token[1]}
            self.consume(['T_INT', 'T_BOOL', 'T_CHAR'])
            token = self.current_token()
            if token[0] == 'T_ID':
                return_dic['declarator'] = []
                return_dic['declarator'].append(token[1])
                self.consume('T_ID')
                token = self.current_token()
                while (token[0] == 'T_COMMA'):
                    self.consume('T_COMMA')
                    token = self.current_token()
                    self.consume('T_ID')
                    return_dic['declarator'].append(token[1])
                if(token[0] == 'T_LSB'):
                    self.consume('T_LSB')
                    token = self.consume('T_DECIMAL')
                    self.consume('T_RSB')
                    return_dic['array_length'] = token[1]
                return return_dic
        else:
            print(SyntaxError(f"Unexpected token {token} in pos {self.pos}"))
            self.pos += 1
            return {}


    def CALL_FUNC(self):
        params = []
        id = self.current_token()[1]
        self.consume('T_ID')
        if self.current_token_type() == 'T_LP':
            self.consume('T_LP')
            params.extend(self.CALL_PARAMS())
            self.consume('T_RP')
            return {'type': 'call_func', 'name': id, 'parameters': params}
        else:
            return {'operand': id}

    def CALL_PARAMS(self):
        params = []
        if self.current_token_type() in ['T_ID', 'T_DECIMAL', 'T_CHARACTER', 'T_HEXADECIMAL'
            , 'T_STRING', 'T_TRUE', 'T_FALSE']:
            params.append(self.CALL_PARAM())
            param = self.CALL_MORE_PARAMS()
            if param != None:
                params.extend(self.CALL_MORE_PARAMS())
            return params
        elif self.current_token_type() == 'T_RP':
            return params

        # return params

    def CALL_MORE_PARAMS(self):
        more_params = []

        if self.current_token_type() == "T_COMMA":
            self.consume("T_COMMA")
            more_params.append(self.CALL_PARAM())
            more_params.extend(self.CALL_MORE_PARAMS())
            return more_params
        elif self.current_token()[1] == ")":
            return more_params

    def CALL_PARAM(self):
        if self.current_token_type() in ['T_ID', 'T_DECIMAL', 'T_CHARACTER', 'T_HEXADECIMAL',
                                         'T_STRING', 'T_TRUE', 'T_FALSE']:
            name = self.EXP1()
            return {'type': 'PARAM', 'expression': name}
        else:
            return

    def FOR(self):
        self.consume('T_FOR')
        self.consume('T_LP')
        def_for = self.DEF_FOR()
        self.consume('T_RP')
        self.consume('T_LB')
        body = self.EXP()
        self.consume('T_RB')
        return {'type': 'FOR', 'def_for': def_for, 'body': body}

    def DEF_FOR(self):
        type_specifier = self.consume(['T_INT', 'T_CHAR', 'T_BOOL'])
        var = self.consume('T_ID')
        if self.current_token_type() == 'T_ASSIGN':
            var_value = self.consume(self.current_token_type())
            self.consume(['T_ID', 'T_DECIMAL', 'T_CHARACTER', 'T_HEXADECIMAL', 'T_STRING'])
        self.consume('T_SEMICOLON')
        relexp = self.RELEXP()
        self.consume('T_SEMICOLON')
        exp1 = self.EXP1()
        return {'type': 'DEF_FOR', 'var_type': type_specifier[1], 'var': var[1], 'var_value': var_value,
                'relexp': relexp, 'exp1': exp1}

    def IF(self):
        self.consume('T_IF')
        self.consume('T_LP')
        relexp = self.RELEXP()
        self.consume('T_RP')
        self.consume('T_LB')
        body = self.EXP()
        self.consume('T_RB')
        else_part = self.ELSE()
        return {'type': 'IF', 'relexp': relexp, 'body': body, 'else': else_part}

    def ELSE(self):
        if self.current_token_type() == 'T_ELSE':
            self.consume('T_ELSE')
            self.consume('T_LB')
            body = self.EXP()
            self.consume('T_RB')
            return {'type': 'ELSE', 'body': body}
        return None

    def PRINT(self):
        self.consume('T_PRINT')
        self.consume('T_LP')
        string = self.consume(['T_STRING', 'T_ID'])
        params_print = self.PARAMS_PRINT()
        self.consume('T_RP')
        self.consume('T_SEMICOLON')
        return {'type': 'PRINT', 'string': string[1], 'params': params_print}

    def PARAMS_PRINT(self):
        params = []
        if self.current_token_type() == 'T_COMMA':
            self.consume('T_COMMA')
            expr1 = self.EXP1()
            params.append(expr1)
            while self.current_token_type() == 'T_COMMA':
                self.consume('T_COMMA')
                expr1 = self.EXP1()
                params.append(expr1)
            return params

    def RETURN(self):
        self.consume('T_RETURN')
        expr = self.EXP1()
        self.consume('T_SEMICOLON')
        return {'type': 'RETURN', 'operand': expr}

    def BREAK(self):
        self.consume('T_BREAK')
        self.consume('T_SEMICOLON')
        return {'type': 'BREAK'}

    def CONTINUE(self):
        self.consume('T_CONTINUE')
        self.consume('T_SEMICOLON')
        return {'type': 'CONTINUE'}

    def COMMENT(self):
        token = self.consume('T_COMMENT')
        return {'type': 'COMMENT', 'value': token[1]}

    def RELEXP(self):
        left = self.EXP1()
        if self.current_token_type() in ['T_ROP_EQ', 'T_ROP_NE', 'T_ROP_S', 'T_ROP_G', 'T_ROP_SE', 'T_ROP_GE']:
            op = self.consume(['T_ROP_EQ', 'T_ROP_NE', 'T_ROP_S', 'T_ROP_G', 'T_ROP_SE', 'T_ROP_GE'])
            right = self.RELEXP()
            return {'type': 'binary_expression', 'operator': op[1], 'left': left, 'right': right}
        return left

    def consume(self, expected_types):
        token = self.current_token()
        try:
            if isinstance(expected_types, list):
                if token[0] not in expected_types:
                    raise SyntaxError(f"Expected token {expected_types}, got {token},pos {self.pos}")
            else:
                if token[0] != expected_types:
                    raise SyntaxError(f"Expected token {expected_types}, got {token},pos {self.pos}")
        except Exception as e:
            print(e)
            if isinstance(expected_types, list):
                token = expected_types[0]
            else:
                token = expected_types
            if (len(self.tokens) -1) != (self.pos + 1):
                if(self.tokens[self.pos + 1][0] != expected_types):
                    self.tokens.insert(self.pos , token)
            else:
                if (len(self.tokens)) != (self.pos):
                    del self.tokens[self.pos]

        self.pos += 1
        return token

    def current_token(self):
        return self.tokens[self.pos]

    def current_token_type(self):
        return self.tokens[self.pos][0]


import json

with open("../tokens.json") as token_file:
    tokens = json.load(token_file)

parser = Parser(tokens)
ast = parser.parse()
print(json.dumps(ast, indent=4))

with open('../parsing_tree.json', 'w') as file:
    json.dump(ast, file)
