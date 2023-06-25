from ply import lex, yacc

#Definicion de tokens
tokens = ( 
    'NUMERO',
    'RESERVADO',  
    'STRING',  
    'IDENTIFICADOR',
    'SIMBOLO_ESPECIAL',
    #'NEWLINE',
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
t_ignore = ' \t'

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
def p_expression_declaraciones1(p):
    ''' declaraciones : declaracion declaraciones 
    ''' 
    print("declaracion declaraciones")


def p_expression_declaraciones2(p):
    ''' declaraciones : declaracion
    ''' 
    print("declaracion")

def p_expression_bloque(p):
    ''' bloque : SIMBOLO_ESPECIAL declaraciones SIMBOLO_ESPECIAL
    '''
    print("SIMBOLO_ESPECIAL declaraciones SIMBOLO_ESPECIAL")


def p_expression_declaracion1(p):
    ''' declaracion : asignacion 
    '''
    print("asignacion")


def p_expression_declaracion2(p):
    ''' declaracion : funcion 
    '''
    print("funcion")


def p_expression_declaracion3(p):
    ''' declaracion : retorno 
    '''
    print("retorno")


def p_expression_declaracion4(p):
    ''' declaracion : inclusion 
    '''
    print("inclusion")

def p_expression_operacion(p):
    ''' operacion : valor SIMBOLO_ESPECIAL valor 
    '''
    print("valor SIMBOLO_ESPECIAL valor")
    

def p_expression_valor(p):
    ''' valor : IDENTIFICADOR
    ''' 
    print("IDENTIFICADOR")


def p_expression_valor2(p):
    ''' valor : NUMERO
    ''' 
    print("NUMERO")

def p_expression_asignacion(p):
    ''' asignacion : RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL valor SIMBOLO_ESPECIAL 
    '''
    print("RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL valor SIMBOLO_ESPECIAL")


def p_expression_asignacion2(p):
    ''' asignacion : RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL
    '''
    print("RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL")


def p_expression_asignacion3(p):##CAMBIADOOOOOOOOOOOOOOO
    ''' asignacion : IDENTIFICADOR SIMBOLO_ESPECIAL operacion SIMBOLO_ESPECIAL 
    '''
    print("IDENTIFICADOR SIMBOLO_ESPECIAL operacion SIMBOLO_ESPECIAL")


def p_expression_asignacion4(p):
    ''' asignacion : IDENTIFICADOR SIMBOLO_ESPECIAL valor 
    '''
    print("IDENTIFICADOR SIMBOLO_ESPECIAL valor")


def p_expression_funcion1(p):
    ''' funcion : RESERVADO RESERVADO SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL bloque 
    '''
    print("RESERVADO RESERVADO SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL bloque")


def p_expression_funcion2(p):
    ''' funcion : RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL  
    '''
    print("RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL")


def p_expression_funcion3(p):
    ''' funcion : RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL bloque  
    '''
    print("RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL bloque")


def p_expression_argumentos1(p):
    ''' argumentos : argumento SIMBOLO_ESPECIAL argumentos 
    '''
    print("argumento SIMBOLO_ESPECIAL argumentos")


def p_expression_argumentos2(p):
    ''' argumentos : argumento 
    '''
    print("argumento")


def p_expression_argumento1(p):
    ''' argumento : asignacion
    '''
    print("asignacion")

def p_expression_argumento2(p):
    ''' argumento : STRING
    '''
    print("STRING")

def p_expression_argumento3(p):
    ''' argumento : referencia
    '''
    print("referencia")

def p_expression_argumento4(p):
    ''' argumento : incremento
    '''
    print("incremento")

def p_expression_argumento5(p):
    ''' argumento : IDENTIFICADOR
    '''
    print("IDENTIFICADOR")


def p_expression_referencia(p):
    ''' referencia : SIMBOLO_ESPECIAL IDENTIFICADOR
    '''
    print("SIMBOLO_ESPECIAL IDENTIFICADOR")

def p_expression_incremento(p):
    ''' incremento : IDENTIFICADOR SIMBOLO_ESPECIAL
    '''
    print("IDENTIFICADOR SIMBOLO_ESPECIAL")

def p_expression_retorno(p):
    ''' retorno : RESERVADO valor SIMBOLO_ESPECIAL
    '''
    print("RESERVADO valor SIMBOLO_ESPECIAL")

def p_expression_inclusion(p):
    ''' inclusion : RESERVADO RESERVADO
    '''
    print("RESERVADO RESERVADO")

# Manejo de errores de parser
def p_error(p):
    print("Error de sintaxis en '%s' en la linea %d" % (p.value, p.lineno))


# Construir el parser
parser = yacc.yacc()

###############################################################################################

# Cadena de entrada
input_string =  '''
#include <stdio.h>
int main(){
    int a = 5;
    return 0;
}
'''

# Ejecutar el lexer
lexer.input(input_string)

# Obtener los tokens
while True:
    token = lexer.token()
    if not token:
        break 
    ##print(str(token.type) + "  →  " + str(token.value) + " " + str(token.lineno) + " " + str(token.lexpos))

# Ejecutar el parser
result = parser.parse(input_string) 
