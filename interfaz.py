"""
ARCHIVO: interfaz.py

DESCRIPCION:
Implementa la ventana principal del sistema utilizando
Tkinter.

PSDT: Como tal no se solicitó en el PDF del ejercicio ni en la guía de desarrollo del ejercicio, 
pero se incluyó para facilitar la visualización de los resultados y la interacción con el sistema.

FUNCIONALIDADES:
- Ventana principal.
- Menu de navegacion.
- Resumen de clientes, servicios y reservas.
- Consulta de estados de las reservas.
- Actualizacion de informacion.

DEPENDENCIAS:
- tkinter: Biblioteca para crear interfaces graficas en Python.
- gestor_sistema.py: Contiene la clase GestorSistema que administra clientes, servicios y reservas.

"""

import tkinter as tk
from tkinter import messagebox

from gestor_sistema import GestorSistema
from ventana_clientes import VentanaClientes
from ventana_reservas import VentanaReservas
from ventana_servicios import VentanaServicios


class InterfazPrincipal:
    """
    Construye la ventana principal de Software FJ.
    """

    def __init__(self, ventana, gestor):

        self.ventana = ventana
        self.gestor = gestor

        # Configuracion de la ventana.
        self.ventana.title("Software FJ - Sistema de gestion")
        self.ventana.geometry("900x600")
        self.ventana.minsize(750, 500)
        self.ventana.configure(bg="#EEEEEE")

        # Construccion de la interfaz.
        self.crear_menu_lateral()
        self.crear_panel_principal()

        # Mostrar informacion inicial.
        self.refrescar_resumen()

        # Confirmacion de cierre.
        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

    # ==============================================
    # MENU LATERAL
    # ==============================================

    def crear_menu_lateral(self):
        """
        Construye el menu lateral con las opciones
        principales del sistema.
        """

        self.menu_lateral = tk.Frame(
            self.ventana,
            bg="#D9E2F3",
            width=180
        )

        self.menu_lateral.pack(
            side="left",
            fill="y"
        )

        self.menu_lateral.pack_propagate(False)

        # Nombre del sistema.
        tk.Label(
            self.menu_lateral,
            text="SOFTWARE FJ",
            bg="#D9E2F3",
            fg="#222222",
            font=("Arial", 15, "bold")
        ).pack(pady=(25, 5))

        tk.Label(
            self.menu_lateral,
            text="Menu principal",
            bg="#D9E2F3",
            fg="#444444",
            font=("Arial", 10)
        ).pack(pady=(0, 25))

        # Botones de navegacion.
        self.crear_boton_menu("Inicio", self.mostrar_inicio)

        self.crear_boton_menu("Clientes", self.abrir_clientes)

        self.crear_boton_menu("Servicios", self.abrir_servicios)

        self.crear_boton_menu("Reservas", self.abrir_reservas)

    def crear_boton_menu(self, texto, comando):
        """
        Crea un boton para el menu lateral.
        """

        tk.Button(
            self.menu_lateral,
            text=texto,
            command=comando,
            width=18,
            bg="#FFFFFF",
            fg="#222222",
            font=("Arial", 10),
            relief="raised",
            cursor="hand2"
        ).pack(
            pady=5,
            padx=10
        )

    # ==============================================
    # PANEL PRINCIPAL
    # ==============================================

    def crear_panel_principal(self):
        """
        Construye el panel donde se muestra el resumen
        general del sistema.
        """

        self.panel_principal = tk.Frame(
            self.ventana,
            bg="#EEEEEE"
        )

        self.panel_principal.pack(
            side="right",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Titulo principal.
        tk.Label(
            self.panel_principal,
            text="Panel principal",
            bg="#EEEEEE",
            fg="#222222",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(5, 5))

        tk.Label(
            self.panel_principal,
            text="Resumen general de Software FJ",
            bg="#EEEEEE",
            fg="#555555",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(0, 25))

        # Indicadores generales.
        tk.Label(
            self.panel_principal,
            text="Informacion general",
            bg="#EEEEEE",
            fg="#222222",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=10)

        # Contenedor de indicadores.
        contenedor = tk.Frame(
            self.panel_principal,
            bg="#EEEEEE"
        )

        contenedor.pack(fill="x", pady=5)

        # Crear tarjetas.
        self.tarjeta_clientes = self.crear_tarjeta(
            contenedor,
            "Clientes registrados",
            0
        )

        self.tarjeta_servicios = self.crear_tarjeta(
            contenedor,
            "Servicios registrados",
            1
        )

        self.tarjeta_reservas = self.crear_tarjeta(
            contenedor,
            "Reservas registradas",
            2
        )

        # Seccion de estados.
        tk.Label(
            self.panel_principal,
            text="Estado de las reservas",
            bg="#EEEEEE",
            fg="#222222",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(30, 10))

        # Contenedor de estados.
        self.panel_estados = tk.LabelFrame(
            self.panel_principal,
            text="Resumen de reservas",
            bg="#FFFFFF",
            fg="#222222",
            font=("Arial", 10),
            padx=15,
            pady=10
        )

        self.panel_estados.pack(
            fill="x",
            pady=5
        )

        # Crear etiquetas para los estados.
        self.etiquetas_estados = {}

        estados = [
            ("Pendientes", "pendientes"),
            ("Confirmadas", "confirmadas"),
            ("Canceladas", "canceladas"),
            ("Procesadas", "procesadas")
        ]

        for nombre, clave in estados:

            fila = tk.Frame(
                self.panel_estados,
                bg="#FFFFFF"
            )

            fila.pack(fill="x", pady=5)

            tk.Label(
                fila,
                text=nombre,
                bg="#FFFFFF",
                fg="#222222",
                font=("Arial", 10)
            ).pack(side="left")

            etiqueta = tk.Label(
                fila,
                text="0",
                bg="#FFFFFF",
                fg="#222222",
                font=("Arial", 10, "bold")
            )

            etiqueta.pack(side="right")

            self.etiquetas_estados[clave] = etiqueta

        # Boton de actualizacion.
        tk.Button(
            self.panel_principal,
            text="Actualizar informacion",
            command=self.refrescar_resumen,
            bg="#D9E2F3",
            fg="#222222",
            font=("Arial", 10),
            padx=10,
            pady=5
        ).pack(
            anchor="e",
            pady=20
        )

    # ==============================================
    # TARJETAS INFORMATIVAS
    # ==============================================

    def crear_tarjeta(self, contenedor, titulo, columna):
        """
        Crea un recuadro para mostrar un indicador.
        """

        tarjeta = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg="#FFFFFF",
            fg="#222222",
            font=("Arial", 9),
            padx=15,
            pady=15
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        contenedor.grid_columnconfigure(
            columna,
            weight=1
        )

        etiqueta_valor = tk.Label(
            tarjeta,
            text="0",
            bg="#FFFFFF",
            fg="#222222",
            font=("Arial", 22, "bold")
        )

        etiqueta_valor.pack()

        return etiqueta_valor

    # ==============================================
    # ACTUALIZACION DE INFORMACION
    # ==============================================

    def refrescar_resumen(self):
        """
        Consulta el gestor y actualiza los indicadores.
        """

        resumen = self.gestor.obtener_resumen()

        # Actualizar cantidad de registros.
        self.tarjeta_clientes.config(
            text=str(resumen["clientes"])
        )

        self.tarjeta_servicios.config(
            text=str(resumen["servicios"])
        )

        self.tarjeta_reservas.config(
            text=str(resumen["reservas"])
        )

        # Actualizar estados de las reservas.
        for clave, etiqueta in self.etiquetas_estados.items():

            etiqueta.config(
                text=str(resumen[clave])
            )

    # ==============================================
    # NAVEGACION
    # ==============================================

    def mostrar_inicio(self):
        """
        Actualiza la informacion del panel principal.
        """

        self.refrescar_resumen()

    def mostrar_seccion_pendiente(self, nombre):
        """
        Muestra un mensaje para las secciones
        que todavia no han sido desarrolladas.
        """

        messagebox.showinfo(
            "Seccion en desarrollo",
            f"La seccion de {nombre} se implementara "
            "en una siguiente etapa."
        )

    def abrir_clientes(self):
        """
        Abre la ventana de administracion de clientes.
        """

        from ventana_clientes import VentanaClientes

        VentanaClientes(
            self.ventana,
            self.gestor
        )

    def abrir_servicios(self):
        """
        Abre la ventana de administracion de servicios.
        """

        from ventana_servicios import VentanaServicios

        VentanaServicios(
        self.ventana,
        self.gestor
    )

    def abrir_reservas(self):
        """
        Abre la ventana de administracion de reservas.
        """

        from ventana_reservas import VentanaReservas

        VentanaReservas(
            self.ventana,
            self.gestor
        )


    # ==============================================
    # CIERRE DE LA APLICACION
    # ==============================================

    def cerrar_aplicacion(self):
        """
        Solicita confirmacion antes de cerrar el programa.
        """

        respuesta = messagebox.askyesno(
            "Cerrar programa",
            "¿Deseas salir de Software FJ?"
        )

        if respuesta:
            self.ventana.destroy()


# ==============================================
# EJECUCION INDEPENDIENTE
# ==============================================

if __name__ == "__main__":

    ventana = tk.Tk()

    gestor = GestorSistema()

    aplicacion = InterfazPrincipal(
        ventana,
        gestor
    )

    ventana.mainloop()
