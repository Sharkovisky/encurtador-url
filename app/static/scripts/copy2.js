function copyToClipboard(element) {
    // Pega o texto do elemento passado
    var copyText = element.innerText;

    // Usa a API moderna para copiar o texto para a área de transferência
    navigator.clipboard.writeText(copyText).then(function() {
        alert("Link copiado para a área de transferência!");
    }).catch(function(err) {
        console.error('Erro ao copiar: ', err);
    });
}

// Exemplo de como adicionar eventos dinamicamente
document.querySelectorAll(".copy-btn").forEach((button) => {
    button.addEventListener("click", function() {
        // O botão pai deve conter o ID correto do link associado
        var linkElement = this.closest("tr").querySelector(".link");
        copyToClipboard(linkElement);
    });
});
