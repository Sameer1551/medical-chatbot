function addMessage(message, isUser) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        } else {
            reject(new Error("Geolocation is not supported by this browser."));
        }
    });
}


async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();

    if (message) {
        addMessage(message, true);
        input.value = '';

        try {
            // Handle location requests
            if (message.toLowerCase().includes('location')) {
                try {
                    const position = await getUserLocation();
                    const locationResponse = await fetch(`/chat?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message: message })
                    });
                    const data = await locationResponse.json();
                    addMessage(data.response, false);
                    return;
                } catch (error) {
                    addMessage("Unable to access location. Please grant location permission.", false);
                    return;
                }
            }

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (data.prompt) {
                const healthIssue = prompt(data.response);
                if (healthIssue) {
                    sendMessage(`issue: ${healthIssue}`);
                }
            } else {
                addMessage(data.response, false);
            }
        } catch (error) {
            addMessage('Sorry, there was an error processing your request.', false);
        }
    }
}

document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});