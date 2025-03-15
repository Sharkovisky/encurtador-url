from app import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    data_cadastro = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(255))

    def __repr__(self):
        return "<Usuario %s>" % self.nome

class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    linkOriginal = db.Column(db.String(1000), nullable=False)
    linkEncurtado = db.Column(db.String(45))
    cliques = db.Column(db.BigInteger)
    usuario = db.Column(db.Integer)

    def __repr__(self):
        return "<Usuario %s>" % self.nome

class LinksProibidos(db.Model):
    __tablename__ = "linksProibidos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return "<Link Proibido %s>" % self.nome

class Denuncias(db.Model):
    __tablename__ = "denuncias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return "<Link Denunciado %s> " % self.nome