function load(){

    var url = "../src/eurofel.py";

    // Utilisation de l'API Fetch pour chercher le fichier
    fetch(url)
    .then(response => {
        if (response.ok) {
        // Le fichier est présent, changer le contenu du paragraphe
        var paragraphe = document.getElementById("load");
        paragraphe.textContent = "Loaded";
        } else {
        // Le fichier n'est pas présent, changer le contenu du paragraphe
        var paragraphe = document.getElementById("load");
        paragraphe.textContent = "Not Loaded";
        }
    })
    .catch(error => {
        // Une erreur s'est produite lors de la recherche du fichier
        console.error("Erreur lors de la recherche du fichier :", error);
    });
}
function monProcessus() {
    let content = Document.getElementById("sb_status");

}
load();
//setInterval(monProcessus, 200);