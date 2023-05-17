import tkinter as tk
import ply.lex as lex

# Definir los tokens y las reglas de expresiones regulares
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Carácter no válido '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Crear la ventana principal
window = tk.Tk()
window.title("Calculadora")

# Crear un cuadro de texto
text_box = tk.Text(window)
text_box.pack()

# Agregar una etiqueta
label = tk.Label(window, text="Resultado:")
label.pack()

# Función para analizar la expresión
def analyze_expression():
    expression = text_box.get("1.0", "end-1c")
    
    # Tokenizar
    result = ""
    lexer.input(expression)
    while True:
        tok = lexer.token()
        if not tok:
            break      # No hay más entrada
        result += str(tok) + "\n"
    
    # Mostrar el resultado
    result_label.config(text=result)

# Botón para analizar la expresión
analyze_button = tk.Button(window, text="Analizar", command=analyze_expression)
analyze_button.pack()

# Etiqueta para mostrar el resultado
result_label = tk.Label(window, text="")
result_label.pack()

# Iniciar el bucle de eventos de la ventana
window.mainloop()
