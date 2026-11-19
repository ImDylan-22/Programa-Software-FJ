"""
ARCHIVO: ventana_clientes.py

DESCRIPCION:
Implementa la ventana grafica para administrar clientes
mediante la biblioteca Tkinter.

PSDT: Como tal no se solicitó en el PDF del ejercicio ni en la guía de desarrollo del ejercicio, 
pero se incluyó para facilitar la visualización de los resultados y la interacción con el sistema.

FUNCIONALIDADES:
- Registrar nuevos clientes.
- Buscar clientes por identificacion.
- Mostrar todos los clientes registrados.
- Limpiar los campos del formulario.
- Visualizar la informacion de los clientes.

DEPENDENCIAS:
- tkinter: Biblioteca para crear interfaces graficas en Python.
- cliente.py: Contiene la definicion de la clase Cliente.
- gestor_sistema.py: Contiene la clase GestorSistema que administra clientes, servicios y reservas.
- excepciones.py: Contiene la definicion de la clase DatosInvalidosError.
- logger_config.py: Configura el registro de eventos y errores del sistema.

"""

import tkinter as tk
from tkinter import messagebox

from cliente import Cliente
from excepciones import DatosInvalidosError
from logger_config import logger


class VentanaClientes:
    """
    Construye la ventana para administrar los clientes
    registrados en Software FJ.
    """

    def __init__(self, ventana_principal, gestor):

        self.gestor = gestor

        # Crear una ventana secundaria.
        self.ventana = tk.Toplevel(ventana_principal)

        self.ventana.title("Software FJ - Gestion de clientes")
        self.ventana.geometry("750x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#EEEEEE")

        # Construir los componentes.
        self.crear_formulario()
        self.crear_botones()
        self.crear_lista_clientes()

        # Mostrar los clientes existentes.
        self.mostrar_clientes()

    # ==============================================
    # FORMULARIO DE CLIENTES
    # ==============================================

    def crear_formulario(self):
        """
        Construye los campos para introducir
        la informacion de un nuevo cliente.
        """

        titulo = tk.Label(
            self.ventana,
            text="GESTION DE CLIENTES",
            bg="#EEEEEE",
            fg="#222222",
            font=("Arial", 17, "bold")
        )

        titulo.pack(pady=15)

        # Contenedor del formulario.
        self.formulario = tk.LabelFrame(
            self.ventana,
            text="Informacion del cliente",
            bg="#FFFFFF",
            fg="#222222",
            font=("Arial", 10),
            padx=15,
            pady=15
        )

        self.formulario.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Identificacion.
        tk.Label(
            self.formulario,
            text="Identificacion:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w", pady=7)

        self.entrada_identificacion = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_identificacion.grid(
            row=0,
            column=1,
            padx=10,
            pady=7
        )

        # Nombre.
        tk.Label(
            self.formulario,
            text="Nombre completo:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=1, column=0, sticky="w", pady=7)

        self.entrada_nombre = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_nombre.grid(
            row=1,
            column=1,
            padx=10,
            pady=7
        )

        # Correo electronico.
        tk.Label(
            self.formulario,
            text="Correo electronico:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=2, column=0, sticky="w", pady=7)

        self.entrada_correo = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_correo.grid(
            row=2,
            column=1,
            padx=10,
            pady=7
        )

        # Telefono.
        tk.Label(
            self.formulario,
            text="Telefono:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=3, column=0, sticky="w", pady=7)

        self.entrada_telefono = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_telefono.grid(
            row=3,
            column=1,
            padx=10,
            pady=7
        )

    # ==============================================
    # BOTONES DEL FORMULARIO
    # ==============================================

    def crear_botones(self):
        """
        Construye los botones para realizar
        las operaciones de administracion.
        """

        contenedor_botones = tk.Frame(
            self.ventana,
            bg="#EEEEEE"
        )

        contenedor_botones.pack(pady=15)

        # Registrar cliente.
        tk.Button(
            contenedor_botones,
            text="Registrar cliente",
            command=self.registrar_cliente,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=0, column=0, padx=5)

        # Buscar cliente.
        tk.Button(
            contenedor_botones,
            text="Buscar cliente",
            command=self.buscar_cliente,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=0, column=1, padx=5)

        # Mostrar todos los clientes.
        tk.Button(
            contenedor_botones,
            text="Mostrar todos",
            command=self.mostrar_clientes,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=0, column=2, padx=5)

        # Limpiar formulario.
        tk.Button(
            contenedor_botones,
            text="Limpiar",
            command=self.limpiar_formulario,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=0, column=3, padx=5)

    # ==============================================
    # LISTA DE CLIENTES
    # ==============================================

    def crear_lista_clientes(self):
        """
        Construye el espacio donde se muestran
        los clientes registrados.
        """

        contenedor_lista = tk.LabelFrame(
            self.ventana,
            text="Clientes registrados",
            bg="#FFFFFF",
            fg="#222222",
            font=("Arial", 10),
            padx=10,
            pady=10
        )

        contenedor_lista.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        # Lista de clientes.
        self.lista_clientes = tk.Listbox(
            contenedor_lista,
            font=("Arial", 10),
            height=12
        )

        self.lista_clientes.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Barra de desplazamiento.
        desplazamiento = tk.Scrollbar(
            contenedor_lista,
            orient="vertical",
            command=self.lista_clientes.yview
        )

        desplazamiento.pack(
            side="right",
            fill="y"
        )

        self.lista_clientes.config(
            yscrollcommand=desplazamiento.set
        )

    # ==============================================
    # REGISTRO DE CLIENTES
    # ==============================================

    def registrar_cliente(self):
        """
        Obtiene los datos del formulario, crea un objeto
        Cliente y lo registra mediante GestorSistema.
        """

        try:
            identificacion = self.entrada_identificacion.get().strip()
            nombre = self.entrada_nombre.get().strip()
            correo = self.entrada_correo.get().strip()
            telefono = self.entrada_telefono.get().strip()

            # Crear el objeto cliente.
            cliente = Cliente(
                identificacion,
                nombre,
                correo,
                telefono
            )

            # Registrar el cliente en el gestor.
            self.gestor.registrar_cliente(cliente)

        except DatosInvalidosError as error:

            messagebox.showerror(
                "Error de registro",
                str(error),
                parent=self.ventana
            )

            logger.error(
                "Error al registrar cliente: %s",
                error
            )

        except Exception as error:

            messagebox.showerror(
                "Error inesperado",
                "No fue posible registrar el cliente."
            )

            logger.exception(
                "Error inesperado al registrar cliente: %s",
                error
            )

        else:

            messagebox.showinfo(
                "Registro exitoso",
                "El cliente fue registrado correctamente.",
                parent=self.ventana
            )

            logger.info(
                "Cliente registrado desde la interfaz."
            )

            self.mostrar_clientes()
            self.limpiar_formulario()

    # ==============================================
    # BUSQUEDA DE CLIENTES
    # ==============================================

    def buscar_cliente(self):
        """
        Busca un cliente utilizando su identificacion.
        """

        identificacion = self.entrada_identificacion.get().strip()

        if not identificacion:

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa la identificacion del cliente.",
                parent=self.ventana
            )

            return

        try:

            cliente = self.gestor.buscar_cliente(identificacion)

            if cliente is None:

                messagebox.showinfo(
                    "Busqueda",
                    "No se encontro ningun cliente.",
                    parent=self.ventana
                )

                return

            # Mostrar los datos encontrados en el formulario.
            self.limpiar_formulario()

            self.entrada_identificacion.insert(
                0,
                cliente.obtener_identificacion()
            )

            self.entrada_nombre.insert(
                0,
                cliente.obtener_nombre()
            )

            self.entrada_correo.insert(
                0,
                cliente.obtener_correo()
            )

            self.entrada_telefono.insert(
                0,
                cliente.obtener_telefono()
            )

            messagebox.showinfo(
                "Busqueda exitosa",
                "Cliente encontrado correctamente.",
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error de busqueda",
                "Ocurrio un problema al buscar el cliente.",
                parent=self.ventana
            )

            logger.exception(
                "Error al buscar cliente: %s",
                error
            )

    # ==============================================
    # MOSTRAR CLIENTES
    # ==============================================

    def mostrar_clientes(self):
        """
        Consulta los clientes registrados y los
        muestra en el componente Listbox.
        """

        self.lista_clientes.delete(0, tk.END)

        clientes = self.gestor.listar_clientes()

        if not clientes:

            self.lista_clientes.insert(
                tk.END,
                "No hay clientes registrados."
            )

            return

        for cliente in clientes:

            informacion = (
                f"Identificacion: {cliente.obtener_identificacion()} | "
                f"Nombre: {cliente.obtener_nombre()} | "
                f"Correo: {cliente.obtener_correo()} | "
                f"Telefono: {cliente.obtener_telefono()}"
            )

            self.lista_clientes.insert(
                tk.END,
                informacion
            )

    # ==============================================
    # LIMPIAR FORMULARIO
    # ==============================================

    def limpiar_formulario(self):
        """
        Borra el contenido de todos los campos
        del formulario.
        """

        self.entrada_identificacion.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_correo.delete(0, tk.END)
        self.entrada_telefono.delete(0, tk.END)
