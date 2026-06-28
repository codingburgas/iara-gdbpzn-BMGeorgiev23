// Communications JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    initializeVideoCall();
});

// ============ CHAT FUNCTIONALITY ============

function initializeChat() {
    const sendBtn = document.getElementById('send-btn');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const templateBtn = document.getElementById('template-btn');
    const templateDropdown = document.getElementById('template-dropdown');
    const templateSelect = document.getElementById('template-select');
    
    // Send message
    if (sendBtn && messageInput) {
        sendBtn.addEventListener('click', function() {
            sendMessage();
        });
        
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // Template dropdown toggle
    if (templateBtn && templateDropdown) {
        templateBtn.addEventListener('click', function() {
            templateDropdown.style.display = templateDropdown.style.display === 'none' ? 'block' : 'none';
        });
    }
    
    // Template selection
    if (templateSelect && messageInput) {
        templateSelect.addEventListener('change', function() {
            if (this.value) {
                messageInput.value = this.value;
                templateDropdown.style.display = 'none';
            }
        });
    }
    
    // Channel selection
    document.querySelectorAll('.list-group-item[data-incident-id]').forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.list-group-item[data-incident-id]').forEach(function(el) {
                el.classList.remove('active');
            });
            this.classList.add('active');
            const incidentId = this.dataset.incidentId;
            const title = this.textContent.trim();
            document.getElementById('chat-title').innerHTML = '<i class="fas fa-comments"></i> ' + title;
            loadMessages(incidentId);
        });
    });
    
    // Load initial messages
    loadMessages(0);
}

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const activeChannel = document.querySelector('.list-group-item.active');
    const incidentId = activeChannel ? activeChannel.dataset.incidentId : 0;
    
    const content = messageInput.value.trim();
    if (!content) return;
    
    fetch('/communications/api/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: content,
            incident_id: incidentId === '0' ? null : incidentId
        })
    }).then(function(response) {
        if (response.ok) {
            messageInput.value = '';
            loadMessages(incidentId);
        }
    });
}

function loadMessages(incidentId) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    fetch('/communications/api/messages?incident_id=' + (incidentId === '0' ? '' : incidentId))
        .then(function(response) { return response.json(); })
        .then(function(messages) {
            if (messages.length === 0) {
                chatMessages.innerHTML = '<div class="text-center text-muted py-4">' +
                    '<i class="fas fa-comments" style="font-size: 2rem;"></i>' +
                    '<p class="mt-2">Няма съобщения</p>' +
                    '</div>';
                return;
            }
            
            var html = '';
            messages.forEach(function(message) {
                html += '<div class="d-flex mb-3">' +
                    '<div class="flex-shrink-0">' +
                    '<i class="fas fa-user-circle" style="font-size: 2rem; color: #6c757d;"></i>' +
                    '</div>' +
                    '<div class="flex-grow-1 ms-3">' +
                    '<div class="d-flex justify-content-between">' +
                    '<strong>' + message.sender + '</strong>' +
                    '<small class="text-muted">' + message.created_at + '</small>' +
                    '</div>' +
                    '<p class="mb-0">' + message.content + '</p>' +
                    '</div>' +
                    '</div>';
            });
            chatMessages.innerHTML = html;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
}

function sendEmergencyMessage() {
    const content = '⚠️ СПЕШНО: Изисква се незабавна помощ!';
    document.getElementById('message-input').value = content;
    sendMessage();
}

function shareLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const content = '📍 Текуща локация: ' +
                position.coords.latitude + ', ' +
                position.coords.longitude;
            document.getElementById('message-input').value = content;
            sendMessage();
        });
    } else {
        alert('Геолокацията не се поддържа от браузъра.');
    }
}

// ============ VIDEO CALL FUNCTIONALITY ============

function initializeVideoCall() {
    // Video call controls
    const audioBtn = document.getElementById('toggle-audio');
    const videoBtn = document.getElementById('toggle-video');
    const endBtn = document.getElementById('end-call');
    const shareBtn = document.getElementById('share-screen');
    
    if (audioBtn) {
        audioBtn.addEventListener('click', function() {
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-microphone');
            icon.classList.toggle('fa-microphone-slash');
            this.classList.toggle('btn-outline-danger');
            this.classList.toggle('btn-danger');
        });
    }
    
    if (videoBtn) {
        videoBtn.addEventListener('click', function() {
            const icon = this.querySelector('i');
            icon.classList.toggle('fa-video');
            icon.classList.toggle('fa-video-slash');
            this.classList.toggle('btn-outline-danger');
            this.classList.toggle('btn-danger');
        });
    }
    
    if (endBtn) {
        endBtn.addEventListener('click', function() {
            if (confirm('Сигурни ли сте, че искате да прекратите обаждането?')) {
                const container = document.getElementById('video-container');
                if (container) {
                    container.innerHTML = '<div class="text-center text-white">' +
                        '<i class="fas fa-phone-slash" style="font-size: 4rem;"></i>' +
                        '<p class="mt-3">Обаждането е прекратено</p>' +
                        '</div>';
                }
            }
        });
    }
    
    if (shareBtn) {
        shareBtn.addEventListener('click', function() {
            if (navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
                navigator.mediaDevices.getDisplayMedia({ video: true })
                    .then(function(stream) {
                        alert('Екранът се споделя!');
                    })
                    .catch(function(err) {
                        console.log('Share screen error:', err);
                    });
            } else {
                alert('Споделянето на екран не се поддържа.');
            }
        });
    }
}