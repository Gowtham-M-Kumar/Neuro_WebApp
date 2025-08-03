document.addEventListener('DOMContentLoaded', function() {
  const objectsDiv = document.getElementById('counting-objects');
  const reward = document.getElementById('reward-area');
  const retryBtn = document.getElementById('retry-btn');
  const number = parseInt(document.querySelector('h2').textContent.match(/\d+/)[0]);
  let count = 0;

  function showObjects() {
    objectsDiv.innerHTML = '';
    count = 0;
    for (let i = 0; i < number; i++) {
      const obj = document.createElement('span');
      obj.className = 'count-object';
      obj.textContent = '🍎';
      obj.style.fontSize = '2em';
      obj.style.cursor = 'pointer';
      obj.addEventListener('click', function() {
        if (!obj.classList.contains('tapped')) {
          obj.classList.add('tapped');
          count++;
          if (count === number) {
            showReward();
            playSound('/media/sounds/correct.wav');
          }
        }
      });
      objectsDiv.appendChild(obj);
    }
  }

  function showReward() {
    reward.innerHTML = '<span style="font-size:2em;">🎉 Well done!</span>';
    setTimeout(() => { reward.innerHTML = ''; }, 2000);
  }

  function playSound(url) {
    const audio = new Audio(url);
    audio.play();
  }

  retryBtn.addEventListener('click', showObjects);
  showObjects();
}); 