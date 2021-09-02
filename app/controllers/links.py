from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link
import string, random

@app.route('/', methods=["GET", "POST"])
def inicio():
    return render_template("link.html")

@app.route('/link', methods=["POST"])
def enviar_link():

    linkOriginal = request.form["linkOriginal"]
    linkEncurtado = request.form["linkEncurtado"]

    app.logger.info(
        "O link encurtado veio null? " + str(linkEncurtado)
    )

    if (linkEncurtado == ""):
        letras = string.ascii_uppercase+string.ascii_lowercase
        linkMisturado = ''.join((random.choice(letras)) for _ in range(6))

        print("LINK MISTURADO AQUI: "+str(linkMisturado))

        linkEncurtado = linkMisturado
        
    link = Link(
        linkOriginal=linkOriginal,
        linkEncurtado=linkEncurtado
    )
    db.session.add(link)
    db.session.commit()


    linkPronto = Link.query.filter(Link.linkOriginal.like(linkOriginal)).first()

    return render_template("link_pronto.html", linkPronto=linkPronto)

@app.route('/<linkEmbaralhado>', methods=["GET"])
def receber_link(linkEmbaralhado):

    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()

    return redirect(linkCerto.linkOriginal)