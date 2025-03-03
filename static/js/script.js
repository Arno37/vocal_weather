document.addEventListener('DOMContentLoaded', function() {
    const microphoneButton = document.getElementById('microphone-button');
    const recognizedTextDiv = document.getElementById('recognized-text');
    const weatherInfoDiv = document.getElementById('weather-info');
    const forecastTableDiv = document.getElementById('forecast-table'); // ✅ Zone séparée pour le tableau météo
    const mapContainer = document.getElementById('map-container');
    const mapFrame = document.getElementById('map-frame');
    const mapCityName = document.getElementById('map-city-name');

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
        let days = 7; // Par défaut, affiche 7 jours
        let city = "";
    
        // ✅ Obtenir la date actuelle
        let today = new Date();
    
        // ✅ Vérification des mots-clés et ajustement de la date
        if (command.includes("aujourd'hui")) {
            days = 1;
            command = command.replace("aujourd'hui", "").trim();
        } else if (command.includes("demain")) {
            days = 1;
            today.setDate(today.getDate() + 1); // ✅ Ajoute 1 jour pour obtenir demain
            command = command.replace("demain", "").trim();
        } else if (command.includes("cette semaine")) {
            days = 7;
            command = command.replace("cette semaine", "").trim();
        }
    
        // ✅ Formater la date au format YYYY-MM-DD
        let formattedDate = today.toISOString().split("T")[0];
        console.log("📆 Date de début des prévisions :", formattedDate);
    
        // Extraction de la ville
        const words = command.split(" ");
        const indexOfA = words.lastIndexOf("à");
        const indexOfDe = words.lastIndexOf("de");
    
        if (indexOfA !== -1) {
            city = words.slice(indexOfA + 1).join(" ");
        } else if (indexOfDe !== -1) {
            city = words.slice(indexOfDe + 1).join(" ");
        } else {
            city = command;
        }
    
        city = capitalizeFirstLetter(city.trim());
    
        console.log("🏙 Ville détectée :", city);
        console.log("📆 Prévisions demandées pour :", days, "jours à partir de", formattedDate);
    
        if (mapCityName) {
            mapCityName.textContent = city;
        }
    
        sendVoiceCommand(city, days, formattedDate);
    }
    
    function sendVoiceCommand(city, days, startDate) {
        fetch('http://127.0.0.1:8000/weather', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `voice_command=${encodeURIComponent(city)}&days=${days}&start_date=${startDate}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur lors de la récupération des données météo.");
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ Données météo reçues :", data);
    
            if (data.weather && data.weather.forecasts && data.weather.forecasts.length > 0) {
                displayWeatherInfo(data, days);
            } else {
                console.error("❌ Aucune prévision météo disponible");
                alert("Aucune donnée météo trouvée.");
            }
        })
        .catch(error => {
            console.error("❌ Erreur lors de la récupération des données météo :", error);
            alert("Erreur lors de la récupération des données météo.");
        });
    }
    
    function capitalizeFirstLetter(string) {
        if (!string) return "";
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    

    function displayWeatherInfo(data, days) {
        const forecasts = data.weather.forecasts.slice(0, days);
        const cityName = data.weather.city || "Ville inconnue";
    
        let forecastHtml = `
            <table class="table table-bordered text-center">
                <thead>
                    <tr>
                        <th>${cityName}</th> <!-- ✅ Ville en titre vertical -->
        `;
    
        // ✅ Ajouter chaque date en en-tête (horizontal)
        forecasts.forEach(forecast => {
            forecastHtml += `<th>${forecast.date}</th>`;
        });
    
        forecastHtml += `</tr></thead><tbody>`;
    
        // ✅ Ligne pour les conditions météo
        forecastHtml += `<tr><td><strong>Condition</strong></td>`;
        forecasts.forEach(forecast => {
            forecastHtml += `<td>${forecast.condition || 'Non spécifiée'}</td>`;
        });
        forecastHtml += `</tr>`;
    
        // ✅ Ligne pour les températures
        forecastHtml += `<tr><td><strong>Température Max</strong></td>`;
        forecasts.forEach(forecast => {
            forecastHtml += `<td>🌡 ${forecast.temperature_max || 'Non spécifiée'}°C</td>`;
        });
        forecastHtml += `</tr>`;
    
        forecastHtml += `</tbody></table>`;
    
        if (forecastTableDiv) {
            forecastTableDiv.innerHTML = forecastHtml;
        } else {
            console.error("❌ 'forecast-table' introuvable !");
        }
    
        weatherInfoDiv.style.display = 'block';
    
        // ✅ Mise à jour de la carte si des coordonnées existent
        if (data.weather.coordinates) {
            const lat = data.weather.coordinates.latitude;
            const lon = data.weather.coordinates.longitude;
            const offset = 0.05;
            const bbox = `${lon - offset}%2C${lat - offset}%2C${lon + offset}%2C${lat + offset}`;
            const mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat}%2C${lon}`;
    
            if (mapFrame) {
                mapFrame.src = mapUrl;
            }
    
            if (mapContainer) {
                mapContainer.style.display = 'block';
            }
        }
    }
    
    
});