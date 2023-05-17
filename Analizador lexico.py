import ply.lex as lex
import tkinter as tk

# Definición de tokens y expresiones regulares
reserved_words = {
    'int': 'INT',
    'for': 'FOR',
    'return': 'RETURN',
    'main': 'MAIN',
    'printf': 'PRINTF',
    'scanf': 'SCANF'
}

special_symbols = [
    '%d',
    '{',
    '}',
    '(',
    ')',
    '"',
    '=',
    '*',
    ';',
    ',',
    '<=',
    '++',
    '\n',
    '&'
]

tokens = [
    'NUMBER',
    'IDENTIFIER'
] + list(reserved_words.values())

def t_NUMBER(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-z]+[0-9]*'
    t.type = reserved_words.get(t.value, 'IDENTIFIER')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Función para analizar el código y clasificar los tokens
def analyze_code():
    code = code_text.get("1.0", tk.END)
    lexer.input(code)
    result = ""
    while True:
        token = lexer.token()
        if not token:
            break
        if token.type in reserved_words.values():
            result += f"Palabra reservada: {token.value}\n"
        elif token.type in special_symbols:
            result += f"Símbolo especial: {token.value}\n"
        elif token.type == "NUMBER":
            result += f"Número: {token.value}\n"
        elif token.type == "IDENTIFIER":
            result += f"Identificador: {token.value}\n"
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

# Crear ventana principal
window = tk.Tk()
window.title("Analizador Léxico")
window.geometry("500x400")

# Crear elementos de la interfaz
code_label = tk.Label(window, text="Código:")
code_label.pack()
code_text = tk.Text(window, height=10)
code_text.pack()

analyze_button = tk.Button(window, text="Analizar", command=analyze_code)
analyze_button.pack()

output_label = tk.Label(window, text="Resultados:")
output_label.pack()
output_text = tk.Text(window, height=10)
output_text.pack()

# Iniciar el bucle principal del programa
window.mainloop()
