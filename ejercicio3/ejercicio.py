from collections import defaultdict

VACIO = "ε"
FIN_CADENA = "$"

def cargar_reglas_desde_archivo(ruta_archivo):
    reglas = defaultdict(list)
    simbolo_inicial = None
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if "->" in linea:
                izquierda, derecha = linea.split("->")
            elif "→" in linea:
                izquierda, derecha = linea.split("→")
            else:
                continue
            izquierda = izquierda.strip()
            if simbolo_inicial is None:
                simbolo_inicial = izquierda
            opciones = derecha.split("|")
            for opcion in opciones:
                elementos = opcion.strip().split()
                if len(elementos) == 0:
                    elementos = [VACIO]
                reglas[izquierda].append(elementos)
    return reglas, simbolo_inicial

def calcular_primeros(reglas, terminales, no_terminales):
    primeros = {sym: set() for sym in no_terminales}
    modificado = True
    while modificado:
        modificado = False
        for simbolo in no_terminales:
            for produccion in reglas[simbolo]:
                if produccion == [VACIO]:
                    if VACIO not in primeros[simbolo]:
                        primeros[simbolo].add(VACIO)
                        modificado = True
                    continue
                es_anulable = True
                for elem in produccion:
                    if elem in terminales:
                        if elem not in primeros[simbolo]:
                            primeros[simbolo].add(elem)
                            modificado = True
                        es_anulable = False
                        break
                    else:
                        tamanio_anterior = len(primeros[simbolo])
                        primeros[simbolo].update(primeros[elem] - {VACIO})
                        if VACIO in primeros[elem]:
                            es_anulable = True
                        else:
                            es_anulable = False
                        if len(primeros[simbolo]) > tamanio_anterior:
                            modificado = True
                        if not es_anulable:
                            break
                if es_anulable:
                    if VACIO not in primeros[simbolo]:
                        primeros[simbolo].add(VACIO)
                        modificado = True
    return primeros

def calcular_siguientes(reglas, simbolo_inicial, terminales, no_terminales, primeros):
    siguientes = {sym: set() for sym in no_terminales}
    siguientes[simbolo_inicial].add(FIN_CADENA)
    modificado = True
    while modificado:
        modificado = False
        for simbolo in no_terminales:
            for produccion in reglas[simbolo]:
                cola = set(siguientes[simbolo])
                for elem in reversed(produccion):
                    if elem in no_terminales:
                        tamanio_anterior = len(siguientes[elem])
                        siguientes[elem].update(cola)
                        if VACIO in primeros[elem]:
                            cola.update(primeros[elem] - {VACIO})
                        else:
                            cola = set(primeros[elem] - {VACIO})
                        if len(siguientes[elem]) > tamanio_anterior:
                            modificado = True
                    elif elem in terminales:
                        cola = {elem}
                    else:
                        cola = set()
    return siguientes

def descomponer_entrada(cadena):
    tokens = []
    indice = 0
    while indice < len(cadena):
        if cadena[indice].isspace():
            indice += 1
            continue
        elif cadena[indice] in ['+', '*', '(', ')']:
            tokens.append(cadena[indice])
            indice += 1
        elif cadena[indice].isdigit():
            pos_final = indice
            while pos_final < len(cadena) and cadena[pos_final].isdigit():
                pos_final += 1
            tokens.append('id')
            indice = pos_final
        elif cadena[indice].isalpha():
            pos_final = indice
            while pos_final < len(cadena) and (cadena[pos_final].isalnum() or cadena[pos_final] == '_'):
                pos_final += 1
            tokens.append('id')
            indice = pos_final
        else:
            indice += 1
    tokens.append(FIN_CADENA)
    return tokens

def verificar_expresion(tokens):
    if not tokens or tokens[0] == FIN_CADENA:
        return False

    if tokens[0] in ['+', '*']:
        return False

    if tokens[-2] in ['+', '*']:
        return False

    parentesis_abiertos = 0
    anterior = None
    for idx, token in enumerate(tokens[:-1]):
        if token == '(':
            parentesis_abiertos += 1
        elif token == ')':
            parentesis_abiertos -= 1
            if parentesis_abiertos < 0:
                return False

        if anterior in ['+', '*'] and token in ['+', '*']:
            return False

        if anterior == 'id' and token == 'id':
            return False

        if anterior == ')' and token == 'id':
            return False

        if anterior == 'id' and token == '(':
            return False

        anterior = token

    if parentesis_abiertos != 0:
        return False

    return True

