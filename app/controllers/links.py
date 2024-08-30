from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, pyperclip, time
from itertools import product

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

    linkPronto = Link.query.filter(Link.linkEncurtado.like(linkEncurtado)).first()

    #pyperclip.copy('The text to be copied to the clipboard.')
    #copiar = pyperclip.paste()

    return render_template("link_pronto.html", linkPronto=linkPronto)

@app.route('/<linkEmbaralhado>', methods=["GET"])
def receber_link(linkEmbaralhado):

    if("i" in linkEmbaralhado or "I" in linkEmbaralhado or "l" in linkEmbaralhado or "L" in linkEmbaralhado):
        
        print("Passou pelo if de i ou L")

        substituicoes = {
        'i': ['I', 'l'],
        'I': ['i', 'L'],
        'l': ['L', 'i'],
        'L': ['l', 'I']
        }
        
        listaPossibilidades = []
        
        for char in linkEmbaralhado:
            if char in substituicoes:
                listaPossibilidades.append(substituicoes[char] + [char])
            else:
                listaPossibilidades.append([char])
        
        todasCombinacoes = product(*listaPossibilidades)
        
        possibilidades = [''.join(combinacoes) for combinacoes in todasCombinacoes]
        

    for p in possibilidades:
        linkCerto = Link.query.filter(Link.linkEncurtado.like(p)).first()
        #print(p)
        if linkCerto !=None:
            return redirect(linkCerto.linkOriginal)
    
    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()

    linkDenunciado = Denuncias.query.filter(Denuncias.nome.like(linkEmbaralhado)).first()
    if (linkDenunciado!=None):
        print("O link acessado foi denunciado:", linkDenunciado.nome)

    if (linkCerto == None):
        return render_template("404.html")

    else:
        linkCerto.cliques = int(linkCerto.cliques)+1

        db.session.add(linkCerto)
        db.session.commit()

        if (linkDenunciado):
            return render_template("aviso.html")

    return redirect(linkCerto.linkOriginal)

@app.route('/acessarLinkDenunciado/<linkEmbaralhado>', methods=["GET", "POST"])
def receber_linkDenunciado(linkEmbaralhado):
        
    linkEncurtado = request.form["linkEncurtado"]
    
    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()
    return redirect(linkCerto.linkOriginal)

@app.route('/contador', methods=["GET"])
def contador_links():

    query = Link.query.order_by(Link.cliques.desc()).limit(10).all()
    
    return render_template("contador.html", query=query)