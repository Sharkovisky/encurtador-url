from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, urllib.parse

@app.route('/denuncias', methods=["GET"])
def denuncia():

    """
    Função de Rota de Denúncias.

    :param:
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

    :param:
    :type:
    :return: Retorna o render_template com o arquivo de rota de denúncias, com uma mensagem dependendo da ação do usuário.
    :rtype:
    :raises ValueError:

    Example:
        >>> denunciar()
        return render_template("denuncias.html", mensagem=mensagem)
        
    """

    linkDenunciado = request.form["linkDenunciado"]

    url_dividida = urllib.parse.urlparse(linkDenunciado)

    if url_dividida.netloc:
        linkEncurtado = url_dividida.path
        linkEncurtado = linkEncurtado.replace("/", "")
        linkDenunciado = linkEncurtado
    
    if(linkDenunciado == ""):
        mensagem = "O campo está vazio."
        return render_template("denuncias.html", mensagem=mensagem)

    denuncia = Denuncias(
        nome=linkDenunciado
    )
    db.session.add(denuncia)
    db.session.commit()

    mensagem = "O link foi denunciado."
    return render_template("denuncias.html", mensagem=mensagem)

@app.route('/acessarLinkDenunciado', methods=["GET", "POST"])
def receber_linkDenunciado():
        
    linkEncurtado = request.form["linkEncurtado"]
    
    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEncurtado)).first()
    return redirect(linkCerto.linkOriginal)