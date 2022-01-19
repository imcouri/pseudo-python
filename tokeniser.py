import ply.lex as lex

class Lexer(object):

    def build(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def test(self, text):
        tokens = []
        self.input(text)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens


    tokens = (
        'VAR',
        'INT', 'DOUBLE',
        'INPUT', 'OUTPUT',
        'SUBROUTINE', 'ENDSUBROUTINE', 'RETURN',
        'IF', 'THEN', 'ELSE', 'ENDIF',
        'WHILE', 'DO', 'ENDWHILE',
        'FOR', 'TO', 'NEXT',
        'INT_CONST', 'DOUBLE_CONST', 'STRING_CONST',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'PERCENT',
        'COMMA', 'NEWLINE',
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LESS_THAN', 'LESS_EQUAL',
        'GREATER_THAN', 'GREATER_EQUAL',
        'EQUALITY', 'NOT_EQUALITY'
    )

    reserved = r''.join(["(?!" + keyword + ")" for keyword in tokens])

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'='
    t_PERCENT = r'%'

    t_LESS_THAN = r'<'
    t_LESS_EQUAL = r'<='
    t_GREATER_THAN = r'>'
    t_GREATER_EQUAL = r'>='
    t_EQUALITY = r'=='
    t_NOT_EQUALITY = r'<>'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'

    t_COMMA = r'\,'

    t_SUBROUTINE = r'SUBROUTINE'
    t_ENDSUBROUTINE = r'ENDSUBROUTINE'
    t_RETURN = r'RETURN'

    t_INT = 'INT'
    t_DOUBLE = 'DOUBLE'

    t_INPUT = 'INPUT'
    t_OUTPUT = 'OUTPUT'

    t_IF = 'IF'
    t_THEN = 'THEN'
    t_ELSE = 'ELSE'
    t_ENDIF = 'ENDIF'

    t_WHILE = 'WHILE'
    t_DO = 'DO'
    t_ENDWHILE = 'ENDWHILE'

    t_FOR = 'FOR'
    t_TO = 'TO'
    t_NEXT = 'NEXT'

    t_VAR = reserved + r'[a-zA-Z_][a-zA-Z0-9_]*'

    t_ignore = " \t"

    def t_DOUBLE_CONST(self, t):
        r'\d+\.\d*'
        t.value = float(t.value)
        return t

    def t_INT_CONST(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING_CONST(self, t):
        r'".*?"'
        t.value = t.value[1:len(t.value) - 1]
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)



lexer = Lexer()
lexer.build()
token = lexer.test(
    '''
    x = 10
    y = 30
    z = 40
    OUTPUT x
    OUTPUT 40
    '''
)

variables = {}

for i,tok in enumerate(token):
    if tok.type == 'VAR':
        if i < len(token) and token[i+1].type == 'EQUALS':
            declarationIndexes = [token[i],token[i+2]]
            variables[declarationIndexes[0].value] = declarationIndexes[1].value
    if tok.type == 'OUTPUT':
        if i < len(token):
            if token[i+1].type == 'VAR':
                print('VARIABLE OUTPUT: ' + str(variables[token[i+1].value]))
            elif token[i+1].type == 'STRING_CONST' or token[i+1].type == 'INT_CONST' or token[i+1].type == 'DOUBLE_CONST':
                print('VALUE OUTPUT: ' + str(token[i + 1].value))


