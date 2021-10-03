from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos
import string, random, requests

@app.route('/', methods=["GET", "POST"])
def inicio():
    return render_template("link.html")

@app.route('/link', methods=["POST"])
def enviar_link():

    linkOriginal = request.form["linkOriginal"]
    linkEncurtado = request.form["linkEncurtado"]
    
    #linksProibidos = LinksProibidos.query.filter(LinksProibidos.nome.like('%'+linkOriginal+'%')).first()
    #linksProibidos = LinksProibidos.query.all()

    #if linksProibidos in linkOriginal:
        #mensagem="Links encurtados não podem ser reencurtados"
        #return render_template("link.html", mensagem=mensagem)

    app.logger.info(
        "O link encurtado veio null? " + str(linkEncurtado)
    )

    if (linkEncurtado == ""):
        letras = string.ascii_uppercase+string.ascii_lowercase
        linkMisturado = ''.join((random.choice(letras)) for _ in range(7))

        print("LINK MISTURADO AQUI: "+str(linkMisturado))

        linkEncurtado = linkMisturado
        
    link = Link(
        linkOriginal=linkOriginal,
        linkEncurtado=linkEncurtado,
        cliques=0
    )
    db.session.add(link)
    db.session.commit()

    if ("L" in link.linkEncurtado):
        linkCompleto = link.linkEncurtado.replace('L', 'I')
        print("O LINK NOVO: "+str(linkCompleto))

        link2 = Link(
            linkOriginal=linkOriginal,
            linkEncurtado=linkCompleto,
            cliques=0
        )
        db.session.add(link2)
        db.session.commit()

        print("O LINK TEM L OU I: "+str(linkEncurtado))

    #linkPronto = Link.query.filter(Link.linkOriginal.like(linkOriginal)).order_by(linkEncurtado.id.desc()).first()
    linkPronto = Link.query.filter(Link.linkEncurtado.like(linkEncurtado)).first()

    return render_template("link_pronto.html", linkPronto=linkPronto)

@app.route('/<linkEmbaralhado>', methods=["GET"])
def receber_link(linkEmbaralhado):

    #linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()
    linkCerto = Link.query.filter_by(linkEncurtado=linkEmbaralhado).first()

    #responses = requests.get(linkCerto.linkOriginal)

    #for response in responses.history:
        #print(response.url)

    linkCerto.cliques = int(linkCerto.cliques)+1

    db.session.add(linkCerto)
    db.session.commit()

    return redirect(linkCerto.linkOriginal)