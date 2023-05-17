import ply.yacc as yacc

# Tokens previamente definidos

tokens = [
    'NUMBER',
    'SIGNO',
    'ESCAPE_N',
    'ESCAPE_D',
    'INCLUDE',
    'SCANF',
    'FOR',
    'PRINTF',
    'INT',
    'STDIO_H',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'QUOTE',
    'TIMES',
    'PLUSPLUS',
    'LTOEQ',
    'MAIN',
    'RETURN',
    'IDENTIFIER',
    'delimitador'
]

t_SIGNO = r'<=|='
t_ESCAPE_N = r'\\n'
t_ESCAPE_D = r'%d'
t_INCLUDE = r'\#include'
t_SCANF = r'scanf'
t_FOR = r'for'
t_PRINTF = r'printf'
t_INT = r'int'
t_STDIO_H = r'<stdio\.h>'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_QUOTE = r'\"'
t_TIMES = r'\*'
t_PLUSPLUS = r'\+\+'
t_LTOEQ = r'<='
t_MAIN = r'main'
t_RETURN = r'return'

reserved_words = {
    'include': 'INCLUDE',
    'scanf': 'SCANF',
    'for': 'FOR',
    'printf': 'PRINTF',
    'int': 'INT',
    'stdio.h': 'STDIO_H',
    'main': 'MAIN',
    'return': 'RETURN'
}

def t_NUMBER(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-z]+[0-9]*'
    t.type = reserved_words.get(t.value, 'IDENTIFIER')
    return t

t_delimitador = r'[()]|{?}|;|,"?|\s'

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Definición de la gramática
def p_programa(p):
    '''programa : declaracionPrincipal
                | sentencia
                | libreria'''

def p_declaracionPrincipal(p):
    'declaracionPrincipal : tdato MAIN delimitadores delimitadores'

def p_sentencia(p):
    '''sentencia : input
                 | loop
                 | output
                 | RETURN NUMBER delimitadores
                 | variable
                 | conjunto
                 | cadena
                 | asignacion
                 | comparacion
                 | incremento
                 | operar
                 | declaracionVariable
                 | escape'''

def p_libreria(p):
    'libreria : INCLUDE cadena programa'

def p_declaracionVariable(p):
    'declaracionVariable : tdato variable SIGNO valor delimitador'

def p_variable(p):
    '''variable : nombre
                | '&' nombre
                | nombre COMMA variable'''

def p_valor(p):
    'valor : NUMBER'

def p_nombre(p):
    '''nombre : 'n'
              | 'fact'
              | IDENTIFIER'''

def p_escape(p):
    '''escape : QUOTE
              | QUOTE ESCAPE_N sentencia'''

def p_asignacion(p):
    '''asignacion : nombre SIGNO NUMBER delimitador
                  | nombre SIGNO nombre delimitador'''

def p_comparacion(p):
    'comparacion : nombre signo valor delimitador'

def p_incremento(p):
    '''incremento : nombre PLUSPLUS delimitador
                  | PLUSPLUS nombre delimitador'''

def p_operaciones(p):
    '''operaciones : TIMES
                   | PLUSPLUS'''

def p_operar(p):
    'operar : nombre operaciones nombre'

def p_delimitadores(p):
    '''delimitadores : LPAREN
                     | RPAREN
                     | LBRACE
                     | RBRACE
                     | SEMICOLON
                     | COMMA
                     | QUOTE
                     | conjunto
                     | conjunto SEMICOLON sentencia delimitadores
                     | conjunto SEMICOLON sentencia'''

def p_conjunto(p):
    '''conjunto : LPAREN RPAREN
                | LBRACE RBRACE
                | LPAREN sentencia RPAREN
                | LBRACE sentencia RBRACE
                | QUOTE sentencia QUOTE
                | LPAREN sentencia delimitador sentencia RPAREN
                | QUOTE sentencia delimitadores'''

def p_cadena(p):
    '''cadena : CADENA_FACTORIAL
              | CADENA_RESULTADO
              | CADENA_ESCAPE
              | STDIO_H'''

def p_input(p):
    'input : SCANF delimitadores delimitadores'

def p_loop(p):
    'loop : FOR delimitador delimitador'

def p_output(p):
    'output : PRINTF delimitadores delimitadores'

# Regla para manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis")

# Construir el analizador sintáctico
parser = yacc.yacc()

# Prueba del analizador sintáctico
data = '''int main() {
    int n;
    printf("Ingrese el numero a calcular el factorial: ");
    scanf("%d", &n);
    int fact = 1;
    for (int c = 1; c <= n; c++) {
        fact = fact * c;
    }
    printf("El factorial de %d es: %d\n", n, fact);
    return 0;
}'''

parser.parse(data)
