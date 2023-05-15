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

const product = document.getElementById("id_produit").addEventListener("change", function() {
const productId = document.getElementById("id_produit").value;

  //requete AJAX vers backend avec id produit
fetch(`/prodSelected/${productId}`)
  .then(response => response.json())
  .then(data => {
  var prod = document.getElementById("prodSelected");
  // affiche les data reçues
  prod.innerHTML = `<p>Nom du produit : ${data.name}</p>
                    <p>Description : ${data.description}</p>
                    <p>Prix initial : ${data.price} euros</p>
                    <p>Promotion : ${data.promotion}</p>`;
    })
  .catch(error => {
    console.error("Une erreur s'est produite lors de la récupération des caractéristiques du produit :", error);
    });
});