
"""
ARCHIVO: prueba_reserva.py

DESCRIPCION:
Realiza pruebas de funcionamiento de la clase Reserva.

OBJETIVO:
Comprobar la creacion, confirmacion, cancelacion
y procesamiento de reservas.

Tambien verifica las validaciones y el manejo
de excepciones durante las operaciones.

"""

from cliente import Cliente
from servicios_especializados import ReservaSala
from reserva import Reserva

from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError
)

from logger_config import logger


print("=== PRUEBAS DE LA CLASE RESERVA ===")


# Crear objetos que seran utilizados en las pruebas.
cliente = Cliente(
    "123456789",
    "Carlos Rodriguez",
    "carlos@gmail.com",
    "3001234567"
)

sala = ReservaSala(
    "SAL001",
    "Sala de reuniones equipada.",
    20
)


# PRUEBA 1: Crear una reserva valida.
print("\nPRUEBA 1: Crear reserva valida")

try:
    reserva1 = Reserva(
        "RES001",
        cliente,
        sala,
        2
    )

    print("Reserva creada correctamente.")
    print(reserva1.mostrar_informacion())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 1: %s", error)


# PRUEBA 2: Crear una reserva sin cliente valido.
print("\nPRUEBA 2: Cliente invalido")

try:
    reserva_invalida = Reserva(
        "RES002",
        "Carlos Rodriguez",
        sala,
        2
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo el cliente invalido.")
    print("Detalle:", error)
    logger.error("Prueba 2: %s", error)


# PRUEBA 3: Crear una reserva sin servicio valido.
print("\nPRUEBA 3: Servicio invalido")

try:
    reserva_invalida = Reserva(
        "RES003",
        cliente,
        "Reserva de salas",
        2
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo el servicio invalido.")
    print("Detalle:", error)
    logger.error("Prueba 3: %s", error)


# PRUEBA 4: Crear una reserva con duracion negativa.
print("\nPRUEBA 4: Duracion negativa")

try:
    reserva_invalida = Reserva(
        "RES004",
        cliente,
        sala,
        -3
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo la duracion negativa.")
    print("Detalle:", error)
    logger.error("Prueba 4: %s", error)


# PRUEBA 5: Confirmar una reserva valida.
print("\nPRUEBA 5: Confirmar reserva")

try:
    reserva1.confirmar()

    print("Reserva confirmada correctamente.")
    print("Estado:", reserva1.obtener_estado())

except (DatosInvalidosError, ServicioNoDisponibleError) as error:
    print("Error:", error)
    logger.error("Prueba 5: %s", error)


# PRUEBA 6: Procesar una reserva confirmada.
print("\nPRUEBA 6: Procesar reserva")

try:
    costo = reserva1.procesar(
        incluir_impuesto=True
    )

    print("Reserva procesada correctamente.")
    print(f"Costo: ${costo:,.2f} COP")
    print("Estado:", reserva1.obtener_estado())

except (DatosInvalidosError, ServicioNoDisponibleError) as error:
    print("Error:", error)
    logger.error("Prueba 6: %s", error)


# PRUEBA 7: Cancelar una reserva pendiente.
print("\nPRUEBA 7: Cancelar reserva")

try:
    reserva2 = Reserva(
        "RES007",
        cliente,
        sala,
        3
    )

    reserva2.cancelar()

    print("Reserva cancelada correctamente.")
    print("Estado:", reserva2.obtener_estado())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 7: %s", error)


# PRUEBA 8: Confirmar una reserva con servicio no disponible.
print("\nPRUEBA 8: Servicio no disponible")

try:
    sala_no_disponible = ReservaSala(
        "SAL002",
        "Sala temporalmente fuera de servicio.",
        15,
        disponible=False
    )

    reserva3 = Reserva(
        "RES008",
        cliente,
        sala_no_disponible,
        2
    )

    reserva3.confirmar()

except ServicioNoDisponibleError as error:
    print("Correcto: no se pudo confirmar la reserva.")
    print("Detalle:", error)
    logger.error("Prueba 8: %s", error)


# PRUEBA 9: Intentar procesar una reserva pendiente.
print("\nPRUEBA 9: Procesar reserva pendiente")

try:
    reserva4 = Reserva(
        "RES009",
        cliente,
        sala,
        2
    )

    reserva4.procesar()

except DatosInvalidosError as error:
    print("Correcto: se rechazo el procesamiento.")
    print("Detalle:", error)
    logger.error("Prueba 9: %s", error)


# PRUEBA 10: Intentar cancelar una reserva procesada.
print("\nPRUEBA 10: Cancelar reserva procesada")

try:
    reserva1.cancelar()

except DatosInvalidosError as error:
    print("Correcto: no se puede cancelar una reserva procesada.")
    print("Detalle:", error)
    logger.error("Prueba 10: %s", error)


print("\n=== FIN DE LAS PRUEBAS DE RESERVAS ===")