let pollingInterval = 1000;
let pollingTimer;

function fetchGameState() {
  fetch(`/game_state/${GAME_ID}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        showMessage(data.error);
        return;
      }
      updateBoard(data);
      if (data.game_over) {
        if (data.ended_by) {
          showMessage(`Game ended by ${data.ended_by}`);
        } else {
          showMessage(data.winner ? `${data.winner} wins!` : 'Draw!');
        }
        clearInterval(pollingTimer);
      }
    });
}

function updateBoard(data) {
  document.getElementById('current-player').textContent = data.current_player;
  document.getElementById('score-b').textContent = data.score.B;
  document.getElementById('score-w').textContent = data.score.W;
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      let cell = document.getElementById(`cell-${r}-${c}`);
      cell.className = 'cell';
      cell.onclick = null;
      let val = data.board[r][c];
      if (val === 'B') {
        cell.classList.add('black');
      } else if (val === 'W') {
        cell.classList.add('white');
      } else if (data.current_player === PLAYER_COLOR && data.valid_moves.some(m => m[0] === r && m[1] === c)) {
        cell.classList.add('valid-move');
        cell.onclick = () => makeMove(r, c);
      }
    }
  }
}

function makeMove(r, c) {
  fetch(`/move/${GAME_ID}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({r: r, c: c, color: PLAYER_COLOR})
  }).then(res => res.json())
    .then(data => {
      if (data.error) {
        showMessage(data.error);
        return;
      }
      updateBoard(data);
      if (data.game_over) {
        if (data.ended_by) {
          showMessage(`Game ended by ${data.ended_by}`);
        } else {
          showMessage(data.winner ? `${data.winner} wins!` : 'Draw!');
        }
        clearInterval(pollingTimer);
      }
    });
}

function showMessage(msg) {
  document.getElementById('message').textContent = msg;
}

document.addEventListener('DOMContentLoaded', () => {
  fetchGameState();
  pollingTimer = setInterval(fetchGameState, pollingInterval);
  // Handle End Game button
  const endBtn = document.getElementById('end-btn');
  if (endBtn) {
    endBtn.onclick = () => {
      fetch(`/end/${GAME_ID}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({by: PLAYER_COLOR})
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          showMessage(data.error);
        } else {
          updateBoard(data);
          showMessage(`Game ended by ${data.ended_by}`);
          clearInterval(pollingTimer);
        }
      });
    };
  }
});