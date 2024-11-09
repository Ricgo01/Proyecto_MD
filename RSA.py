# Universidad del Valle de Guatemala
# Facultad de Matematica 
# Matematica Discreta 
# Proyecto 2 - Criptografia con RSA
# 
# Autores:
#   Ricardo Godinez - 23247
#   Vianka Castro - 23201
# 
# Fecha:
#   9/11/2024
# #
import random
import sympy
import numpy as np


#Genera un numero primo de un rango exclusivo 
def generar_primo(rango_inferior, rango_superior):
    lista_Primos = list(sympy.primerange(rango_inferior,rango_superior +1))

    if lista_Primos: 
        return random.choice(lista_Primos)
    
    else:
        print("Error, no se pude encontrar un numero primo en el rango seleccionado")
        return None

# Calcula el máximo común divisor (MCD) de dos números usando el algoritmo de Euclides
def mcd(a, b):
    if b == 0:
        return abs(a) 
    r = a % b
    while r != 0:
        a = b
        b = r
        r = a % b 
    return abs(b) 

# Calcula los coeficientes de Bézout para dos números a y b
def bezout(a, b):
    M = np.array([[1, 0], [0, 1]])

    while b != 0:
        c = a // b
        T = np.array([[-c, 1],
                      [1, 0]])

        M = np.dot(M, T)

        a0 = a
        b0 = b

        a = b0
        b = a0 % b0

    y = M[0, 1]
    x = M[1, 1]
    
    return a, x, y

# Calcula el inverso modular de 'e' módulo 'n' utilizando los coeficientes de Bézout
def inverso_modular(e, n):
    mcd, x, y = bezout(e, n) 

    if mcd != 1:
        print("No existe un inverso modular porque e y n no son coprimos")
        return None

    if x < 0:
        x += n

    return x

# Genera un par de claves RSA (pública y privada) en base a un rango para seleccionar números primos
def generar_llaves(rango_inferior, rango_superior):

    p = q = generar_primo(rango_inferior, rango_superior)
    while p == q:
        q = generar_primo(rango_inferior, rango_superior)

    n = p * q 
    tot = (p - 1) * (q - 1)

    e = random.randint(2, tot - 1)
    while mcd(e, tot) != 1:
        e = random.randint(2, tot - 1)

    d = inverso_modular(e, tot)
    if d is None:
        return "Error: No se pudo encontrar el inverso modular"

    tupla_pub = (int(e), int(n))
    tupla_priv = (int(d), int(n))
    return tupla_pub, tupla_priv
    
# Encripta un mensaje usando la clave pública
def encriptar(caracter, llave_publica):
    e, n = llave_publica
    
    if caracter >= n:
        print("Error: El mensaje es muy largo para ser encriptado")
        return None
    
    caracter_encriptado = pow(caracter, e, n)
    return caracter_encriptado
        
# Desencripta un mensaje cifrado usando la clave privada
def desencriptar(mensaje_encriptado, llave_privada):
    d,n = llave_privada
    
    if mensaje_encriptado >= n:
        print("Error: El mensaje encriptado es incorrecto")
        return None
    
    mensaje_desencriptado = pow(mensaje_encriptado, d, n)
    return mensaje_desencriptado

def main():
    llave_publica = None
    llave_privada = None
    mensaje_encriptado = None

    while True:
        print("\n===== Programa RSA =====")
        print("MENU")
        print("1. Iniciar")
        print("2. Salir")

        opcion = input("Ingrese una opcion > ")

        if opcion == "1":
            print("----- Generar Llaves ----")
            rango_inferior = int(input("Ingrese el rango inferior > "))
            rango_superior = int(input("Ingrese el rango superior > "))
            llave_publica, llave_privada = generar_llaves(rango_inferior, rango_superior)
            
            if llave_publica and llave_privada:
                print("Llave publica:", llave_publica)
                print("Llave privada:", llave_privada)

                # Encriptar e
                mensaje = int(input("Ingresa el mensaje a encriptar : "))
                mensaje_encriptado = encriptar(mensaje, llave_publica)
                if mensaje_encriptado is not None:
                    print("Mensaje encriptado:", mensaje_encriptado)

                # Desencriptar
                mensaje_descifrado = desencriptar(mensaje_encriptado, llave_privada)
                if mensaje_descifrado is not None:
                    print("Mensaje desencriptado:", mensaje_descifrado)

        elif opcion == "2":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

main()