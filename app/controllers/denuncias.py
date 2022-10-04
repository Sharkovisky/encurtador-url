from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests

@app.route('/denuncias', methods=["GET"])
def denuncia():
    return render_template("denuncias.html")

@app.route('/denunciarLink', methods=["POST"])
def denunciar():

    linkDenunciado = request.form["linkDenunciado"]

    if(linkDenunciado == ""):
        mensagem = "Campo está vazio."
        return render_template("denuncias.html", mensagem=mensagem)

    denuncia = Denuncias(
        nome=linkDenunciado
    )
    db.session.add(denuncia)
    db.session.commit()

    mensagem = "Link denunciado"
    return render_template("denuncias.html", mensagem=mensagem)