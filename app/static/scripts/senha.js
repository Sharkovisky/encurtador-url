// Mostrar a senha do usuário quando ele clicar no botão
document.getElementById("togglePassword").addEventListener("click", function () {
    let passwordField = document.getElementById("inputPassword");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
});