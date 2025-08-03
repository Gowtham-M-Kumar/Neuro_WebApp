document.addEventListener('DOMContentLoaded', function() {
  const canvas = document.getElementById('tracing-canvas');
  const ctx = canvas.getContext('2d');
  let drawing = false;
  let points = [];

  function startDraw(e) {
    drawing = true;
    points = [];
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
    points.push([e.offsetX, e.offsetY]);
  }

  function draw(e) {
    if (!drawing) return;
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.strokeStyle = '#007bff';
    ctx.lineWidth = 8;
    ctx.lineCap = 'round';
    ctx.stroke();
    points.push([e.offsetX, e.offsetY]);
  }

  function endDraw() {
    drawing = false;
    // Placeholder: always show reward
    showReward();
    playSound('/media/sounds/correct.wav');
  }

  function showReward() {
    const reward = document.getElementById('reward-area');
    reward.innerHTML = '<span style="font-size:2em;">🎉 Great job!</span>';
    setTimeout(() => { reward.innerHTML = ''; }, 2000);
  }

  function playSound(url) {
    const audio = new Audio(url);
    audio.play();
  }

  canvas.addEventListener('mousedown', startDraw);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', endDraw);
  canvas.addEventListener('mouseleave', endDraw);

  // Touch support
  canvas.addEventListener('touchstart', function(e) {
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    startDraw({ offsetX: touch.clientX - rect.left, offsetY: touch.clientY - rect.top });
    e.preventDefault();
  });
  canvas.addEventListener('touchmove', function(e) {
    if (!drawing) return;
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    draw({ offsetX: touch.clientX - rect.left, offsetY: touch.clientY - rect.top });
    e.preventDefault();
  });
  canvas.addEventListener('touchend', endDraw);

  document.getElementById('retry-btn').addEventListener('click', function() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    points = [];
  });
}); 