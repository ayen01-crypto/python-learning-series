/*
Main Application JavaScript
This file handles the frontend logic for the chat application.
*/

class ChatApp {
    constructor() {
        this.token = localStorage.getItem('chat_token') || null;
        this.currentUser = null;
        this.currentRoom = null;
        this.websocket = null;
        this.typingTimeout = null;
        
        this.initializeElements();
        this.bindEvents();
        this.checkAuthStatus();
    }
    
    initializeElements() {
        // Auth elements
        this.authModal = document.getElementById('auth-modal');
        this.loginForm = document.getElementById('login-form');
        this.registerForm = document.getElementById('register-form');
        this.loginTab = document.getElementById('login-tab');
        this.registerTab = document.getElementById('register-tab');
        
        // Chat elements
        this.chatContainer = document.getElementById('chat-container');
        this.currentUserSpan = document.getElementById('current-user');
        this.logoutBtn = document.getElementById('logout-btn');
        this.roomsList = document.getElementById('rooms-list');
        this.usersList = document.getElementById('users-list');
        this.currentRoomHeader = document.getElementById('current-room');
        this.messagesContainer = document.getElementById('messages-container');
        this.messageForm = document.getElementById('message-form');
        this.messageInput = document.getElementById('message-input');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.createRoomBtn = document.getElementById('create-room-btn');
    }
    
    bindEvents() {
        // Auth events
        this.loginTab.addEventListener('click', () => this.switchAuthTab('login'));
        this.registerTab.addEventListener('click', () => this.switchAuthTab('register'));
        this.loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        this.registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        
        // Chat events
        this.logoutBtn.addEventListener('click', () => this.handleLogout());
        this.messageForm.addEventListener('submit', (e) => this.handleSendMessage(e));
        this.messageInput.addEventListener('input', () => this.handleTyping());
        this.createRoomBtn.addEventListener('click', () => this.handleCreateRoom());
    }
    
    switchAuthTab(tab) {
        if (tab === 'login') {
            this.loginTab.classList.add('active');
            this.registerTab.classList.remove('active');
            this.loginForm.classList.remove('hidden');
            this.registerForm.classList.add('hidden');
        } else {
            this.loginTab.classList.remove('active');
            this.registerTab.classList.add('active');
            this.loginForm.classList.add('hidden');
            this.registerForm.classList.remove('hidden');
        }
    }
    