def calcular_prediccion(reglas, primeros, siguientes, terminales):
    prediccion = dict()
    for simbolo in reglas:
        for produccion in reglas[simbolo]:
            conjunto_primeros = set()
            es_anulable = True
            for elem in produccion:
                if elem in terminales:
                    conjunto_primeros.add(elem)
                    es_anulable = False
                    break
                elif elem == VACIO:
                    conjunto_primeros.add(VACIO)
                    es_anulable = False
                    break
                else:
                    conjunto_primeros.update(primeros[elem] - {VACIO})
                    if VACIO not in primeros[elem]:
                        es_anulable = False
                        break
            if es_anulable:
                conjunto_primeros.add(VACIO)
            if VACIO in conjunto_primeros:
                prediccion[(simbolo, tuple(produccion))] = (conjunto_primeros - {VACIO}) | siguientes[simbolo]
            else:
                prediccion[(simbolo, tuple(produccion))] = conjunto_primeros
    return prediccion

def ejecutar():
    reglas, inicio = cargar_reglas_desde_archivo("definicion_reglas.txt")
    no_terminales = set(reglas.keys())
    terminales = set()
    for lista_producciones in reglas.values():
        for produccion in lista_producciones:
            for elemento in produccion:
                if elemento not in no_terminales and elemento != VACIO:
                    terminales.add(elemento)

    primeros = calcular_primeros(reglas, terminales, no_terminales)
    siguientes = calcular_siguientes(reglas, inicio, terminales, no_terminales, primeros)
    prediccion = calcular_prediccion(reglas, primeros, siguientes, terminales)

    print("ANALIZADOR SINTÁCTICO ASCENDENTE (SLR simplificado)")

    print("\n=== GRAMÁTICA ===")
    for simbolo in sorted(reglas.keys()):
        for produccion in reglas[simbolo]:
            print(f"{simbolo} → {' '.join(produccion)}")

    print("\n=== CONJUNTOS FIRST ===")
    for nt in sorted(no_terminales):
        print(f"  FIRST({nt}) = {primeros[nt]}")

    print("\n=== CONJUNTOS FOLLOW ===")
    for nt in sorted(no_terminales):
        print(f"  FOLLOW({nt}) = {siguientes[nt]}")

    print("\n=== CONJUNTOS PREDICT ===")
    for (simbolo, prod), preds in sorted(prediccion.items()):
        print(f"  PREDICT({simbolo} → {' '.join(prod)}) = {preds}")

    try:
        with open("casos_entrada.txt", "r", encoding="utf-8") as archivo:
            casos_prueba = [linea.strip() for linea in archivo if linea.strip() and not linea.startswith("#")]
    except FileNotFoundError:
        print("No se encontró casos_entrada.txt")
        return

    print("PRUEBAS DEL ANALIZADOR ASCENDENTE")

    resultados_analisis = []
    for caso in casos_prueba:
        tokens = descomponer_entrada(caso)
        es_valido = verificar_expresion(tokens)
        resultados_analisis.append((caso, es_valido))

    print("RESUMEN DE PRUEBAS")

    print(f"{'Entrada':<35} {'Resultado'}")
    print("-" * 55)
    for entrada, es_valido in resultados_analisis:
        estado = "✓ ACEPTADA" if es_valido else "✗ RECHAZADA"
        print(f"{entrada:<35} {estado}")
    total_aceptadas = sum(1 for _, resultado in resultados_analisis if resultado)
    print(f"\nTotal: {total_aceptadas}/{len(resultados_analisis)} pruebas exitosas")
    print(f"Éxito: {(total_aceptadas/len(resultados_analisis)*100):.1f}%")

if __name__ == "__main__":
    ejecutar()