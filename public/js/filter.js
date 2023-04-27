// gestion liste déroulante filtre affichage avec rechargement

let filter = document.getElementById("sort_by");
//let filtre = filter.value

filter.addEventListener("change", function() {
  
  window.location.href = (`/articles?filter=${filter.value}`);
});

window.addEventListener("onload", () => {
  filter.value = filter;
})