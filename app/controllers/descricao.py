from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos
import string, random, requests

@app.route('/descricao', methods=["GET"])
def descricao():

    """
    Função de Rota para mostrar a descrição do projeto.

    :param link:
    :type:
    :return: Retorna o render_template com o arquivo de rota de descrição.
    :rtype:
    :raises ValueError:

    Example:
        
        .. note::
            
    """

    return render_template("descricao.html")