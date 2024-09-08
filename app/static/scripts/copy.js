function copyToClipboard() {
    // Pega o texto do parágrafo com o link
    var copyText = document.getElementById("link").innerText;

    // Usa a API moderna para copiar o texto para a área de transferência
    navigator.clipboard.writeText(copyText).then(function() {
        alert("Link copiado para a área de transferência!");
    }).catch(function(err) {
        console.error('Erro ao copiar: ', err);
    });
}