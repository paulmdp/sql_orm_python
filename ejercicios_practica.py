#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3
from unicodedata import name

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)


def fill():
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)
    
    lista_tutor = ['Tom','Jerry','Spyke']
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for x in lista_tutor:
        tutornew = Tutor(name=x)
        session.add(tutornew)
 
    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)

    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor.
    lista_student = [('Hernan', 14, 2, 2),
            ('Jeremias', 13, 1, 1),
            ('Pato', 14, 2, 2),
            ('Paul', 13, 1, 1),
            ('Luis', 15, 3, 3),
            ('Lolo', 15, 3, 3),
            ('Paco', 16, 4, 2),
            ('Hugo', 16, 4, 2),
            ]
    for x in lista_student:
        studentnew = Estudiante(name=x[0], age=x[1], grade=x[2], tutor_id=x[3])
        session.add(studentnew)
 
    session.commit()    

def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creaods de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
    # Conectarse a la base de datos
    Session = sessionmaker(bind=engine)
    session = Session()

    # Leo todos los registros
    query = session.query(Estudiante)

    for estudiante in query:
        print(estudiante)
 

def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name

    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name == tutor)
    for tutor4student in query:
        print(tutor4student)

   

def modify(id, name):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality
    Session = sessionmaker(bind=engine)
    session = Session()

    tutor = Tutor(name=name)
    # Agrego nuevo tutor
    session.add(tutor)

    # Busco al nuevo tutor
    query = session.query(Tutor).filter(Tutor.name == name)
    newtutor = query.first()
      
    # Busco al estudiante para cambiarle el tutor
    query = session.query(Estudiante).filter(Estudiante.id == id)
    estudiante = query.first()

    # Actualizando el estudiante
    estudiante.tutor = newtutor
    session.add(estudiante)

    session.commit()

    fetch()

def count_grade(grade):
    print('Estudiante por grado de grado', grade)
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona

    Session = sessionmaker(bind=engine)
    session = Session()
    contador = session.query(Estudiante).filter(Estudiante.grade == grade).count()
    print(contador)



if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill()
    fetch()

    tutor = 'Jerry'
    search_by_tutor(tutor)

    nuevo_tutor = 'Harry'
    id_est = 2
    modify(id_est, nuevo_tutor)

    grade = 3
    count_grade(grade)
