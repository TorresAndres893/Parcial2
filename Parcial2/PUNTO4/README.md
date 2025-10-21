# Parcial 2 - Punto 4

## Enunciado / Objetivo

4. Implemente un parser usando el algoritmo **CYK**.
   Realice pruebas sobre el rendimiento de este algoritmo comparándolo con un **parser de tipo predictivo LL(1)**.
   Finalmente, realice una **comparación del rendimiento** entre ambos parsers mediante gráficos.

---

## Requisitos

* Python 3.10 o superior
* Librerías necesarias:

  ```bash
  pip install matplotlib
  ```

---

## Archivos

* `comparacion_parsers.py`: Código fuente principal que implementa los dos parsers, ejecuta las pruebas y genera los gráficos.
* `comparacion_parsers.png`: Gráfica generada automáticamente con los resultados de rendimiento.

---

## Ejecución / Comandos

1. **Ejecutar el programa principal**:

   ```bash
   python comparacion_parsers.py
   ```

   * El programa genera cadenas aleatorias y mide el tiempo de ejecución de ambos algoritmos.

   * Muestra los resultados por consola en formato:

     ```
     Tamaño=  5 | CYK=0.000200s | Predictivo=0.000010s
     Tamaño= 10 | CYK=0.000800s | Predictivo=0.000012s
     Tamaño= 20 | CYK=0.003000s | Predictivo=0.000015s
     ...
     ```

   * También produce una gráfica comparativa guardada automáticamente como:

     ```
     comparacion_parsers.png
     ```

2. **Visualizar la gráfica**
   El gráfico muestra la relación entre el **tamaño de la cadena analizada** y el **tiempo de ejecución** de cada parser.

   * Eje X → Tamaño de la cadena.
   * Eje Y → Tiempo de ejecución promedio (en segundos).
   * Línea naranja → Parser CYK (crecimiento cúbico).
   * Línea azul → Parser Predictivo LL(1) (crecimiento lineal).

---

## Características

* **Parser CYK (Cocke–Younger–Kasami)**:

  * Analiza cadenas con una gramática en **Forma Normal de Chomsky (CNF)**.
  * Usa una **tabla triangular** para determinar si la cadena pertenece al lenguaje.
  * Complejidad: `O(n³)`.

* **Parser Predictivo LL(1)**:

  * Basado en una gramática de expresiones aritméticas simple (`E`, `T`, `F`).
  * Implementado mediante **pila y lookahead**.
  * Complejidad: `O(n)`.

* **Pruebas de rendimiento**:

  * Se ejecutan con distintos tamaños de entrada (`n = 5, 10, 20, 30, 40, 50, 80, 120`).
  * Se mide el tiempo promedio de 20 ejecuciones por tamaño.
  * Se grafica el crecimiento temporal de cada algoritmo.

---

## Conclusiones

* El **parser CYK** es más general (puede procesar cualquier gramática libre de contexto en CNF), pero su rendimiento decrece rápidamente con cadenas más largas debido a su complejidad cúbica.
* El **parser predictivo LL(1)** es mucho más eficiente y rápido, aunque requiere gramáticas adecuadas y sin ambigüedad.
* La gráfica confirma que el parser predictivo mantiene tiempos casi constantes, mientras que el parser CYK crece de forma exponencial.

---

## Notas

* Verificar instalación de Python:

  ```bash
  python --version
  ```

* Si no tienes entorno gráfico, puedes comentar la línea:

  ```python
  plt.show()
  ```

  para que solo se guarde el archivo `comparacion_parsers.png`.


---

¿Deseas que te genere este `README.md` como archivo descargable listo para incluir en tu entrega (por ejemplo, en formato Markdown o PDF)?

