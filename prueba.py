from ply import lex, yacc

#Definicion de tokens
tokens = ( 
    'DIGITO',
    'RESERVADO',  
    'STRING',  
    'IDENTIFICADOR',
    'SIMBOLO_ESPECIAL',
)

# Expresiones regulares para los tokens 
t_RESERVADO = r'(int|main|for|return|printf|scanf|\#include|\<stdio.h\>)'
t_SIMBOLO_ESPECIAL = r'(\+\+|\*|\=|\;|\,|\(|\)|\{|\}|\<=|\&)'
t_STRING = r'"([^"]*)"' 
t_IDENTIFICADOR = r'([a-z]|[A-Z])+'


# Funciones de manejo de tokens
def t_DIGITO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar caracteres de espacio en blanco
t_ignore = '(\n| )\t'

# Manejo de errores de tokens
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Definición de reglas de producción
def p_expression_programa(p):
    ''' programa : bloque
    ''' 
    pass

def p_expression_bloque(p):
    ''' bloque : SIMBOLO_ESPECIAL declaraciones SIMBOLO_ESPECIAL
    '''
    pass

def p_expression_declaraciones(p):
    ''' declaraciones : declaracion declaraciones
    | declaracion
    '''
    pass

def p_expression_declaracion(p):
    ''' declaracion : incluir
    | funcion
    | asignacion
    | expresion
    '''
    pass

def p_expression_incluir(p):
    ''' incluir : RESERVADO RESERVADO
    '''
    pass

def p_expression_funcion(p):
    ''' funcion : RESERVADO argumento SIMBOLO_ESPECIAL
    | RESERVADO RESERVADO SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL bloque
    | RESERVADO SIMBOLO_ESPECIAL parametros SIMBOLO_ESPECIAL bloque
    '''
    pass

def p_argumentos_funcion(p):
    ''' argumento : SIMBOLO_ESPECIAL parametros SIMBOLO_ESPECIAL'''
    pass

def p_expression_parametros(p):
    ''' parametros : parametro SIMBOLO_ESPECIAL parametros
    | parametro
    '''
    pass

def p_expression_parametro(p):
    ''' parametro : string 
    '''
    pass

def p_expression_string(p):
    ''' string : STRING 
    '''
    pass

def p_expression_asignacion(p):
    ''' asignacion : RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL expresion SIMBOLO_ESPECIAL
    | IDENTIFICADOR SIMBOLO_ESPECIAL expresion SIMBOLO_ESPECIAL
    | IDENTIFICADOR DIGITO
    '''
    if p[1] == 'return':
        p[0] = p[2]
    pass

def p_expression_expresiones(p):
    ''' expresiones : expresion SIMBOLO_ESPECIAL expresion
    | expresion expresion
    ''' 
    pass

def p_expression_expresion(p):
     ''' expresion : IDENTIFICADOR
    | DIGITO 
    ''' 
     p[0] = p[1]

# Manejo de errores de parser
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)

# Construir el parser
parser = yacc.yacc()

# Cadena de entrada
input_string = '''
    #include <stdio.h>
    int main()
    {
        int c, n, fact  = 1;
        printf("Ingrese el numero a calcular el factorial: \n");
        scanf("%d ", &n);
        for (c = 1; c <= n; c++){
            fact = fact * c;
            }
        printf("El factorial de %d es: %d\n", n, fact);
        return 0;
    }

'''

#'#include <stdio.h> int main() { int c, n, fact = 1; printf("Ingrese el numero a calcular el factorial: \n"); scanf("%d", &n); for (c = 1; c <= n; c++){ fact = fact * c;} printf("El factorial de %d es: %d\n", n, fact); return 0; }'

# Ejecutar el lexer
lexer.input(input_string)

# Obtener los tokens
while True:
    token = lexer.token()
    if not token:
        break
    print(token)

# Ejecutar el parser
result = parser.parse(input_string)
print("Resultado:", result)