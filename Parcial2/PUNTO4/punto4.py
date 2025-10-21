

import time
import random
import statistics
import matplotlib.pyplot as plt



gramatica_cyk = {
    'S': [['A', 'B'], ['B', 'C']],
    'A': [['B', 'A'], ['a']],
    'B': [['C', 'C'], ['b']],
    'C': [['A', 'B'], ['a']]
}

def parser_cyk(gramatica, cadena):

    n = len(cadena)
    if n == 0:
        return False  
    tabla = [[set() for _ in range(n)] for _ in range(n)]

    for i, simbolo in enumerate(cadena):
        for izquierda, reglas in gramatica.items():
            for derecha in reglas:
                if len(derecha) == 1 and derecha[0] == simbolo:
                    tabla[i][i].add(izquierda)

    for longitud in range(2, n + 1):
        for i in range(0, n - longitud + 1):
            j = i + longitud - 1
            for k in range(i, j):
                for izquierda, reglas in gramatica.items():
                    for derecha in reglas:
                        if len(derecha) == 2:
                            B, C = derecha
                            if B in tabla[i][k] and C in tabla[k + 1][j]:
                                tabla[i][j].add(izquierda)

    return 'S' in tabla[0][n - 1]

def parser_predictivo(tokens):
  
    pila = ['E']  
    indice = 0
    n = len(tokens)

    while pila:
        cima = pila.pop()

        if cima == 'ε':
            continue

        if cima in ['+', '*', '(', ')', 'id']:
            if indice < n and tokens[indice] == cima:
                indice += 1
            else:
                return False
        else:

            actual = tokens[indice] if indice < n else None

            if cima == 'E':
                pila.extend(['E\'', 'T'])
            elif cima == 'E\'':
                if actual == '+':
                    pila.extend(['E\'', 'T', '+'])
                else:
                    pila.append('ε')
            elif cima == 'T':
                pila.extend(['T\'', 'F'])
            elif cima == 'T\'':
                if actual == '*':
                    pila.extend(['T\'', 'F', '*'])
                else:
                    pila.append('ε')
            elif cima == 'F':
                if actual == '(':
                    pila.extend([')', 'E', '('])
                elif actual == 'id':
                    pila.append('id')
                else:
                    return False
            else:
                return False

    return indice == n

def generar_cadena_terminal(longitud):
    return ''.join(random.choice(['a', 'b']) for _ in range(longitud))

def generar_tokens_expresion(longitud):

    tokens = []
    for _ in range(longitud):
        tokens.append('id')
        if random.random() < 0.4:
            tokens.append(random.choice(['+', '*']))
    return tokens

def medir_rendimiento(tamanos, repeticiones=10, semilla=0):
    
    random.seed(semilla)
    tiempos_cyk = []
    tiempos_predictivo = []

    for tam in tamanos:
        lista_cyk = []
        lista_pred = []

        for _ in range(repeticiones):
            cadena = generar_cadena_terminal(tam)

            t0 = time.perf_counter()
            parser_cyk(gramatica_cyk, cadena)
            t1 = time.perf_counter()
            lista_cyk.append(t1 - t0)

            tokens = generar_tokens_expresion(max(1, tam // 2))
            t0 = time.perf_counter()
            parser_predictivo(tokens)
            t1 = time.perf_counter()
            lista_pred.append(t1 - t0)

        tiempos_cyk.append(statistics.mean(lista_cyk))
        tiempos_predictivo.append(statistics.mean(lista_pred))

    return tiempos_cyk, tiempos_predictivo

def main():
    tamanos = [5, 10, 20, 30, 40, 50, 80, 120]
    repeticiones = 20

    print("⏳ Midiendo tiempos de ejecución... Por favor espere.")
    tiempos_cyk, tiempos_pred = medir_rendimiento(tamanos, repeticiones)

    print("\nResultados (tiempos promedio en segundos):")
    for tam, tcyk, tpred in zip(tamanos, tiempos_cyk, tiempos_pred):
        print(f" Tamaño={tam:3d} | CYK={tcyk:.6f}s | Predictivo={tpred:.6f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(tamanos, tiempos_cyk, marker='o', label='Parser CYK')
    plt.plot(tamanos, tiempos_pred, marker='s', label='Parser Predictivo LL(1)')
    plt.title('Comparación de rendimiento entre CYK y Parser Predictivo LL(1)')
    plt.xlabel('Tamaño de la cadena / referencia')
    plt.ylabel('Tiempo de ejecución (s) (promedio)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    nombre_archivo = 'comparacion_parsers.png'
    plt.savefig(nombre_archivo, dpi=150)
    print(f"\n📊 Gráfica guardada como: {nombre_archivo}")

    plt.show()

if __name__ == '__main__':
    main()
