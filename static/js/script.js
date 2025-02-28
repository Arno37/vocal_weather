function processVoiceCommand(command) {
    console.log("🔍 Commande vocale reçue :", command);
    let days = 7; 
    let city = "";

    // ✅ Supprimer "aujourd'hui" avant d'extraire la ville
    if (command.includes("aujourd'hui")) {
        days = 1; 
        command = command.replace("aujourd'hui", "").trim();
    }

    // ✅ Extraction de la ville
    const words = command.split(" ");
    const indexOfA = words.lastIndexOf("à");
    const indexOfDe = words.lastIndexOf("de");

    if (indexOfA !== -1) {
        city = words.slice(indexOfA + 1).join(" ");
    } else if (indexOfDe !== -1) {
        city = words.slice(indexOfDe + 1).join(" ");
    } else {
        city = command;  // 🔹 Si pas de "à" ou "de", prendre toute la commande
    }

    city = city.trim(); // 🔹 Nettoyer la ville

    console.log("🏙 Ville détectée :", city);
    sendVoiceCommand(city, days);
}
