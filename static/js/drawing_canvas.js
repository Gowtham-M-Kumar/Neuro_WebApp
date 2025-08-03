document.addEventListener('DOMContentLoaded', function() {
// Drawing Canvas Logic
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let erasing = false;
let lastX = 0;
let lastY = 0;

const colorPicker = document.getElementById('colorPicker');
const brushSize = document.getElementById('brushSize');
let currentColor = colorPicker ? colorPicker.value : '#000000';
let currentSize = brushSize ? brushSize.value : 2;

if (colorPicker) {
    colorPicker.addEventListener('input', (e) => {
        currentColor = e.target.value;
    });
}
if (brushSize) {
    brushSize.addEventListener('input', (e) => {
        currentSize = e.target.value;
    });
}

// --- Drawing Data Model ---
let strokes = [];
let undoneStrokes = [];
let currentStroke = null;

// --- Drawing Logic (modified) ---
function startDraw(e) {
    drawing = true;
    erasing = false;
    [lastX, lastY] = getPos(e);
    currentStroke = {
        color: currentColor,
        size: parseInt(currentSize),
        points: [lastX, lastY],
        erasing: false
    };
}

function startErase(e) {
    drawing = true;
    erasing = true;
    [lastX, lastY] = getPos(e);
    currentStroke = {
        color: '#fff',
        size: parseInt(currentSize),
        points: [lastX, lastY],
        erasing: true
    };
}

function draw(e) {
    if (!drawing) return;
    ctx.strokeStyle = erasing ? '#fff' : currentColor;
    ctx.lineWidth = currentSize;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    const [x, y] = getPos(e);
    ctx.lineTo(x, y);
    ctx.stroke();
    [lastX, lastY] = [x, y];
    if (currentStroke) {
        currentStroke.points.push(x, y);
    }
}

function endDraw() {
    if (drawing && currentStroke && currentStroke.points.length >= 4) {
        strokes.push(currentStroke);
        undoneStrokes = [];
    }
    drawing = false;
    currentStroke = null;
}

function redrawCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const stroke of strokes) {
        ctx.strokeStyle = stroke.erasing ? '#fff' : stroke.color;
        ctx.lineWidth = stroke.size;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.beginPath();
        for (let i = 0; i < stroke.points.length - 2; i += 2) {
            ctx.moveTo(stroke.points[i], stroke.points[i + 1]);
            ctx.lineTo(stroke.points[i + 2], stroke.points[i + 3]);
        }
        ctx.stroke();
    }
}

// Undo/Redo
function undo() {
    if (strokes.length > 0) {
        undoneStrokes.push(strokes.pop());
        redrawCanvas();
    }
}
function redo() {
    if (undoneStrokes.length > 0) {
        strokes.push(undoneStrokes.pop());
        redrawCanvas();
    }
}

function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    if (e.touches && e.touches.length > 0) {
        return [e.touches[0].clientX - rect.left, e.touches[0].clientY - rect.top];
    } else {
        return [e.clientX - rect.left, e.clientY - rect.top];
    }
}

// Mouse events
canvas.addEventListener('mousedown', (e) => {
    if (window.currentTool === 'eraser') startErase(e);
    else startDraw(e);
});
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', endDraw);
canvas.addEventListener('mouseleave', endDraw);

// Touch events
canvas.addEventListener('touchstart', (e) => {
    if (window.currentTool === 'eraser') startErase(e);
    else startDraw(e);
});
canvas.addEventListener('touchmove', draw);
canvas.addEventListener('touchend', endDraw);

// Toolbar tool selection (add undo/redo)
window.currentTool = 'brush';
document.querySelectorAll('.tool-button').forEach(btn => {
    btn.addEventListener('click', function() {
        const tool = this.getAttribute('data-tool');
        if (tool === 'brush') window.currentTool = 'brush';
        if (tool === 'eraser') window.currentTool = 'eraser';
        if (tool === 'clear') {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            strokes = [];
            undoneStrokes = [];
        }
        if (tool === 'undo') undo();
        if (tool === 'redo') redo();
    });
});

// --- AJAX Save/Load ---
function getDrawingId() {
    // Try to get drawing_id from a data attribute or URL
    const url = window.location.pathname;
    const match = url.match(/canvas\/(\d+)/);
    if (match) return match[1];
    if (window.drawingId) return window.drawingId;
    return null;
}

function serializeDrawing() {
    return {
        strokes: strokes,
        // Add more metadata if needed
    };
}

function saveDrawing() {
    const drawingId = getDrawingId();
    if (!drawingId) {
        alert('No drawing ID found.');
        return;
    }
    const data = {
        canvas_data: serializeDrawing(),
        width: canvas.width,
        height: canvas.height,
        is_completed: false, // or true if needed
        strokes_count: strokes.length,
        colors_used: Array.from(new Set(strokes.map(s => s.color))),
        tools_used: Array.from(new Set(strokes.map(s => s.erasing ? 'eraser' : 'brush'))),
    };
    fetch(`/drawing/save/${drawingId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(res => {
        if (res.success) {
            showSaveMessage('Saved!');
        } else {
            showSaveMessage('Save failed: ' + (res.error || 'Unknown error'));
        }
    })
    .catch(() => showSaveMessage('Save failed'));
}

function loadDrawing() {
    const drawingId = getDrawingId();
    if (!drawingId) return;
    fetch(`/drawing/load/${drawingId}/`)
        .then(res => res.json())
        .then(data => {
            if (data.canvas_data && data.canvas_data.strokes) {
                strokes = data.canvas_data.strokes;
                undoneStrokes = [];
                redrawCanvas();
            }
        });
}

function showSaveMessage(msg) {
    const indicator = document.getElementById('saveIndicator');
    const message = document.getElementById('saveMessage');
    if (indicator && message) {
        message.textContent = msg;
        indicator.style.display = 'block';
        setTimeout(() => { indicator.style.display = 'none'; }, 1500);
    }
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return '';
}

// --- Button Handlers ---
document.getElementById('saveBtn')?.addEventListener('click', saveDrawing);
document.getElementById('newVersionBtn')?.addEventListener('click', function() {
    const drawingId = getDrawingId();
    if (!drawingId) return;
    fetch(`/drawing/version/${drawingId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() },
    })
    .then(res => res.json())
    .then(res => {
        if (res.success && res.new_drawing_id) {
            window.location.href = `/drawing/canvas/${res.new_drawing_id}/`;
        } else {
            alert('Failed to create new version.');
        }
    });
});
document.getElementById('exportBtn')?.addEventListener('click', function() {
    const url = canvas.toDataURL('image/png');
    const a = document.createElement('a');
    a.href = url;
    a.download = 'drawing.png';
    a.click();
});

// --- Load drawing if editing ---
loadDrawing();
}); 