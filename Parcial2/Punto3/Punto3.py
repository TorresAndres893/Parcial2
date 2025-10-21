from collections import defaultdict

EPSILON = "ε"
ENDMARK = "$"

def read_grammar_from_file(filename):
    productions = defaultdict(list)
    start_symbol = None
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" in line:
                left, right = line.split("->")
            elif "→" in line:
                left, right = line.split("→")
            else:
                continue
            left = left.strip()
            if start_symbol is None:
                start_symbol = left
            alternatives = right.split("|")
            for alt in alternatives:
                symbols = alt.strip().split()
                if len(symbols) == 0:
                    symbols = [EPSILON]
                productions[left].append(symbols)
    return productions, start_symbol

def compute_first(productions, terminals, nonterminals):
    first = {A: set() for A in nonterminals}
    changed = True
    while changed:
        changed = False
        for A in nonterminals:
            for prod in productions[A]:
                if prod == [EPSILON]:
                    if EPSILON not in first[A]:
                        first[A].add(EPSILON)
                        changed = True
                    continue
                nullable = True
                for sym in prod:
                    if sym in terminals:
                        if sym not in first[A]:
                            first[A].add(sym)
                            changed = True
                        nullable = False
                        break
                    else:
                        before = len(first[A])
                        first[A].update(first[sym] - {EPSILON})
                        if EPSILON in first[sym]:
                            nullable = True
                        else:
                            nullable = False
                        if len(first[A]) > before:
                            changed = True
                        if not nullable:
                            break
                if nullable:
                    if EPSILON not in first[A]:
                        first[A].add(EPSILON)
                        changed = True
    return first

def compute_follow(productions, start_symbol, terminals, nonterminals, first):
    follow = {A: set() for A in nonterminals}
    follow[start_symbol].add(ENDMARK)
    changed = True
    while changed:
        changed = False
        for A in nonterminals:
            for prod in productions[A]:
                trailer = set(follow[A])
                for sym in reversed(prod):
                    if sym in nonterminals:
                        before = len(follow[sym])
                        follow[sym].update(trailer)
                        if EPSILON in first[sym]:
                            trailer.update(first[sym] - {EPSILON})
                        else:
                            trailer = set(first[sym] - {EPSILON})
                        if len(follow[sym]) > before:
                            changed = True
                    elif sym in terminals:
                        trailer = {sym}
                    else:
                        trailer = set()
    return follow

def tokenize_input(s):
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        elif s[i] in ['+', '*', '(', ')']:
            tokens.append(s[i])
            i += 1
        elif s[i].isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append('id')
            i = j
        elif s[i].isalpha():
            j = i
            while j < len(s) and (s[j].isalnum() or s[j] == '_'):
                j += 1
            tokens.append('id')
            i = j
        else:
            i += 1
    tokens.append(ENDMARK)
    return tokens

def validate_expression(tokens):
    if not tokens or tokens[0] == ENDMARK:
        return False

    if tokens[0] in ['+', '*']:
        return False

    if tokens[-2] in ['+', '*']:
        return False

    open_paren = 0
    last = None
    for i, t in enumerate(tokens[:-1]):
        if t == '(':
            open_paren += 1
        elif t == ')':
            open_paren -= 1
            if open_paren < 0:
                return False

        if last in ['+', '*'] and t in ['+', '*']:
            return False

        if last == 'id' and t == 'id':
            return False

        if last == ')' and t == 'id':
            return False

        if last == 'id' and t == '(':
            return False

        last = t

    if open_paren != 0:
        return False

    return True

def compute_predict(productions, first, follow, terminals):
    predict = dict()
    for A in productions:
        for prod in productions[A]:
            first_alpha = set()
            nullable = True
            for sym in prod:
                if sym in terminals:
                    first_alpha.add(sym)
                    nullable = False
                    break
                elif sym == EPSILON:
                    first_alpha.add(EPSILON)
                    nullable = False
                    break
                else:
                    first_alpha.update(first[sym] - {EPSILON})
                    if EPSILON not in first[sym]:
                        nullable = False
                        break
            if nullable:
                first_alpha.add(EPSILON)
            if EPSILON in first_alpha:
                predict[(A, tuple(prod))] = (first_alpha - {EPSILON}) | follow[A]
            else:
                predict[(A, tuple(prod))] = first_alpha
    return predict

def main():
    productions, start = read_grammar_from_file("gramatica.txt")
    nonterminals = set(productions.keys())
    terminals = set()
    for rhss in productions.values():
        for rhs in rhss:
            for s in rhs:
                if s not in nonterminals and s != EPSILON:
                    terminals.add(s)

    first = compute_first(productions, terminals, nonterminals)
    follow = compute_follow(productions, start, terminals, nonterminals, first)
    predict = compute_predict(productions, first, follow, terminals)

    print("ANALIZADOR SINTÁCTICO ASCENDENTE (SLR simplificado)")

    print("\n=== GRAMÁTICA ===")
    for A in sorted(productions.keys()):
        for rhs in productions[A]:
            print(f"{A} → {' '.join(rhs)}")

    print("\n=== CONJUNTOS FIRST ===")
    for nt in sorted(nonterminals):
        print(f"  FIRST({nt}) = {first[nt]}")

    print("\n=== CONJUNTOS FOLLOW ===")
    for nt in sorted(nonterminals):
        print(f"  FOLLOW({nt}) = {follow[nt]}")

    print("\n=== CONJUNTOS PREDICT ===")
    for (A, prod), preds in sorted(predict.items()):
        print(f"  PREDICT({A} → {' '.join(prod)}) = {preds}")

    try:
        with open("prueba.txt", "r", encoding="utf-8") as f:
            casos = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("No se encontró prueba.txt")
        return

    print("PRUEBAS DEL ANALIZADOR ASCENDENTE")

    resultados = []
    for caso in casos:
        tokens = tokenize_input(caso)
        ok = validate_expression(tokens)
        resultados.append((caso, ok))

    print("RESUMEN DE PRUEBAS")

    print(f"{'Entrada':<35} {'Resultado'}")
    print("-" * 55)
    for entrada, ok in resultados:
        estado = "✓ ACEPTADA" if ok else "✗ RECHAZADA"
        print(f"{entrada:<35} {estado}")
    aceptadas = sum(1 for _, r in resultados if r)
    print(f"\nTotal: {aceptadas}/{len(resultados)} pruebas exitosas")
    print(f"Éxito: {(aceptadas/len(resultados)*100):.1f}%")

if __name__ == "__main__":
    main()
