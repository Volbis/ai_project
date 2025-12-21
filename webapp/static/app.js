// YOLOv5 Web App - Main JavaScript
const API_URL = 'http://localhost:8001';
let ws = null;
let webcamStream = null;
let isWebcamActive = false;
let animationFrame = null;
let stats = { fps: 0, latency: 0, objectCount: 0, avgConf: 0 };
let objectsChart = null;
let performanceChart = null;
let uploadedFiles = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeTheme();
    initializeWebcam();
    initializeUpload();
    initializeDashboard();
    loadStatistics();
    loadHistory();
    
    // Auto-refresh statistics every 5 seconds
    setInterval(loadStatistics, 5000);
});

// Tab Management
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Update active states
            tabBtns.forEach(b => b.classList.remove('active', 'text-blue-600', 'border-b-2', 'border-blue-600'));
            tabContents.forEach(c => c.classList.add('hidden'));
            
            btn.classList.add('active', 'text-blue-600', 'border-b-2', 'border-blue-600');
            document.getElementById(`${tabName}-tab`).classList.remove('hidden');
            
            // Load data when switching tabs
            if (tabName === 'dashboard') loadStatistics();
            if (tabName === 'history') loadHistory();
        });
    });
    
    // Set initial active state
    document.querySelector('.tab-btn').classList.add('text-blue-600', 'border-b-2', 'border-blue-600');
}

// Theme Management
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        html.classList.add('dark');
    }
    
    themeToggle.addEventListener('click', () => {
        html.classList.toggle('dark');
        const newTheme = html.classList.contains('dark') ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
    });
}

// Webcam Management
function initializeWebcam() {
    const startBtn = document.getElementById('startWebcam');
    const stopBtn = document.getElementById('stopWebcam');
    const confThreshold = document.getElementById('confThreshold');
    const confValue = document.getElementById('confValue');
    
    startBtn.addEventListener('click', startWebcamDetection);
    stopBtn.addEventListener('click', stopWebcamDetection);
    
    confThreshold.addEventListener('input', (e) => {
        confValue.textContent = e.target.value;
    });
}

async function startWebcamDetection() {
    try {
        const video = document.getElementById('webcam');
        const canvas = document.getElementById('webcamCanvas');
        const placeholder = document.getElementById('webcamPlaceholder');
        const stats = document.getElementById('webcamStats');
        const startBtn = document.getElementById('startWebcam');
        const stopBtn = document.getElementById('stopWebcam');
        
        // Get webcam stream
        webcamStream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 1280, height: 720 } 
        });
        video.srcObject = webcamStream;
        
        // Show video
        video.classList.remove('hidden');
        canvas.classList.remove('hidden');
        placeholder.classList.add('hidden');
        stats.classList.remove('hidden');
        startBtn.classList.add('hidden');
        stopBtn.classList.remove('hidden');
        
        isWebcamActive = true;
        
        console.log('🎥 Webcam démarrée, connexion WebSocket...');
        
        // Connect WebSocket
        connectWebSocket();
        
    } catch (error) {
        console.error('Error accessing webcam:', error);
        alert('Erreur: Impossible d\'accéder à la webcam. Vérifiez les permissions.');
    }
}

function stopWebcamDetection() {
    isWebcamActive = false;
    
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
    }
    
    if (ws) {
        ws.close();
        ws = null;
    }
    
    if (animationFrame) {
        cancelAnimationFrame(animationFrame);
    }
    
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('webcamCanvas');
    const placeholder = document.getElementById('webcamPlaceholder');
    const stats = document.getElementById('webcamStats');
    const startBtn = document.getElementById('startWebcam');
    const stopBtn = document.getElementById('stopWebcam');
    
    video.classList.add('hidden');
    canvas.classList.add('hidden');
    placeholder.classList.remove('hidden');
    stats.classList.add('hidden');
    startBtn.classList.remove('hidden');
    stopBtn.classList.add('hidden');
    
    document.getElementById('liveDetections').innerHTML = '<p class="text-gray-500 dark:text-gray-400 text-center py-8">Aucune détection</p>';
}

