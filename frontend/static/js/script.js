document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const interestInput = document.getElementById('interest-text');
    const addInterestButton = document.getElementById('add-interest-button');

    const userId = '1'; // In a real app, you'd manage user sessions

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    addInterestButton.addEventListener('click', addInterest);

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessageToChat('user', message);
            messageInput.value = '';

            fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    content_type: 'response',
                    user_input: message
                }),
            })
            .then(response => response.json())
            .then(data => {
                addMessageToChat('bot', data.content);
            })
            .catch(error => console.error('Error:', error));
        }
    }

    function addInterest() {
        const interest = interestInput.value.trim();
        if (interest) {
            fetch('/add_interest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    interest: interest
                }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                interestInput.value = '';
            })
            .catch(error => console.error('Error:', error));
        }
    }

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
