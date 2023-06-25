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

# Definición de las reglas de la gramática
def p_declaraciones(p):
    '''
    declaraciones : declaracion declaraciones
                  | declaracion
    '''
    if len(p) == 3:
        p[0] ='declaraciones → ' + p[1] + "\n" + p[2]
    else:
        p[0] ='declaraciones → ' + p[1]

def p_declaracion(p):
    '''
    declaracion : asignacion
                | funcion
                | inclusion
                | retorno
    '''
    p[0] ="declaracion → " + p[1]

def p_inclusion(p):
    '''
    inclusion : RESERVADO RESERVADO
    '''
    p[0] = "inclusion → " + " ".join(p[1:])

def p_funcion(p):
    '''
    funcion : RESERVADO RESERVADO PARENTESIS_ABIERTO PARENTESIS_CERRADO bloque
            | RESERVADO PARENTESIS_ABIERTO argumentos PARENTESIS_CERRADO PUNTOCOMA
            | RESERVADO PARENTESIS_ABIERTO argumentos PARENTESIS_CERRADO bloque

    '''
    p[0] = "funcion → " + " ".join(p[1:])

def p_bloque(p):
    '''
    bloque : LLAVE_ABIERTA declaraciones LLAVE_CERRADA
    '''
    p[0] = "bloque → " + " ".join(p[1:])

def p_asignacion(p):
    '''
    asignacion : RESERVADO IDENTIFICADOR IGUAL valor PUNTOCOMA
               | IDENTIFICADOR IGUAL valor
               | IDENTIFICADOR MENOR_IGUAL valor 
               | IDENTIFICADOR IGUAL operacion PUNTOCOMA
    '''
    p[0] = "asignacion → " + " ".join(p[1:])

def p_valor(p):
    '''
    valor : IDENTIFICADOR
          | NUMERO
    '''
    p[0] = "valor → " + str(p[1])

def p_argumentos(p):
    '''
    argumentos : argumento
               | argumento COMA argumentos
               | argumento PUNTOCOMA argumentos
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[2] == ',':
        p[0] = p[1] + " " +p[2] + " " + p[3]
    elif len(p) == 4 and p[2] == ';':
        p[0] = p[1] + " " +p[2] + " " + p[3]

def p_argumento(p):
    '''
    argumento : STRING
              | referencia
              | IDENTIFICADOR
              | asignacion
              | incremento
    '''
    p[0] = "argumento → " + str(p[1])

def p_referencia(p):
    '''
    referencia : AMPERSON IDENTIFICADOR
    '''
    p[0] = "referencia → " + " ".join(p[1:])

def p_incremento(p):
    '''
    incremento : IDENTIFICADOR MASMAS
    '''
    p[0] = "incremento → " + " ".join(p[1:])

def p_operacion(p):
    '''
    operacion : valor MULT valor
    '''
    p[0] = "operacion → " + " ".join(p[1:])

def p_retorno(p):
    '''
    retorno : RESERVADO valor PUNTOCOMA
    '''
    p[0] = "retorno → " + " ".join(p[1:])

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
for token in lexer:
    print(f'Token: {token.type}, Valor: {token.value}, Línea: {token.lineno}')

# Construir el parser
parser = yacc.yacc(debug=True)

# Analizar la cadena de entrada
result = parser.parse(input_string)

# Imprimir el resultado del análisis
if result:
    print("\n\n") 
    print("El resultado del análisis es: \n\n" + result)
else:
    print("El análisis no tuvo éxito.")
