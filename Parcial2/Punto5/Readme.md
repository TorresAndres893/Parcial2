# **Punto 5 - Analizador Descendente Recursivo**

## **Enunciado**

**5. Diseñe e implemente un algoritmo de emparejamiento para el algoritmo descendente recursivo.**


## **Ejecución**

```bash
python analizador_descendente.py
````

### **Resultados esperados**

```
Entrada: 'id + id * id'
Tokens: ['id', '+', 'id', '*', 'id']
Resultado: Sintaxis correcta

Entrada: '( id + id ) * id'
Tokens: ['(', 'id', '+', 'id', ')', '*', 'id']
Resultado: Sintaxis correcta

Entrada: 'id +'
Tokens: ['id', '+']
Resultado: Sintaxis incorrecta

Entrada: 'id * ( id )'
Tokens: ['id', '*', '(', 'id', ')']
Resultado: Sintaxis correcta

Entrada: '( id + id'
Tokens: ['(', 'id', '+', 'id']
Resultado: Sintaxis incorrecta
```

---

## **Características**

* **Lenguaje:** Python
* **Tipo de analizador:** Descendente Recursivo
* **Objetivo:** Validar expresiones aritméticas simples con `id`, `+`, `*`, `(` y `)`.
* **Método de análisis:** Coincidencias mediante operacion recursiva mediante funciones que implementan reglas gramaticales.
* **Tipo de gramática:** LL(1), sin recursión por la izquierda.

### **Gramática utilizada**

```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → id | ( E )
```

### **Entradas válidas**

* `id + id * id`
* `( id + id ) * id`
* `id * ( id )`

### **Entradas inválidas**

* `id +`
* `( id + id`

---

## **Conclusiones**

* El **analizador descendente recursivo** es una técnica eficaz para implementar parsers de gramáticas LL(1), ya que cada no terminal se traduce naturalmente en una función recursiva.
* El uso de un **algoritmo de emparejamiento** garantiza que los tokens sean procesados en orden y permite detectar errores de forma temprana.
* Esta implementación demuestra cómo la recursión permite representar la jerarquía de operadores y paréntesis sin necesidad de estructuras de control complejas.
* El analizador propuesto constituye una base sólida para la comprensión de procesos de **análisis sintáctico** en compiladores e intérpretes.

```


¿Quieres que le agregue una pequeña sección final con recomendaciones o posibles mejoras del analizador (por ejemplo, manejo de más operadores o mensajes de error detallados)?
```
