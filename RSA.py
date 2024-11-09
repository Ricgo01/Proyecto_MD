import random
import sympy
import numpy as np

def generar_primo(rango_inferior, rango_superior):
    lista_Primos = list(sympy.primerange(rango_inferior,rango_superior +1))

    if lista_Primos: 
        return random.choice(lista_Primos)
    
    else:
        print("Error, no se pude encontrar un numero primo en el rango seleccionado")
        return None

def mcd(a, b):
    if b == 0:
        return abs(a) 
    r = a % b
    while r != 0:
        a = b
        b = r
        r = a % b 
    return abs(b) 

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

def inverso_modular(e, n):
    mcd, x, y = bezout(e, n) 

    if mcd != 1:
        print("No existe un inverso modular porque e y n no son coprimos")
        return None

    if x < 0:
        x += n

    return x


