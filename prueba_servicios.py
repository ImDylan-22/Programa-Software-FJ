"""
ARCHIVO: prueba_servicios.py

DESCRIPCION:
Realiza pruebas de funcionamiento de la clase abstracta
Servicio y sus tres clases especializadas.

OBJETIVO:
Comprobar la herencia, el polimorfismo, los calculos
de costos y el manejo de excepciones.

"""

from servicio import Servicio
from servicios_especializados import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError
)

from logger_config import logger


print("=== PRUEBAS DE SERVICIOS SOFTWARE FJ ===")


# PRUEBA 1: Comprobar que Servicio es abstracta.
print("\nPRUEBA 1: Instanciar clase abstracta")

try:
    servicio = Servicio(
        "S001",
        "Servicio general",
        "Descripcion general",
        50000
    )

except TypeError as error:
    print("Correcto: Servicio es una clase abstracta.")
    logger.info("Prueba 1: clase abstracta verificada.")


# PRUEBA 2: Crear una reserva de sala.
print("\nPRUEBA 2: Crear reserva de sala")

try:
    sala = ReservaSala(
        "SAL001",
        "Sala de reuniones equipada.",
        20
    )

    print("Sala creada correctamente.")
    print(sala.describir_servicio())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 2: %s", error)


# PRUEBA 3: Crear alquiler de equipos.
print("\nPRUEBA 3: Crear alquiler de equipos")

try:
    equipo = AlquilerEquipo(
        "EQ001",
        "Alquiler de equipos audiovisuales.",
        "Proyector"
    )

    print("Equipo creado correctamente.")
    print(equipo.describir_servicio())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 3: %s", error)


# PRUEBA 4: Crear asesoria especializada.
print("\nPRUEBA 4: Crear asesoria")

try:
    asesoria = AsesoriaEspecializada(
        "ASE001",
        "Asesoria profesional en tecnologia.",
        "Tecnologia"
    )

    print("Asesoria creada correctamente.")
    print(asesoria.describir_servicio())

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 4: %s", error)


# PRUEBA 5: Calcular sala con impuesto.
print("\nPRUEBA 5: Calculo de sala con impuesto")

try:
    costo = sala.calcular_costo(
        2,
        incluir_impuesto=True
    )

    print(f"Costo de 2 horas con impuesto: ${costo:,.2f} COP")

except (DatosInvalidosError, ServicioNoDisponibleError) as error:
    print("Error:", error)
    logger.error("Prueba 5: %s", error)


# PRUEBA 6: Calcular equipo con descuento.
print("\nPRUEBA 6: Calculo de equipo con descuento")

try:
    costo = equipo.calcular_costo(
        3,
        descuento=10
    )

    print(f"Costo de 3 dias con descuento: ${costo:,.2f} COP")

except (DatosInvalidosError, ServicioNoDisponibleError) as error:
    print("Error:", error)
    logger.error("Prueba 6: %s", error)


# PRUEBA 7: Calcular asesoria con impuesto y descuento.
print("\nPRUEBA 7: Calculo de asesoria con impuesto y descuento")

try:
    costo = asesoria.calcular_costo(
        2,
        incluir_impuesto=True,
        descuento=15
    )

    print(
        f"Costo de asesoria con impuesto y descuento: "
        f"${costo:,.2f} COP"
    )

except (DatosInvalidosError, ServicioNoDisponibleError) as error:
    print("Error:", error)
    logger.error("Prueba 7: %s", error)


# PRUEBA 8: Intentar utilizar un servicio no disponible.
print("\nPRUEBA 8: Servicio no disponible")

try:
    sala.cambiar_disponibilidad(False)

    sala.calcular_costo(2)

except ServicioNoDisponibleError as error:
    print("Correcto: se detecto la falta de disponibilidad.")
    print("Detalle:", error)
    logger.error("Prueba 8: %s", error)


# PRUEBA 9: Intentar calcular con cantidad negativa.
print("\nPRUEBA 9: Cantidad negativa")

try:
    equipo.calcular_costo(-2)

except DatosInvalidosError as error:
    print("Correcto: se rechazo la cantidad negativa.")
    print("Detalle:", error)
    logger.error("Prueba 9: %s", error)


# PRUEBA 10: Introducir un descuento incorrecto.
print("\nPRUEBA 10: Descuento incorrecto")

try:
    asesoria.calcular_costo(
        2,
        descuento=150
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo el descuento.")
    print("Detalle:", error)
    logger.error("Prueba 10: %s", error)


print("\n=== FIN DE LAS PRUEBAS DE SERVICIOS ===")