from app import app, db
from flask import render_template, request
from app.models.tables import Usuario, Link

@app.route('/', methods=["GET", "POST"])
def inicio():
    return render_template("link.html")

@app.route('/link', methods=["POST"])
def enviar_link():

    linkOriginal = request.form["linkOriginal"]
    linkEncurtado = request.form["linkEncurtado"]

    link = Link(
        linkOriginal=linkOriginal,
        linkEncurtado=linkEncurtado
    )
    db.session.add(link)
    db.session.commit()

    linkPronto = Link.query.filter(Link.linkOriginal.like(linkOriginal)).first()

    return render_template("link_pronto.html", linkPronto=linkPronto)
