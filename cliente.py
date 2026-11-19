"""
ARCHIVO: cliente.py

DESCRIPCION:
Define la clase Cliente, encargada de almacenar y
administrar la informacion personal y de contacto
de los clientes registrados.

CONCEPTOS:
- Herencia.
- Encapsulacion.
- Validacion de datos.
- Manejo de excepciones personalizadas.

DEPENDENCIAS:
- entidad.py: Para heredar los atributos de identificacion y nombre.
- excepciones.py: Para manejar errores de validacion y duplicados.
- logger_config.py: Para registrar eventos y errores del sistema.

"""

import re

from entidad import Entidad
from excepciones import DatosInvalidosError
from logger_config import logger


class Cliente(Entidad):
    """
    Representa un cliente registrado..

    Hereda de Entidad los atributos de identificacion
    y nombre, e incorpora correo electronico y telefono.

    Atributos privados:
        __correo (str): Correo electronico del cliente.
        __telefono (str): Numero telefonico del cliente.
    """

    def __init__(self, identificacion, nombre, correo, telefono):
        """
        Inicializa un cliente con sus datos personales.

        Parametros:
            identificacion (str): Identificador del cliente.
            nombre (str): Nombre completo.
            correo (str): Correo electronico.
            telefono (str): Numero de contacto.

        Excepciones:
            DatosInvalidosError: Si el correo o telefono
            no cumplen las validaciones establecidas.
        """

        # Inicializar los atributos heredados de Entidad.
        super().__init__(identificacion, nombre)

        # Validar los datos de contacto.
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

        # Registrar la creacion del cliente.
        logger.info(
            "Cliente registrado: %s",
            self.obtener_identificacion()
        )

    @staticmethod
    def _validar_correo(correo):
        """
        Comprueba que el correo tenga un formato valido.

        Parametros:
            correo (str): Direccion de correo electronico.

        Retorno:
            str: Correo validado y sin espacios externos.

        Excepciones:
            DatosInvalidosError: Si el correo esta vacio
            o no cumple el formato establecido.
        """

        if not isinstance(correo, str):
            raise DatosInvalidosError(
                "El correo debe ser un texto."
            )

        correo = correo.strip()

        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not correo or not re.fullmatch(patron, correo):
            raise DatosInvalidosError(
                "El correo electronico no tiene un formato valido."
            )

        return correo

    @staticmethod
    def _validar_telefono(telefono):
        """
        Comprueba que el telefono contenga entre 7 y 15 digitos.

        Permite espacios, guiones y el simbolo + como
        caracteres de formato.

        Parametros:
            telefono (str): Numero telefonico del cliente.

        Retorno:
            str: Telefono validado.

        Excepciones:
            DatosInvalidosError: Si el numero no es valido.
        """

        if not isinstance(telefono, str):
            raise DatosInvalidosError(
                "El telefono debe ingresarse como texto."
            )

        telefono = telefono.strip()

        # Comprobar los caracteres permitidos.
        if not re.fullmatch(r"\+?[\d\s-]+", telefono):
            raise DatosInvalidosError(
                "El telefono contiene caracteres no permitidos."
            )

        # Contar unicamente los digitos.
        digitos = re.sub(r"\D", "", telefono)

        if not 7 <= len(digitos) <= 15:
            raise DatosInvalidosError(
                "El telefono debe contener entre 7 y 15 digitos."
            )

        return telefono

    def obtener_correo(self):
        """
        Devuelve el correo electronico del cliente.

        Retorno:
            str: Correo electronico registrado.
        """
        return self.__correo

    def obtener_telefono(self):
        """
        Devuelve el telefono del cliente.

        Retorno:
            str: Numero telefonico registrado.
        """
        return self.__telefono

    def actualizar_correo(self, nuevo_correo):
        """
        Valida y actualiza el correo electronico.

        Parametros:
            nuevo_correo (str): Nueva direccion de correo.

        Excepciones:
            DatosInvalidosError: Si el correo no es valido.
        """

        # Validar antes de modificar el atributo.
        correo_validado = self._validar_correo(nuevo_correo)

        self.__correo = correo_validado

        logger.info(
            "Correo actualizado para el cliente %s",
            self.obtener_identificacion()
        )

    def actualizar_telefono(self, nuevo_telefono):
        """
        Valida y actualiza el numero telefonico.

        Parametros:
            nuevo_telefono (str): Nuevo numero de contacto.

        Excepciones:
            DatosInvalidosError: Si el telefono no es valido.
        """

        # Validar antes de modificar el atributo.
        telefono_validado = self._validar_telefono(nuevo_telefono)

        self.__telefono = telefono_validado

        logger.info(
            "Telefono actualizado para el cliente %s",
            self.obtener_identificacion()
        )

    def mostrar_informacion(self):
        """
        Devuelve la informacion general del cliente.

        Retorno:
            str: Identificacion, nombre, correo y telefono.
        """

        return (
            f"Identificacion: {self.obtener_identificacion()}\n"
            f"Nombre: {self.obtener_nombre()}\n"
            f"Correo: {self.__correo}\n"
            f"Telefono: {self.__telefono}"
        )
