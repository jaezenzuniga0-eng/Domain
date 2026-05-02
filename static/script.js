// ===== Global Variables =====

let updateInterval;
let historyUpdateInterval;

// ===== DOM Elements =====

const videoStream = document.getElementById('videoStream');
const gestureName = document.getElementById('gestureName');
const gestureConfidence = document.getElementById('gestureConfidence');
const gestureCharacter = document.getElementById('gestureCharacter');
const statusText = document.getElementById('statusText');
const statusBadge = document.getElementById('statusBadge');
const captureBtn = document.getElementById('captureBtn');
const referenceBtn = document.getElementById('referenceBtn');
const statsBtn = document.getElementById('statsBtn');
const clearBtn = document.getElementById('clearBtn');
const referenceModal = document.getElementById('referenceModal');
const statsModal = document.getElementById('statsModal');
const historyList = document.getElementById('historyList');

// ===== Initialization =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔮 Domain Expansion Mobile App Initializing...');
    
    // Initialize event listeners
    captureBtn.addEventListener('click', captureFrame);
    referenceBtn.addEventListener('click', showReference);
    statsBtn.addEventListener('click', showStats);
    clearBtn.addEventListener('click', clearHistory);
    
    // Close modals on outside click
    window.addEventListener('click', function(event) {
        if (event.target === referenceModal) {
            closeModal('referenceModal');
        }
        if (event.target === statsModal) {
            closeModal('statsModal');
        }
    });
    
    // Start updates
    updateGestures();
    updateHistory();
    
    // Set up intervals
    updateInterval = setInterval(updateGestures, 500); // Update every 500ms
    historyUpdateInterval = setInterval(updateHistory, 1000); // Update every 1s
    
    // Check server health
    checkServerHealth();
    
    console.log('✅ App initialized successfully');
});

// ===== Gesture Updates =====

async function updateGestures() {
    try {
        const response = await fetch('/api/gestures');
        const data = await response.json();
        
        if (Object.keys(data).length === 0) {
            // No gestures detected
            gestureName.textContent = '👋 Show a hand gesture...';
            gestureConfidence.textContent = '';
            gestureCharacter.textContent = '';
            resetGestureCard();
        } else {
            // Display first detected hand
            const handKey = Object.keys(data)[0];
            const gesture = data[handKey];
            
            gestureName.textContent = `🔮 ${gesture.technique}`;
            gestureConfidence.textContent = `Confidence: ${(gesture.confidence * 100).toFixed(1)}%`;
            gestureCharacter.textContent = `Character: ${gesture.character}`;
            
            updateGestureCardColor(gesture.technique);
        }
    } catch (error) {
        console.error('Error fetching gestures:', error);
        updateStatus('Error connecting to server', 'error');
    }
}

function updateGestureCardColor(technique) {
    const gestureColors = {
        'Unlimited Void': '#ff00ff',
        'Chimera Shadow Garden': '#00ff00',
        'Malevolent Shrine': '#ff0000',
        'Idle Death Gamble': '#ffa500',
        'Evolving Womb': '#00ffff',
        'Cursed Speech Technique': '#ffff00'
    };
    
    const currentGesture = document.querySelector('.current-gesture');
    if (currentGesture && gestureColors[technique]) {
        currentGesture.style.borderLeftColor = gestureColors[technique];
    }
}

function resetGestureCard() {
    const currentGesture = document.querySelector('.current-gesture');
    if (currentGesture) {
        currentGesture.style.borderLeftColor = '#ff00ff';
    }
}

// ===== History Updates =====

