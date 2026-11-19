"""
ARCHIVO: ventana_servicios.py

DESCRIPCION:
Implementa la ventana grafica para administrar los
servicios disponibles en el sistema.

PSDT: Como tal no se solicitó en el PDF del ejercicio ni en la guía de desarrollo del ejercicio, 
pero se incluyó para facilitar la visualización de los resultados y la interacción con el sistema.

FUNCIONALIDADES:
- Registrar reservas de salas.
- Registrar alquileres de equipos.
- Registrar asesorias especializadas.
- Buscar servicios por codigo.
- Mostrar todos los servicios registrados.
- Consultar la disponibilidad de los servicios.
- Limpiar los campos del formulario.

DEPENDENCIAS:
- tkinter: Biblioteca para crear interfaces graficas en Python.
- servicios_especializados.py: Contiene la definicion de las clases ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
- gestor_sistema.py: Contiene la clase GestorSistema que administra clientes, servicios y reservas.
- excepciones.py: Contiene la definicion de la clase DatosInvalidosError.
- logger_config.py: Configura el registro de eventos y errores del sistema.
"""

import tkinter as tk
from tkinter import messagebox

from servicios_especializados import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

from excepciones import DatosInvalidosError
from logger_config import logger


class VentanaServicios:
    """
    Construye la ventana para administrar los servicios
    registrados en Software FJ.
    """

    def __init__(self, ventana_principal, gestor):

        self.gestor = gestor

        # Crear ventana secundaria.
        self.ventana = tk.Toplevel(ventana_principal)

        self.ventana.title("Software FJ - Gestion de servicios")
        self.ventana.geometry("780x650")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#EEEEEE")

        # Variable para seleccionar el tipo de servicio.
        self.tipo_servicio = tk.StringVar()

        self.tipo_servicio.set("Reserva de salas")

        # Variable para controlar la disponibilidad.
        self.disponibilidad = tk.BooleanVar(value=True)

        # Construir los componentes.
        self.crear_formulario()
        self.crear_botones()
        self.crear_lista_servicios()

        # Mostrar los servicios existentes.
        self.mostrar_servicios()

    # ==============================================
    # FORMULARIO DE SERVICIOS
    # ==============================================

    def crear_formulario(self):
        """
        Construye el formulario para registrar servicios.
        """

        tk.Label(
            self.ventana,
            text="GESTION DE SERVICIOS",
            bg="#EEEEEE",
            fg="#222222",
            font=("Arial", 17, "bold")
        ).pack(pady=15)

        self.formulario = tk.LabelFrame(
            self.ventana,
            text="Informacion del servicio",
            bg="#FFFFFF",
            fg="#222222",
            font=("Arial", 10),
            padx=15,
            pady=12
        )

        self.formulario.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Tipo de servicio.
        tk.Label(
            self.formulario,
            text="Tipo de servicio:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w", pady=6)

        opciones = [
            "Reserva de salas",
            "Alquiler de equipos",
            "Asesoria especializada"
        ]

        self.menu_tipo = tk.OptionMenu(
            self.formulario,
            self.tipo_servicio,
            *opciones,
            command=self.actualizar_campos
        )

        self.menu_tipo.config(width=28)

        self.menu_tipo.grid(
            row=0,
            column=1,
            padx=10,
            pady=6,
            sticky="w"
        )

        # Codigo del servicio.
        tk.Label(
            self.formulario,
            text="Codigo:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=1, column=0, sticky="w", pady=6)

        self.entrada_codigo = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_codigo.grid(
            row=1,
            column=1,
            padx=10,
            pady=6
        )

        # Descripcion.
        tk.Label(
            self.formulario,
            text="Descripcion:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=2, column=0, sticky="w", pady=6)

        self.entrada_descripcion = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_descripcion.grid(
            row=2,
            column=1,
            padx=10,
            pady=6
        )

        # Contenedor para los campos especificos.
        self.campos_especificos = tk.Frame(
            self.formulario,
            bg="#FFFFFF"
        )

        self.campos_especificos.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        # Campo de disponibilidad.
        self.check_disponibilidad = tk.Checkbutton(
            self.formulario,
            text="Servicio disponible",
            variable=self.disponibilidad,
            bg="#FFFFFF",
            font=("Arial", 10)
        )

        self.check_disponibilidad.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=10
        )

        # Crear los campos iniciales.
        self.actualizar_campos()

    # ==============================================
    # CAMPOS SEGUN EL TIPO DE SERVICIO
    # ==============================================

    def actualizar_campos(self, seleccion=None):
        """
        Cambia los campos del formulario dependiendo
        del tipo de servicio seleccionado.
        """

        # Eliminar los campos anteriores.
        for elemento in self.campos_especificos.winfo_children():
            elemento.destroy()

        # Reiniciar el diccionario de entradas.
        # Esto evita conservar referencias a campos eliminados.
            self.entradas_especificas = {}

        tipo = self.tipo_servicio.get()

        if tipo == "Reserva de salas":

            self.crear_campo_especifico(
                "Capacidad de personas:",
                "capacidad"
            )

            self.crear_campo_especifico(
                "Tarifa por hora:",
                "tarifa"
            )

        elif tipo == "Alquiler de equipos":

            self.crear_campo_especifico(
                "Tipo de equipo:",
                "tipo_equipo"
            )

            self.crear_campo_especifico(
                "Tarifa por dia:",
                "tarifa"
            )

        elif tipo == "Asesoria especializada":

            self.crear_campo_especifico(
                "Area de asesoria:",
                "area"
            )

            self.crear_campo_especifico(
                "Tarifa por hora:",
                "tarifa"
            )

    def crear_campo_especifico(self, texto, nombre):
        """
        Crea un campo adicional dentro del formulario.
        """

        fila = len(self.campos_especificos.winfo_children()) // 2

        tk.Label(
            self.campos_especificos,
            text=texto,
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=6
        )

        entrada = tk.Entry(
            self.campos_especificos,
            width=35
        )

        entrada.grid(
            row=fila,
            column=1,
            padx=10,
            pady=6
        )

        # Guardar la referencia al campo.
        if not hasattr(self, "entradas_especificas"):
            self.entradas_especificas = {}

        self.entradas_especificas[nombre] = entrada

    # ==============================================
    # BOTONES
    # ==============================================

    def crear_botones(self):
        """
        Construye los botones de administracion.
        """

        contenedor_botones = tk.Frame(
            self.ventana,
            bg="#EEEEEE"
        )

        contenedor_botones.pack(pady=12)

        tk.Button(
            contenedor_botones,
            text="Registrar servicio",
            command=self.registrar_servicio,
            bg="#D9E2F3",
            width=18,
            font=("Arial", 9)
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            contenedor_botones,
            text="Buscar servicio",
            command=self.buscar_servicio,
            bg="#D9E2F3",
            width=18,
            font=("Arial", 9)
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            contenedor_botones,
            text="Mostrar todos",
            command=self.mostrar_servicios,
            bg="#D9E2F3",
            width=18,
            font=("Arial", 9)
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            contenedor_botones,
            text="Limpiar",
            command=self.limpiar_formulario,
            bg="#D9E2F3",
            width=18,
            font=("Arial", 9)
        ).grid(row=0, column=3, padx=5)

    # ==============================================
    # LISTA DE SERVICIOS
    # ==============================================

    def crear_lista_servicios(self):
        """
        Construye el espacio para mostrar los servicios.
        """

        contenedor_lista = tk.LabelFrame(
            self.ventana,
            text="Servicios registrados",
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

        self.lista_servicios = tk.Listbox(
            contenedor_lista,
            font=("Arial", 9),
            height=12
        )

        self.lista_servicios.pack(
            side="left",
            fill="both",
            expand=True
        )

        desplazamiento = tk.Scrollbar(
            contenedor_lista,
            orient="vertical",
            command=self.lista_servicios.yview
        )

        desplazamiento.pack(
            side="right",
            fill="y"
        )

        self.lista_servicios.config(
            yscrollcommand=desplazamiento.set
        )

    # ==============================================
    # REGISTRAR SERVICIOS
    # ==============================================

    def registrar_servicio(self):
        """
        Obtiene los datos del formulario y crea
        el objeto correspondiente al tipo seleccionado.
        """

        try:

            codigo = self.entrada_codigo.get().strip()

            descripcion = self.entrada_descripcion.get().strip()

            disponible = self.disponibilidad.get()

            # Obtener los campos especificos.
            datos = {
                nombre: entrada.get().strip()
                for nombre, entrada in self.entradas_especificas.items()
            }

            # Crear una reserva de sala.
            if self.tipo_servicio.get() == "Reserva de salas":

                servicio = ReservaSala(
                    codigo,
                    descripcion,
                    int(datos["capacidad"]),
                    float(datos["tarifa"]),
                    disponible
                )

            # Crear un alquiler de equipos.
            elif self.tipo_servicio.get() == "Alquiler de equipos":

                servicio = AlquilerEquipo(
                    codigo,
                    descripcion,
                    datos["tipo_equipo"],
                    float(datos["tarifa"]),
                    disponible
                )

            # Crear una asesoria especializada.
            elif self.tipo_servicio.get() == "Asesoria especializada":

                servicio = AsesoriaEspecializada(
                    codigo,
                    descripcion,
                    datos["area"],
                    float(datos["tarifa"]),
                    disponible
                )

            # Registrar el servicio en el gestor.
            self.gestor.registrar_servicio(servicio)

        except ValueError:

            messagebox.showerror(
                "Datos incorrectos",
                "La capacidad y las tarifas deben contener valores numericos.",
                parent=self.ventana
            )

        except DatosInvalidosError as error:

            messagebox.showerror(
                "Error de registro",
                str(error),
                parent=self.ventana
            )

            logger.error(
                "Error al registrar servicio: %s",
                error
            )

        except Exception as error:

            import traceback

            # Mostrar el error completo en la terminal.    
            print("\n=== ERROR AL REGISTRAR SERVICIO ===")
            traceback.print_exc()
            print("=== FIN DEL ERROR ===\n")


            # Mostrar el error especifico en la ventana.
            messagebox.showerror(
                "Error inesperado",
                f"Tipo de error: {type(error).__name__}\n\n"
                f"Detalle: {error}",
                parent=self.ventana
            )

            logger.exception(
                "Error inesperado al registrar servicio: %s",
                error
            )

        else:

            messagebox.showinfo(
                "Registro exitoso",
                "El servicio fue registrado correctamente.",
                parent=self.ventana
            )

            logger.info(
                "Servicio registrado desde la interfaz."
            )

            self.mostrar_servicios()
            self.limpiar_formulario()

    # ==============================================
    # BUSCAR SERVICIOS
    # ==============================================

    def buscar_servicio(self):
        """
        Busca un servicio mediante su codigo.
        """

        codigo = self.entrada_codigo.get().strip()

        if not codigo:

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa el codigo del servicio.",
                parent=self.ventana
            )

            return

        try:

            servicio = self.gestor.buscar_servicio(codigo)

            if servicio is None:

                messagebox.showinfo(
                    "Busqueda",
                    "No se encontro ningun servicio.",
                    parent=self.ventana
                )

                return

            # Mostrar informacion del servicio.
            self.lista_servicios.delete(0, tk.END)

            informacion = self.obtener_informacion(servicio)

            self.lista_servicios.insert(
                tk.END,
                informacion
            )

            messagebox.showinfo(
                "Busqueda exitosa",
                "Servicio encontrado correctamente.",
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error de busqueda",
                "Ocurrio un problema al buscar el servicio.",
                parent=self.ventana
            )

            logger.exception(
                "Error al buscar servicio: %s",
                error
            )

    # ==============================================
    # MOSTRAR SERVICIOS
    # ==============================================

    def mostrar_servicios(self):
        """
        Consulta los servicios registrados y los
        muestra en la lista.
        """

        self.lista_servicios.delete(0, tk.END)

        servicios = self.gestor.listar_servicios()

        if not servicios:

            self.lista_servicios.insert(
                tk.END,
                "No hay servicios registrados."
            )

            return

        for servicio in servicios:

            informacion = self.obtener_informacion(servicio)

            self.lista_servicios.insert(
                tk.END,
                informacion
            )

    def obtener_informacion(self, servicio):
        """
        Organiza la informacion de un servicio
        para mostrarla en la lista.
        """

        informacion = (
            f"Codigo: {servicio.obtener_codigo()} | "
            f"Nombre: {servicio.obtener_nombre()} | "
            f"Descripcion: {servicio.obtener_descripcion()} | "
        )

        if isinstance(servicio, ReservaSala):

            informacion += (
                f"Capacidad: {servicio.obtener_capacidad()} personas | "
                f"Tarifa por hora: ${servicio.obtener_tarifa_base():,.2f} COP"
            )

        elif isinstance(servicio, AlquilerEquipo):

            informacion += (
                f"Equipo: {servicio.obtener_tipo_equipo()} | "
                f"Tarifa por dia: ${servicio.obtener_tarifa_base():,.2f} COP"
            )

        elif isinstance(servicio, AsesoriaEspecializada):

            informacion += (
                f"Area: {servicio.obtener_area()} | "
                f"Tarifa por hora: ${servicio.obtener_tarifa_base():,.2f} COP"
            )

        estado = "Disponible" if servicio.esta_disponible() else "No disponible"

        informacion += f" | Estado: {estado}"

        return informacion

    # ==============================================
    # LIMPIAR FORMULARIO
    # ==============================================

    def limpiar_formulario(self):
        """
        Borra los campos del formulario y restablece
        la disponibilidad inicial.
        """

        self.entrada_codigo.delete(0, tk.END)

        self.entrada_descripcion.delete(0, tk.END)

        for entrada in self.entradas_especificas.values():
            entrada.delete(0, tk.END)

        self.disponibilidad.set(True)

        self.tipo_servicio.set("Reserva de salas")

        self.actualizar_campos()