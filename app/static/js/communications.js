// Communications JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    initializeVideoCall();
});

// ============ CHAT FUNCTIONALITY ============

function initializeChat() {
    var sendBtn = document.getElementById('send-btn');
    var messageInput = document.getElementById('message-input');
    var chatMessages = document.getElementById('chat-messages');
    var templateBtn = document.getElementById('template-btn');
    var templateDropdown = document.getElementById('template-dropdown');
    var templateSelect = document.getElementById('template-select');
    
    // Emergency elements
    var emergencyBtn = document.getElementById('emergency-btn');
    var emergencyInputContainer = document.getElementById('emergency-input-container');
    var emergencyInput = document.getElementById('emergency-input');
    var emergencySendBtn = document.getElementById('emergency-send-btn');
    var emergencyCancelBtn = document.getElementById('emergency-cancel-btn');
    
    // Flag to prevent double sending
    var isSending = false;
    
    // Send message function
    function sendMessage(isEmergency) {
        // Prevent double sending
        if (isSending) return;
        
        var activeChannel = document.querySelector('.list-group-item.active');
        var incidentId = activeChannel ? activeChannel.dataset.incidentId : 0;
        
        var content;
        if (isEmergency) {
            content = emergencyInput.value.trim();
            if (!content) return;
        } else {
            content = messageInput.value.trim();
            if (!content) return;
        }
        
        isSending = true;
        
        fetch('/communications/api/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                incident_id: incidentId === '0' ? null : incidentId,
                is_emergency: isEmergency
            })
        }).then(function(response) {
            isSending = false;
            if (response.ok) {
                if (isEmergency) {
                    emergencyInput.value = '';
                    hideEmergencyInput();
                } else {
                    messageInput.value = '';
                }
                loadMessages(incidentId);
            }
        }).catch(function() {
            isSending = false;
        });
    }
    
    function showEmergencyInput() {
        if (emergencyInputContainer) {
            emergencyInputContainer.style.display = 'block';
            emergencyInput.focus();
        }
    }
    
    function hideEmergencyInput() {
        if (emergencyInputContainer) {
            emergencyInputContainer.style.display = 'none';
            emergencyInput.value = '';
        }
    }
    
    // --- Send Button ---
    if (sendBtn) {
        // Remove any existing listeners by cloning
        var newSendBtn = sendBtn.cloneNode(true);
        sendBtn.parentNode.replaceChild(newSendBtn, sendBtn);
        sendBtn = document.getElementById('send-btn');
        
        sendBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            sendMessage(false);
        });
    }
    
    // --- Message Input (Enter key) ---
    if (messageInput) {
        // Remove any existing listeners by cloning
        var newMessageInput = messageInput.cloneNode(true);
        messageInput.parentNode.replaceChild(newMessageInput, messageInput);
        messageInput = document.getElementById('message-input');
        
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                e.stopPropagation();
                sendMessage(false);
            }
        });
    }
    
    // --- Emergency Button ---
    if (emergencyBtn) {
        var newEmergencyBtn = emergencyBtn.cloneNode(true);
        emergencyBtn.parentNode.replaceChild(newEmergencyBtn, emergencyBtn);
        emergencyBtn = document.getElementById('emergency-btn');
        
        emergencyBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            showEmergencyInput();
        });
    }
    
    // --- Emergency Send ---
    if (emergencySendBtn) {
        var newEmergencySendBtn = emergencySendBtn.cloneNode(true);
        emergencySendBtn.parentNode.replaceChild(newEmergencySendBtn, emergencySendBtn);
        emergencySendBtn = document.getElementById('emergency-send-btn');
        
        emergencySendBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            sendMessage(true);
        });
    }
    
    // --- Emergency Input (Enter key) ---
    if (emergencyInput) {
        var newEmergencyInput = emergencyInput.cloneNode(true);
        emergencyInput.parentNode.replaceChild(newEmergencyInput, emergencyInput);
        emergencyInput = document.getElementById('emergency-input');
        
        emergencyInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                e.stopPropagation();
                sendMessage(true);
            }
        });
    }
    
    // --- Emergency Cancel ---
    if (emergencyCancelBtn) {
        var newEmergencyCancelBtn = emergencyCancelBtn.cloneNode(true);
        emergencyCancelBtn.parentNode.replaceChild(newEmergencyCancelBtn, emergencyCancelBtn);
        emergencyCancelBtn = document.getElementById('emergency-cancel-btn');
        
        emergencyCancelBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            hideEmergencyInput();
        });
    }
    
    // --- Template dropdown toggle ---
    if (templateBtn && templateDropdown) {
        var newTemplateBtn = templateBtn.cloneNode(true);
        templateBtn.parentNode.replaceChild(newTemplateBtn, templateBtn);
        templateBtn = document.getElementById('template-btn');
        
        templateBtn.addEventListener('click', function(e) {
            e.preventDefault();
            templateDropdown.style.display = templateDropdown.style.display === 'none' ? 'block' : 'none';
        });
    }
    
    // --- Template selection ---
    if (templateSelect && messageInput) {
        var newTemplateSelect = templateSelect.cloneNode(true);
        templateSelect.parentNode.replaceChild(newTemplateSelect, templateSelect);
        templateSelect = document.getElementById('template-select');
        
        templateSelect.addEventListener('change', function() {
            if (this.value) {
                messageInput.value = this.value;
                templateDropdown.style.display = 'none';
            }
        });
    }
    
    // --- Channel selection ---
    document.querySelectorAll('.list-group-item[data-incident-id]').forEach(function(item) {
        var newItem = item.cloneNode(true);
        item.parentNode.replaceChild(newItem, item);
        
        newItem.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.list-group-item[data-incident-id]').forEach(function(el) {
                el.classList.remove('active');
            });
            this.classList.add('active');
            var incidentId = this.dataset.incidentId;
            var title = this.textContent.trim();
            document.getElementById('chat-title').innerHTML = '<i class="fas fa-comments"></i> ' + title;
            loadMessages(incidentId);
            hideEmergencyInput();
        });
    });
    
    // Load initial messages
    loadMessages(0);
}

