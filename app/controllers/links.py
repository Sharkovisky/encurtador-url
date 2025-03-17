from app import app, db, os
from flask import render_template, request, redirect, session
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, time, re, urllib.parse
from itertools import product
from flask_login import login_required, current_user
from flask_paginate import Pagination
from app.controllers.validacao import *

@app.route('/', methods=["GET", "POST"])
def inicio():

    """
    Função de Rota inicial.

    :param link:
    :type:
    :return: Retorna o render_template com o arquivo de rota inicial.
    :rtype:
    :raises ValueError:

    Example:
        
        .. note::
    """

    return render_template("link.html")

@app.route('/encurtarLink', methods=["POST"])
def enviar_link():

    """
    Função de Rota para receber o Link, encurtá-lo e devolvê-lo ao usuário.

    :param link:
    :type:
    :return: Retorna o render_template com o template de link_pronto com o link encurtado ao usuário.
    :rtype:
    :raises ValueError:

    Example:

        .. note::
            Esta função assume que os valores são Strings.
    """

    linkOriginal = request.form["linkOriginal"]
    linkEncurtado = request.form["linkEncurtado"].strip().lower()

    app.logger.info(
        "O link encurtado veio null? " + str(linkEncurtado)
    )

    if (verificar_link_proibido(linkOriginal)==True):
        mensagem = "Não é permitido encurtar links de outros encurtadores."
        return render_template("link.html", mensagem=mensagem)

    if (verificacaoTextoURL(linkOriginal)==True):
        mensagem = "Não é permitido ter texto antes do link."
        return render_template("link.html", mensagem=mensagem)

    if (verificacaoURL(linkEncurtado)==True):
        mensagem = "Não é permitido ter como texto personalizado um outro link."
        return render_template("link.html", mensagem=mensagem)
    
    if (validar_https(linkOriginal)==False):
        mensagem = "Não é permitido encurtar links fora do padrão HTTPS."
        return render_template("link.html", mensagem=mensagem) 

    if (linkEncurtado == ""):
        letras = string.ascii_uppercase+string.ascii_lowercase
        linkMisturado = ''.join((random.choice(letras)) for _ in range(7))

        linkEncurtado = linkMisturado

    else:
        
        if (verificar_link_com_espacos(linkEncurtado)==False):
            mensagem = "Não é permitido ter espaços entre as palavras."
            return render_template("link.html", mensagem=mensagem)

        if (validar_apenas_letras(linkEncurtado)==False):
            mensagem = "Não é permitido ter números e/ou caracteres especiais no link personalizado."
            return render_template("link.html", mensagem=mensagem)

        if (limite_caracteres(linkEncurtado)==True):
            mensagem = "Não é permitido links personalizados com mais de 45 caracteres."
            return render_template("link.html", mensagem=mensagem)

        linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEncurtado)).first()
        if linkCerto !=None:
            mensagem = "Endereço personalizado já está em uso."
            return render_template("link.html", mensagem=mensagem)

        if("i" in linkEncurtado or "I" in linkEncurtado or "l" in linkEncurtado or "L" in linkEncurtado):

            for p in variarPossibilidades(linkEncurtado):
                linkCerto = Link.query.filter(Link.linkEncurtado.like(p)).first()
                if linkCerto !=None:
                    mensagem = "Endereço personalizado já está em uso."
                    return render_template("link.html", mensagem=mensagem)

    if current_user.is_authenticated:  # Verifica se o usuário está logado
        usuario = Usuario.query.filter(Usuario.id.like(current_user.id)).first()
        link = Link(
            linkOriginal=linkOriginal,
            linkEncurtado=linkEncurtado,
            cliques=0,
            usuario=usuario.id
        )

    else:
        usuario = None
        link = Link(
            linkOriginal=linkOriginal,
            linkEncurtado=linkEncurtado,
            cliques=0,
            usuario=usuario
        )

    db.session.add(link)
    db.session.commit()

    linkPronto = Link.query.filter(Link.linkEncurtado.like(linkEncurtado)).first()

    return render_template("link_pronto.html", linkPronto=linkPronto)

@app.route('/<linkEmbaralhado>', methods=["GET"])
def receber_link(linkEmbaralhado):

    """
    Função de Rota para receber o Link e redirecioná-lo ao Link Original.

    :param link: Recebe a String link, a qual será verificado se há I ou L em sua composição e retornará ao usuário caso tenha sido encontrado um link no banco de dados.
    :type link(String(100)):
    :return: Retorna o redirecionamento até o linkOriginal para a página encurtada do usuário.
    :rtype: String
    :raises ValueError: Se a String estiver vazia

    Example:
        >>> receber_link("ROoLjLp")
        redirect(linkCerto.linkOriginal)

        .. note::
            Esta função assume que os valores são Strings.
    """
    linkDenunciado = Denuncias.query.filter(Denuncias.nome.like(linkEmbaralhado)).first()
    if (linkDenunciado!=None):
        return render_template("aviso.html", linkEmbaralhado=linkEmbaralhado)

    if("i" in linkEmbaralhado or "I" in linkEmbaralhado or "l" in linkEmbaralhado or "L" in linkEmbaralhado):

        for p in variarPossibilidades(linkEmbaralhado):
            linkCerto = Link.query.filter(Link.linkEncurtado.like(p)).first()
            if linkCerto !=None:
                contagemCliques(linkCerto)
                return redirect(linkCerto.linkOriginal)
    
    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()

    if (linkCerto == None):
        return render_template("404.html")

    else:
        contagemCliques(linkCerto)

        if (linkDenunciado):
            return render_template("aviso.html", linkEmbaralhado=linkEmbaralhado)

    return redirect(linkCerto.linkOriginal)

@app.route('/contador', methods=["GET"])
def contador_links():

    """
    Função de Rota para mostrar o contador de links mais acessados.

    :param link:
    :type:
    :return: Retorna o render_template da página de contador com a consulta ao banco de dados.
    :rtype:
    :raises ValueError:

    Example:
        >>> contador_links()
        render_template("contador.html", query=query)

        .. note::
            Esta função assume que os valores são Strings.
    """

    query = Link.query.order_by(Link.cliques.desc()).limit(10).all()
    
    return render_template("contador.html", query=query)

@app.route('/meusLinks', methods=["GET"])
@login_required
def meus_links():

    """
    Função de Rota para mostrar os links encurtados pelo usuário logado.

    :param link:
    :type:
    :return: Retorna o render_template da página de meus links com a consulta ao banco de dados.
    :rtype:
    :raises ValueError:

    Example:
        >>> meus_links()
        render_template("meus_links.html", query=query)

        .. note::
            Esta função assume que os valores são Strings.
    """

    consulta = Link.query.filter(Link.usuario.like(current_user.id)).all()

    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    query = consulta[start:end]

    pagination = Pagination(page=page, per_page=per_page, total=len(consulta))

    return render_template("meus_links.html", query=query, pagination=pagination)