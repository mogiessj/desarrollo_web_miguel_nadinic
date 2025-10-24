from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_cors import cross_origin
from utils.validations import *
from database import db
from werkzeug.utils import secure_filename
import hashlib, filetype, os, random, uuid
from datetime import datetime, timedelta
import time

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
        #obtener datos del formulario 
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
        unidad = request.form.get("unidad", "").lower()
        fecha_entrega = request.form.get("fecha")
        descripcion = request.form.get("descripcion", "")
        fotos = request.files.getlist("fotos[]")

        print("Datos recibidos:", nombre, comuna_id, tipo, cantidad, fecha_entrega)

        errores = []

        #validaciones
        session_db = db.SessionLocal()
        errores += validar_region_y_comuna(session_db, region_id, comuna_id)
        if sector:
            errores += validar_sector(sector)
        errores += validar_nombre(nombre)
        errores += validar_email(email)
        if celular:
            errores += validar_celular(celular)
        errores += validar_tipo(tipo)
        errores += validar_cantidad(str(cantidad))
        errores += validar_edad(str(edad))
        errores += validar_unidad(unidad)
        errores += validar_fecha(fecha_entrega)
        if contacto and (len(idContacto) < 4 or len(idContacto) > 50):
            errores.append("ID de contacto inválido")

        if not fotos or len(fotos) == 0:
            errores.append("Debe subir al menos una foto")
        for f in fotos:
            if f.filename == "":
                errores.append("Uno de los archivos no tiene nombre")
            elif not f.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                errores.append(f"Archivo {f.filename} no permitido")

        if errores:
            return render_template("aviso.html", errores=errores)

        #insertar a la base de datos
        try:
            comuna_id = int(comuna_id)
            cantidad = int(cantidad)
            edad = int(edad)
            fecha_entrega_dt = datetime.strptime(fecha_entrega, "%Y-%m-%dT%H:%M")

            nuevo_aviso = db.AvisoAdopcion(
                fecha_ingreso=datetime.now(),
                comuna_id=comuna_id,
                sector=sector,
                nombre=nombre,
                email=email,
                celular=celular or None,
                tipo=tipo,
                cantidad=cantidad,
                edad=edad,
                unidad_medida='m' if unidad == "meses" else 'a',
                fecha_entrega=fecha_entrega_dt,
                descripcion=descripcion
            )

            session_db.add(nuevo_aviso)
            session_db.flush()  #para el id automático

            #contacto
            if contacto:
                nuevo_contacto = db.ContactarPor(
                    nombre=contacto,
                    identificador=idContacto,
                    actividad_id=nuevo_aviso.id
                )
                session_db.add(nuevo_contacto)

            #fotos
            for f in fotos:
                filename = secure_filename(f.filename)
                ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(ruta)
                nueva_foto = db.Foto(
                    ruta_archivo=ruta,
                    nombre_archivo=filename,
                    actividad_id=nuevo_aviso.id
                )
                session_db.add(nueva_foto)

            session_db.commit()
            session['mensaje'] = "Aviso agregado correctamente"
            return redirect(url_for('index'))

        except Exception as e:
            session_db.rollback()
            errores.append(f"Ocurrió un error guardando en la base de datos: {str(e)}")
            return render_template("aviso.html", errores=errores)
        finally:
            session_db.close()

    return render_template("aviso.html")

@app.route('/avisos_por_dia')
def avisos_por_dia():
    session_db = db.SessionLocal()
    try:
        # Contar avisos por día
        resultados = session_db.query(
            db.func.date(db.AvisoAdopcion.fecha_ingreso).label('dia'),
            db.func.count(db.AvisoAdopcion.id).label('cantidad')
        ).group_by('dia').order_by('dia').all()

        # Convertir a lista de dicts
        data = [{"dia": str(fila.dia), "cantidad": fila.cantidad} for fila in resultados]

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session_db.close()

@app.route('/avisos_por_tipo')
def avisos_por_tipo():
    try:
        session_db = db.SessionLocal()
        # Consulta usando SQLAlchemy
        resultado = session_db.query(
            db.AvisoAdopcion.tipo, db.func.count(db.AvisoAdopcion.id)
        ).group_by(db.AvisoAdopcion.tipo).all()

        # Convertir a lista de dicts
        data = [{"tipo": fila[0], "cantidad": fila[1]} for fila in resultado]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session_db.close()

@app.route('/avisos_tipo_mes')
def avisos_tipo_mes():
    try:
        session_db = db.SessionLocal()

        # Consulta: contar avisos por mes y tipo
        from sqlalchemy import extract, func

        resultado = session_db.query(
            extract('month', db.AvisoAdopcion.fecha_ingreso).label('mes'),
            db.AvisoAdopcion.tipo,
            func.count(db.AvisoAdopcion.id).label('cantidad')
        ).group_by('mes', db.AvisoAdopcion.tipo).order_by('mes').all()

        # Inicializar datos con 0
        meses = range(1, 13)
        datos = {m: {'gato': 0, 'perro': 0} for m in meses}

        # Llenar datos
        for fila in resultado:
            try:
                mes = int(fila.mes)
                tipo = (fila.tipo or '').strip().lower()
                if tipo in ['gato', 'perro']:
                    datos[mes][tipo] = fila.cantidad
            except Exception as ex:
                print("Fila ignorada por error:", fila, ex)

        # Preparar listas para Highcharts
        from datetime import datetime
        categorias = [datetime(2025, m, 1).strftime('%B') for m in meses]  # nombres de meses
        series = [
            {'name': 'Gatos', 'data': [datos[m]['gato'] for m in meses]},
            {'name': 'Perros', 'data': [datos[m]['perro'] for m in meses]}
        ]

        return jsonify({'categorias': categorias, 'series': series})

    except Exception as e:
        print("Error en /api/avisos_tipo_mes:", e)
        return jsonify({'error': str(e)}), 500

    finally:
        session_db.close()

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