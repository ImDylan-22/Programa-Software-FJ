# prueba_parte1.py

"""
PRUEBAS DE LA PARTE 1 - SOFTWARE FJ

Objetivo:
Comprobar el funcionamiento de las excepciones
personalizadas y la clase abstracta Entidad.
"""

from entidad import Entidad
from excepciones import DatosInvalidosError
from logger_config import logger


# Clase temporal para realizar las pruebas.
class EntidadPrueba(Entidad):

    def mostrar_informacion(self):
        return "Entidad de prueba"


print("=== PRUEBA INICIAL SOFTWARE FJ ===")


# PRUEBA 1: Verificar que Entidad es abstracta.
try:
    objeto = Entidad("123", "Prueba")

except TypeError:
    print("Correcto: Entidad es una clase abstracta.")
    logger.info("Prueba de clase abstracta exitosa.")


# PRUEBA 2: Crear una entidad con datos validos.
try:
    objeto = EntidadPrueba("123", "Usuario de prueba")

    print("Correcto: entidad creada.")
    print("Nombre:", objeto.obtener_nombre())

    logger.info("Creacion de entidad de prueba exitosa.")

except Exception as error:
    print("Error:", error)
    logger.error("Error al crear entidad: %s", error)


# PRUEBA 3: Comprobar validacion de identificacion.
try:
    objeto = EntidadPrueba("", "Usuario")

except DatosInvalidosError as error:
    print("Correcto: se detecto un dato invalido.")
    print("Detalle:", error)

    logger.error("Validacion de datos: %s", error)


print("=== FIN DE LAS PRUEBAS ===")