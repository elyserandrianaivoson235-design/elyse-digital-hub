function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    if (chatWindow) {
        chatWindow.classList.toggle('hidden');
    }
}

const btn = document.getElementById('bokotra-hafatira');
if (btn) {
    btn.addEventListener('click', function(event) {
        const anaranaInput = document.querySelector('input[name="anarana"]');
        if (anaranaInput) {
            const anarana = anaranaInput.value;
            if (anarana.trim() !== "") {
                console.log("Hafatra avy amin'i: " + anarana);
            }
        }
    });
}

const toeranaOra = document.getElementById('ora-izao');
if (toeranaOra) {
    setInterval(() => {
        const data = new Date();
        toeranaOra.textContent = data.toLocaleTimeString();
    }, 1000);
}

document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow && !chatWindow.classList.contains('hidden')) {
            chatWindow.classList.add('hidden');
        }
    }
});