import string, random, requests, pyperclip, time, re
from itertools import product

def verificacaoURL(link): #Função para verificar se o dado recebido possui um link.

    url = r"https?://[^\s]+"
    match = re.search(url, link)

    if match:
        return True
    else:
        return False

def verificacaoTextoURL(link): #Função para verificar se há texto antes do link.

    url = r"https?://[^\s]+"
    match = re.search(url, link)

    if match and match.start() > 0:
        return True
    else:
        return False

def variarPossibilidades(link): #Função para verificar todas as possibilidades com links que possuam I ou L.

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