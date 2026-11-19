"""
ARCHIVO: prueba_gestor.py

DESCRIPCION:
Realiza pruebas de funcionamiento de la clase GestorSistema.

OBJETIVO:
Comprobar el registro, busqueda y administracion
de clientes, servicios y reservas.

Tambien verifica el control de duplicados,
el manejo de excepciones y el resumen del sistema.

"""

from cliente import Cliente
from servicios_especializados import ReservaSala
from gestor_sistema import GestorSistema

from excepciones import DatosInvalidosError

from logger_config import logger


print("=== PRUEBAS DEL GESTOR GENERAL ===")


# PRUEBA 1: Inicializar el gestor.
print("\nPRUEBA 1: Inicializar gestor")

gestor = GestorSistema()

print("Gestor inicializado correctamente.")


# PRUEBA 2: Registrar un cliente.
print("\nPRUEBA 2: Registrar cliente")

try:
    cliente = Cliente(
        "123456789",
        "Carlos Rodriguez",
        "carlos@gmail.com",
        "3001234567"
    )

    gestor.registrar_cliente(cliente)

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 2: %s", error)

else:
    print("Cliente registrado correctamente.")

finally:
    print("Finalizacion de la prueba 2.")


# PRUEBA 3: Intentar registrar un cliente duplicado.
print("\nPRUEBA 3: Cliente duplicado")

try:
    cliente_duplicado = Cliente(
        "123456789",
        "Carlos Rodriguez",
        "carlos@gmail.com",
        "3001234567"
    )

    gestor.registrar_cliente(cliente_duplicado)

except DatosInvalidosError as error:
    print("Correcto: se rechazo el cliente duplicado.")
    print("Detalle:", error)
    logger.error("Prueba 3: %s", error)


# PRUEBA 4: Registrar un servicio.
print("\nPRUEBA 4: Registrar servicio")

try:
    sala = ReservaSala(
        "SAL001",
        "Sala de reuniones equipada.",
        20
    )

    gestor.registrar_servicio(sala)

    print("Servicio registrado correctamente.")

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 4: %s", error)


# PRUEBA 5: Intentar registrar un servicio duplicado.
print("\nPRUEBA 5: Servicio duplicado")

try:
    sala_duplicada = ReservaSala(
        "SAL001",
        "Otra sala de reuniones.",
        15
    )

    gestor.registrar_servicio(sala_duplicada)

except DatosInvalidosError as error:
    print("Correcto: se rechazo el servicio duplicado.")
    print("Detalle:", error)
    logger.error("Prueba 5: %s", error)


# PRUEBA 6: Buscar un cliente.
print("\nPRUEBA 6: Buscar cliente")

cliente_encontrado = gestor.buscar_cliente("123456789")

if cliente_encontrado is not None:
    print("Cliente encontrado.")
    print("Nombre:", cliente_encontrado.obtener_nombre())

else:
    print("No se encontro el cliente.")


# PRUEBA 7: Buscar un servicio.
print("\nPRUEBA 7: Buscar servicio")

servicio_encontrado = gestor.buscar_servicio("SAL001")

if servicio_encontrado is not None:
    print("Servicio encontrado.")
    print("Nombre:", servicio_encontrado.obtener_nombre())

else:
    print("No se encontro el servicio.")


# PRUEBA 8: Crear una reserva.
print("\nPRUEBA 8: Crear reserva")

try:
    reserva = gestor.crear_reserva(
        "RES001",
        "123456789",
        "SAL001",
        2
    )

    print("Reserva creada correctamente.")
    print(reserva.mostrar_informacion())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 8: %s", error)


# PRUEBA 9: Crear reserva con cliente inexistente.
print("\nPRUEBA 9: Cliente inexistente")

try:
    gestor.crear_reserva(
        "RES002",
        "999999999",
        "SAL001",
        2
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo la reserva.")
    print("Detalle:", error)
    logger.error("Prueba 9: %s", error)


# PRUEBA 10: Confirmar una reserva.
print("\nPRUEBA 10: Confirmar reserva")

try:
    gestor.confirmar_reserva("RES001")

    print("Reserva confirmada correctamente.")

    reserva_encontrada = gestor.buscar_reserva("RES001")

    print("Estado:", reserva_encontrada.obtener_estado())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 10: %s", error)


# PRUEBA 11: Procesar una reserva.
print("\nPRUEBA 11: Procesar reserva")

try:
    costo = gestor.procesar_reserva(
        "RES001",
        incluir_impuesto=True
    )

    print("Reserva procesada correctamente.")
    print(f"Costo: ${costo:,.2f} COP")

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 11: %s", error)


# PRUEBA 12: Cancelar otra reserva.
print("\nPRUEBA 12: Cancelar reserva")

try:
    gestor.crear_reserva(
        "RES003",
        "123456789",
        "SAL001",
        1
    )

    gestor.cancelar_reserva("RES003")

    print("Reserva cancelada correctamente.")

    reserva_cancelada = gestor.buscar_reserva("RES003")

    print("Estado:", reserva_cancelada.obtener_estado())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 12: %s", error)


# PRUEBA 13: Consultar resumen del sistema.
print("\nPRUEBA 13: Resumen general")

resumen = gestor.obtener_resumen()

print("Clientes registrados:", resumen["clientes"])
print("Servicios registrados:", resumen["servicios"])
print("Reservas registradas:", resumen["reservas"])

print("Reservas pendientes:", resumen["pendientes"])
print("Reservas confirmadas:", resumen["confirmadas"])
print("Reservas canceladas:", resumen["canceladas"])
print("Reservas procesadas:", resumen["procesadas"])


# PRUEBA 14: Consultar las listas internas.
print("\nPRUEBA 14: Consultar registros")

print("Cantidad de clientes:", len(gestor.listar_clientes()))
print("Cantidad de servicios:", len(gestor.listar_servicios()))
print("Cantidad de reservas:", len(gestor.listar_reservas()))


print("\n=== FIN DE LAS PRUEBAS DEL GESTOR ===")