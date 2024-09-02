from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests

@app.route('/denuncias', methods=["GET"])
def denuncia():

    """
    Função de Rota de Denúncias.

    :param link:
    :type:
    :return: Retorna o render_template com o arquivo de rota de denúncias.
    :rtype:
    :raises ValueError:

    Example:
        
        .. note::
    """
    return render_template("denuncias.html")

@app.route('/denunciarLink', methods=["POST"])
def denunciar():

    """
    Função de Rota para receber o link a ser denunciado e inseri-lo na tabela de links denunciados.

    :param link:
    :type:
    :return: Retorna o render_template com o arquivo de rota de denúncias, com uma mensagem dependendo da ação do usuário.
    :rtype:
    :raises ValueError:

    Example:
        >>> denunciar()
        return render_template("denuncias.html", mensagem=mensagem)
        
        .. note::
    """

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