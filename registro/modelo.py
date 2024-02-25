from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_restful import Api
from .registro import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(100))
    contraseña = db.Column(db.String(100))

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

usuarioSchema = UsuarioSchema()