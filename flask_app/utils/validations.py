import re
import filetype
from datetime import datetime
from sqlalchemy import text

def validar_region_y_comuna(session, region_id, comuna_id):
    errores = []

    #validar región
    region = session.execute(
        text("SELECT id FROM region WHERE id = :id"),
        {"id": region_id}
    ).first()
    if not region:
        errores.append("La región seleccionada no existe.")
        return errores

    #validar comuna
    comuna = session.execute(
        text("SELECT id, region_id FROM comuna WHERE id = :id"),
        {"id": comuna_id}
    ).first()
    if not comuna:
        errores.append("La comuna seleccionada no existe.")
        return errores

    #validar relación
    if comuna.region_id != region.id:
        errores.append("La comuna no pertenece a la región seleccionada.")

    return errores

def validar_sector(sector):
    error = []
    if len(sector) > 100:
        error.append("El sector no puede tener más de 100 caracteres.")
    return error

def validar_nombre(nombre):
    error = []
    if len(nombre) <= 3 or len(nombre) > 200:
        error.append("Nombre inválido")
    return error

def validar_email(email):
    error = []
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_regex, email) or len(email) < 0:
        error.append("Email inválido")
    return error

def validar_celular(celular):
    error = []
    celular_regex = r'^\+?56?9\.?\d{8}$'
    if not re.match(celular_regex, celular):
        error.append("Celular inválido")
    return error

def validar_tipo(tipo):
    error = []
    if tipo not in ['perro', 'gato']:
        error.append("Tipo inválido")
    return error

def validar_cantidad(cantidad):
    error = []
    if not cantidad.isdigit() or int(cantidad) < 1:
        error.append("Cantidad inválida")
    return error

def validar_edad(edad):
    error = []
    if not edad.isdigit() or int(edad) < 1:
        error.append("Edad inválida")
    return error

def validar_unidad(unidad):
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