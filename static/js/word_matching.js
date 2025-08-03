document.addEventListener('DOMContentLoaded', function() {
  const gameDiv = document.getElementById('matching-game');
  const reward = document.getElementById('reward-area');
  const retryBtn = document.getElementById('retry-btn');
  // Placeholder: just show a correct match button
  function showGame() {
    gameDiv.innerHTML = '';
    const btn = document.createElement('button');
    btn.textContent = 'Match!';
    btn.onclick = function() {
      showReward();
      playSound('/media/sounds/correct.wav');
    };
    gameDiv.appendChild(btn);
  }
  function showReward() {
    reward.innerHTML = '<span style="font-size:2em;">🎉 Correct!</span>';
    setTimeout(() => { reward.innerHTML = ''; }, 2000);
  }
  function playSound(url) {
    const audio = new Audio(url);
    audio.play();
  }
  retryBtn.addEventListener('click', showGame);
  showGame();
}); 