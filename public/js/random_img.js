function selectRandomImages() {
  // tableau images
  const images = ["public/img/casquette.jpg", "public/img/rateau.jpg", "public/img/arrosoir.jpg", "public/img/ordinateur.jpg", 
                  "public/img/ceinture.jpg", "public/img/imprimante.jpg", "public/img/ordinateur2.jpg", "public/img/oreiller.jpg",
                  "public/img/souris.jpg", "public/img/styloplume.jpg", "public/img/vase.jpg", "public/img/tuyau-d-arrosage.jpg",
                  "public/img/blouson.jpg", "public/img/blocnote.jpg"];
    
  // tableau descriptions images
  const descriptions = ["Casquette", "Rateau", "Arrosoir", "Ordinateur portable", 
                        "Ceinture", "Imprimante", "Ordinateur de bureau", "Oreiller",
                        "Souris", "Stylo plume", "Vase", "Tuyau d'arrosage", "Blouson",
                        "Bloc-notes"]; 
    
  // récupère l'élément <div> qui va contenir les cartes
  const cardsContainer = document.querySelector(".card-container"); 
  // tableau pour stocker les images
  const selectedImages = []; 
    
  // 2 rangées d'images avec une div
  for (let i = 0; i < 2; i++) { 
    const imagesRow = document.createElement("div"); 
    imagesRow.classList.add("images-row"); 
        
    // 3 images aléatoires pour chaque rangée dans tableau selectedImages
    for (let j = 0; j < 3; j++) { 
      let randomIndex;
      do {
        randomIndex = Math.floor(Math.random() * images.length); 
      } while (selectedImages.includes(randomIndex)); 
        
      // ajoute l'index de l'image sélectionnée au tableau
      selectedImages.push(randomIndex); 

      // récupère le nom de l'image et la description
      const randomImage = images[randomIndex]; 
      const randomDescription = descriptions[randomIndex]; 

      // crée un élément div pour la carte et son CSS "card"
      const card = document.createElement("div"); 
      card.classList.add("card");

      // crée un élément image son CSS "card-image" et sa "src" avec le nom de l'image sélectionnée
      const cardImage = document.createElement("img"); 
      cardImage.classList.add("card-image"); 
      cardImage.setAttribute("src", randomImage); 

      // crée un <p> pour la description son CSS "card-description et sa description
      const cardDescription = document.createElement("p"); 
      cardDescription.classList.add("card-description"); 
      cardDescription.textContent = randomDescription; 

      card.appendChild(cardImage); // ajoute <img> à la div de la carte
      card.appendChild(cardDescription); // ajoute l'élément <p> à la div de la carte
      imagesRow.appendChild(card); // ajoute la div de la carte à la div de la rangée d'images
    }
    cardsContainer.appendChild(imagesRow); // ajoute la div de la rangée d'images à la div globale qui contient toutes les cartes
  }
}
window.addEventListener("load", selectRandomImages); // lance la fonction au chargement de la page index.html 
  