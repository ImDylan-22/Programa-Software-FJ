"""
ARCHIVO: ventana_reservas.py

DESCRIPCION:
Implementa la ventana grafica para administrar las
reservas de clientes y servicios.

PSDT: Como tal no se solicitó en el PDF del ejercicio ni en la guía de desarrollo del ejercicio, 
pero se incluyó para facilitar la visualización de los resultados y la interacción con el sistema.

FUNCIONALIDADES:
- Crear nuevas reservas.
- Buscar reservas por codigo.
- Mostrar todas las reservas.
- Confirmar reservas.
- Cancelar reservas.
- Procesar reservas y calcular sus costos.
- Aplicar impuestos y descuentos.

DEPENDENCIAS:
- tkinter: Biblioteca para crear interfaces graficas en Python.
- gestor_sistema.py: Contiene la clase GestorSistema que administra clientes, servicios y reservas.
- excepciones.py: Contiene la definicion de la clase DatosInvalidosError.
- logger_config.py: Configura el registro de eventos y errores del sistema.
"""

import tkinter as tk
from tkinter import messagebox

from excepciones import DatosInvalidosError
from logger_config import logger


class VentanaReservas:
    """
    Construye la ventana para administrar las reservas
    registradas en Software FJ.
    """

    def __init__(self, ventana_principal, gestor):

        self.gestor = gestor

        # Crear ventana secundaria.
        self.ventana = tk.Toplevel(ventana_principal)

        self.ventana.title("Software FJ - Gestion de reservas")
        self.ventana.geometry("850x680")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#EEEEEE")

        # Variable para controlar los impuestos.
        self.incluir_impuesto = tk.BooleanVar(value=False)

        # Construir los componentes.
        self.crear_formulario()
        self.crear_botones()
        self.crear_lista_reservas()

        # Mostrar las reservas existentes.
        self.mostrar_reservas()

    # ==============================================
    # FORMULARIO DE RESERVAS
    # ==============================================

    def crear_formulario(self):
        """
        Construye los campos necesarios para crear
        y consultar una reserva.
        """

        tk.Label(
            self.ventana,
            text="GESTION DE RESERVAS",
            bg="#EEEEEE",
            fg="#222222",
            font=("Arial", 17, "bold")
        ).pack(pady=15)

        self.formulario = tk.LabelFrame(
            self.ventana,
            text="Informacion de la reserva",
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

        # Codigo de reserva.
        tk.Label(
            self.formulario,
            text="Codigo de reserva:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w", pady=6)

        self.entrada_codigo = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_codigo.grid(
            row=0,
            column=1,
            padx=10,
            pady=6
        )

        # Identificacion del cliente.
        tk.Label(
            self.formulario,
            text="Identificacion del cliente:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=1, column=0, sticky="w", pady=6)

        self.entrada_cliente = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_cliente.grid(
            row=1,
            column=1,
            padx=10,
            pady=6
        )

        # Codigo del servicio.
        tk.Label(
            self.formulario,
            text="Codigo del servicio:",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=2, column=0, sticky="w", pady=6)

        self.entrada_servicio = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_servicio.grid(
            row=2,
            column=1,
            padx=10,
            pady=6
        )

        # Duracion de la reserva.
        tk.Label(
            self.formulario,
            text="Duracion (horas o dias):",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=3, column=0, sticky="w", pady=6)

        self.entrada_duracion = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_duracion.grid(
            row=3,
            column=1,
            padx=10,
            pady=6
        )

        # Opcion para incluir impuestos.
        self.check_impuesto = tk.Checkbutton(
            self.formulario,
            text="Incluir impuesto al procesar",
            variable=self.incluir_impuesto,
            bg="#FFFFFF",
            font=("Arial", 10)
        )

        self.check_impuesto.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=6
        )

        # Descuento.
        tk.Label(
            self.formulario,
            text="Descuento (%):",
            bg="#FFFFFF",
            font=("Arial", 10)
        ).grid(row=5, column=0, sticky="w", pady=6)

        self.entrada_descuento = tk.Entry(
            self.formulario,
            width=35
        )

        self.entrada_descuento.insert(0, "0")

        self.entrada_descuento.grid(
            row=5,
            column=1,
            padx=10,
            pady=6
        )

    # ==============================================
    # BOTONES
    # ==============================================

    def crear_botones(self):
        """
        Construye los botones para administrar
        las diferentes operaciones de reservas.
        """

        contenedor_botones = tk.Frame(
            self.ventana,
            bg="#EEEEEE"
        )

        contenedor_botones.pack(pady=12)

        tk.Button(
            contenedor_botones,
            text="Crear reserva",
            command=self.crear_reserva,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=0, column=0, padx=4, pady=5)

        tk.Button(
            contenedor_botones,
            text="Buscar reserva",
            command=self.buscar_reserva,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=0, column=1, padx=4, pady=5)

        tk.Button(
            contenedor_botones,
            text="Mostrar todas",
            command=self.mostrar_reservas,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=0, column=2, padx=4, pady=5)

        tk.Button(
            contenedor_botones,
            text="Confirmar",
            command=self.confirmar_reserva,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=1, column=0, padx=4, pady=5)

        tk.Button(
            contenedor_botones,
            text="Cancelar",
            command=self.cancelar_reserva,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=1, column=1, padx=4, pady=5)

        tk.Button(
            contenedor_botones,
            text="Procesar",
            command=self.procesar_reserva,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=1, column=2, padx=4, pady=5)

        tk.Button(
            contenedor_botones,
            text="Limpiar",
            command=self.limpiar_formulario,
            bg="#D9E2F3",
            width=17,
            font=("Arial", 9)
        ).grid(row=1, column=3, padx=4, pady=5)

    # ==============================================
    # LISTA DE RESERVAS
    # ==============================================

    def crear_lista_reservas(self):
        """
        Construye el espacio donde se muestran
        las reservas registradas.
        """

        contenedor_lista = tk.LabelFrame(
            self.ventana,
            text="Reservas registradas",
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

        self.lista_reservas = tk.Listbox(
            contenedor_lista,
            font=("Arial", 9),
            height=13
        )

        self.lista_reservas.pack(
            side="left",
            fill="both",
            expand=True
        )

        desplazamiento = tk.Scrollbar(
            contenedor_lista,
            orient="vertical",
            command=self.lista_reservas.yview
        )

        desplazamiento.pack(
            side="right",
            fill="y"
        )

        self.lista_reservas.config(
            yscrollcommand=desplazamiento.set
        )

    # ==============================================
    # CREAR RESERVAS
    # ==============================================

    def crear_reserva(self):
        """
        Obtiene los datos del formulario y solicita
        al gestor general la creacion de una reserva.
        """

        try:

            codigo = self.entrada_codigo.get().strip()

            identificacion = self.entrada_cliente.get().strip()

            codigo_servicio = self.entrada_servicio.get().strip()

            duracion = float(
                self.entrada_duracion.get().strip()
            )

            # Crear la reserva mediante el gestor.
            self.gestor.crear_reserva(
                codigo,
                identificacion,
                codigo_servicio,
                duracion
            )

        except ValueError:

            messagebox.showerror(
                "Datos incorrectos",
                "La duracion debe ser un numero valido.",
                parent=self.ventana
            )

        except DatosInvalidosError as error:

            messagebox.showerror(
                "Error de registro",
                str(error),
                parent=self.ventana
            )

            logger.error(
                "Error al crear reserva: %s",
                error
            )

        except Exception as error:

            messagebox.showerror(
                "Error inesperado",
                "No fue posible crear la reserva.",
                parent=self.ventana
            )

            logger.exception(
                "Error inesperado al crear reserva: %s",
                error
            )

        else:

            messagebox.showinfo(
                "Registro exitoso",
                "La reserva fue creada correctamente.",
                parent=self.ventana
            )

            logger.info(
                "Reserva creada desde la interfaz."
            )

            self.mostrar_reservas()
            self.limpiar_formulario()

    # ==============================================
    # BUSCAR RESERVAS
    # ==============================================

    def buscar_reserva(self):
        """
        Busca una reserva utilizando su codigo.
        """

        codigo = self.entrada_codigo.get().strip()

        if not codigo:

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa el codigo de la reserva.",
                parent=self.ventana
            )

            return

        try:

            reserva = self.gestor.buscar_reserva(codigo)

            if reserva is None:

                messagebox.showinfo(
                    "Busqueda",
                    "No se encontro ninguna reserva.",
                    parent=self.ventana
                )

                return

            # Mostrar los datos de la reserva.
            self.lista_reservas.delete(0, tk.END)

            informacion = self.obtener_informacion(reserva)

            self.lista_reservas.insert(
                tk.END,
                informacion
            )

            # Mostrar los datos relacionados.
            self.entrada_cliente.delete(0, tk.END)
            self.entrada_servicio.delete(0, tk.END)
            self.entrada_duracion.delete(0, tk.END)

            self.entrada_cliente.insert(
                0,
                reserva.obtener_cliente().obtener_identificacion()
            )

            self.entrada_servicio.insert(
                0,
                reserva.obtener_servicio().obtener_codigo()
            )

            self.entrada_duracion.insert(
                0,
                str(reserva.obtener_duracion())
            )

            messagebox.showinfo(
                "Busqueda exitosa",
                "Reserva encontrada correctamente.",
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error de busqueda",
                "Ocurrio un problema al buscar la reserva.",
                parent=self.ventana
            )

            logger.exception(
                "Error al buscar reserva: %s",
                error
            )

    # ==============================================
    # MOSTRAR RESERVAS
    # ==============================================

    def mostrar_reservas(self):
        """
        Consulta las reservas registradas y las
        muestra en la lista de la ventana.
        """

        self.lista_reservas.delete(0, tk.END)

        reservas = self.gestor.listar_reservas()

        if not reservas:

            self.lista_reservas.insert(
                tk.END,
                "No hay reservas registradas."
            )

            return

        for reserva in reservas:

            informacion = self.obtener_informacion(reserva)

            self.lista_reservas.insert(
                tk.END,
                informacion
            )

    def obtener_informacion(self, reserva):
        """
        Organiza los datos de una reserva para
        mostrarlos en la lista.
        """

        cliente = reserva.obtener_cliente()

        servicio = reserva.obtener_servicio()

        costo = reserva.obtener_costo()

        if costo is None:

            costo_texto = "Pendiente"

        else:

            costo_texto = f"${costo:,.2f} COP"

        informacion = (
            f"Codigo: {reserva.obtener_codigo()} | "
            f"Cliente: {cliente.obtener_nombre()} | "
            f"Servicio: {servicio.obtener_nombre()} | "
            f"Duracion: {reserva.obtener_duracion()} | "
            f"Estado: {reserva.obtener_estado()} | "
            f"Costo: {costo_texto}"
        )

        return informacion

    # ==============================================
    # CONFIRMAR RESERVAS
    # ==============================================

    def confirmar_reserva(self):
        """
        Cambia el estado de una reserva a confirmada.
        """

        codigo = self.entrada_codigo.get().strip()

        if not codigo:

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa el codigo de la reserva.",
                parent=self.ventana
            )

            return

        try:

            self.gestor.confirmar_reserva(codigo)

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )

            logger.exception(
                "Error al confirmar reserva: %s",
                error
            )

        else:

            messagebox.showinfo(
                "Reserva confirmada",
                "La reserva fue confirmada correctamente.",
                parent=self.ventana
            )

            logger.info(
                "Reserva confirmada: %s",
                codigo
            )

            self.mostrar_reservas()

    # ==============================================
    # CANCELAR RESERVAS
    # ==============================================

    def cancelar_reserva(self):
        """
        Cancela una reserva utilizando su codigo.
        """

        codigo = self.entrada_codigo.get().strip()

        if not codigo:

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa el codigo de la reserva.",
                parent=self.ventana
            )

            return

        try:

            self.gestor.cancelar_reserva(codigo)

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )

            logger.exception(
                "Error al cancelar reserva: %s",
                error
            )

        else:

            messagebox.showinfo(
                "Reserva cancelada",
                "La reserva fue cancelada correctamente.",
                parent=self.ventana
            )

            logger.info(
                "Reserva cancelada: %s",
                codigo
            )

            self.mostrar_reservas()

    # ==============================================
    # PROCESAR RESERVAS
    # ==============================================

    def procesar_reserva(self):
        """
        Procesa una reserva y calcula su costo final,
        teniendo en cuenta impuestos y descuentos.
        """

        codigo = self.entrada_codigo.get().strip()

        if not codigo:

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa el codigo de la reserva.",
                parent=self.ventana
            )

            return

        try:

            descuento = float(
                self.entrada_descuento.get().strip()
            )

            # Procesar la reserva mediante el gestor.
            self.gestor.procesar_reserva(
                codigo,
                incluir_impuesto=self.incluir_impuesto.get(),
                descuento=descuento
            )

            # Consultar nuevamente la reserva.
            reserva = self.gestor.buscar_reserva(codigo)

        except ValueError:

            messagebox.showerror(
                "Dato incorrecto",
                "El descuento debe ser un valor numerico.",
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error de procesamiento",
                str(error),
                parent=self.ventana
            )

            logger.exception(
                "Error al procesar reserva: %s",
                error
            )

        else:

            messagebox.showinfo(
                "Procesamiento exitoso",
                f"Reserva procesada correctamente.\n\n"
                f"Costo final: ${reserva.obtener_costo():,.2f} COP",
                parent=self.ventana
            )

            logger.info(
                "Reserva procesada: %s",
                codigo
            )

            self.mostrar_reservas()

    # ==============================================
    # LIMPIAR FORMULARIO
    # ==============================================

    def limpiar_formulario(self):
        """
        Limpia los campos del formulario y restablece
        los valores iniciales.
        """

        self.entrada_codigo.delete(0, tk.END)

        self.entrada_cliente.delete(0, tk.END)

        self.entrada_servicio.delete(0, tk.END)

        self.entrada_duracion.delete(0, tk.END)

        self.entrada_descuento.delete(0, tk.END)

        self.entrada_descuento.insert(0, "0")

        self.incluir_impuesto.set(False)