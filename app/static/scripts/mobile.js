document.addEventListener("DOMContentLoaded", function () {
    if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        document.querySelectorAll("label").forEach(label => label.style.display = "none");
        let placeholderLinkOriginal = document.getElementById("linkOriginal");
        let placeholderLinkPersonalizado = document.getElementById("linkEncurtado");

        if (placeholderLinkOriginal.placeholder === "") {
            placeholderLinkOriginal.placeholder = "Link a ser encurtado";
        }
        if (placeholderLinkPersonalizado.placeholder === "(Opcional)") {
            placeholderLinkPersonalizado.placeholder = "Link personalizado";
        }
    }
});