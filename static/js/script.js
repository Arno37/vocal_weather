document.addEventListener('DOMContentLoaded', function() {
    const microphoneButton = document.getElementById('microphone-button');
    const recognizedTextDiv = document.getElementById('recognized-text');
    const weatherInfoDiv = document.getElementById('weather-info');
    let isRecording = false;
    let recognition;
    let recordingTimeout;
    console.log("Début de l'enregistrement");

    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.lang = 'fr-FR';
        recognition.continuous = false;
        recognition.interimResults = false;

        microphoneButton.addEventListener('click', function() {
            if (isRecording) {
                stopRecording();
            } else {
                startRecording();
            }
        });

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript.toLowerCase();
            recognizedTextDiv.textContent = "Ma demande est : " + transcript;
            console.log(`Transcript : ${transcript}`);
            processVoiceCommand(transcript);
        };

        recognition.onend = function() {
            if (isRecording) {
                recognition.start();
            }
        };
    } else {
        alert("Votre navigateur ne supporte pas la reconnaissance vocale.");
        microphoneButton.disabled = true;
    }

    function startRecording() {
        isRecording = true;
        microphoneButton.classList.add('recording');
        recognizedTextDiv.textContent = '';
        weatherInfoDiv.style.display = 'none';
        recognition.start();
        recordingTimeout = setTimeout(stopRecording, 10000);
    }

    function stopRecording() {
        isRecording = false;
        recognition.stop();
        microphoneButton.classList.remove('recording');
        clearTimeout(recordingTimeout);
    }

    function processVoiceCommand(command) {
        console.log("🔍 Commande vocale reçue :", command);
        let days = 7; // Par défaut, affichage sur 7 jours
        let city = "";

        // Supprimer "aujourd'hui" avant d'extraire la ville
        if (command.includes("aujourd'hui")) {
            days = 1;
            command = command.replace("aujourd'hui", "").trim();
        }

        // Extraction de la ville
        const words = command.split(" ");
        const indexOfA = words.lastIndexOf("à");
        const indexOfDe = words.lastIndexOf("de");

        if (indexOfA !== -1) {
            city = words.slice(indexOfA + 1).join(" ");
        } else if (indexOfDe !== -1) {
            city = words.slice(indexOfDe + 1).join(" ");
        } else {
            city = command;  // Si pas de "à" ou "de", prendre toute la commande
        }

        city = city.trim(); // Nettoyer la ville

        console.log("🏙 Ville détectée :", city);
        sendVoiceCommand(city, days);
    }

    function sendVoiceCommand(city, days) {
        fetch('http://127.0.0.1:8000/weather', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `voice_command=${encodeURIComponent(city)}&days=${days}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des données météo');
            }
            return response.json();  // Convertit la réponse en JSON
        })
        .then(data => {
            console.log("Données météo reçues :", data);  // Affiche toute la réponse
    
            if (data.weather && data.weather.forecasts && data.weather.forecasts.length > 0) {
                console.log("Prévisions météo reçues :", data.weather.forecasts);  // Affiche les prévisions météo
                displayWeatherInfo(data, days);  // Affiche les informations météo
            } else {
                console.error("Aucune prévision météo disponible");
                alert('Aucune donnée météo trouvée ou structure de données incorrecte.');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données météo :', error);
            alert('Erreur lors de la récupération des données météo.');
        });
        function displayWeatherInfo(data, days) {
            const forecasts = data.weather.forecasts.slice(0, days);
        
            // Créer le tableau HTML
            let forecastHtml = `
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Condition</th>
                            <th>Température Max</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
        
            forecasts.forEach(forecast => {
                forecastHtml += `
                    <tr>
                        <td>${forecast.date}</td>
                        <td>${forecast.condition || 'Non spécifiée'}</td>
                        <td>${forecast.temperature_max || 'Non spécifiée'}°C</td>
                    </tr>
                `;
            });
        
            forecastHtml += '</tbody></table>';  // Fermer le tableau
        
            // Insérer le tableau dans le DOM
            weatherInfoDiv.innerHTML = forecastHtml;
            weatherInfoDiv.style.display = 'block'; // Afficher la section météo
        }
        
    }
    

});