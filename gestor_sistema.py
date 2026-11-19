"""
ARCHIVO: gestor_sistema.py

DESCRIPCION:
Implementa la clase GestorSistema, encargada de
administrar los clientes, servicios y reservas
mediante listas internas.

PSDT: Esta clase no se solicitó de forma directa en el PDF del ejercicio, pero es necesaria para organizar
el sistema y facilitar la gestion de los objetos.

FUNCIONALIDADES:
- Registro y busqueda de clientes.
- Registro y busqueda de servicios.
- Creacion y consulta de reservas.
- Confirmacion y cancelacion de reservas.
- Procesamiento de reservas.
- Control de registros duplicados.
- Consulta de informacion general.

CONCEPTOS:
- Programacion orientada a objetos.
- Encapsulacion.
- Manejo de listas.
- Asociacion entre objetos.
- Manejo de excepciones.

DEPENDENCIAS:
- cliente.py: Para asociar clientes a las reservas.
- servicio.py: Para asociar servicios a las reservas.
- reserva.py: Para crear y administrar reservas.
- excepciones.py: Para manejar errores de validacion y disponibilidad.
- logger_config.py: Para registrar eventos y errores del sistema.

"""

from cliente import Cliente
from servicio import Servicio
from reserva import Reserva

from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError   
)

from logger_config import logger


