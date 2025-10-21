# Parcial 2 - Punto 1 y 2

## Enunciado/objetivo

1. Diseñe una gramatico de un lenguaje de programacion que permita hacer las opceraciones CRUD en una base de datos.

2. Implementacion la gramatica del punto 1 en BISON o ANTLR4 y realice pruebas de lenguaje.

## Requisitos

- Java (JDK 17 o superior)
- Entorno con soporte gráfico (para `-gui`, opcional; si no, usa `-tree` para salida textual)

## Archivos

- `Grama2.g4`: Gramática ANTLR que define las operaciones CRUD (Punto 1 y 2).
- `antlr-4.13.2-complete.jar`: Biblioteca ANTLR para generar y ejecutar el parser.
- `Prueba1.txt`: Archivo con sentencias CRUD válidas para pruebas.
- `Prueba2.txt`: Archivo con una sentencia inválida para verificar errores.
- `README.md`: Este archivo con instrucciones.

## Ejecución / comandos

1. **Generar el parser con ANTLR**:
   ```bash
   java -jar antlr-4.13.2-complete.jar Grama2.g4
   ```
   - Se generaran los archivos Java `Grama2Parser.java` y `Grama2Lexer.java`.

2. **Compilar los archivos generados**:
   ```bash
   javac -cp antlr-4.13.2-complete.jar *.java
   ```
   - Compila el parser y lexer.

3. **Probar sentencias válidas (Punto 2)**:
   ```bash
   java -cp antlr-4.13.2-complete.jar:. org.antlr.v4.gui.TestRig Grama2 programa -gui < Prueba1.txt
   ```
   - Muestra un árbol gráfico de análisis para las sentencias CRUD válidas.
   - Si no tienes entorno gráfico, usa:
     ```bash
     java -cp antlr-4.13.2-complete.jar:. org.antlr.v4.gui.TestRig Grama2 programa -tree < Prueba1.txt
     ```
   - Contenido de `test.txt` (ejemplos CRUD):
     ```
     CREATE TABLE usuarios (id, nombre);
     INSERT INTO usuarios (id, nombre) VALUES (1, 'Juan');
     SELECT id, nombre FROM usuarios WHERE id = 1;
     UPDATE usuarios SET nombre = 'Pedro', edad = 25 WHERE id = 1;
     DELETE FROM usuarios WHERE id = 1;
     DROP TABLE usuarios;
     ```

4. **Probar sentencia inválida (Punto 2)**:
   ```bash
   java -cp antlr-4.13.2-complete.jar:. org.antlr.v4.gui.TestRig Grama2 programa -tokens < Prueba2.txt
   ```
   - Muestra tokens y un error de sintaxis para `SELECT FROM usuarios;`.
   - Salida esperada:
     ```
     line 1:7 mismatched input 'FROM' expecting ID
     ```

5. **Limpieza (opcional)**:
   ```bash
   rm *.java *.class *.tokens *.interp
   ```
   - Elimina archivos generados para mantener el directorio limpio.

## Características

- **Punto 1 (Gramática)**:
  - Soporta operaciones CRUD: `CREATE TABLE`, `INSERT INTO`, `SELECT`, `UPDATE`, `DELETE FROM`, `DROP TABLE`.
  - Maneja listas de campos (`id, nombre`), valores (`1, 'Juan'`), asignaciones (`nombre = 'Pedro'`), y condiciones (`id = 1 AND nombre = 'Juan'`).
  - Operadores relacionales: `=`, `!=`, `>`, `<`, `>=`, `<=`.
  - Valores: números, cadenas entre comillas simples, booleanos (`TRUE`, `FALSE`).
  - La gramática es libre de recursividad izquierda en condiciones usando `condicionSimple`.

- **Punto 2 (Implementación ANTLR)**:
  - Gramática en formato ANTLR 4 (`Grama2.g4`).
  - Parser generado que produce árboles de análisis sintáctico.
  - Pruebas cubren casos válidos e inválidos.

- **Ventajas**:
  - La gramática es extensible (fácil agregar más operadores o tipos de datos).
  - ANTLR genera código eficiente y soporta visualización gráfica de árboles.

## Conclusiones

La gramática diseñada en el Punto 1 cumple con los requisitos para un lenguaje básico de operaciones CRUD para bases de datos relacionales.
El Punto 2 el uso de ANTLR como herramienta para implementar y probar gramáticas complejas, generando un parser que valida sintaxis de manera precisa y eficiente. 
Las pruebas se realizan con el fin que el parser acepta sentencias válidas y rechaza inválidas.

## Notas

- Verificar instalación de Java:
  ```bash
  java -version
  ```
- Contribuyeron: [Lista de colaboradores, ej. @usuario1, @usuario2].
- Licencia: MIT (libre para uso educativo).
---


