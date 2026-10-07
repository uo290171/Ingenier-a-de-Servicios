# coding: utf8
import math

"""Módulo para calcular los valores del seno entre 0 y pi."""

def seno():
    """Construye y devuelve una lista con los valores de sin(x) 
    para x entre 0 y pi a intervalos regulares de 0.1."""
    resultados = []
    x = 0.0
    # Usamos pi del módulo math. Como flotantes, controlamos el bucle hasta pi.
    while x <= math.pi:
        resultados.append(math.sin(x))
        x += 0.1
    return resultados

if __name__ == "__main__":
    print("Demo del módulo seno.py:")
    lista_senos = seno()
    print(lista_senos)