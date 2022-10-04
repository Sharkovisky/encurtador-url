from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests

@app.route('/', methods=["GET", "POST"])
def inicio():
    return render_template("link.html")

@app.route('/encurtarLink', methods=["POST"])
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

    if ("l" in link.linkEncurtado):
        linkCompleto = link.linkEncurtado.replace('l', 'i')
        print("O LINK NOVO: "+str(linkCompleto))

        link2 = Link(
            linkOriginal=linkOriginal,
            linkEncurtado=linkCompleto,
            cliques=0
        )
        db.session.add(link2)
        db.session.commit()

        print("O LINK TEM L OU I: "+str(linkEncurtado))

    if ("i" in link.linkEncurtado):
        linkCompleto = link.linkEncurtado.replace('i', 'l')
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

    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()
    #linkCerto = Link.query.filter_by(linkEncurtado=linkEmbaralhado).first()
    #linkCerto = Link.query.filter(Link.linkEncurtado.iexact==linkEmbaralhado).first()

    linkDenunciado = Denuncias.query.filter(Denuncias.nome.like(linkEmbaralhado)).first()
    print(linkDenunciado)
    #linkDenunciado = Link.query.filter(Link.linkEncurtado.like(linksDenunciados))

    #responses = requests.get(linkCerto.linkOriginal)

    #for response in responses.history:
        #print(response.url)

    if (linkCerto == None):
        return render_template("404.html")

    else:
        linkCerto.cliques = int(linkCerto.cliques)+1

        db.session.add(linkCerto)
        db.session.commit()

        if (linkDenunciado):
            return render_template("aviso.html")

    return redirect(linkCerto.linkOriginal)