"""
Este archivo contiene el código CORREGIDO según PEP 8.
Todas las violaciones han sido resueltas.
"""

from typing import Dict, List


# Corrección: función en snake_case, espacios correctos
def calcular_total(precio, cantidad):
    resultado = precio * cantidad
    return resultado


# Corrección: variables en snake_case
nombre_usuario = "Francisco"
apellido_usuario = "Math"


# Corrección: clase en PascalCase
class UsuarioManager:
    def __init__(self, nombre):
        self.nombre = nombre

    # Corrección: nombre de método más corto y descriptivo
    def obtener_informacion(self):
        return f"Usuario: {self.nombre}"


# Corrección: espacios correctos alrededor de paréntesis y comas
def funcion_bien_espaciada(arg1, arg2):
    lista = [1, 2, 3, 4, 5]
    return lista


# Corrección: statements separados en líneas individuales
x = 1
y = 2
z = 3


# Corrección: comparación directa con booleanos
def verificar_estado(activo):
    if activo:
        return "Activo"
    return "Inactivo"


# Corrección: función normal en vez de lambda innecesaria
def sumar(x, y):
    return x + y


# Corrección: indentación consistente (solo espacios)
def funcion_sin_problemas():
    if True:
        print("línea 1")
        print("línea 2")


# Corrección: todas las variables son utilizadas
def calcular_precio():
    precio_base = 100
    descuento = 0.2
    precio_final = precio_base * (1 - descuento)
    return precio_final


# Corrección: espacios alrededor de operadores
resultado = 10 + 20 * 30


# Corrección: sin líneas en blanco excesivas
def otra_funcion():
    pass


# Ejemplo adicional: docstrings correctos
def funcion_con_docstring(parametro: str) -> str:
    """
    Función de ejemplo con docstring correcto.

    Args:
        parametro: Descripción del parámetro

    Returns:
        str: Descripción del valor retornado
    """
    return parametro.upper()


# Ejemplo: constantes en UPPERCASE
MAX_INTENTOS = 3
API_URL = "https://api.ejemplo.com"


# Ejemplo: uso correcto de type hints
def procesar_datos(datos: List[Dict[str, str]]) -> Dict[str, int]:
    """Procesa una lista de diccionarios y retorna resumen."""
    return {"total": len(datos)}


if __name__ == "__main__":
    # Código de ejemplo ejecutable
    print(f"Nombre: {nombre_usuario} {apellido_usuario}")
    print(f"Total: {calcular_total(10, 5)}")

    manager = UsuarioManager("Francisco")
    print(manager.obtener_informacion())

    print(f"Estado: {verificar_estado(True)}")
    print(f"Suma: {sumar(5, 3)}")
    print(f"Precio final: {calcular_precio()}")
