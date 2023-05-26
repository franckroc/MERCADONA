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

// formulaire création promotion
// caractéristiques du produit sélectionné
const product = document.getElementById("id_produit").addEventListener("change", function() {
const productId = document.getElementById("id_produit").value;

  //requete AJAX vers backend avec id produit
fetch(`/prodSelected/${productId}`)
  .then(response => response.json())
  .then(data => {
  var prod = document.getElementById("prodSelected");
  // affiche les datas reçues
  prod.innerHTML = `<p><strong>Nom du produit :</strong>${data.name}</p> 
                    <p><strong>Description :</strong> ${data.description}</p> 
                    <p><strong>Prix initial :</strong> ${data.price} euros</p> 
                    <p><strong>Promotion :</strong> ${data.promotion}</p>`;
        })
  .catch(error => {
    console.error("Une erreur s'est produite lors de la récupération des caractéristiques du produit :", error);
    });
});

// fonction exportation PDF
const pdfExportation = document.getElementById("btnExport");
pdfExportation.addEventListener("click", async() => {
  await fetch("/export-pdf")
    .then(response => response.json())
    .then(response => {
      var respPDF = document.getElementById("responseExportPDF")
      var respPath = document.getElementById("pathPDF")
      respPDF.innerHTML = `<strong>${response.PDF}</strong>`
      respPath.innerHTML = `<a href="${response.PATH}" target="_blank" style="color: yellow;">Télécharger ici</a>`
      })
    .catch(error => {
      console.error("Une erreur est survenue lors de la création du PDF: ",error);
      });
}); 