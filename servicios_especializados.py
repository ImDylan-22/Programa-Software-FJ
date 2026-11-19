"""
ARCHIVO: servicios_especializados.py

DESCRIPCION:
Contiene las clases especializadas que representan
los servicios ofrecidos por la empresa.

CLASES:
- ReservaSala.
- AlquilerEquipo.
- AsesoriaEspecializada.

CONCEPTOS:
- Herencia.
- Polimorfismo.
- Sobrescritura de metodos.
- Validacion de parametros.

DEPENDENCIAS:
- servicio.py: Para heredar los atributos y metodos de la clase abstracta Servicio.
- excepciones.py: Para manejar errores de validacion y disponibilidad.
- logger_config.py: Para configurar el registro de eventos.

"""

from servicio import Servicio
from excepciones import DatosInvalidosError
from logger_config import logger


# ==================================================
# SERVICIO 1: RESERVA DE SALAS
# ==================================================

class ReservaSala(Servicio):
    """
    Representa el servicio de alquiler de salas.

    Atributos adicionales:
        __capacidad: Cantidad maxima de personas.
    """

    def __init__(self, codigo, descripcion, capacidad,
                 tarifa_hora=50000, disponible=True):

        # Inicializar los atributos heredados.
        super().__init__(
            codigo,
            "Reserva de salas",
            descripcion,
            tarifa_hora,
            disponible
        )

        # Validar la capacidad.
        if isinstance(capacidad, bool) or not isinstance(capacidad, int):
            raise DatosInvalidosError(
                "La capacidad debe ser un numero entero."
            )

        if capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad debe ser mayor que cero."
            )

        self.__capacidad = capacidad

        logger.info("Servicio de sala creado: %s", codigo)

    def obtener_capacidad(self):
        """Devuelve la capacidad maxima de la sala."""
        return self.__capacidad

    def validar_parametros(self, cantidad):
        """
        Valida la cantidad de horas solicitadas.

        Excepciones:
            DatosInvalidosError: Si las horas son incorrectas.
            ServicioNoDisponibleError: Si la sala no esta disponible.
        """

        self._comprobar_disponibilidad()
        self._validar_cantidad(cantidad)

        return True

    def calcular_costo(self, cantidad, incluir_impuesto=False,
                       descuento=0):
        """
        Calcula el costo de alquiler de una sala por horas.
        """

        self.validar_parametros(cantidad)

        total = self._calcular_total(
            cantidad,
            incluir_impuesto,
            descuento
        )

        logger.info(
            "Costo de reserva de sala calculado: %.2f",
            total
        )

        return total

    def describir_servicio(self):
        """Devuelve la descripcion del servicio de salas."""

        return (
            f"Servicio: {self.obtener_nombre()}\n"
            f"Codigo: {self.obtener_codigo()}\n"
            f"Descripcion: {self.obtener_descripcion()}\n"
            f"Capacidad: {self.__capacidad} personas\n"
            f"Tarifa por hora: ${self.obtener_tarifa_base():,.2f} COP"
        )


# ==================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ==================================================

class AlquilerEquipo(Servicio):
    """
    Representa el servicio de alquiler de equipos.

    Atributos adicionales:
        __tipo_equipo: Categoria del equipo alquilado.
    """

    def __init__(self, codigo, descripcion, tipo_equipo,
                 tarifa_dia=30000, disponible=True):

        super().__init__(
            codigo,
            "Alquiler de equipos",
            descripcion,
            tarifa_dia,
            disponible
        )

        # Validar el tipo de equipo.
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatosInvalidosError(
                "El tipo de equipo es obligatorio."
            )

        self.__tipo_equipo = tipo_equipo.strip()

        logger.info("Servicio de equipo creado: %s", codigo)

    def obtener_tipo_equipo(self):
        """Devuelve la categoria del equipo."""
        return self.__tipo_equipo

    def validar_parametros(self, cantidad):
        """
        Valida la cantidad de dias de alquiler.

        Para este servicio se utilizan dias completos.
        """

        self._comprobar_disponibilidad()

        cantidad = self._validar_cantidad(cantidad)

        if not cantidad.is_integer():
            raise DatosInvalidosError(
                "El alquiler debe realizarse por dias completos."
            )

        return True

    def calcular_costo(self, cantidad, incluir_impuesto=False,
                       descuento=0):
        """
        Calcula el costo del alquiler de equipos por dias.
        """

        self.validar_parametros(cantidad)

        total = self._calcular_total(
            cantidad,
            incluir_impuesto,
            descuento
        )

        logger.info(
            "Costo de alquiler de equipo calculado: %.2f",
            total
        )

        return total

    def describir_servicio(self):
        """Devuelve la descripcion del alquiler de equipos."""

        return (
            f"Servicio: {self.obtener_nombre()}\n"
            f"Codigo: {self.obtener_codigo()}\n"
            f"Descripcion: {self.obtener_descripcion()}\n"
            f"Tipo de equipo: {self.__tipo_equipo}\n"
            f"Tarifa por dia: ${self.obtener_tarifa_base():,.2f} COP"
        )


# ==================================================
# SERVICIO 3: ASESORIAS ESPECIALIZADAS
# ==================================================

class AsesoriaEspecializada(Servicio):
    """
    Representa el servicio de asesoria especializada.

    Atributos adicionales:
        __area: Area o especialidad de la asesoria.
    """

    def __init__(self, codigo, descripcion, area,
                 tarifa_hora=80000, disponible=True):

        super().__init__(
            codigo,
            "Asesoria especializada",
            descripcion,
            tarifa_hora,
            disponible
        )

        # Validar el area de asesoria.
        if not isinstance(area, str) or not area.strip():
            raise DatosInvalidosError(
                "El area de asesoria es obligatoria."
            )

        self.__area = area.strip()

        logger.info("Servicio de asesoria creado: %s", codigo)

    def obtener_area(self):
        """Devuelve el area de especializacion."""
        return self.__area

    def validar_parametros(self, cantidad):
        """
        Valida la cantidad de horas de asesoria solicitadas.
        """

        self._comprobar_disponibilidad()
        self._validar_cantidad(cantidad)

        return True

    def calcular_costo(self, cantidad, incluir_impuesto=False,
                       descuento=0):
        """
        Calcula el costo de una asesoria por horas.
        """

        self.validar_parametros(cantidad)

        total = self._calcular_total(
            cantidad,
            incluir_impuesto,
            descuento
        )

        logger.info(
            "Costo de asesoria calculado: %.2f",
            total
        )

        return total

    def describir_servicio(self):
        """Devuelve la descripcion de la asesoria."""

        return (
            f"Servicio: {self.obtener_nombre()}\n"
            f"Codigo: {self.obtener_codigo()}\n"
            f"Descripcion: {self.obtener_descripcion()}\n"
            f"Area de asesoria: {self.__area}\n"
            f"Tarifa por hora: ${self.obtener_tarifa_base():,.2f} COP"
        )