    async handleLogin(e) {
        e.preventDefault();
        
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.token = data.token;
                this.currentUser = data.user;
                localStorage.setItem('chat_token', this.token);
                this.showChatInterface();
                this.connectWebSocket();
                this.loadRooms();
            } else {
                alert('Login failed: ' + data.error);
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed: Network error');
        }
    }
    
    async handleRegister(e) {
        e.preventDefault();
        
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        
        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                alert('Registration successful! Please login.');
                this.switchAuthTab('login');
            } else {
                alert('Registration failed: ' + data.error);
            }
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed: Network error');
        }
    }
    
    handleLogout() {
        if (this.websocket) {
            this.websocket.close();
        }
        
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('chat_token');
        this.showAuthInterface();
    }
    
    checkAuthStatus() {
        if (this.token) {
            // Verify token (simplified - in a real app you'd check with the server)
            this.showChatInterface();
            this.connectWebSocket();
            this.loadRooms();
        } else {
            this.showAuthInterface();
        }
    }
    
    showAuthInterface() {
        this.authModal.classList.remove('hidden');
        this.chatContainer.classList.add('hidden');
    }
    
    showChatInterface() {
        this.authModal.classList.add('hidden');
        this.chatContainer.classList.remove('hidden');
        this.currentUserSpan.textContent = this.currentUser.username;
    }
    
    connectWebSocket() {
        // Close existing connection if any
        if (this.websocket) {
            this.websocket.close();
        }
        
        // Connect to WebSocket server
        this.websocket = new WebSocket('ws://localhost:8081');
        
        this.websocket.onopen = () => {
            console.log('WebSocket connection established');
            
            // Authenticate with the server
            this.websocket.send(JSON.stringify({
                action: 'authenticate',
                token: this.token
            }));
        };
        
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };
        
        this.websocket.onclose = () => {
            console.log('WebSocket connection closed');
        };
        
        this.websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }
    
    handleWebSocketMessage(data) {
        switch (data.action) {
            case 'auth_success':
                console.log('Authentication successful');
                break;
                
            case 'auth_error':
                console.error('Authentication failed:', data.message);
                this.handleLogout();
                break;
                
            case 'new_message':
                this.displayMessage(data.message);
                break;
                
            case 'user_joined':
                this.addUserToList(data.user_id, data.username);
                break;
                
            case 'user_left':
                this.removeUserFromList(data.user_id);
                break;
                
            case 'typing_start':
                this.showTypingIndicator(data.username);
                break;
                
            case 'typing_stop':
                this.hideTypingIndicator(data.username);
                break;
                
            case 'room_joined':
                this.currentRoom = data.room_id;
                this.currentRoomHeader.textContent = data.room_name;
                this.loadMessages(data.room_id);
                break;
                
            default:
                console.log('Unknown WebSocket message:', data);
        }
    }
    
    async loadRooms() {
        try {
            const response = await fetch('/api/rooms', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            
            const rooms = await response.json();
            
            if (response.ok) {
                this.renderRooms(rooms);
                
                // Join the first room by default
                if (rooms.length > 0) {
                    this.joinRoom(rooms[0].id);
                }
            }
        } catch (error) {
            console.error('Error loading rooms:', error);
        }
    }
    
    renderRooms(rooms) {
        this.roomsList.innerHTML = '';
        
        rooms.forEach(room => {
            const li = document.createElement('li');
            li.textContent = room.name;
            li.dataset.roomId = room.id;
            li.addEventListener('click', () => this.joinRoom(room.id));
            this.roomsList.appendChild(li);
        });
    }
    
    joinRoom(roomId) {
        if (this.currentRoom === roomId) return;
        
        // Send join room message to server
        this.websocket.send(JSON.stringify({
            action: 'join_room',
            room_id: roomId
        }));
        
        // Update UI
        const roomItems = this.roomsList.querySelectorAll('li');
        roomItems.forEach(item => {
            if (item.dataset.roomId === roomId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
    
    async loadMessages(roomId) {
        try {
            const response = await fetch(`/api/messages/${roomId}`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            
            const messages = await response.json();
            
            if (response.ok) {
                this.messagesContainer.innerHTML = '';
                // Display messages in reverse order (oldest first)
                messages.reverse().forEach(msg => this.displayMessage(msg));
                this.scrollToBottom();
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }
    
    displayMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.user_id === this.currentUser.id ? 'own' : 'other'}`;
        
        const messageHeader = document.createElement('div');
        messageHeader.className = 'message-header';
        messageHeader.innerHTML = `
            <span class="username">${message.username}</span>
            <span class="timestamp">${new Date(message.timestamp).toLocaleTimeString()}</span>
        `;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = message.content;
        
        messageDiv.appendChild(messageHeader);
        messageDiv.appendChild(messageContent);
        this.messagesContainer.appendChild(messageDiv);
        
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    handleSendMessage(e) {
        e.preventDefault();
        
        if (!this.currentRoom || !this.messageInput.value.trim()) return;
        
        const content = this.messageInput.value.trim();
        
        // Send message to server
        this.websocket.send(JSON.stringify({
            action: 'send_message',
            room_id: this.currentRoom,
            content: content
        }));
        
        // Clear input
        this.messageInput.value = '';
    }
    
    handleTyping() {
        if (!this.currentRoom) return;
        
        // Clear previous timeout
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }
        
        // Send typing start
        this.websocket.send(JSON.stringify({
            action: 'typing_start',
            room_id: this.currentRoom
        }));
        
        // Set timeout to send typing stop
        this.typingTimeout = setTimeout(() => {
            this.websocket.send(JSON.stringify({
                action: 'typing_stop',
                room_id: this.currentRoom
            }));
        }, 1000);
    }
    
    showTypingIndicator(username) {
        this.typingIndicator.textContent = `${username} is typing...`;
    }
    
    hideTypingIndicator(username) {
        if (this.typingIndicator.textContent.includes(username)) {
            this.typingIndicator.textContent = '';
        }
    }
    
    addUserToList(userId, username) {
        // Check if user is already in list
        const existingItem = this.usersList.querySelector(`[data-user-id="${userId}"]`);
        if (existingItem) return;
        
        const li = document.createElement('li');
        li.textContent = username;
        li.dataset.userId = userId;
        this.usersList.appendChild(li);
    }
    
    removeUserFromList(userId) {
        const item = this.usersList.querySelector(`[data-user-id="${userId}"]`);
        if (item) {
            item.remove();
        }
    }
    
    async handleCreateRoom() {
        const roomName = prompt('Enter room name:');
        if (!roomName) return;
        
        try {
            const response = await fetch('/api/rooms', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ name: roomName })
            });
            
            const room = await response.json();
            
            if (response.ok) {
                // Refresh rooms list
                this.loadRooms();
            } else {
                alert('Failed to create room: ' + room.error);
            }
        } catch (error) {
            console.error('Error creating room:', error);
            alert('Failed to create room: Network error');
        }
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});