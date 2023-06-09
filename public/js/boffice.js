// Récupération des éléments HTML
const createProductLink = document.querySelector("#linkCreateProd");
const createProductForm = document.querySelector("#form-prod-container");

const createPromoLink = document.querySelector("#linkCreatePromo");
const createPromoForm = document.querySelector("#form-promo-container");

const updateProdLink = document.querySelector("#linkUpdateProd");
const updateProductForm = document.querySelector("#form-updateProd-container");


// Afficher/masquer les formulaires
function displayUpdateProdForm() {
  createPromoForm.style.display = "none";
  createProductForm.style.display = "none";
  updateProductForm.style.display =
    updateProductForm.style.display === "none" ? "block" : "none";
}

function displayProductForm() {
  createPromoForm.style.display = "none";
  updateProductForm.style.display = "none";
  createProductForm.style.display =
    createProductForm.style.display === "none" ? "block" : "none";
}

function displayPromoForm() {
  createProductForm.style.display = "none";
  updateProductForm.style.display = "none";
  createPromoForm.style.display =
    createPromoForm.style.display === "none" ? "block" : "none";
}

// Ajout d'un écouteur d'événements sur les liens "Créer Produit" et "créer promo"
// et "modifier prod"

createProductLink.addEventListener("click", (event) => {
  event.preventDefault();
  displayProductForm();
});

createPromoLink.addEventListener("click", (event) => {
  event.preventDefault();
  displayPromoForm();
});

updateProdLink.addEventListener("click", (event) => {
  event.preventDefault();
  displayUpdateProdForm();
});

// formulaire modification produit
const productUpdate = document.getElementById("id_prodUpdate").addEventListener("change", function() {
  const prodIdUpdate = document.getElementById("id_prodUpdate").value;
  fetch(`/prodUpdate/${prodIdUpdate}`)
    .then(response => response.json())
    .then(data => {
      const labelUpdate = document.getElementById("libelleUpdate");
      const descriptUpdate = document.getElementById("descriptionUpdate");
      const priceUpdate = document.getElementById("prixUpdate");
      const promoInPromo = document.getElementById("promoOnUpdate");
      const promoNotPromo = document.getElementById("promoOffUpdate");
      const catUpdate = document.getElementById("categorieUpdate");

      labelUpdate.value = `${data.libelle}`;
      descriptUpdate.value = `${data.description}`;
      priceUpdate.value = `${data.prix}`;

      if (data.en_promo === true ) {
        console.log("true");
        promoInPromo.checked = true;
        promoNotPromo.checked = false;
      } else {
        promoNotPromo.checked = true;
        promoInPromo.checked = false;

      }
      catUpdate.value = `${data.categorie}`;
    })
    .catch(error => {
      console.error("Une erreur s'est produite lors de la récupération des caractéristiques du produit :", error);
    });
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
  var waitingMsg = document.getElementById("waitMsg");
  waitingMsg.innerHTML = "Waiting ..."

  await fetch("/export-pdf")
    .then(response => response.json())
    .then(response => {
      var respPDF = document.getElementById("responseExportPDF");
      var respPath = document.getElementById("pathPDF");
      waitingMsg.style.display = 'none';
      respPDF.innerHTML = `<strong>${response.PDF}</strong>`;
      respPath.innerHTML = `<a href="${response.PATH}" target="_blank" style="color: yellow;">Télécharger ici</a>`;

        // efface les messages après 10 s
      setTimeout(function() {
         respPath.style.display = 'none';
         respPDF.style.display = 'none';
      }, 10000);
      })

    .catch(error => {
      console.error("Une erreur est survenue lors de la création du PDF: ",error);
      });
}); 