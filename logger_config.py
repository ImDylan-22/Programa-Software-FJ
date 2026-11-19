"""
ARCHIVO: logger_config.py

DESCRIPCION:
Configura el sistema de registro de eventos y errores
de la aplicacion mediante el modulo logging.

FUNCION:
Guardar automaticamente los eventos y errores
en el archivo logs.txt.
"""

import logging


def configurar_logger():
    """
    Configura y devuelve el registro de eventos
    y errores de la aplicacion.

    Retorno:
        logging.Logger: Objeto encargado de registrar
        los eventos y errores del sistema.
    """

    # Crear el logger principal.
    logger = logging.getLogger("SoftwareFJ")

    # Establecer el nivel minimo de registro.
    logger.setLevel(logging.INFO)

    # Evitar crear varios manejadores del mismo archivo.
    if not logger.handlers:

        # Crear o abrir el archivo de registros.
        archivo = logging.FileHandler(
            "logs.txt",
            encoding="utf-8"
        )

        # Definir el formato de los registros.
        formato = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # Aplicar el formato al archivo.
        archivo.setFormatter(formato)

        # Conectar el archivo con el logger.
        logger.addHandler(archivo)

    return logger


# Crear el logger para que otros archivos puedan importarlo.
logger = configurar_logger()



# Inicializamos el registro del sistema.
logger = configurar_logger()