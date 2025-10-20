import re

class AnalizadorDescendenteRecursivo:
    def __init__(self, entrada):
        self.tokens = self.tokenizar(entrada)
        self.posicion = 0 #posicion de token 

    def tokenizar(self, entrada):
        tokens = []
        entrada = entrada.strip()
        i = 0
        while i < len(entrada):
            caracter = entrada[i]
            if caracter.isspace():
                i += 1
                continue
            if caracter.isalpha():
                j = i
                while j < len(entrada) and entrada[j].isalnum():
                    j += 1
                tokens.append('id') #se guarda el is
                i = j
            elif caracter in ['+', '*', '(', ')']: #se guarda el simbolo
                tokens.append(caracter)
                i += 1
            else:
                raise ValueError(f"Carácter no válido: {caracter}")
        return tokens

    def emparejar(self, esperado):# busca coincidencia en los tokenes 
        if self.posicion < len(self.tokens) and self.tokens[self.posicion] == esperado:
            self.posicion += 1
            return True
        return False

    def analizar_E(self): # regla par E.
        posicion_inicial = self.posicion
        if self.analizar_T() and self.analizar_E_prima():
            return True
        self.posicion = posicion_inicial
        return False

    def analizar_E_prima(self):# regla prara E'
        posicion_inicial = self.posicion
        if self.emparejar('+'):
            if self.analizar_T() and self.analizar_E_prima():
                return True
            self.posicion = posicion_inicial
            return False
        return True

    def analizar_T(self): #Regla para T
        posicion_inicial = self.posicion
        if self.analizar_F() and self.analizar_T_prima():
            return True
        self.posicion = posicion_inicial
        return False

    def analizar_T_prima(self): #Regla para T'
        posicion_inicial = self.posicion
        if self.emparejar('*'):
            if self.analizar_F() and self.analizar_T_prima():
                return True
            self.posicion = posicion_inicial
            return False
        return True

    def analizar_F(self): #regla para F
        posicion_inicial = self.posicion
        if self.emparejar('id'):
            return True
        if self.emparejar('('):
            if self.analizar_E() and self.emparejar(')'):
                return True
            self.posicion = posicion_inicial
        return False

    def analizar(self): # Entrada valida
        resultado = self.analizar_E()
        return resultado and self.posicion == len(self.tokens)

def probar_analizador(entrada):
    try:
        analizador = AnalizadorDescendenteRecursivo(entrada)
        print(f"Entrada: '{entrada}'")
        print(f"Tokens: {analizador.tokens}")
        if analizador.analizar():
            print("Resultado: Sintaxis correcta")
        else:
            print("Resultado: Sintaxis incorrecta")
    except ValueError as e:
        print(f"Resultado: Error - {e}")
#Pruebas del parse
probar_analizador("id + id * id") #Resultado: Correcto
probar_analizador("( id + id ) * id") #Resultado: Correcto
probar_analizador("id +") #Resultado: Incorrecto
probar_analizador("id * ( id )") #Resultado: Correcto
probar_analizador("( id + id") #Resultado: Incorrecto

