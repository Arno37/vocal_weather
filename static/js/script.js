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
        recognition.continuous = false; // Mode non continu pour détecter les pauses
        recognition.interimResults = false;

        microphoneButton.addEventListener('click', function() {
            if (isRecording) {
                stopRecording();
            } else {
                startRecording();
            }
        });

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            recognizedTextDiv.textContent = "Ma demande est: " + transcript;
            sendVoiceCommand(transcript);
        };

        recognition.onend = function() {
            if (isRecording) {
                recognition.start(); // Redémarre la reconnaissance en cas de silence
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

        // Arrête l'enregistrement après 10 secondes
        recordingTimeout = setTimeout(stopRecording, 10000);
    }

    function stopRecording() {
        isRecording = false;
        recognition.stop();
        microphoneButton.classList.remove('recording');
        clearTimeout(recordingTimeout);
    }

    function sendVoiceCommand(voiceCommand) {
        fetch('/weather', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'voice_command=' + encodeURIComponent(voiceCommand)
        })
        .then(response => response.json())
        .then(data => {
            displayWeatherInfo(data);
        })
        .catch(error => {
            alert('Erreur lors de la récupération des données météo.');
        });
    }

    function displayWeatherInfo(weatherData) {
        document.getElementById('city-name').textContent = weatherData.city;
        document.getElementById('condition').textContent = weatherData.condition;
        document.getElementById('temperature').textContent = weatherData.temperature;
        document.getElementById('forecast').textContent = weatherData.forecast;
        weatherInfoDiv.style.display = 'flex';
    }
});
