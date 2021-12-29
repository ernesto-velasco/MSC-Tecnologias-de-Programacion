# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json
#from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:catastro@localhost:5432/books_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Editorial(db.Model):
    __tablename__ = 'editorial'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True)

    def __init__(self, nombre):
        self.nombre = nombre

class Genero(db.Model):
    __tablename__ = 'genero'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True)

    def __init__(self, nombre):
        self.nombre = nombre

class Autor(db.Model):
    __tablename__ = 'autor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True)
    fecha_nacimiento = db.Column(db.Date)
    nacionalidad = db.Column(db.String(80))
    def __init__(self, nombre, fecha_nacimiento, nacionalidad):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad

class Libro(db.Model):
    __tablename__ = 'libro'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))

    id_editorial = db.Column(db.Integer, db.ForeignKey('editorial.id', ondelete='CASCADE'))
    id_genero = db.Column(db.Integer, db.ForeignKey('genero.id', ondelete='CASCADE'))
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id', ondelete='CASCADE'))
    
    def __init__(self, 
            titulo, 
            fecha_publicacion, 
            numero_paginas, 
            formato, 
            id_editorial,
            id_genero,
            id_autor):
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.id_editorial = id_editorial
        self.id_genero = id_genero
        self.id_autor = id_autor

class Favorito(db.Model):
    __tablename__ = 'favorito'
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), primary_key=True)
    id_libro = db.Column(db.Integer, db.ForeignKey('libro.id', ondelete='CASCADE'), primary_key=True)
    fecha = db.Column(db.Date)

    def __init__(self, id_usuario, id_libro, fecha):
        self.id_usuario = id_usuario
        self.id_libro = id_libro
        self.fecha = fecha

@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    usuario = Usuario.query.filter_by(email=email).first()
    #bcrypt.check_password_hash(usuario.password, password)
    if (usuario and usuario.password == password):
        return jsonify(success=True), 200
    return jsonify(success=False, msg="Usuario o contraseña incorrecta"), 402

@app.route('/registrarUsuario', methods=['POST'])
def user_register():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    #password_cifrado = bcrypt.generate_password_hash(password).decode('utf8')
    #print(password_cifrado)
    validar_usuario = Usuario.query.filter_by(email=email).first()
    if (validar_usuario and validar_usuario.email == email):
        return jsonify(success=False), 422 # El email ya ha sido registrado
    usuario_nuevo = Usuario(email=email, password=password)
    db.session.add(usuario_nuevo)
    db.session.commit()
    return jsonify(success=True), 200

@app.route('/consulta')
def consulta():
    # * inicializar diccionario
    dict_consultas = {}

    # * Consultas a la bd
    consulta_editoriales = Editorial.query.all()
    consulta_generos = Genero.query.all()
    consulta_autores = Autor.query.all()

    # * Convertir en diccionario
    dict_consultas['editoriales'] = list_to_dict(consulta_editoriales)
    dict_consultas['generos'] = list_to_dict(consulta_generos)
    dict_consultas['autores'] = list_to_dict(consulta_autores)

    # * Convertir en formato JSON
    json_string = json.dumps(dict_consultas, ensure_ascii=False)
    # ! json_string = jsonify(dict_consultas)

    return json_string, 200

def list_to_dict(list):
    new_dict = {}
    for idx, data in enumerate(list):
        new_dict[idx] = {
            'id': data.id,
            'nombre': data.nombre
        }
    return new_dict

@app.route('/registrarLibro', methods=['POST'])
def registrar_libro():
    print("Registrar libro")
    request_data = request.get_json()
    print(request_data)
    titulo = request_data['titulo']
    fecha_publicacion = request_data['fecha_publicacion']
    numero_paginas = request_data['numero_paginas']
    formato = request_data['formato']
    id_autor = request_data['autor']
    id_editorial = request_data['editorial']
    id_genero = request_data['genero']
    if (titulo == '' or fecha_publicacion == '' or numero_paginas == '' or formato == '' or id_autor == '' or id_editorial == '' or id_genero == ''):
        return jsonify(message="Todos los campos son obligatorios"), 422
    libro_nuevo = Libro(
        titulo=titulo, 
        fecha_publicacion=fecha_publicacion, 
        numero_paginas=numero_paginas, 
        formato=formato,
        id_autor=id_autor,
        id_editorial=id_editorial,
        id_genero = id_genero
    )
    db.session.add(libro_nuevo)
    db.session.commit()
    return jsonify(message="El libro {} ha sido registrado".format(titulo)), 200

