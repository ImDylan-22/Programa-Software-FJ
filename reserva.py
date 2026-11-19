"""
ARCHIVO: reserva.py

DESCRIPCION:
Implementa la clase Reserva, encargada de relacionar
un cliente con un servicio y administrar el ciclo de
vida de una reserva.

FUNCIONALIDADES:
- Creacion de reservas.
- Validacion de clientes y servicios.
- Confirmacion de reservas.
- Cancelacion de reservas.
- Procesamiento y calculo de costos.
- Control de estados.
- Manejo de excepciones.

DEPENDENCIAS:
- cliente.py: Para asociar un cliente a la reserva.
- servicio.py: Para heredar los atributos y metodos de la clase abstracta Servicio.
- excepciones.py: Para manejar errores de validacion y disponibilidad.
- logger_config.py: Para registrar eventos y errores del sistema.

"""

import math

from cliente import Cliente
from servicio import Servicio

from excepciones import DatosInvalidosError
from logger_config import logger


class Reserva:
    """
    Representa una reserva realizada por un cliente.

    Cada reserva relaciona un cliente con un servicio,
    establece una duracion y controla su estado.

    Estados posibles:
        Pendiente.
        Confirmada.
        Cancelada.
        Procesada.
    """

    def __init__(self, codigo, cliente, servicio, duracion):
        """
        Inicializa una reserva.

        Parametros:
            codigo (str): Identificador de la reserva.
            cliente (Cliente): Cliente que solicita el servicio.
            servicio (Servicio): Servicio solicitado.
            duracion (int o float): Cantidad contratada.

        Excepciones:
            DatosInvalidosError: Cuando los datos son incorrectos.
        """

        # Validar el codigo de la reserva.
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidosError(
                "El codigo de la reserva es obligatorio."
            )

        # Comprobar que el objeto recibido sea un Cliente.
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "La reserva debe estar asociada a un cliente valido."
            )

        # Comprobar que el servicio pertenezca a la clase Servicio.
        # Tambien acepta sus clases derivadas.
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError(
                "La reserva debe estar asociada a un servicio valido."
            )

        # Validar la duracion.
        if isinstance(duracion, bool):
            raise DatosInvalidosError(
                "La duracion debe ser un numero positivo."
            )

        try:
            duracion = float(duracion)

        except (TypeError, ValueError) as error:
            raise DatosInvalidosError(
                "La duracion debe ser numerica."
            ) from error

        if not math.isfinite(duracion) or duracion <= 0:
            raise DatosInvalidosError(
                "La duracion debe ser mayor que cero."
            )

        # Inicializar los atributos privados.
        self.__codigo = codigo.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion

        # Toda reserva comienza pendiente.
        self.__estado = "Pendiente"

        # El costo se calcula cuando se procesa la reserva.
        self.__costo = None

        logger.info(
            "Reserva %s creada para el cliente %s.",
            self.__codigo,
            self.__cliente.obtener_nombre()
        )

    # ==============================================
    # METODOS DE CONSULTA
    # ==============================================

    def obtener_codigo(self):
        """Devuelve el codigo de la reserva."""
        return self.__codigo

    def obtener_cliente(self):
        """Devuelve el objeto Cliente asociado."""
        return self.__cliente

    def obtener_servicio(self):
        """Devuelve el servicio asociado."""
        return self.__servicio

    def obtener_duracion(self):
        """Devuelve la duracion de la reserva."""
        return self.__duracion

    def obtener_estado(self):
        """Devuelve el estado actual de la reserva."""
        return self.__estado

    def obtener_costo(self):
        """Devuelve el costo calculado de la reserva."""
        return self.__costo

    # ==============================================
    # CONFIRMACION DE RESERVAS
    # ==============================================

    def confirmar(self):
        """
        Confirma una reserva pendiente.

        Antes de confirmar comprueba:
        - Que la reserva este pendiente.
        - Que el servicio este disponible.
        - Que la duracion sea valida para el servicio.

        Retorno:
            bool: True si la confirmacion fue exitosa.

        Excepciones:
            DatosInvalidosError: Si el estado no permite confirmar.
            ServicioNoDisponibleError: Si el servicio no esta disponible.
        """

        if self.__estado != "Pendiente":
            raise DatosInvalidosError(
                "Solamente se pueden confirmar reservas pendientes."
            )

        # Validar las condiciones especificas del servicio.
        self.__servicio.validar_parametros(self.__duracion)

        # Cambiar el estado cuando todas las validaciones sean exitosas.
        self.__estado = "Confirmada"

        logger.info(
            "Reserva %s confirmada correctamente.",
            self.__codigo
        )

        return True

    # ==============================================
    # CANCELACION DE RESERVAS
    # ==============================================

    def cancelar(self):
        """
        Cancela una reserva pendiente o confirmada.

        No permite cancelar reservas que ya fueron procesadas
        o que anteriormente fueron canceladas.

        Retorno:
            bool: True si la cancelacion fue exitosa.

        Excepciones:
            DatosInvalidosError: Si el estado no permite cancelar.
        """

        if self.__estado not in ("Pendiente", "Confirmada"):
            raise DatosInvalidosError(
                "No se puede cancelar una reserva "
                "que ya fue cancelada o procesada."
            )

        self.__estado = "Cancelada"

        logger.info(
            "Reserva %s cancelada.",
            self.__codigo
        )

        return True

    # ==============================================
    # PROCESAMIENTO DE RESERVAS
    # ==============================================

    def procesar(self, incluir_impuesto=False, descuento=0):
        """
        Procesa una reserva confirmada y calcula su costo.

        Parametros:
            incluir_impuesto (bool): Indica si aplica impuesto.
            descuento (float): Descuento porcentual.

        Retorno:
            float: Costo final de la reserva.

        Excepciones:
            DatosInvalidosError: Si el estado no permite procesar.
            ServicioNoDisponibleError: Si el servicio no esta disponible.
        """

        if self.__estado != "Confirmada":
            raise DatosInvalidosError(
                "Solamente se pueden procesar reservas confirmadas."
            )

        # Calcular el costo utilizando el metodo del servicio.
        # El polimorfismo permite utilizar la implementacion
        # correspondiente a cada servicio especializado.
        costo_calculado = self.__servicio.calcular_costo(
            self.__duracion,
            incluir_impuesto,
            descuento
        )

        # Actualizar el costo y el estado despues del calculo exitoso.
        self.__costo = costo_calculado
        self.__estado = "Procesada"

        logger.info(
            "Reserva %s procesada. Costo: %.2f COP.",
            self.__codigo,
            self.__costo
        )

        return self.__costo

    # ==============================================
    # INFORMACION GENERAL DE LA RESERVA
    # ==============================================

    def mostrar_informacion(self):
        """
        Devuelve un resumen de la reserva.

        Incluye informacion del cliente, servicio,
        duracion, estado y costo cuando este disponible.
        """

        informacion = (
            f"Codigo de reserva: {self.__codigo}\n"
            f"Cliente: {self.__cliente.obtener_nombre()}\n"
            f"Identificacion: {self.__cliente.obtener_identificacion()}\n"
            f"Servicio: {self.__servicio.obtener_nombre()}\n"
            f"Duracion: {self.__duracion:g}\n"
            f"Estado: {self.__estado}\n"
        )

        if self.__costo is not None:
            informacion += (
                f"Costo: ${self.__costo:,.2f} COP\n"
            )
        else:
            informacion += "Costo: Pendiente de procesamiento\n"

        return informacion