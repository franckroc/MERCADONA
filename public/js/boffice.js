// Récupération des éléments HTML
const createProductLink = document.querySelector("#linkCreateProd");
const createProductForm = document.querySelector("#form-prod-container");

const createPromoLink = document.querySelector("#linkCreatePromo");
const createPromoForm = document.querySelector("#form-promo-container");
// Afficher/masquer les formulaires
function displayProductForm() {
  createPromoForm.style.display = "none";
  createProductForm.style.display =
    createProductForm.style.display === "none" ? "block" : "none";
}

function displayPromoForm() {
  createProductForm.style.display = "none";
  createPromoForm.style.display =
  createPromoForm.style.display === "none" ? "block" : "none";
}

// Ajout d'un écouteur d'événements sur les liens "Créer Produit" et "créer promo"
createProductLink.addEventListener("click", (event) => {
  event.preventDefault();
  displayProductForm();
});

createPromoLink.addEventListener("click", (event) => {
  event.preventDefault();
  displayPromoForm();
});
