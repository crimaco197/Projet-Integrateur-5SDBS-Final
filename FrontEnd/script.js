async function fetchData() {
    const url = 'http://192.168.37.69:50000/start_orchestration/?url=https://www.youtube.com/';
    const options = {
        method: 'GET',
    };

    try {
        // Envoi de la requête
        const response = await fetch(url, options);

        // Vérification du statut de la réponse
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Traitement de la réponse JSON
        const result = await response.json();
        console.log(result);

        // Récupérer l'élément où afficher les données
        const output = document.getElementById('output');
        
        // Affichage des données sans le statut
        if (output) {
            output.innerHTML = `
                <p><strong>Prediction:</strong> ${result.execution_output.prediction}</p>
                <p><strong>Confidence:</strong> ${result.execution_output.confidence}%</p>
            `;
        }
    } catch (error) {
        console.error(error);

        // En cas d'erreur, affichez un message d'erreur dans l'élément HTML
        const output = document.getElementById('output');
        if (output) {
            output.textContent = `Erreur : ${error.message}`;
        }
    }
}

// Lancement de la fonction fetchData au chargement du popup
fetchData();