"""
ARCHIVO: servicio.py

DESCRIPCION:
Define la clase abstracta Servicio, que establece
la estructura y los metodos comunes de los servicios
ofrecidos por Software FJ.

CONCEPTOS:
- Abstraccion.
- Encapsulacion.
- Metodos abstractos.
- Validacion de parametros.

DEPENDENCIAS:
- abc: Para definir la clase abstracta y sus metodos.
- excepciones.py: Para manejar errores de validacion y disponibilidad.

"""

import math
from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


class Servicio(ABC):
    """
    Clase abstracta que representa un servicio de Software FJ.

    Las clases derivadas deben implementar los metodos:
        calcular_costo()
        describir_servicio()
        validar_parametros()

    Atributos privados:
        __codigo: Identificador del servicio.
        __nombre: Nombre del servicio.
        __descripcion: Descripcion general.
        __tarifa_base: Tarifa inicial del servicio.
        __disponible: Estado de disponibilidad.
    """

    def __init__(self, codigo, nombre, descripcion,
                 tarifa_base, disponible=True):
        """
        Inicializa los datos generales de un servicio.

        Parametros:
            codigo (str): Identificador del servicio.
            nombre (str): Nombre del servicio.
            descripcion (str): Descripcion del servicio.
            tarifa_base (float): Tarifa inicial.
            disponible (bool): Estado de disponibilidad.

        Excepciones:
            DatosInvalidosError: Si algun dato es incorrecto.
        """

        # Validar los datos de texto.
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidosError(
                "El codigo del servicio es obligatorio."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio es obligatorio."
            )

        if not isinstance(descripcion, str) or not descripcion.strip():
            raise DatosInvalidosError(
                "La descripcion del servicio es obligatoria."
            )

        # Validar la tarifa base.
        try:
            tarifa_base = float(tarifa_base)

        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(
                "La tarifa base debe ser un valor numerico."
            ) from error

        if not math.isfinite(tarifa_base) or tarifa_base <= 0:
            raise DatosInvalidosError(
                "La tarifa base debe ser mayor que cero."
            )

        # Validar el estado de disponibilidad.
        if not isinstance(disponible, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        # Inicializar los atributos privados.
        self.__codigo = codigo.strip()
        self.__nombre = nombre.strip()
        self.__descripcion = descripcion.strip()
        self.__tarifa_base = tarifa_base
        self.__disponible = disponible

    def obtener_codigo(self):
        """Devuelve el codigo identificador del servicio."""
        return self.__codigo

    def obtener_nombre(self):
        """Devuelve el nombre del servicio."""
        return self.__nombre

    def obtener_descripcion(self):
        """Devuelve la descripcion del servicio."""
        return self.__descripcion

    def obtener_tarifa_base(self):
        """Devuelve la tarifa base del servicio."""
        return self.__tarifa_base

    def esta_disponible(self):
        """Indica si el servicio esta disponible."""
        return self.__disponible

    def cambiar_disponibilidad(self, disponible):
        """
        Modifica el estado de disponibilidad.

        Parametros:
            disponible (bool): Nuevo estado del servicio.

        Excepciones:
            DatosInvalidosError: Si el valor no es booleano.
        """

        if not isinstance(disponible, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        self.__disponible = disponible

    def _comprobar_disponibilidad(self):
        """
        Comprueba si el servicio puede utilizarse.

        Excepciones:
            ServicioNoDisponibleError: Si esta deshabilitado.
        """

        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.__nombre} no esta disponible."
            )

    def _validar_cantidad(self, cantidad):
        """
        Comprueba que la cantidad sea un numero positivo.

        Parametros:
            cantidad (int o float): Cantidad solicitada.

        Retorno:
            float: Cantidad validada.
        """

        if isinstance(cantidad, bool):
            raise DatosInvalidosError(
                "La cantidad debe ser un numero positivo."
            )

        try:
            cantidad = float(cantidad)

        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(
                "La cantidad debe ser numerica."
            ) from error

        if not math.isfinite(cantidad) or cantidad <= 0:
            raise DatosInvalidosError(
                "La cantidad debe ser mayor que cero."
            )

        return cantidad

    def _calcular_total(self, cantidad, incluir_impuesto=False,
                        descuento=0):
        """
        Calcula el costo final aplicando impuesto y descuento.

        El impuesto de ejemplo utilizado es del 19 %.

        Parametros:
            cantidad (float): Cantidad del servicio.
            incluir_impuesto (bool): Indica si aplica impuesto.
            descuento (float): Descuento porcentual entre 0 y 100.

        Retorno:
            float: Costo total calculado.
        """

        if not isinstance(incluir_impuesto, bool):
            raise DatosInvalidosError(
                "El indicador de impuesto debe ser booleano."
            )

        if isinstance(descuento, bool):
            raise DatosInvalidosError(
                "El descuento debe ser numerico."
            )

        try:
            descuento = float(descuento)

        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(
                "El descuento debe ser numerico."
            ) from error

        if not math.isfinite(descuento) or not 0 <= descuento <= 100:
            raise DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )

        cantidad = self._validar_cantidad(cantidad)

        # Calcular el costo inicial.
        subtotal = self.__tarifa_base * cantidad

        # Aplicar el descuento.
        subtotal -= subtotal * (descuento / 100)

        # Aplicar el impuesto cuando corresponda.
        if incluir_impuesto:
            subtotal += subtotal * 0.19

        return round(subtotal, 2)

    @abstractmethod
    def calcular_costo(self, cantidad, incluir_impuesto=False,
                       descuento=0):
        """
        Calcula el costo del servicio.

        Debe implementarse en cada clase especializada.
        """
        pass

    @abstractmethod
    def describir_servicio(self):
        """
        Devuelve una descripcion del servicio.

        Debe implementarse en cada clase especializada.
        """
        pass

    @abstractmethod
    def validar_parametros(self, cantidad):
        """
        Valida los parametros necesarios para utilizar
        el servicio.

        Debe implementarse en cada clase especializada.
        """
        pass