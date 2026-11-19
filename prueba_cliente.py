"""
ARCHIVO: prueba_cliente.py

DESCRIPCION:
Realiza pruebas de funcionamiento de la clase Cliente.

OBJETIVO:
Comprobar el registro de clientes, las validaciones
de datos y la actualizacion de informacion.

"""

from cliente import Cliente
from excepciones import DatosInvalidosError
from logger_config import logger


print("=== PRUEBAS DE LA CLASE CLIENTE ===")


# PRUEBA 1: Registro de un cliente valido.
print("\nPRUEBA 1: Registro de cliente valido")

try:
    cliente = Cliente(
        "123456789",
        "Dylan Arturo",
        "dylan@gmail.com",
        "3001234567"
    )

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Fallo en la prueba 1: %s", error)

else:
    print("Cliente registrado correctamente.")
    print(cliente.mostrar_informacion())

finally:
    print("Finalizacion de la prueba 1.")


# PRUEBA 2: Correo electronico incorrecto.
print("\nPRUEBA 2: Correo electronico incorrecto")

try:
    cliente_invalido = Cliente(
        "987654321",
        "Pepito Perez",
        "correo_incorrecto",
        "3101234567"
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo el correo.")
    print("Detalle:", error)
    logger.error("Prueba 2: %s", error)

else:
    print("Error: se acepto un correo incorrecto.")

finally:
    print("Finalizacion de la prueba 2.")


# PRUEBA 3: Numero telefonico incorrecto.
print("\nPRUEBA 3: Telefono incorrecto")

try:
    cliente_invalido = Cliente(
        "456789123",
        "Fulanito Gomez",
        "fulanito@gmail.com",
        "123"
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo el telefono.")
    print("Detalle:", error)
    logger.error("Prueba 3: %s", error)

else:
    print("Error: se acepto un telefono incorrecto.")

finally:
    print("Finalizacion de la prueba 3.")


# PRUEBA 4: Actualizacion correcta del correo.
print("\nPRUEBA 4: Actualizacion del correo")

try:
    cliente.actualizar_correo("nuevo@gmail.com")

except DatosInvalidosError as error:
    print("Error:", error)
    logger.error("Prueba 4: %s", error)

else:
    print("Correo actualizado correctamente.")
    print("Nuevo correo:", cliente.obtener_correo())

finally:
    print("Finalizacion de la prueba 4.")


# PRUEBA 5: Actualizacion con correo incorrecto.
print("\nPRUEBA 5: Actualizacion con correo invalido")

correo_anterior = cliente.obtener_correo()

try:
    cliente.actualizar_correo("correo_sin_formato")

except DatosInvalidosError as error:
    print("Correcto: se rechazo la actualizacion.")
    print("Detalle:", error)
    logger.error("Prueba 5: %s", error)

else:
    print("Error: se acepto un correo incorrecto.")

finally:
    print("Correo actual:", cliente.obtener_correo())
    print("Finalizacion de la prueba 5.")

# Comprobar que el correo anterior se conserva.
assert cliente.obtener_correo() == correo_anterior


# PRUEBA 6: Identificacion vacia.
print("\nPRUEBA 6: Identificacion vacia")

try:
    cliente_invalido = Cliente(
        "",
        "Pedro Gomez",
        "pedro@gmail.com",
        "3201234567"
    )

except DatosInvalidosError as error:
    print("Correcto: se rechazo la identificacion.")
    print("Detalle:", error)
    logger.error("Prueba 6: %s", error)

else:
    print("Error: se acepto una identificacion vacia.")

finally:
    print("Finalizacion de la prueba 6.")


print("\n=== FIN DE LAS PRUEBAS DE CLIENTE ===")