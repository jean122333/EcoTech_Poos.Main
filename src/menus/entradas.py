# menus/entradas.py
"""Entrada de datos, validaciones y manejo de errores compartidos por todos los menús.

Aquí se distingue:
  * VALIDACIÓN: revisar lo que escribe el usuario ANTES de usarlo (volver a preguntar).
  * EXCEPCIÓN: algo anormal que ocurre al ejecutar (BD caída, restricción violada...).
"""
import functools
import logging
from datetime import date

from persistencia.conexion import ERRORES_INTEGRIDAD

MENSAJE_SEGURO = "No fue posible completar la operación."
MENSAJE_INTEGRIDAD = ("Ya existe un registro con esos datos "
                      "o hace referencia a algo que no existe.")


# ---------------------------------------------------------------- manejo de errores
def manejar_errores(accion, mensaje_integridad=MENSAJE_INTEGRIDAD):
    """Decorador: ejecuta la operación del menú y responde de forma controlada.

    - ValueError          -> dato inválido del usuario o del dominio (mensaje claro).
    - ERRORES_INTEGRIDAD  -> duplicado o clave foránea inexistente (mensaje claro).
    - Exception           -> fallo inesperado: el detalle va a ecotech.log y el usuario
                             solo ve un mensaje seguro (sin rutas, SQL ni credenciales).
    """
    def decorador(funcion):
        @functools.wraps(funcion)
        def envoltura(*args, **kwargs):
            try:
                return funcion(*args, **kwargs)
            except ValueError as error:
                print("Datos inválidos:", error)
            except ERRORES_INTEGRIDAD:
                print(mensaje_integridad)
            except Exception:
                logging.exception("Error al %s", accion)
                print(MENSAJE_SEGURO)
        return envoltura
    return decorador


# ---------------------------------------------------------------- validación de entradas
def solicitar_opcion(maximo):
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Debe ingresar un número.")
            continue

        if opcion < 0 or opcion > maximo:
            print("Opción fuera de rango.")
            continue
        return opcion


def solicitar_texto(mensaje, obligatorio=True):
    while True:
        texto = input(f"{mensaje}: ").strip()
        if texto or not obligatorio:
            return texto
        print("Este dato no puede estar vacío.")


def solicitar_entero(mensaje, opcional=False):
    """Entero positivo. Con opcional=True, Enter vacío devuelve None."""
    while True:
        texto = input(f"{mensaje}: ").strip()
        if opcional and not texto:
            return None
        try:
            valor = int(texto)
        except ValueError:
            print("Debe ingresar un número entero.")
            continue

        if valor <= 0:
            print("Debe ser un número positivo.")
            continue
        return valor


def solicitar_decimal(mensaje, minimo=0.0, maximo=None, opcional=False):
    while True:
        texto = input(f"{mensaje}: ").strip().replace(",", ".")
        if opcional and not texto:
            return None
        try:
            valor = float(texto)
        except ValueError:
            print("Debe ingresar un número.")
            continue

        if valor < minimo or (maximo is not None and valor > maximo):
            tope = f" y {maximo}" if maximo is not None else ""
            print(f"El valor debe estar entre {minimo}{tope}.")
            continue
        return valor


def solicitar_fecha(mensaje, opcional=False):
    """Fecha AAAA-MM-DD. Enter vacío = hoy (o None si opcional=True)."""
    while True:
        texto = input(f"{mensaje} (AAAA-MM-DD, vacío = {'sin cambio' if opcional else 'hoy'}): ").strip()
        if not texto:
            return None if opcional else date.today().isoformat()
        try:
            return date.fromisoformat(texto).isoformat()
        except ValueError:
            print("Fecha inválida. Ejemplo: 2026-09-24")


def confirmar(mensaje):
    return input(f"{mensaje} (s/n): ").strip().lower() in ("s", "si", "sí")


# ---------------------------------------------------------------- menú genérico
def ejecutar_menu(titulo, opciones):
    """Muestra un menú y llama a la función elegida hasta que el usuario elige 0.

    opciones: {numero: (texto, funcion)}
    """
    while True:
        print(f"\n===== {titulo} =====")
        for numero, (texto, _) in opciones.items():
            print(f"{numero}. {texto}")
        print("0. Volver")

        opcion = solicitar_opcion(max(opciones))
        if opcion == 0:
            return
        opciones[opcion][1]()