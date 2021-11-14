from app import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))

    def __repr__(self):
        return "<Usuario %s>" % self.nome

class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    linkOriginal = db.Column(db.String(1000), nullable=False)
    linkEncurtado = db.Column(db.String(45))
    cliques = db.Column(db.BigInteger)

    def __repr__(self):
        return "<Usuario %s>" % self.nome

class LinksProibidos(db.Model):
    __tablename__ = "linksProibidos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "<Link Proibido %s>" % self.nome

class Denuncias(db.Model):
    __tablename__ = "denuncias"

    id = db.Column(db.Integer, primary_key=True)
    