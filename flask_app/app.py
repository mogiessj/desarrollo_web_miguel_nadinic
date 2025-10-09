from flask import Flask, request, render_template, redirect, url_for, session
from utils.validations import *
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)


app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_aviso', methods=['GET', 'POST'])
def agregar_aviso():
    if request.method == 'POST':
        # Datos del formulario
        region_id = request.form.get("region")
        comuna_id = request.form.get("comuna")
        sector = request.form.get("sector", "")
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        celular = request.form.get("celular", "")
        contacto = request.form.get("contacto", "")
        idContacto = request.form.get("idContacto", "")
        tipo = request.form.get("tipo")
        cantidad = request.form.get("cantidad")
        edad = request.form.get("edad")
        unidad = request.form.get("unidad")
        fecha_entrega = request.form.get("fecha")
        descripcion = request.form.get("descripcion", "")
        fotos = request.files.getlist("fotos[]")

        errores = []

        # Validaciones
        try:
            conn = db.get_conn()
            cursor = conn.cursor()
            errores += validar_region_y_comuna(cursor, region_id, comuna_id)
            errores += validar_sector(cursor, sector)
            errores += validar_nombre(cursor, nombre)
            errores += validar_email(cursor, email)
            if celular:
                errores += validar_celular(cursor, celular)
            errores += validar_tipo(cursor, tipo)
            errores += validar_cantidad(cursor, cantidad)
            errores += validar_edad(cursor, edad)
            errores += validar_unidad(cursor, unidad)
            errores += validar_fecha(fecha_entrega)
        except Exception as e:
            errores.append(f"Error de base de datos: {str(e)}")
        finally:
            cursor.close()
            conn.close()

        # Validar contacto
        if contacto and (len(idContacto) < 4 or len(idContacto) > 50):
            errores.append("ID de contacto inválido")

        # Validar fotos
        if not fotos or len(fotos) == 0:
            errores.append("Debe subir al menos una foto")
        for f in fotos:
            if f.filename == "":
                errores.append("Uno de los archivos no tiene nombre")
            elif not f.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                errores.append(f"Archivo {f.filename} no permitido")

        if errores:
            return render_template("aviso.html", errores=errores)

        # Guardar datos en DB
        try:
            conn = db.get_conn()
            cursor = conn.cursor()

            # Inserta aviso_adopcion
            sql_aviso = """INSERT INTO aviso_adopcion 
                (fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion)
                VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_aviso, (
                comuna_id, sector, nombre, email, celular or None,
                tipo, cantidad, edad, 'm' if unidad == "meses" else 'a', fecha_entrega, descripcion
            ))
            aviso_id = cursor.lastrowid

            # Contacto
            if contacto:
                cursor.execute(
                    "INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES (%s, %s, %s)",
                    (contacto, idContacto, aviso_id)
                )

            # Fotos
            for f in fotos:
                filename = secure_filename(f.filename)
                ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(ruta)
                cursor.execute(
                    "INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES (%s, %s, %s)",
                    (ruta, filename, aviso_id)
                )

            conn.commit()
        except Exception as e:
            return render_template("aviso.html", errores=[f"Ocurrió un error guardando en la base de datos: {str(e)}"])
        finally:
            cursor.close()
            conn.close()

        # Redirigir a index con mensaje de éxito
        session['mensaje'] = "Aviso agregado correctamente"
        return redirect(url_for('index'))

    # GET → mostrar formulario
    return render_template("aviso.html")


@app.route('/aviso')
def aviso():
    return render_template('aviso.html')

@app.route('/listado')
def listado():
    return render_template('listado.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

if __name__ == '__main__':
    app.run(debug=True)