from app import app, db, os
from flask import render_template, request, redirect, session
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, time, re, urllib.parse
from itertools import product
from flask_login import login_required, current_user

def variarPossibilidades(link, maximo_variacoes=1000):

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

    """ Gera variações substituindo I ↔ L, mas limita o número máximo. """

    mapeamento = {'i': 'l', 'l': 'i'}
    posicoes = [i for i, c in enumerate(link) if c in mapeamento]

    num_possivel = min(len(posicoes), maximo_variacoes)

    variacoes = set()
    for combinacao in product(*[(c, mapeamento.get(c, c)) for c in link]):
        variacoes.add("".join(combinacao))
        if len(variacoes) >= maximo_variacoes:
            break
    
    return variacoes

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

def limite_caracteres(link):
    MAXIMO_DE_CARACTERES = 45 #Este valor segue o máximo de caracteres estipulado no banco de dados, se alterar lá, é necessário alterar aqui.
    if len(link) > MAXIMO_DE_CARACTERES:
        return True
    else:
        return False

def validar_https(link):
    padrao = r"^https://[\w\-]+(\.[\w\-]+)+[/#?]?.*$"
    return re.match(padrao, link) is not None