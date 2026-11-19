"""
ARCHIVO: excepciones.py

DESCRIPCION:
Contiene las excepciones personalizadas utilizadas
para controlar los errores de la aplicacion.
"""


# Excepcion general del sistema.
class ErrorSoftwareFJ(Exception):
    """Clase base para los errores de Software FJ."""
    pass


# Error cuando los datos ingresados no son validos.
class DatosInvalidosError(ErrorSoftwareFJ):
    """Controla los datos que no cumplen las validaciones."""
    pass
    """Se importa en entidad.py para validar la identificacion y el nombre de las entidades."""

# Error cuando se registra un cliente duplicado.
class ClienteDuplicadoError(ErrorSoftwareFJ):
    """Controla el registro de clientes existentes."""
    pass

# Error cuando no se encuentra un cliente.
class ClienteNoEncontradoError(ErrorSoftwareFJ):
    """Controla las busquedas de clientes inexistentes."""
    pass

# Error cuando un servicio no esta disponible.
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Controla la disponibilidad de los servicios."""
    pass


# Error cuando una reserva presenta inconsistencias.
class ReservaInvalidaError(ErrorSoftwareFJ):
    """Controla las reservas incorrectas."""
    pass

# Error cuando se intenta realizar una operacion no permitida.
class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Controla las operaciones no permitidas."""
    pass