@app.route('/registrarGenero', methods=['POST'])
def registrar_genero():
    request_data = request.get_json()
    nombre = request_data['nombre']
    if (nombre == ''):
        return jsonify(message="Todos los campos son obligatorios"), 422
    nuevo_registro = Genero(nombre=nombre)
    db.session.add(nuevo_registro)
    db.session.commit()
    return jsonify(message="El genero {} ha sido registrado".format(nombre)), 200

@app.route('/registrarEditorial', methods=['POST'])
def registrar_editorial():
    request_data = request.get_json()
    nombre = request_data['nombre']
    if (nombre == ''):
        return jsonify(message="Todos los campos son obligatorios"), 422
    nuevo_registro = Editorial(nombre=nombre)
    db.session.add(nuevo_registro)
    db.session.commit()
    return jsonify(message="La editorial {} ha sido registrado".format(nombre)), 200

@app.route('/registrarAutor', methods=['POST'])
def registrar_autor():
    request_data = request.get_json()
    nombre = request_data['nombre']
    fecha_nacimiento = request_data['fecha_nacimiento']
    nacionalidad = request_data['nacionalidad']
    if (nombre == '' or fecha_nacimiento == '' or nacionalidad == ''):
        return jsonify(message="Todos los campos son obligatorios"), 422
    nuevo_registro = Autor(
        nombre = nombre, 
        fecha_nacimiento = fecha_nacimiento,
        nacionalidad = nacionalidad
    )
    db.session.add(nuevo_registro)
    db.session.commit()
    return jsonify(message="El autor {} ha sido registrado".format(nombre)), 200

@app.route('/obtenerLibros')
def obtener_libros():
    data = db.session.query(Libro, Genero, Editorial, Autor).filter(
        Libro.id_genero == Genero.id
    ).filter(
        Libro.id_editorial == Editorial.id
    ).filter(
        Libro.id_autor == Autor.id
    ).all()
    data_dict = {}
    for idx, data in enumerate(data):
        data_dict[idx] = {
            'id': data.Libro.id,
            'titulo': data.Libro.titulo,
            'formato': data.Libro.formato,
            'autor': data.Autor.nombre,
            'editorial': data.Editorial.nombre,
            'genero': data.Genero.nombre
        }
    json_string = json.dumps(data_dict, ensure_ascii=False)
    return json_string, 200

@app.route('/obtenerGeneros')
def obtener_generos():
    data = Genero.query.all()
    data_dict = {}
    for idx, data in enumerate(data):
        data_dict[idx] = {
            'id': data.id,
            'nombre': data.nombre
        }
    json_string = json.dumps(data_dict, ensure_ascii=False)
    return json_string, 200

@app.route('/obtenerEditoriales')
def obtener_editoriales():
    data = Editorial.query.all()
    data_dict = {}
    for idx, data in enumerate(data):
        data_dict[idx] = {
            'id': data.id,
            'nombre': data.nombre
        }
    json_string = json.dumps(data_dict, ensure_ascii=False)
    return json_string, 200

@app.route('/obtenerAutores')
def obtener_autores():
    data = Autor.query.all()
    data_dict = {}
    for idx, data in enumerate(data):
        data_dict[idx] = {
            'id': data.id,
            'nombre': data.nombre,
            'fecha_nacimiento': data.fecha_nacimiento,
            'nacionalidad': data.nacionalidad
        }
    json_string = json.dumps(data_dict, ensure_ascii=False, default=str)
    return json_string, 200

