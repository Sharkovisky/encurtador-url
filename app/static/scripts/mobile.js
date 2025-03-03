document.addEventListener("DOMContentLoaded", function () {
    if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        
        document.getElementById("data1").classList.remove("container_form");
        document.getElementById("data2").classList.add("container_form");
        document.getElementById("data3").classList.add("pt-3");
    }
});