document.addEventListener('DOMContentLoaded', function() {
    const microphoneButton = document.getElementById('microphone-button');
    const recognizedTextDiv = document.getElementById('recognized-text');
    const weatherInfoDiv = document.getElementById('weather-info');
    let isRecording = false;
    let recognition;
    let recordingTimeout;

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
            recognizedTextDiv.textContent = "Ma demande est: " + transcript;
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
        let days = 7; // ✅ Par défaut, affichage sur 7 jours
        let city = "";

        if (command.includes("aujourd'hui")) {
            days = 1; // ✅ Si "aujourd'hui" est précisé, on affiche 1 jour seulement
        }

        // Extraction de la ville
        const words = command.split(" ");
        const indexOfA = words.lastIndexOf("à");
        const indexOfDe = words.lastIndexOf("de");
        if (indexOfA !== -1) {
            city = words.slice(indexOfA + 1).join(" ");
        } else if (indexOfDe !== -1) {
            city = words.slice(indexOfDe + 1).join(" ");
        }

        if (!city) {
            alert("Veuillez préciser une ville.");
            return;
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
            console.log("Données reçues :", data);
            displayWeatherInfo(data, days);
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données météo :', error);
            alert('Erreur lors de la récupération des données météo.');
        });
    }

    function displayWeatherInfo(weatherData, days) {
        if (!weatherData.weather) {
            alert("Données météo non disponibles !");
            return;
        }

        let forecastContainer = document.getElementById('forecast');
        let cityName = document.getElementById('city-name');
        let condition = document.getElementById('condition');
        let temperature = document.getElementById('temperature');

        cityName.textContent = weatherData.weather.city;
        forecastContainer.innerHTML = '';
        condition.textContent = '';
        temperature.textContent = '';

        if (!weatherData.weather.forecasts || weatherData.weather.forecasts.length === 0) {
            forecastContainer.innerHTML = "Aucune donnée météo.";
            return;
        }

        if (days === 1) {
            // ✅ Affichage de la météo du jour uniquement
            const today = new Date().toISOString().split('T')[0];

            const todayForecast = weatherData.weather.forecasts.find(forecast => forecast.date === today);

            if (todayForecast) {
                condition.textContent = todayForecast.condition;
                temperature.textContent = todayForecast.temperature_max + "°C";
            } else {
                condition.textContent = "Aucune prévision disponible pour aujourd'hui.";
                temperature.textContent = "";
            }

            // ✅ Cacher complètement la section "Prévisions" si on affiche juste la météo du jour
            forecastContainer.style.display = "none";
        } else {
            // ✅ Affichage du tableau des prévisions sur 7 jours
            forecastContainer.style.display = "block";
            forecastContainer.innerHTML = `<h3>Prévisions pour les 7 prochains jours :</h3>
                                           <div id="forecast-grid"></div>`;

            let forecastGrid = document.createElement("div");
            forecastGrid.id = "forecast-grid";
            forecastGrid.style.display = "flex";
            forecastGrid.style.overflowX = "auto";
            forecastGrid.style.gap = "10px";

            weatherData.weather.forecasts.slice(0, 7).forEach(forecast => {
                let forecastElement = document.createElement('div');
                forecastElement.style.border = "1px solid #ddd";
                forecastElement.style.padding = "10px";
                forecastElement.style.minWidth = "120px";
                forecastElement.style.textAlign = "center";
                forecastElement.style.borderRadius = "5px";
                forecastElement.style.boxShadow = "2px 2px 5px rgba(0,0,0,0.1)";
                
                forecastElement.innerHTML = `<strong>${forecast.date}</strong><br>${forecast.condition}<br>${forecast.temperature_max}°C`;

                forecastGrid.appendChild(forecastElement);
            });

            forecastContainer.appendChild(forecastGrid);

            // ✅ Ne pas afficher la météo du jour
            condition.textContent = "";
            temperature.textContent = "";
        }

        weatherInfoDiv.style.display = 'block';
    }
});
