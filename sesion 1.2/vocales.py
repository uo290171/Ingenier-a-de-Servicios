# coding: utf8

def contar_vocales(cadena):
    """Recibe una cadena y devuelve un diccionario con el número de 
    repeticiones de cada vocal ('a', 'e', 'i', 'o', 'u')."""
    # Inicializamos el diccionario con las vocales a cero
    resultado = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    
    # Pasamos la cadena a minúsculas para contar tanto mayúsculas como minúsculas
    cadena_min = cadena.lower()
    
    for letra in cadena_min:
        if letra in resultado:
            resultado[letra] += 1
            
    return resultado

if __name__ == "__main__":
    txt = "Esto es una prueba. Esta cadena contiene vocales variadas"
    result = contar_vocales(txt)
    print("Texto analizado:", txt)
    print("Resultado:", result)