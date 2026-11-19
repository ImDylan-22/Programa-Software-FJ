"""
ARCHIVO: entidad.py

DESCRIPCION:
Contiene la clase abstracta Entidad, que sirve como base
para las entidades del sistema, como clientes, servicios y reservas.

DEPENDENCIAS:
- abc: Para definir la clase abstracta y sus metodos.
- excepciones.py: Para manejar errores de validacion de datos.
- cliente.py: Para la herencia de la clase Cliente.
"""

from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError


# Clase abstracta principal del sistema.
class Entidad(ABC):

    def __init__(self, identificacion, nombre):

        # Validamos la identificacion.
        if not identificacion or not identificacion.strip():
            raise DatosInvalidosError(
                "La identificacion es obligatoria."
            )

        # Validamos el nombre.
        if not nombre or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre es obligatorio."
            )

        # Atributos encapsulados.
        self.__identificacion = identificacion.strip()
        self.__nombre = nombre.strip()

    # Metodo para consultar la identificacion.
    def obtener_identificacion(self):
        return self.__identificacion

    # Metodo para consultar el nombre.
    def obtener_nombre(self):
        return self.__nombre

    # Metodo abstracto que deben implementar las clases hijas.
    @abstractmethod
    def mostrar_informacion(self):
        pass