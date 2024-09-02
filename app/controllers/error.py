from app import app
from flask import render_template

@app.errorhandler(404)
def pagina_nao_encontrada(e):

    """
    Função de Rota para erros número 404.

    :param link:
    :type:
    :return: Retorna o render_template com o template de rota de erro 404.
    :rtype:
    :raises ValueError:

    Example:

        .. note:: 
        
    """

    return render_template("404.html"), 404