function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8001/ws');
    
    ws.onopen = () => {
        console.log('✅ WebSocket connecté avec succès!');
        // Attendre un peu que la vidéo soit prête, puis commencer à envoyer
        setTimeout(() => {
            console.log('Démarrage de l\'envoi de frames...');
            sendWebcamFrame();
        }, 500);
    };
    
    ws.onmessage = (event) => {
        console.log('Frame reçue du serveur');
        const data = JSON.parse(event.data);
        displayWebcamDetections(data);
        updateWebcamStats(data);
    };
    
    ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        alert('Erreur WebSocket. Vérifiez que le serveur est actif sur localhost:8001');
    };
    
    ws.onclose = () => {
        console.log('⚠️ WebSocket déconnecté');
        if (isWebcamActive) {
            // Réessayer la connexion si la webcam est toujours active
            setTimeout(() => {
                console.log('Tentative de reconnexion...');
                connectWebSocket();
            }, 2000);
        }
    };
}

function sendWebcamFrame() {
    if (!isWebcamActive || !ws || ws.readyState !== WebSocket.OPEN) {
        console.log('Cannot send frame:', { isWebcamActive, wsState: ws?.readyState });
        return;
    }
    
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('webcamCanvas');
    
    // Vérifier que la vidéo est prête
    if (!video.videoWidth || !video.videoHeight) {
        console.log('Video not ready, retrying...');
        setTimeout(() => sendWebcamFrame(), 100);
        return;
    }
    
    const ctx = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    
    const frameData = canvas.toDataURL('image/jpeg', 0.8);
    const model = document.getElementById('modelSelect').value;
    const confidence = parseFloat(document.getElementById('confThreshold').value);
    
    const startTime = Date.now();
    
    try {
        ws.send(JSON.stringify({
            frame: frameData,
            model: model,
            confidence: confidence,
            timestamp: startTime
        }));
        console.log('Frame sent successfully');
    } catch (error) {
        console.error('Error sending frame:', error);
    }
    
    // Send next frame after 500ms (2 FPS) pour meilleure stabilité
    if (isWebcamActive) {
        setTimeout(() => sendWebcamFrame(), 500);
    }
}

function displayWebcamDetections(data) {
    const canvas = document.getElementById('webcamCanvas');
    const img = new Image();
    
    img.onload = () => {
        const ctx = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
    };
    
    img.src = data.image;
    
    // Update detections list with better display
    const liveDetections = document.getElementById('liveDetections');
    if (data.detections.length === 0) {
        liveDetections.innerHTML = `
            <div class="text-center py-8">
                <i class="fas fa-search text-4xl text-gray-400 mb-3"></i>
                <p class="text-gray-500 dark:text-gray-400 font-medium">Aucun objet détecté</p>
                <p class="text-xs text-gray-400 dark:text-gray-500 mt-2">
                    Montrez des personnes, animaux, ou objets à la caméra
                </p>
            </div>
        `;
    } else {
        // Group detections by class
        const grouped = {};
        data.detections.forEach(det => {
            if (!grouped[det.class]) {
                grouped[det.class] = [];
            }
            grouped[det.class].push(det);
        });
        
        liveDetections.innerHTML = Object.entries(grouped).map(([className, dets]) => `
            <div class="detection-box bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900 dark:to-blue-900 p-3 rounded-lg border border-green-200 dark:border-green-700">
                <div class="flex items-center justify-between mb-1">
                    <div class="flex items-center">
                        <span class="w-3 h-3 bg-green-500 rounded-full mr-2 pulse-dot"></span>
                        <span class="font-bold text-gray-800 dark:text-white">${className}</span>
                    </div>
                    <span class="text-lg font-bold text-green-600 dark:text-green-400">×${dets.length}</span>
                </div>
                <div class="flex flex-wrap gap-1">
                    ${dets.map(det => `
                        <span class="text-xs px-2 py-1 bg-green-500 text-white rounded-full font-medium">
                            ${(det.confidence * 100).toFixed(0)}%
                        </span>
                    `).join('')}
                </div>
            </div>
        `).join('');
    }
}

