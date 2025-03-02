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
            city = command;
        }

        city = city.trim();

        console.log("🏙 Ville détectée :", city);

        if (mapCityName) {
            mapCityName.textContent = city;
            console.log("📍 Ville mise à jour sur la carte :", city);
        } else {
            console.error("❌ L'élément 'map-city-name' n'a pas été trouvé.");
        }

        sendVoiceCommand(city, days);
    }

    function sendVoiceCommand(city, days) {
        fetch('http://127.0.0.1:8000/weather', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `voice_command=${encodeURIComponent(city)}&days=${days}`
        })
        .then(response => response.json())
        .then(data => {
            console.log("Données météo reçues :", data);

            if (data.weather && data.weather.forecasts && data.weather.forecasts.length > 0) {
                displayWeatherInfo(data, days);
            } else {
                console.error("Aucune prévision météo disponible");
                alert('Aucune donnée météo trouvée.');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données météo :', error);
            alert('Erreur lors de la récupération des données météo.');
        });
    }

    function displayWeatherInfo(data, days) {
        const forecasts = data.weather.forecasts.slice(0, days);
        const cityName = data.weather.city || "Ville inconnue";

        let forecastHtml = `
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Nom</th>
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
                    <td>${cityName}</td>
                    <td>${forecast.date}</td>
                    <td>${forecast.condition || 'Non spécifiée'}</td>
                    <td>${forecast.temperature_max || 'Non spécifiée'}°C</td>
                </tr>
            `;
        });

        forecastHtml += '</tbody></table>';

        if (forecastTableDiv) {
            forecastTableDiv.innerHTML = forecastHtml;
        } else {
            console.error("❌ 'forecast-table' introuvable !");
        }

        weatherInfoDiv.style.display = 'block';

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
