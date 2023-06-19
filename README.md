
# TEORIA DE LA COMPUTACION

  

## ANALIZADOR LEXICO Y SINTÁCTICO CON PLY (YACC/LEX)

  

### TOKENS
- NUMERO
- RESERVADO
- STRING
- IDENTIFICADOR
- SIMBOLO_ESPECIAL  

### Expresiones regulares para los tokens 
| Reglas|         Expresiones regulares       |
|----------|----------------------------|
| t_RESERVADO | r'(int&#124;main&#124;for&#124;return&#124;printf&#124;scanf&#124;\#include&#124;\<stdio.h\>)' |
| t_SIMBOLO_ESPECIAL | r'(\+\+&#124;\*&#124;\=&#124;\;&#124;\,&#124;\(&#124;\)&#124;\{&#124;\}&#124;\<=&#124;\&)'   |
| t_STRING | r'"([ ^" ]*)"'   |
| t_IDENTIFICADOR | r'([a-z]&#124;[A-Z])+'   | 

### Gramatica:

- **bloque**:
	- SIMBOLO_ESPECIAL declaraciones SIMBOLO_ESPECIAL 
- **declaraciones**:
	- declaracion declaraciones 
	- declaracion
- **declaracion**: 
	- asignacion
	- funcion 
	- inclusion
	- retorno
- **operacion**:
	- valor SIMBOLO_ESPECIAL valor
- **valor**:
  - IDENTIFICADOR
  - NUMERO
- **asignacion** : 
  - RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL valor SIMBOLO_ESPECIAL
  - RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL
  - RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL valor SIMBOLO_ESPECIAL 
  - IDENTIFICADOR SIMBOLO_ESPECIAL operacion SIMBOLO_ESPECIAL
  - IDENTIFICADOR SIMBOLO_ESPECIAL valor
- **funcion**:
	- RESERVADO RESERVADO SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL bloque 
	- RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL 
	- RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL bloque
- **argumentos** :
	- argumento SIMBOLO_ESPECIAL argumentos
	- argumento
- **argumento** :
	- asignacion 
	- STRING 
	- referencia 
	- incremento 
	- IDENTIFICADOR
- **referencia**:
	- SIMBOLO_ESPECIAL IDENTIFICADOR
- **incremento**:
	- IDENTIFICADOR SIMBOLO_ESPECIAL
- **retorno**:
	- RESERVADO valor SIMBOLO_ESPECIAL
- **inclusion**:
	- RESERVADO RESERVADO

 ### Codigo en C a analizar
 <code> #include <stdio.h>
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
 </code>
 
### Con lo cual obtenemos la siguiente tabla
<table><thead><tr><th>Declaración</th><th>Tipo</th><th>Gramática</th></tr></thead><tbody><tr><td><code>#include &lt;stdio.h&gt;</code></td><td>inclusión</td><td><code>RESERVADO RESERVADO</code></td></tr><tr><td><code>int main(){ }</code></td><td>función</td><td><code>RESERVADO RESERVADO SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL bloque</code></td></tr><tr><td><code>int c; int n;</code></td><td>asignación</td><td><code>RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL</code></td></tr><tr><td><code>int fact = 1;</code></td><td>asignación</td><td><code>RESERVADO IDENTIFICADOR SIMBOLO_ESPECIAL valor SIMBOLO_ESPECIAL</code></td></tr><tr><td><code>printf( A );</code></td><td>función</td><td><code>RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL</code></td></tr><tr><td><code>"Ingrese el numero a calcular el factorial: \n"</code></td><td>argumentos</td><td><code>STRING</code></td></tr><tr><td><code>scanf( A );</code></td><td>función</td><td><code>RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL</code></td></tr><tr><td><code>"%d ", &amp;n</code></td><td>argumentos</td><td><code>argumento SIMBOLO_ESPECIAL argumentos</code></td></tr><tr><td><code>"%d "</code></td><td>argumento</td><td><code>STRING</code></td></tr><tr><td><code>&amp;n</code></td><td>referencia</td><td><code>SIMBOLO_ESPECIAL IDENTIFICADOR</code></td></tr><tr><td><code>for ( A ){ }</code></td><td>función</td><td><code>RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL bloque</code></td></tr><tr><td><code>c = 1; c &lt;= n; c++</code></td><td>argumentos</td><td><code>argumento SIMBOLO_ESPECIAL argumentos</code></td></tr><tr><td><code>c = 1</code></td><td>asignación</td><td><code>IDENTIFICADOR SIMBOLO_ESPECIAL valor</code></td></tr><tr><td><code>c &lt;= n</code></td><td>asignación</td><td><code>IDENTIFICADOR SIMBOLO_ESPECIAL valor</code></td></tr><tr><td><code>c++</code></td><td>incremento</td><td><code>IDENTIFICADOR SIMBOLO_ESPECIAL</code></td></tr><tr><td><code>fact = fact * c;</code></td><td>asignación</td><td><code>IDENTIFICADOR SIMBOLO_ESPECIAL operacion SIMBOLO_ESPECIAL</code></td></tr><tr><td><code>fact * c</code></td><td>operación</td><td><code>valor SIMBOLO_ESPECIAL valor</code></td></tr><tr><td><code>printf("El factorial de %d es: %d\n", n, fact);</code></td><td>función</td><td><code>RESERVADO SIMBOLO_ESPECIAL argumentos SIMBOLO_ESPECIAL SIMBOLO_ESPECIAL</code></td></tr><tr><td><code>return 0;</code></td><td>retorno</td><td><code>RESERVADO valor SIMBOLO_ESPECIAL</code></td></tr></tbody></table>