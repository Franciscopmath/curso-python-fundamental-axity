"""
Este archivo contiene VIOLACIONES INTENCIONALES a PEP 8
para demostrar las herramientas de calidad de código.
"""

import sys
import os
from typing import List,Dict
import json

# Violación: función sin espacios, nombres incorrectos
def calcularTotal(precio,cantidad):
    resultado=precio*cantidad
    return resultado

# Violación: nombres de variables
nombreUsuario = "Francisco"
ApellidoUsuario = "Math"

# Violación: clase con nombre incorrecto (snake_case en vez de PascalCase)
class usuario_manager:
    def __init__(self,nombre):
        self.Nombre=nombre

    # Violación: línea muy larga
    def obtener_informacion_completa_del_usuario_con_todos_los_detalles_disponibles_en_el_sistema(self):
        return f"Usuario: {self.Nombre}"

# Violación: espacios en blanco innecesarios
def funcion_mal_espaciada( arg1 , arg2 ):
    lista = [ 1,2,3,4,5 ]
    diccionario = { "clave" : "valor" }
    return lista

# Violación: múltiples statements en una línea
x = 1; y = 2; z = 3

# Violación: comparación con True/False
def verificar_estado(activo):
    if activo == True:
        return "Activo"
    if activo == False:
        return "Inactivo"

# Violación: uso de lambda innecesario
sumar = lambda x, y: x + y

# Violación: imports no utilizados (json)
# Violación: indentación mixta (tabs y espacios) - simulada
def funcion_con_problemas():
    if True:
        print("línea 1")
	    print("línea 2")  # Tab en vez de espacios

# Violación: variable no usada
def calcular_precio():
    precio_base = 100
    descuento = 0.2
    precio_final = precio_base
    return precio_final  # descuento nunca se usa

# Violación: sin espacios alrededor de operadores
resultado=10+20*30

# Violación: demasiadas líneas en blanco


def otra_funcion():
    pass
