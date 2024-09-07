from app import db
from app.models.tables import LinksProibidos

l1 = LinksProibidos(nome = "bit.ly")
db.session.add(l1)
db.session.commit()

l2 = LinksProibidos(nome = "tinyurl.com")
db.session.add(l2)
db.session.commit()

l3 = LinksProibidos(nome = "encurtador.com.br")
db.session.add(l3)
db.session.commit()

l4 = LinksProibidos(nome = "e.fslab.dev")
db.session.add(l3)
db.session.commit()