function updateWebcamStats(data) {
    const latency = Date.now() - new Date(data.timestamp).getTime();
    const fps = 1000 / (data.processing_time * 1000 + latency);
    
    document.getElementById('fps').textContent = fps.toFixed(1);
    document.getElementById('latency').textContent = latency.toFixed(0);
    
    document.getElementById('quickObjectCount').textContent = data.detections.length;
    
    if (data.detections.length > 0) {
        const avgConf = data.detections.reduce((sum, d) => sum + d.confidence, 0) / data.detections.length;
        document.getElementById('quickAvgConf').textContent = (avgConf * 100).toFixed(1) + '%';
    }
    
    document.getElementById('quickProcessTime').textContent = (data.processing_time * 1000).toFixed(0) + 'ms';
}

// Upload Management
function initializeUpload() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const processBtn = document.getElementById('processUpload');
    
    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-blue-500', 'bg-blue-50', 'dark:bg-blue-900');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-blue-500', 'bg-blue-50', 'dark:bg-blue-900');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-blue-500', 'bg-blue-50', 'dark:bg-blue-900');
        
        const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
        handleFiles(files);
    });
    
    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        handleFiles(files);
    });
    
    processBtn.addEventListener('click', processUploadedImages);
}

function handleFiles(files) {
    uploadedFiles = files;
    const preview = document.getElementById('uploadPreview');
    const processBtn = document.getElementById('processUpload');
    
    if (files.length === 0) return;
    
    preview.classList.remove('hidden');
    processBtn.classList.remove('hidden');
    
    preview.innerHTML = files.map((file, index) => {
        const url = URL.createObjectURL(file);
        return `
            <div class="relative group">
                <img src="${url}" class="w-full h-32 object-cover rounded-lg">
                <div class="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity rounded-lg flex items-center justify-center">
                    <span class="text-white text-sm">${file.name}</span>
                </div>
            </div>
        `;
    }).join('');
}

async function processUploadedImages() {
    const resultsDiv = document.getElementById('uploadResults');
    const processBtn = document.getElementById('processUpload');
    
    processBtn.disabled = true;
    processBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Traitement en cours...';
    
    resultsDiv.innerHTML = '<div class="text-center py-8"><i class="fas fa-spinner fa-spin text-4xl text-blue-500"></i></div>';
    
    try {
        const formData = new FormData();
        uploadedFiles.forEach(file => formData.append('files', file));
        
        const model = document.getElementById('modelSelect').value;
        const confidence = document.getElementById('confThreshold').value;
        
        const response = await fetch(`${API_URL}/detect/batch?model=${model}&confidence=${confidence}`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayUploadResults(data.results);
        } else {
            throw new Error('Traitement échoué');
        }
        
    } catch (error) {
        console.error('Error processing images:', error);
        resultsDiv.innerHTML = '<p class="text-red-500 text-center py-8">Erreur lors du traitement</p>';
    } finally {
        processBtn.disabled = false;
        processBtn.innerHTML = '<i class="fas fa-magic mr-2"></i>Analyser les images';
    }
}