class GestorSistema:
    """
    Administra los clientes, servicios y reservas
    registrados en Software FJ.

    Los datos se almacenan en listas internas,
    sin utilizar bases de datos.
    """

    def __init__(self):
        """
        Inicializa las listas internas del sistema.
        """

        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        logger.info("Gestor del sistema inicializado.")

    # ==============================================
    # GESTION DE CLIENTES
    # ==============================================

    def registrar_cliente(self, cliente):
        """
        Registra un cliente en el sistema.

        Parametros:
            cliente (Cliente): Objeto que se desea registrar.

        Retorno:
            Cliente: Cliente registrado.

        Excepciones:
            DatosInvalidosError: Si el cliente es incorrecto
            o ya se encuentra registrado.
        """

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "El objeto proporcionado no es un cliente valido."
            )

        identificacion = cliente.obtener_identificacion()

        # Evitar identificaciones duplicadas.
        if self.buscar_cliente(identificacion) is not None:
            raise DatosInvalidosError(
                "Ya existe un cliente con esa identificacion."
            )

        self.__clientes.append(cliente)

        logger.info(
            "Cliente %s registrado correctamente.",
            identificacion
        )

        return cliente

    def buscar_cliente(self, identificacion):
        """
        Busca un cliente mediante su identificacion.

        Retorno:
            Cliente: Si encuentra coincidencia.
            None: Si no encuentra el cliente.
        """

        if not isinstance(identificacion, str):
            return None

        identificacion = identificacion.strip()

        for cliente in self.__clientes:

            if cliente.obtener_identificacion() == identificacion:
                return cliente

        return None

    def listar_clientes(self):
        """
        Devuelve una copia de la lista de clientes.

        La copia evita que se modifique directamente
        la lista interna desde otros componentes.
        """

        return self.__clientes.copy()

    # ==============================================
    # GESTION DE SERVICIOS
    # ==============================================

    def registrar_servicio(self, servicio):
        """
        Registra un servicio especializado.

        Parametros:
            servicio (Servicio): Objeto del servicio.

        Retorno:
            Servicio: Servicio registrado.

        Excepciones:
            DatosInvalidosError: Si el servicio es incorrecto
            o su codigo ya existe.
        """

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError(
                "El objeto proporcionado no es un servicio valido."
            )

        codigo = servicio.obtener_codigo()

        # Evitar codigos duplicados.
        if self.buscar_servicio(codigo) is not None:
            raise DatosInvalidosError(
                "Ya existe un servicio con ese codigo."
            )

        self.__servicios.append(servicio)

        logger.info(
            "Servicio %s registrado correctamente.",
            codigo
        )

        return servicio

    def buscar_servicio(self, codigo):
        """
        Busca un servicio mediante su codigo.

        Retorno:
            Servicio: Si encuentra coincidencia.
            None: Si no encuentra el servicio.
        """

        if not isinstance(codigo, str):
            return None

        codigo = codigo.strip()

        for servicio in self.__servicios:

            if servicio.obtener_codigo() == codigo:
                return servicio

        return None

    def listar_servicios(self):
        """Devuelve una copia de la lista de servicios."""

        return self.__servicios.copy()

    # ==============================================
    # GESTION DE RESERVAS
    # ==============================================

    def crear_reserva(self, codigo, identificacion_cliente,
                      codigo_servicio, duracion):
        """
        Crea una reserva utilizando un cliente y un servicio
        que previamente deben estar registrados.

        Parametros:
            codigo (str): Codigo de la nueva reserva.
            identificacion_cliente (str): Identificacion del cliente.
            codigo_servicio (str): Codigo del servicio.
            duracion (float): Duracion contratada.

        Retorno:
            Reserva: Objeto creado y registrado.

        Excepciones:
            DatosInvalidosError: Si faltan datos,
            existen duplicados o no se encuentran objetos.
        """

        # Comprobar que no exista otra reserva con el mismo codigo.
        if self.buscar_reserva(codigo) is not None:
            raise DatosInvalidosError(
                "Ya existe una reserva con ese codigo."
            )

        # Buscar el cliente.
        cliente = self.buscar_cliente(identificacion_cliente)

        if cliente is None:
            raise DatosInvalidosError(
                "No se encontro el cliente solicitado."
            )

        # Buscar el servicio.
        servicio = self.buscar_servicio(codigo_servicio)

        if servicio is None:
            raise DatosInvalidosError(
                "No se encontro el servicio solicitado."
            )

        # Crear la reserva.
        reserva = Reserva(
            codigo,
            cliente,
            servicio,
            duracion
        )

        # Agregar la reserva a la lista interna.
        self.__reservas.append(reserva)

        logger.info(
            "Reserva %s creada correctamente.",
            codigo
        )

        return reserva

    def buscar_reserva(self, codigo):
        """
        Busca una reserva mediante su codigo.

        Retorno:
            Reserva: Si encuentra coincidencia.
            None: Si no encuentra la reserva.
        """

        if not isinstance(codigo, str):
            return None

        codigo = codigo.strip()

        for reserva in self.__reservas:

            if reserva.obtener_codigo() == codigo:
                return reserva

        return None

    def listar_reservas(self):
        """Devuelve una copia de la lista de reservas."""

        return self.__reservas.copy()

    # ==============================================
    # OPERACIONES SOBRE RESERVAS
    # ==============================================

    def confirmar_reserva(self, codigo):
        """
        Busca y confirma una reserva.

        Retorno:
            bool: True si se confirma correctamente.
        """

        reserva = self.buscar_reserva(codigo)

        if reserva is None:
            raise DatosInvalidosError(
                "No se encontro la reserva solicitada."
            )

        resultado = reserva.confirmar()

        logger.info("Reserva %s confirmada.", codigo)

        return resultado

    def cancelar_reserva(self, codigo):
        """
        Busca y cancela una reserva.

        Retorno:
            bool: True si se cancela correctamente.
        """

        reserva = self.buscar_reserva(codigo)

        if reserva is None:
            raise DatosInvalidosError(
                "No se encontro la reserva solicitada."
            )

        resultado = reserva.cancelar()

        logger.info("Reserva %s cancelada.", codigo)

        return resultado

    def procesar_reserva(self, codigo, incluir_impuesto=False,
                         descuento=0):
        """
        Busca y procesa una reserva confirmada.

        Retorno:
            float: Costo final calculado.
        """

        reserva = self.buscar_reserva(codigo)

        if reserva is None:
            raise DatosInvalidosError(
                "No se encontro la reserva solicitada."
            )

        costo = reserva.procesar(
            incluir_impuesto,
            descuento
        )

        logger.info(
            "Reserva %s procesada por %.2f COP.",
            codigo,
            costo
        )

        return costo

    # ==============================================
    # INFORMACION GENERAL DEL SISTEMA
    # ==============================================

    def obtener_resumen(self):
        """
        Devuelve un resumen de los registros del sistema.
        """

        cantidad_clientes = len(self.__clientes)
        cantidad_servicios = len(self.__servicios)
        cantidad_reservas = len(self.__reservas)

        reservas_pendientes = sum(
            1 for reserva in self.__reservas
            if reserva.obtener_estado() == "Pendiente"
        )

        reservas_confirmadas = sum(
            1 for reserva in self.__reservas
            if reserva.obtener_estado() == "Confirmada"
        )

        reservas_canceladas = sum(
            1 for reserva in self.__reservas
            if reserva.obtener_estado() == "Cancelada"
        )

        reservas_procesadas = sum(
            1 for reserva in self.__reservas
            if reserva.obtener_estado() == "Procesada"
        )

        return {
            "clientes": cantidad_clientes,
            "servicios": cantidad_servicios,
            "reservas": cantidad_reservas,
            "pendientes": reservas_pendientes,
            "confirmadas": reservas_confirmadas,
            "canceladas": reservas_canceladas,
            "procesadas": reservas_procesadas
        }