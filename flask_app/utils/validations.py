import re
import filetype
from datetime import datetime

def validar_region_y_comuna(cursor, region_id, comuna_id):
    errores = []

    # Validar región
    cursor.execute("SELECT id FROM region WHERE id = %s", (region_id,))
    region = cursor.fetchone()
    if not region:
        errores.append("La región seleccionada no existe.")
        return errores  # no hace falta seguir si no existe la región

    # Validar comuna
    cursor.execute("SELECT id, region_id FROM comuna WHERE id = %s", (comuna_id,))
    comuna = cursor.fetchone()
    if not comuna:
        errores.append("La comuna seleccionada no existe.")
        return errores

    # Validar relación
    if comuna["region_id"] != region["id"]:
        errores.append("La comuna no pertenece a la región seleccionada.")

    return errores

def validar_sector(cursor, sector):
    error = []
    if len(sector) > 100:
        error.append("El sector no puede tener más de 100 caracteres.")
    return error

def validar_nombre(cursor, nombre):
    error = []
    if len(nombre) <= 3 or len(nombre) > 200:
        error.append("Nombre inválido")
    return error

def validar_email(cursor, email):
    error = []
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_regex, email) or len(email) < 0:
        error.append("Email inválido")
    return error

def validar_celular(cursor, celular):
    error = []
    celular_regex = r'^\+?56?9[0-9]{8}$'
    if not re.match(celular_regex, celular):
        error.append("Celular inválido")
    return error

def validar_tipo(cursor, tipo):
    error = []
    if tipo not in ['perro', 'gato']:
        error.append("Tipo inválido")
    return error

def validar_cantidad(cursor, cantidad):
    error = []
    if not cantidad.isdigit() or int(cantidad) <= 1:
        error.append("Cantidad inválida")
    return error

def validar_edad(cursor, edad):
    error = []
    if not edad.isdigit() or int(edad) < 1:
        error.append("Edad inválida")
    return error

def validar_unidad(cursor, unidad):
    error = []
    if unidad not in ['meses', 'años']:
        error.append("Unidad inválida")
    return error

def validar_fecha(fecha_entrega_str):
    errores = []
    # Convertir el string del formulario a datetime
    fecha_entrega = datetime.fromisoformat(fecha_entrega_str)
    # Comparar con la fecha actual
    if fecha_entrega < datetime.now():
        errores.append("La fecha de entrega no puede ser en el pasado.")
    return errores