async function updateHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (data.length === 0) {
            historyList.innerHTML = '<p class="empty-state">No detections yet...</p>';
            return;
        }
        
        // Display latest detections (reverse order)
        const latestDetections = data.slice(-10).reverse();
        historyList.innerHTML = latestDetections.map(detection => `
            <div class="history-item">
                <span class="history-item-technique">${detection.technique}</span>
                <span style="margin: 0 10px;">•</span>
                <span>${detection.character}</span>
                <br>
                <span class="history-item-time">${new Date(detection.timestamp).toLocaleTimeString()}</span>
                <span style="margin: 0 10px;">•</span>
                <span class="history-item-time">${(detection.confidence * 100).toFixed(1)}%</span>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error fetching history:', error);
    }
}

// ===== Server Health Check =====

async function checkServerHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        updateStatus('Connected', 'success');
    } catch (error) {
        console.error('Server health check failed:', error);
        updateStatus('Connection Error', 'error');
    }
}

// ===== Capture Frame =====

async function captureFrame() {
    try {
        captureBtn.disabled = true;
        captureBtn.textContent = '📸 Capturing...';
        
        const response = await fetch('/api/capture', {
            method: 'POST'
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `domain_expansion_${new Date().toISOString().slice(0,19).replace(/:/g,'-')}.png`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            updateStatus('Screenshot captured!', 'success');
        } else {
            updateStatus('Failed to capture screenshot', 'error');
        }
    } catch (error) {
        console.error('Error capturing frame:', error);
        updateStatus('Error capturing frame', 'error');
    } finally {
        captureBtn.disabled = false;
        captureBtn.textContent = '📸 Capture';
    }
}

// ===== Reference Guide =====

async function showReference() {
    try {
        const response = await fetch('/api/gesture-reference');
        const gestures = await response.json();
        
        const referenceContent = document.getElementById('referenceContent');
        referenceContent.innerHTML = Object.entries(gestures).map(([name, info]) => `
            <div class="gesture-card">
                <h3>🔮 ${name}</h3>
                <p><strong>Gesture:</strong> ${info.gesture}</p>
                <p><strong>Description:</strong> ${info.description}</p>
                <p><strong>Character:</strong> ${info.character}</p>
                <p><strong>Power:</strong> ${info.power}</p>
            </div>
        `).join('');
        
        referenceModal.style.display = 'block';
    } catch (error) {
        console.error('Error fetching reference:', error);
        updateStatus('Error loading reference', 'error');
    }
}

// ===== Statistics =====

async function showStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        const statsContent = document.getElementById('statsContent');
        const techniqueList = Object.entries(stats.technique_counts)
            .sort(([, a], [, b]) => b - a)
            .map(([technique, count]) => `<p>• <strong>${technique}:</strong> ${count} detections</p>`)
            .join('');
        
        statsContent.innerHTML = `
            <div style="margin-bottom: 15px;">
                <p><strong>📊 Total Detections:</strong> ${stats.total_detections}</p>
                <p><strong>🏆 Most Detected:</strong> ${stats.most_detected || 'None'}</p>
                <p><strong>📖 Available Techniques:</strong> ${stats.techniques_available.length}</p>
            </div>
            <div>
                <h3 style="color: #00ffff; margin-bottom: 10px;">Detection Breakdown</h3>
                ${techniqueList || '<p>No detections yet...</p>'}
            </div>
        `;
        
        statsModal.style.display = 'block';
    } catch (error) {
        console.error('Error fetching stats:', error);
        updateStatus('Error loading statistics', 'error');
    }
}

// ===== Clear History =====

async function clearHistory() {
    if (!confirm('Are you sure you want to clear all detection history?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear-history', {
            method: 'POST'
        });
        
        if (response.ok) {
            historyList.innerHTML = '<p class="empty-state">History cleared</p>';
            updateStatus('History cleared', 'success');
            setTimeout(updateHistory, 1000);
        }
    } catch (error) {
        console.error('Error clearing history:', error);
        updateStatus('Error clearing history', 'error');
    }
}

// ===== Modal Functions =====

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// ===== Status Updates =====

function updateStatus(message, status) {
    statusText.textContent = message;
    const dot = statusBadge.querySelector('.status-dot');
    
    if (status === 'success') {
        dot.style.background = '#00ff00';
        statusBadge.style.borderColor = '#00ff00';
        statusBadge.style.background = 'rgba(0, 255, 0, 0.1)';
    } else if (status === 'error') {
        dot.style.background = '#ff0000';
        statusBadge.style.borderColor = '#ff0000';
        statusBadge.style.background = 'rgba(255, 0, 0, 0.1)';
    } else {
        dot.style.background = '#00ff00';
        statusBadge.style.borderColor = '#00ff00';
        statusBadge.style.background = 'rgba(0, 255, 0, 0.1)';
    }
}

// ===== Cleanup =====

window.addEventListener('beforeunload', function() {
    clearInterval(updateInterval);
    clearInterval(historyUpdateInterval);
});

console.log('✨ Domain Expansion Mobile Interface Loaded');
