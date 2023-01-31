from ply import lex, yacc

# Define the tokens
tokens = ('NUMBER', 'WHITESPACE', 'PLUS', 'MINUS',
          'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'FN', 'NAME', 'LBRACE', 'RBRACE', 'DISPLAY')

# Define the lexer


def t_DISPLAY(t):
    r'display'
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_WHITESPACE(t):
    r'\s+'
    pass


def t_FN(t):
    r'fn'
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


def t_PLUS(t):
    r'\+'
    return t


def t_LBRACE(t):
    r'{'
    return t


def t_RBRACE(t):
    r'}'
    return t


def t_MINUS(t):
    r'-'
    return t


def t_TIMES(t):
    r'\*'
    return t


def t_DIVIDE(t):
    r'/'
    return t


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


# Define the parser


def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]


def p_display_call(p):
    'statement : DISPLAY LPAREN expression RPAREN'
    p[0] = ('display', p[3])


def display(expression):
    print(expression)



def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


def p_error(p):
    print(f"Syntax error in input at line: {p.lineno}")


def p_function_declaration(p):
    'function_declaration : FN NAME LPAREN RPAREN'
    # Do something with the function name here
    print("Function declared:", p[2])


# parser = yacc.yacc(start='function_declaration')
parser = yacc.yacc(start='statement_list', write_tables=False)


def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")


while True:
    try:
        s = read_file('../main.es')
    except EOFError:
        break
    if not s:
        print("The file is empty.")
        break
    else:
        result = parser.parse(s)
        display(result)
        break
