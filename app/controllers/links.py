from app import app, db, os
from flask import render_template, request, redirect, session
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, time, re, urllib.parse
from itertools import product
from flask_login import login_required, current_user
from urllib.parse import urlparse

def variarPossibilidades(link):

    """
    Função para verificar todas as possibilidades possíveis com links que possuam I ou L.

    :param link: Recebimento do link encurtado depois da rota '/'.
    :type link(String(100)):
    :return: Retorna um Array com todas as possibilidades de links com a troca das letras "I" e "L".
    :rtype: String
    :raises ValueError: Se a String estiver vazia

    Example:
        >>> variarPossibilidades("https://g1.globo.com/")
        ["https://g1.globo.com/", "https://g1.giobo.com/", "https://g1.gIobo.com/", "https://g1.gLobo.com/"]

        .. note::
            Esta função assume que os valores são Strings.
    """

    substituicoes = {
        'i': ['I', 'l'],
        'I': ['i', 'L'],
        'l': ['L', 'i'],
        'L': ['l', 'I']
        }
        
    listaPossibilidades = []
        
    for char in link:
        if char in substituicoes:
            listaPossibilidades.append(substituicoes[char] + [char])
        else:
            listaPossibilidades.append([char])
        
    todasCombinacoes = product(*listaPossibilidades)
        
    possibilidades = [''.join(combinacoes) for combinacoes in todasCombinacoes]

    return possibilidades

def contagemCliques(link):

    """
    Função para acrescentar mais um clique ao saldo de cliques.

    :param link: Recebe a String link, a qual será consultada no banco de dados.
    :type link(String(100)):
    :return: Retorna um objeto chamado 'link' com um acréscimo ao valor de cliques.
    :rtype: String
    :raises ValueError: Se a String estiver vazia

    Example:
        >>> contagemCliques("portal_IFRO")
        1

        .. note::
            Esta função assume que os valores são Strings.
    """

    link.cliques = int(link.cliques)+1

    db.session.add(link)
    db.session.commit()
    
    return link

def verificacaoTextoURL(link):

    """
    Função para verificar se há texto antes do link.

    :param link: Recebe a String link, a qual será verificada se existe texto antes do link.
    :type link(String(100)):
    :return: Retorna True para quando a condição é verdadeira em ter texto antes do link. Retorna falso para quando a condição é falsa em ter texto antes do link.
    :rtype: String
    :raises ValueError: Se a String estiver vazia

    Example:
        >>> verificacaoTextoURL("Fonte: https://g1.globo.com/")
        True
        >>> verificacaoTextoURL("https://g1.globo.com/")
        False

        .. note::
            Esta função assume que os valores são Strings.
    """

    url = r"https?://[^\s]+"
    match = re.search(url, link)

    if match and match.start() > 0:
        return True
    else:
        return False

def verificacaoURL(link):

    """
    Função para verificar se o dado recebido possui um link.

    :param link: Recebe a String link, a qual será verificada se é um link de fato.
    :type link(String(100)):
    :return: Retorna True para quando a condição é verdadeira sobre a String ser um link. Retorna falso para quando a condição é falsa sobre a String ser um link.
    :rtype: String
    :raises ValueError: Se a String estiver vazia

    Example:
        >>> verificacaoURL("https://g1.globo.com/")
        True
        >>> verificacaoURL(" ")
        False

        .. note::
            Esta função assume que os valores são Strings.
    """

    url = r"https?://[^\s]+"
    match = re.search(url, link)

    if match:
        return True
    else:
        return False

def verificar_link_proibido(link):
    url_dividida = urllib.parse.urlparse(link)
    dominio = url_dividida.netloc
    link_proibido = LinksProibidos.query.filter_by(nome=dominio).first()

    if link_proibido:
        return True
    else:
        return False

def verificar_link_com_espacos(link):
    return bool(re.match(r"^\S+$", link))

def validar_apenas_letras(link):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]+$", link))

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
    linkEncurtado = request.form["linkEncurtado"]

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
    
    #if (is_blocked(linkOriginal)==True):
        #mensagem = "Não é permitido encurtar link de sites adultos."
        #return render_template("link.html", mensagem=mensagem) 

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
            print(p)
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
    query = Link.query.filter(Link.usuario.like(current_user.id)).all()
    
    return render_template("meus_links.html", query=query)