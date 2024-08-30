from app import app, db
from flask import render_template, request, redirect
from app.models.tables import Usuario, Link, LinksProibidos, Denuncias
import string, random, requests, pyperclip, time, re
from itertools import product

def variarPossibilidades(link):

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
    link.cliques = int(link.cliques)+1

    db.session.add(link)
    db.session.commit()
    
    return link

def verificacaoTextoURL(link):

    url = r"https?://[^\s]+"
    match = re.search(url, link)

    if match and match.start() > 0:
        return True
    else:
        return False

def verificacaoURL(link):

    url = r"https?://[^\s]+"
    match = re.search(url, link)

    if match:
        return True
    else:
        return False

@app.route('/', methods=["GET", "POST"])
def inicio():
    return render_template("link.html")

@app.route('/encurtarLink', methods=["POST"]) #Rota para receber o Link, encurtá-lo e devolvê-lo ao usuário.
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

    if (verificacaoTextoURL(linkOriginal)==True):
        mensagem = "Não é permitido ter texto antes do link"
        return render_template("link.html", mensagem=mensagem)

    if (verificacaoURL(linkEncurtado)==True):
        mensagem = "Não é permitido ter como texto personalizado um outro link"
        return render_template("link.html", mensagem=mensagem)

    if (linkEncurtado == ""):
        letras = string.ascii_uppercase+string.ascii_lowercase
        linkMisturado = ''.join((random.choice(letras)) for _ in range(7))

        print("LINK MISTURADO AQUI: "+str(linkMisturado))

        linkEncurtado = linkMisturado

    else:
        
        if("i" in linkEncurtado or "I" in linkEncurtado or "l" in linkEncurtado or "L" in linkEncurtado):
        
            print("Passou pelo if de i ou L")

            for p in variarPossibilidades(linkEncurtado):
                linkCerto = Link.query.filter(Link.linkEncurtado.like(p)).first()
                print(p)
                if linkCerto !=None:
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

@app.route('/<linkEmbaralhado>', methods=["GET"]) #Rota para receber o Link e redirecioná-lo ao Link Original
def receber_link(linkEmbaralhado):

    if("i" in linkEmbaralhado or "I" in linkEmbaralhado or "l" in linkEmbaralhado or "L" in linkEmbaralhado):
        
        print("Passou pelo if de i ou L")

        for p in variarPossibilidades(linkEmbaralhado):
            linkCerto = Link.query.filter(Link.linkEncurtado.like(p)).first()
            print(p)
            if linkCerto !=None:
                contagemCliques(linkCerto)
                return redirect(linkCerto.linkOriginal)
    
    linkCerto = Link.query.filter(Link.linkEncurtado.like(linkEmbaralhado)).first()

    linkDenunciado = Denuncias.query.filter(Denuncias.nome.like(linkEmbaralhado)).first()
    if (linkDenunciado!=None):
        print("O link acessado foi denunciado:", linkDenunciado.nome)

    if (linkCerto == None):
        return render_template("404.html")

    else:
        contagemCliques(linkCerto)

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