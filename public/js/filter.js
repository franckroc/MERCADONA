// gestion liste déroulante filtre affichage avec rechargement

let filter = document.getElementById("sort_by");

filter.addEventListener("change", function() {
  
  window.location.href = (`/articles?filter=${filter.value}`);
});

window.addEventListener("onload", () => {
  filter.value = filter;
})