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
    cliques = db.Column(db.Boolean)

    def __repr__(self):
        return "<Usuario %s>" % self.nome