function displayUploadResults(results) {
    const resultsDiv = document.getElementById('uploadResults');
    
    resultsDiv.innerHTML = results.map(result => `
        <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-4">
            <h4 class="font-medium text-gray-800 dark:text-white mb-3 flex items-center">
                <i class="fas fa-image mr-2 text-blue-500"></i>
                ${result.filename}
            </h4>
            <img src="data:image/jpeg;base64,${result.image}" class="w-full rounded-lg mb-3 shadow-md">
            
            ${result.detections && result.detections.length > 0 ? `
                <div class="bg-green-50 dark:bg-green-900 rounded-lg p-3 mb-2">
                    <h5 class="font-bold text-green-800 dark:text-green-200 mb-2 flex items-center">
                        <i class="fas fa-check-circle mr-2"></i>
                        ${result.detections.length} objet(s) détecté(s)
                    </h5>
                    <div class="space-y-1">
                        ${result.detections.map(det => `
                            <div class="flex justify-between items-center bg-white dark:bg-gray-800 px-3 py-2 rounded">
                                <div class="flex items-center">
                                    <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                                    <span class="font-medium text-gray-800 dark:text-white">${det.class}</span>
                                </div>
                                <span class="text-sm px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded font-bold">
                                    ${(det.confidence * 100).toFixed(1)}%
                                </span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : `
                <div class="bg-yellow-50 dark:bg-yellow-900 rounded-lg p-4 text-center">
                    <i class="fas fa-exclamation-triangle text-3xl text-yellow-500 mb-2"></i>
                    <p class="text-yellow-800 dark:text-yellow-200 font-medium">Aucun objet détecté</p>
                    <p class="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                        YOLOv5 détecte : personnes, animaux, véhicules, objets du quotidien
                    </p>
                    <p class="text-xs text-yellow-600 dark:text-yellow-400 mt-2">
                        💡 Essayez avec une photo contenant des personnes, voitures, ou objets physiques
                    </p>
                </div>
            `}
            
            <div class="mt-2 text-xs text-gray-500 dark:text-gray-400 flex justify-between">
                <span><i class="fas fa-clock mr-1"></i>Traité en ${(result.processing_time * 1000).toFixed(0)}ms</span>
            </div>
        </div>
    `).join('');
}

// Dashboard Management
function initializeDashboard() {
    // Initialize charts
    const ctx1 = document.getElementById('objectsChart').getContext('2d');
    objectsChart = new Chart(ctx1, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
                    '#ef4444', '#6366f1', '#14b8a6', '#f97316', '#84cc16'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    const ctx2 = document.getElementById('performanceChart').getContext('2d');
    performanceChart = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temps de traitement (ms)',
                data: [],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_URL}/statistics`);
        const data = await response.json();
        
        // Update stat cards
        document.getElementById('totalDetections').textContent = data.total_detections;
        document.getElementById('totalImages').textContent = data.total_images_processed;
        document.getElementById('avgFps').textContent = data.fps.toFixed(1);
        
        // Update objects chart
        const labels = Object.keys(data.objects_detected);
        const values = Object.values(data.objects_detected);
        
        objectsChart.data.labels = labels;
        objectsChart.data.datasets[0].data = values;
        objectsChart.update();
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// History Management
async function loadHistory() {
    try {
        const response = await fetch(`${API_URL}/history`);
        const data = await response.json();
        
        const historyList = document.getElementById('historyList');
        
        if (data.history.length === 0) {
            historyList.innerHTML = '<p class="text-gray-500 dark:text-gray-400 text-center py-8">Aucun historique</p>';
            return;
        }
        
        historyList.innerHTML = data.history.reverse().map(item => `
            <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                <div class="flex items-center justify-between mb-2">
                    <span class="font-medium text-gray-800 dark:text-white">${item.filename}</span>
                    <span class="text-sm text-gray-500 dark:text-gray-400">${new Date(item.timestamp).toLocaleString()}</span>
                </div>
                <div class="flex flex-wrap gap-2">
                    ${item.detections.map(det => `
                        <span class="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded">
                            ${det.class}: ${(det.confidence * 100).toFixed(0)}%
                        </span>
                    `).join('')}
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

document.getElementById('clearHistory').addEventListener('click', async () => {
    if (confirm('Êtes-vous sûr de vouloir effacer l\'historique ?')) {
        try {
            await fetch(`${API_URL}/history`, { method: 'DELETE' });
            loadHistory();
        } catch (error) {
            console.error('Error clearing history:', error);
        }
    }
});