@app.route('/agregarFavorito', methods=['POST'])
def agregar_favorito():
    print("Agregar favorito")
    request_data = request.get_json()
    print(request_data)
    id_usuario = 1
    id_libro = request_data['id_libro']
    fecha = date.today()
    validar_favorito = Favorito.query.where(Favorito.id_libro == id_libro).where( Favorito.id_usuario == id_usuario).first()
    # validar_favorito = db.session.query(Favorito, Libro, Usuario).filter(
    #         Favorito.id_libro == Libro.id
    #     ).filter(
    #         Favorito.id_usuario == Usuario.id
    #     ).first()
    if (validar_favorito):
        return jsonify(message = "Este libro ya ha sido agregado a tu favoritos"), 422 # El favorito ya ha sido registrado
    favorito = Favorito(
        id_usuario=id_usuario,
        id_libro=id_libro,
        fecha=fecha
    )
    db.session.add(favorito)
    db.session.commit()
    return jsonify(message = "El libro ha sido agregado a tu favoritos"), 200

@app.route("/obtenerFavoritos")
def obtener_favoritos():
    id_usuario = 1
    #data = Favorito.query.join(Libro, Favorito.id_libro == Libro.id).filter(Favorito.id_usuario == id_usuario).add_columns(Libro.titulo, Favorito.fecha)
    data = db.session.query(Favorito, Libro).filter(Favorito.id_usuario == id_usuario).filter(Favorito.id_libro == Libro.id).all()
    data_dict = {}
    for idx, data in enumerate(data):
        data_dict[idx] = {
            'id' : data.Favorito.id_libro,
            'id_usuario' : data.Favorito.id_usuario,
            'titulo': data.Libro.titulo,
            'fecha': data.Favorito.fecha
        }
        # data_dict[idx] = {
        #     'titulo': data.titulo,
        #     'fecha': data.fecha
        # }
    json_string = json.dumps(data_dict, ensure_ascii=False, default=str)
    return json_string, 200

@app.route('/eliminarFavorito/<id>', methods=['DELETE'])
def eliminar_favorito(id):
    print("ELIMINAR")
    id_usuario = 1
    id_libro = id
    favorito = Favorito.query.filter_by(id_libro = id_libro).filter_by(id_usuario = id_usuario).first()
    db.session.delete(favorito)
    db.session.commit()
    return jsonify(message="Registro eliminado.")

@app.route('/eliminarGenero/<id>', methods=['DELETE'])
def eliminar_genero(id):
    print("ELIMINAR")
    genero = Genero.query.filter_by(id = id).first()
    db.session.delete(genero)
    db.session.commit()
    return jsonify(message="Registro eliminado.")

@app.route('/eliminarEditorial/<id>', methods=['DELETE'])
def eliminar_editorial(id):
    print("ELIMINAR")
    editorial = Editorial.query.filter_by(id = id).first()
    db.session.delete(editorial)
    db.session.commit()
    return jsonify(message="Registro eliminado.")

@app.route('/eliminarAutor/<id>', methods=['DELETE'])
def eliminar_autor(id):
    print("ELIMINAR")
    autor = Autor.query.filter_by(id = id).first()
    db.session.delete(autor)
    db.session.commit()
    return jsonify(message="Registro eliminado.")

@app.route('/obtenerLibro/<id>')
def obtener_libro(id):
    libro = Libro.query.filter_by(id = id).first()
    dict_libro = {}
    dict_libro = {
        'titulo': libro.titulo,
        'fecha_publicacion': libro.fecha_publicacion,
        'numero_paginas': libro.numero_paginas,
        'formato': libro.formato,
        'id_autor': libro.id_autor,
        'id_genero': libro.id_genero,
        'id_editorial': libro.id_editorial,
    }
    return json.dumps(dict_libro, ensure_ascii=False, default=str)

@app.route('/actualizarLibro', methods=['PATCH'])
def actualizar_libro():
    request_data = request.get_json()
    print(request_data)
    libro = Libro.query.filter_by(id = request_data['id_libro']).first()
    libro.titulo = request_data['titulo']
    libro.fecha_publicacion = request_data['fecha_publicacion']
    libro.numero_paginas = request_data['numero_paginas']
    libro.formato = request_data['formato']
    libro.id_genero = request_data['genero']
    libro.id_autor = request_data['autor']
    libro.id_editorial = request_data['editorial']
    db.session.commit()
    return jsonify(message="El libro fue actualizado")

@app.route('/eliminarLibro/<id>', methods=['DELETE'])
def eliminar_libro(id):
    libro = Libro.query.filter_by(id = id).first()
    db.session.delete(libro)
    db.session.commit()
    return jsonify(message="Elemento <b>{}</b> eliminado exitosamente.".format(libro.titulo))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)