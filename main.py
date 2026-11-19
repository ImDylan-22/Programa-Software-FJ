"""
ARCHIVO: main.py

DESCRIPCION:
Archivo principal para iniciar el programa.
Se encarga de crear la ventana principal, inicializar
el gestor del sistema y ejecutar la interfaz grafica.
"""

import tkinter as tk

from gestor_sistema import GestorSistema
from interfaz import InterfazPrincipal


def iniciar_programa():
    """
    Inicializa los componentes principales de Software FJ
    y ejecuta la interfaz grafica.
    """

    # Crear ventana principal de Tkinter.
    ventana = tk.Tk()

    # Crear el gestor general del sistema.
    gestor = GestorSistema()

    # Construir la interfaz principal.
    InterfazPrincipal(ventana, gestor)

    # Mantener la ventana activa.
    ventana.mainloop()


# Ejecutar el programa.
if __name__ == "__main__":
    iniciar_programa()