from ply import lex, yacc 

# Definición de tokens
tokens = (
    'NUMERO',
    'RESERVADO',
    'IDENTIFICADOR',
    'STRING',
    'MASMAS',  # ++
    'MULT',    # *
    'IGUAL',   # =
    'PUNTOCOMA',  # ;
    'COMA',    # ,
    'PARENTESIS_ABIERTO',  # (
    'PARENTESIS_CERRADO',  # )
    'LLAVE_ABIERTA',  # {
    'LLAVE_CERRADA',  # }
    'MENOR_IGUAL',  # <=
    'AMPERSON',  # &
)

# Expresiones regulares para los tokens
t_RESERVADO = r'(int|main|for|return|printf|scanf|\#include|<stdio.h>)'
t_IDENTIFICADOR = r'([a-z]|[A-Z])+'
t_STRING = r'"([^"\\]|\\.)*"'
t_MASMAS = r'\+\+'
t_MULT = r'\*'
t_IGUAL = r'\='
t_PUNTOCOMA = r'\;'
t_COMA = r'\,'
t_PARENTESIS_ABIERTO = r'\('
t_PARENTESIS_CERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'
t_MENOR_IGUAL = r'\<='
t_AMPERSON = r'\&'

# Funciones de manejo de tokens
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar caracteres de espacio en blanco
t_ignore = ' \t'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores de tokens
def t_error(t):
    print("Carácter ilegal →%s←" % t.value[0])
    t.lexer.skip(1)

class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []

    def __str__(self):
        if self.value is not None:
            return f'{self.type}: {self.value}'
        else:
            return self.type


# Definición de las reglas de la gramática
def p_declaraciones(p):
    '''
    declaraciones : declaracion declaraciones
                  | declaracion
    '''
    if len(p) == 3:
        p[0] = Node('declaraciones', children=[p[1], p[2]])
    else:
        p[0] = Node('declaraciones', children=[p[1]])


def p_declaracion(p):
    '''
    declaracion : asignacion
                | funcion
                | inclusion
                | retorno
    '''
    p[0] = Node('declaracion', children=[p[1]])

def p_inclusion(p):
    '''
    inclusion : RESERVADO RESERVADO
    '''
    p[0] = Node('inclusion', children=[Node('RESERVADO', value=p[1]), Node('RESERVADO', value=p[2])])

def p_funcion(p):
    '''
    funcion : RESERVADO RESERVADO PARENTESIS_ABIERTO PARENTESIS_CERRADO bloque
            | RESERVADO PARENTESIS_ABIERTO argumentos PARENTESIS_CERRADO PUNTOCOMA
            | RESERVADO PARENTESIS_ABIERTO argumentos PARENTESIS_CERRADO bloque

    ''' 
    if p[2] != '(':
        p[0] = Node('funcion', children=[Node('RESERVADO', value=p[1]), Node('RESERVADO', value=p[2]), Node('PARENTESIS_ABIERTO', value=p[3]), Node('PARENTESIS_CERRADO', value=p[4]), p[5]])
    else:
        if p[5] == ';':
            p[0] = Node('funcion', children=[Node('RESERVADO', value=p[1]), Node('PARENTESIS_ABIERTO', value=p[2]), p[3], Node('PARENTESIS_CERRADO', value=p[4]), Node('PUNTOCOMA', value=p[5])])
        else:
            p[0] = Node('funcion', children=[Node('RESERVADO', value=p[1]), Node('PARENTESIS_ABIERTO', value=p[2]), p[3], Node('PARENTESIS_CERRADO', value=p[4]), p[5]])

def p_bloque(p):
    '''
    bloque : LLAVE_ABIERTA declaraciones LLAVE_CERRADA
    '''
    p[0] = Node('bloque', children=[Node('LLAVE_ABIERTA', value=p[1]), p[2], Node('LLAVE_CERRADA', value=p[3])])

def p_asignacion(p):
    '''
    asignacion : RESERVADO IDENTIFICADOR IGUAL valor PUNTOCOMA
               | IDENTIFICADOR IGUAL valor
               | IDENTIFICADOR MENOR_IGUAL valor 
               | IDENTIFICADOR IGUAL operacion PUNTOCOMA
    '''
    if p[1] != 'int':
        if p[2] != '=':
            p[0] = Node('asignacion', children=[Node('IDENTIFICADOR', value=p[1]), Node('MENOR_IGUAL', value=p[2]), p[3]])
        else:
            p[0] = Node('asignacion', children=[Node('IDENTIFICADOR', value=p[1]), Node('IGUAL', value=p[2]), p[3]])
    else:
        if p[3] != '=':
            p[0] = Node('asignacion', children=[Node('RESERVADO', value=p[1]), Node('IDENTIFICADOR', value=p[2]), Node('IGUAL', value=p[3]), p[4], Node('PUNTOCOMA', value=p[5])])
        else:
            p[0] = Node('asignacion', children=[Node('RESERVADO', value=p[1]), Node('IDENTIFICADOR', value=p[2]), Node('IGUAL', value=p[3]), p[4], Node('PUNTOCOMA', value=p[5])])

