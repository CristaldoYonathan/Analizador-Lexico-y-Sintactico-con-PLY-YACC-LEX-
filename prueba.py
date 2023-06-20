from ply import lex, yacc

#Definicion de tokens
tokens = ( 
    'NUMERO',
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
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar caracteres de espacio en blanco
t_ignore = '( )\t'

#t_ignore_COMMENT = r'\/\/.*'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    
# Manejo de errores de tokens
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex() 

###############################################################################################

# Definición de reglas de producción 
def p_expression_bloque(p):
    ''' bloque : SIMBOLO_ESPECIAL declaraciones SIMBOLO_ESPECIAL
    '''
    pass

def p_expression_declaraciones(p):
    ''' declaraciones : declaracion declaraciones 
                      | declaracion
    ''' 
    pass
#    if len(p) == 3:
#        p[0] = str(p[1]) + str(p[2])
#    else:
#        p[0] = str(p[1])

def p_expression_declaracion(p):
    ''' declaracion : asignacion 
                    | funcion 
                    | inclusion 
                    | retorno 
    '''

#    if p[1] == 'asignacion':
#        p[0] = str(p[1])
#    if p[1] == 'funcion':
#        p[0] = str(p[2])
#    if p[1] == 'inclusion':
#        p[0] = str(p[3])
#    if p[1] == 'retorno':
#        p[0] = str(p[4])

def p_expression_operacion(p):
    ''' operacion : valor SIMBOLO_ESPECIAL valor 
    '''
    pass
    

def p_expression_valor(p):
    ''' valor : IDENTIFICADOR
                | NUMERO
    ''' 
    pass

def p_expression_asignacion(p):
    ''' asignacion : RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL valor SIMBOLO_ESPECIAL 
                    | RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL
                    | IDENTIFICADOR SIMBOLO_ESPECIAL operacion SIMBOLO_ESPECIAL 
                    | IDENTIFICADOR SIMBOLO_ESPECIAL valor 
    '''
    pass

def p_expression_funcion(p):
    ''' funcion : RESERVADO RESERVADO SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL bloque 
                | RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL 
                | RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL bloque
    '''
    pass

def p_expression_argumentos(p):
    ''' argumentos : argumento SIMBOLO_ESPECIAL argumentos 
                    | argumento
    '''
    pass

def p_expression_argumento(p):
    ''' argumento : asignacion
                    | STRING
                    | referencia
                    | incremento
                    | IDENTIFICADOR
    '''
    pass

def p_expression_referencia(p):
    ''' referencia : SIMBOLO_ESPECIAL IDENTIFICADOR
    '''
    pass

def p_expression_incremento(p):
    ''' incremento : IDENTIFICADOR SIMBOLO_ESPECIAL
    '''
    pass   

def p_expression_retorno(p):
    ''' retorno : RESERVADO valor SIMBOLO_ESPECIAL
    '''
    pass

def p_expression_inclusion(p):
    ''' inclusion : RESERVADO RESERVADO
    '''
#    if p[1] == '#include' and p[2] == '<stdio.h>':
#        p[0] = '#include <stdio.h>'


# Manejo de errores de parser
def p_error(p):
    print("Error de sintaxis en '%s' en la linea %d" % (p.value, p.lineno))


# Construir el parser
parser = yacc.yacc()

###############################################################################################

# Cadena de entrada
input_string = '''
#include <stdio.h>
        int main ( ) {
        ㅤㅤㅤint c;
        ㅤㅤㅤint n;
        ㅤㅤㅤint fact = 1;
        ㅤㅤㅤprintf("Ingrese el numero a calcular el factorial: \n");
        ㅤㅤㅤscanf("%d ", &n);
        ㅤㅤㅤfor (c = 1; c <= n; c++){
        ㅤㅤㅤㅤㅤㅤfact = fact * c;
        ㅤㅤㅤ}
        ㅤㅤㅤprintf("El factorial de %d es: %d\n", n, fact);
        ㅤㅤㅤreturn 0;
}
'''

#input_string = input('Ingrese una cadena de texto: ')

# Ejecutar el lexer
lexer.input(input_string)

# Obtener los tokens
while True:
    token = lexer.token()
    if not token:
        break 
    print(str(token.type) + "  →  " + str(token.value) + " " + str(token.lineno) + " " + str(token.lexpos))

# Ejecutar el parser
result = parser.parse(input_string) 
