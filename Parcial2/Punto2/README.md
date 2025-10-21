# Parcial 2 - Punto 1 y 2

## Enunciado/objetivo

El objetivo del Punto 1 es diseñar una gramática en notación BNF para un lenguaje de programación que soporte operaciones CRUD (Create, Read, Update, Delete) en una base de datos relacional. La gramática debe cubrir la creación de tablas, inserción de registros, consultas, actualizaciones y eliminaciones, con soporte para listas de campos, valores, condiciones lógicas y operadores relacionales.

El Punto 2 consiste en implementar la gramática del Punto 1 usando ANTLR, generar el parser y realizar pruebas con sentencias válidas e inválidas para verificar el funcionamiento del analizador sintáctico.

Esta solución implementa una gramática simple inspirada en SQL, adaptada para un lenguaje de programación general, y usa ANTLR para el parser.

## Requisitos

- Java (JDK 17 o superior)
- Entorno con soporte gráfico (para `-gui`, opcional; si no, usa `-tree` para salida textual)

## Archivos

- `Grama2.g4`: Gramática ANTLR que define las operaciones CRUD (Punto 1 y 2).
- `antlr-4.13.2-complete.jar`: Biblioteca ANTLR para generar y ejecutar el parser.
- `test.txt`: Archivo con sentencias CRUD válidas para pruebas.
- `test_invalid.txt`: Archivo con una sentencia inválida para verificar errores.
- `README.md`: Este archivo con instrucciones.

## Ejecución / comandos

1. **Generar el parser con ANTLR**:
   ```bash
   java -jar antlr-4.13.2-complete.jar Grama2.g4
   ```
   - Esto crea archivos Java como `Grama2Parser.java` y `Grama2Lexer.java`.

2. **Compilar los archivos generados**:
   ```bash
   javac -cp antlr-4.13.2-complete.jar *.java
   ```
   - Compila el parser y lexer.

3. **Probar sentencias válidas (Punto 2)**:
   ```bash
   java -cp antlr-4.13.2-complete.jar:. org.antlr.v4.gui.TestRig Grama2 programa -gui < test.txt
   ```
   - Muestra un árbol gráfico de análisis para las sentencias CRUD válidas.
   - Si no tienes entorno gráfico, usa:
     ```bash
     java -cp antlr-4.13.2-complete.jar:. org.antlr.v4.gui.TestRig Grama2 programa -tree < test.txt
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
   java -cp antlr-4.13.2-complete.jar:. org.antlr.v4.gui.TestRig Grama2 programa -tokens < test_invalid.txt
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
  - Gramática en formato ANTLR 4 (`Grama2.g4`), con tokens para palabras clave y símbolos.
  - Parser generado que produce árboles de análisis sintáctico.
  - Pruebas cubren casos válidos (todas las CRUD) e inválidos (falta `listaCampos` en `SELECT`).
  - Maneja espacios en blanco y errores de sintaxis con mensajes claros.

- **Ventajas**:
  - La gramática es extensible (fácil agregar más operadores o tipos de datos).
  - ANTLR genera código eficiente y soporta visualización gráfica de árboles.

## Conclusiones

La gramática diseñada en el Punto 1 cumple con los requisitos para un lenguaje básico de operaciones CRUD, permitiendo estructuras SQL-like simples pero robustas para bases de datos relacionales. El Punto 2 demuestra que ANTLR es una herramienta efectiva para implementar y probar gramáticas complejas, generando un parser que valida sintaxis de manera precisa y eficiente. Las pruebas confirman que el parser acepta sentencias válidas y rechaza inválidas, validando el diseño. En general, esta solución proporciona una base sólida para un lenguaje de programación enfocado en bases de datos, con potencial para extensiones como joins o transacciones.

## Notas

- Verificar instalación de Java:
  ```bash
  java -version
  ```
- Contribuyeron: [Lista de colaboradores, ej. @usuario1, @usuario2].
- Licencia: MIT (libre para uso educativo).
---


