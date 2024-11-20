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
#   19/11/2024
#
# Descripción del Proyecto:
# Este programa implementa el algoritmo RSA, un sistema de criptografía asimétrica
# que utiliza números primos para generar claves públicas y privadas, permitiendo
# cifrar y descifrar mensajes de manera segura.
# #
import random
import sympy
import numpy as np


# Genera un número primo dentro de un rango dado
# Parámetros:
#   rango_inferior (int): límite inferior del rango.
#   rango_superior (int): límite superior del rango.
# Retorna:
#   int: un número primo aleatorio dentro del rango, o None si no hay primos disponibles.
def generar_primo(rango_inferior, rango_superior):
    lista_Primos = list(sympy.primerange(rango_inferior,rango_superior +1))

    if lista_Primos: 
        return random.choice(lista_Primos)
    
    else:
        print("Error, no se pude encontrar un numero primo en el rango seleccionado")
        return None

# Calcula el máximo común divisor (MCD) de dos números utilizando el algoritmo de Euclides.
# Parámetros:
#   a (int): primer número.
#   b (int): segundo número.
# Retorna:
#   int: el MCD de a y b.
def mcd(a, b):
    if b == 0:
        return abs(a) 
    r = a % b
    while r != 0:
        a = b
        b = r
        r = a % b 
    return abs(b) 


# Calcula los coeficientes de Bézout para dos números.
# Parámetros:
#   a (int): primer número.
#   b (int): segundo número.
# Retorna:
#   (int, int, int): el MCD de a y b, y los coeficientes de Bézout x e y.
def bezout(a, b):
    M = np.array([[1, 0], [0, 1]])  # Matriz identidad para mantener el estado de los coeficientes.

    while b != 0:
        c = a // b
        T = np.array([[-c, 1],
                      [1, 0]]) # Transformación lineal.

        M = np.dot(M, T)

        a0 = a
        b0 = b

        a = b0
        b = a0 % b0

    y = M[0, 1]
    x = M[1, 1]
    
    return a, x, y


# Calcula el inverso modular de un número dado.
# Parámetros:
#   e (int): número para el cual se calcula el inverso.
#   n (int): módulo.
# Retorna:
#   int: el inverso modular de e módulo n, o None si no existe.
def inverso_modular(e, n):
    mcd, x, y = bezout(e, n) 

    if mcd != 1:
        print("No existe un inverso modular porque e y n no son coprimos")
        return None

    if x < 0:
        x += n # Ajusta el valor del inverso para que sea positivo.

    return x

# Genera un par de claves RSA (pública y privada).
# Parámetros:
#   rango_inferior (int): límite inferior del rango para los números primos.
#   rango_superior (int): límite superior del rango para los números primos.
# Retorna:
#   (tuple, tuple): las claves pública y privada.
def generar_llaves(rango_inferior, rango_superior):

    p = q = generar_primo(rango_inferior, rango_superior)
    while p == q:  # Asegura que p y q sean distintos.
        q = generar_primo(rango_inferior, rango_superior)

    n = p * q  
    tot = (p - 1) * (q - 1)  # Función totient de Euler.

    e = random.randint(2, tot - 1) 
    while mcd(e, tot) != 1:  # Encuentra un e coprimo con tot.
        e = random.randint(2, tot - 1)

    d = inverso_modular(e, tot)
    if d is None:
        return "Error: No se pudo encontrar el inverso modular"

    tupla_pub = (int(e), int(n))
    tupla_priv = (int(d), int(n))
    return tupla_pub, tupla_priv
    
# Cifra un mensaje usando la clave pública.
# Parámetros:
#   caracter (int): mensaje a cifrar (en forma de número entero).
#   llave_publica (tuple): clave pública (e, n).
# Retorna:
#   int: el mensaje cifrado, o None si el mensaje es demasiado grande.
def encriptar(caracter, llave_publica):
    e, n = llave_publica
    
    if caracter >= n:
        print("Error: El mensaje es muy largo para ser encriptado")
        return None
    
    caracter_encriptado = pow(caracter, e, n)
    return caracter_encriptado
        

# Descifra un mensaje cifrado usando la clave privada.
# Parámetros:
#   mensaje_encriptado (int): mensaje cifrado.
#   llave_privada (tuple): clave privada (d, n).
# Retorna:
#   int: el mensaje original descifrado, o None si el mensaje cifrado es inválido.
def desencriptar(mensaje_encriptado, llave_privada):
    d,n = llave_privada
    
    if mensaje_encriptado >= n:
        print("Error: El mensaje encriptado es incorrecto")
        return None
    
    mensaje_desencriptado = pow(mensaje_encriptado, d, n)
    return mensaje_desencriptado

# Función principal que implementa la interacción con el usuario.
# Permite generar claves, cifrar y descifrar mensajes.
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