function loadMessages(incidentId) {
    var chatMessages = document.getElementById('chat-messages');
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
                var emergencyClass = message.is_emergency ? 'emergency-message' : '';
                var emergencyBadge = message.is_emergency ? 
                    '<span class="badge bg-danger ms-2"><i class="fas fa-exclamation-triangle"></i> СПЕШНО</span>' : '';
                
                html += '<div class="d-flex mb-3 ' + emergencyClass + '">' +
                    '<div class="flex-shrink-0">' +
                    '<i class="fas fa-user-circle" style="font-size: 2rem; color: #6c757d;"></i>' +
                    '</div>' +
                    '<div class="flex-grow-1 ms-3">' +
                    '<div class="d-flex justify-content-between align-items-center">' +
                    '<strong>' + message.sender + emergencyBadge + '</strong>' +
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
    var emergencyBtn = document.getElementById('emergency-btn');
    if (emergencyBtn) {
        emergencyBtn.click();
    }
}

// ============ VIDEO CALL FUNCTIONALITY ============

function initializeVideoCall() {
    var audioBtn = document.getElementById('toggle-audio');
    var videoBtn = document.getElementById('toggle-video');
    var endBtn = document.getElementById('end-call');
    var shareBtn = document.getElementById('share-screen');
    
    if (audioBtn) {
        var newAudioBtn = audioBtn.cloneNode(true);
        audioBtn.parentNode.replaceChild(newAudioBtn, audioBtn);
        audioBtn = document.getElementById('toggle-audio');
        
        audioBtn.addEventListener('click', function() {
            var icon = this.querySelector('i');
            icon.classList.toggle('fa-microphone');
            icon.classList.toggle('fa-microphone-slash');
            this.classList.toggle('btn-outline-danger');
            this.classList.toggle('btn-danger');
        });
    }
    
    if (videoBtn) {
        var newVideoBtn = videoBtn.cloneNode(true);
        videoBtn.parentNode.replaceChild(newVideoBtn, videoBtn);
        videoBtn = document.getElementById('toggle-video');
        
        videoBtn.addEventListener('click', function() {
            var icon = this.querySelector('i');
            icon.classList.toggle('fa-video');
            icon.classList.toggle('fa-video-slash');
            this.classList.toggle('btn-outline-danger');
            this.classList.toggle('btn-danger');
        });
    }
    
    if (endBtn) {
        var newEndBtn = endBtn.cloneNode(true);
        endBtn.parentNode.replaceChild(newEndBtn, endBtn);
        endBtn = document.getElementById('end-call');
        
        endBtn.addEventListener('click', function() {
            if (confirm('Сигурни ли сте, че искате да прекратите обаждането?')) {
                var container = document.getElementById('video-container');
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
        var newShareBtn = shareBtn.cloneNode(true);
        shareBtn.parentNode.replaceChild(newShareBtn, shareBtn);
        shareBtn = document.getElementById('share-screen');
        
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