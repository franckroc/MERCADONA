let btnCatalog = document.getElementById("catalogueBtn");
btnCatalog.addEventListener("click", function() {
    window.location.href = "/articles";
});

let btnAdmin = document.getElementById("adminBtn");
btnAdmin.addEventListener("click", function() {
    window.location.replace("/admin/");
});