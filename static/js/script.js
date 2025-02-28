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
});