def p_valor(p):
    '''
    valor : IDENTIFICADOR
          | NUMERO
    '''
    if str(p[1]).isdigit():
        p[0] = Node('valor', children=[Node('NUMERO', value=p[1])])
    else:
        p[0] = Node('valor', children=[Node('IDENTIFICADOR', value=p[1])])

def p_argumentos(p):
    '''
    argumentos : argumento
               | argumento COMA argumentos
               | argumento PUNTOCOMA argumentos
    '''
    if len(p) == 2:
        p[0] = Node('argumentos', children=[p[1]])
    else:
        if p[2] == ',':
            p[0] = Node('argumentos', children=[p[1], Node('COMA', value=p[2]), p[3]])
        else:
            p[0] = Node('argumentos', children=[p[1], Node('PUNTOCOMA', value=p[2]), p[3]])

def p_argumento(p):
    '''
    argumento : STRING
              | referencia
              | IDENTIFICADOR
              | asignacion
              | incremento
    '''
    if str(p[1]).startswith('"'):
        p[0] = Node('argumento', children=[Node('STRING', value=p[1])])
    if str(p[1]).__contains__('referencia') or str(p[1]).__contains__('asignacion') or str(p[1]).__contains__('incremento'):
        p[0] = Node('argumento', children=[p[1]])
    else:
        p[0] = Node('argumento', children=[Node('IDENTIFICADOR', value=p[1])])

def p_referencia(p):
    '''
    referencia : AMPERSON IDENTIFICADOR
    '''
    p[0] = Node('referencia', children=[Node('AMPERSON', value=p[1]), Node('IDENTIFICADOR', value=p[2])])

def p_incremento(p):
    '''
    incremento : IDENTIFICADOR MASMAS
    '''
    p[0] = Node('incremento', children=[Node('IDENTIFICADOR', value=p[1]), Node('MASMAS', value=p[2])])

def p_operacion(p):
    '''
    operacion : valor MULT valor
    '''
    p[0] = Node('operacion', children=[p[1], Node('MULT', value=p[2]), p[3]])

def p_retorno(p):
    '''
    retorno : RESERVADO valor PUNTOCOMA
    '''
    p[0] = Node('retorno', children=[Node('RESERVADO', value=p[1]), p[2], Node('PUNTOCOMA', value=p[3])])

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error de sintaxis en la entrada. Token inesperado: {p.value}"+ " en la línea " + str(p.lineno))
    else:
        print("Error de sintaxis en la entrada. Final inesperado.")

# Construir el lexer
lexer = lex.lex()

# Cadena de entrada
input_string = '''
#include <stdio.h>
int main() {
    int c = 1;
    int n = 1;
    int fact = 1;
    printf("Ingrese el numero a calcular el factorial: \\n");
    scanf("%d", &n);
    for (c = 1; c <= n; c++) {
        fact = fact * c;
    }
    printf("El factorial de %d es: %d\\n", n, fact);
    return 0;
}
'''

# Darle la cadena de entrada al lexer
lexer.input(input_string)

# Iterar sobre los tokens encontrados
# for token in lexer: print(f'Token: {token.type}, Valor: {token.value}, Línea: {token.lineno}')

# Construir el parser
parser = yacc.yacc(debug=True)

# Analizar la cadena de entrada
result = parser.parse(input_string)

# Función auxiliar para imprimir el árbol
def print_tree(node, level=0, file=None):
    indent = '    ' * level
    if node.value is not None:
        print(indent + f'{node.type}: {node.value}', file=file)
    else:
        print(indent + node.type, file=file)
    for child in node.children:
        if isinstance(child, Node):
            print_tree(child, level + 1, file=file)
        else:
            print(indent + '    ' + str(child), file=file)


# Imprimir el árbol de descomposición gramatical
print("El árbol de descomposición gramatical es:\n")
print_tree(result)

# Guardar la salida en un archivo de texto
with open('salida.txt', 'w') as file:
    print_tree(result, file=file) 