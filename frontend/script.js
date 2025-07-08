document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const apiUrl = 'http://127.0.0.1:8000/api/chat';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const messageText = userInput.value.trim();
        if (!messageText) return;

        // Display user message
        addMessage(messageText, 'user-message');
        userInput.value = '';

        // Display loading indicator
        const loadingMessage = addMessage('...', 'ai-message loading');

        try {
            // Send message to backend
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: messageText })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Update loading message with actual reply, rendered as Markdown
            if (window.marked) {
                loadingMessage.innerHTML = window.marked.parse(data.reply);
            } else {
                loadingMessage.textContent = data.reply;
            }
            loadingMessage.classList.remove('loading');

        } catch (error) {
            console.error('Fetch error:', error);
            loadingMessage.textContent = 'Error: Could not get a response.';
            loadingMessage.classList.remove('loading');
        }
    });

    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        
        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
        return p; // Return the paragraph element to update it later
    }
}); 