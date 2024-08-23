from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, pyperclip, time

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

    else:
        linkComLetrasIguais = ""
        contador = 0
        letrasIL = "i"+"I"
        letrasIL2 = "l"+"L"

        while Link.query.filter(Link.linkEncurtado.like(linkComLetrasIguais)).first()==None:
            
            linkComLetrasIguais = linkEncurtado.replace(random.choice(letrasIL), random.choice(letrasIL2), contador)
            linkComLetrasIguais = linkEncurtado.replace(random.choice(letrasIL), random.choice(letrasIL2), contador+1)
            print("Link: "+str(linkComLetrasIguais)+" Contador: "+str(contador))
            contador=contador+1
            if(contador==len(linkEncurtado)):
                link = Link(
                    linkOriginal=linkOriginal,
                    linkEncurtado=linkEncurtado,
                    cliques=0
                )
                db.session.add(link)
                db.session.commit()

                linkPronto = Link.query.filter(Link.linkEncurtado.like(linkEncurtado)).first()
                return render_template("link_pronto.html", linkPronto=linkPronto)

        mensagem = "Endereço personalizado já está em uso"
        return render_template("link.html", mensagem=mensagem)

    link = Link(
        linkOriginal=linkOriginal,
        linkEncurtado=linkEncurtado,
        cliques=0
    )
    db.session.add(link)
    db.session.commit()

    '''
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
    '''
    #linkPronto = Link.query.filter(Link.linkOriginal.like(linkOriginal)).order_by(linkEncurtado.id.desc()).first()
    linkPronto = Link.query.filter(Link.linkEncurtado.like(linkEncurtado)).first()

    #pyperclip.copy('The text to be copied to the clipboard.')
    #copiar = pyperclip.paste()

    return render_template("link_pronto.html", linkPronto=linkPronto)

@app.route('/<linkEmbaralhado>', methods=["GET"])
def receber_link(linkEmbaralhado):

    if(linkEmbaralhado==None):
        return render_template("link.html")
    '''
    if(Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()==None):
        #print("O link acessado é encurtado: " +linkEmbaralhado)
        
        if("i" in linkEmbaralhado):
            #linkComLetrasIguais = linkEmbaralhado.replace("l", "i", 1)
            linkComLetrasIguais = linkEmbaralhado.replace("i", "l", 1)
            print("Pesquisa nova: " +linkComLetrasIguais)
            linkCerto = Link.query.filter(Link.linkEncurtado.like(linkComLetrasIguais)).first()
            print(linkCerto)
    '''
    #print(Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first())
    
    linkComLetrasIguais = ""
    contador = 0
    letrasIL = "i"+"I"
    letrasIL2 = "l"+"L"
    #print(letrasIL)
    #print(letrasIL2)

    if(Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()==None):
        while Link.query.filter(Link.linkEncurtado.like(linkComLetrasIguais)).first()==None:
        
            linkComLetrasIguais = linkEmbaralhado.replace(random.choice(letrasIL), random.choice(letrasIL2), contador)
            linkComLetrasIguais = linkEmbaralhado.replace(random.choice(letrasIL), random.choice(letrasIL2), contador+1)
            print("Link: "+str(linkComLetrasIguais)+" Contador: "+str(contador))
            contador=contador+1
            if(contador==len(linkEmbaralhado)):
                return render_template("404.html")
        
        linkCerto = Link.query.filter(Link.linkEncurtado.like(linkComLetrasIguais)).first()
        return redirect(linkCerto.linkOriginal)
        
    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()
    #linkCerto = Link.query.filter_by(linkEncurtado=linkEmbaralhado).first()
    #linkCerto = Link.query.filter(Link.linkEncurtado.iexact==linkEmbaralhado).first()

    linkDenunciado = Denuncias.query.filter(Denuncias.nome.like(linkEmbaralhado)).first()
    if (linkDenunciado!=None):
        print("O link acessado foi denunciado:", linkDenunciado.nome)

    #linkDenunciado = Link.query.filter(Link.linkEncurtado.like(linksDenunciados))

    if (linkCerto == None):
        return render_template("404.html")

    else:
        linkCerto.cliques = int(linkCerto.cliques)+1

        db.session.add(linkCerto)
        db.session.commit()

        if (linkDenunciado):
            return render_template("aviso.html")

    return redirect(linkCerto.linkOriginal)