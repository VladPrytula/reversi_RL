# Reversi (Othello) - from random bot to Deep Reinforcement Learning

## 1. Introduction
This project implements the classic two-player game Reversi (also known as Othello) as a web application using Flask. It supports human-vs-human (PvP), human-vs-bot (PvB) with two bot strategies (Random and Alpha-Beta), and bot-vs-bot (BvB) modes. The codebase is structured to separate board representation, rule verification, game state management, and bot algorithms into modular components for clarity, maintainability, and extensibility.

We will be working through various algorithms starting with very basic ones and moving towards DeepRL.

Currently the ones that are implmented are:
1. Random bot :) (yes, that one). For this one there is no separate section explainin the algorithm since it just moves randomly on the allowed spot
1. Alpha-Beta (the one and the only) - detailed writing can be found in [tex/alpha_beta.pdf](tex/alpha_beta.pdf)

## 2. Architecture and Module Organization
```
├── app.py            # Flask application and HTTP/JSON endpoints
├── game.py           # Game engine: ReversiGame class
├── board.py          # Board representation and operations
├── checks.py         # Rule verification and move-generation logic
├── bots/             # Bot and player interfaces
│   ├── base.py       # Abstract Player, Human, Bot classes
│   ├── random_bot.py # Random move selection bot
│   └── alpha_beta_bot.py # Alpha-Beta pruning bot
├── static/           # Frontend assets (CSS/JS)
└── templates/        # HTML templates
```  
Each component has a single responsibility:
- **board.py** encapsulates the board grid and primitive operations (clone, apply move, score counting).
- **checks.py** contains all rules: flipping logic, valid-move generation, and color utilities.
- **game.py** orchestrates the game flow: turn-taking, graceful termination, and exposes an interface for both bots and the web frontend.
- **bots/** implements the Player hierarchy and AI strategies.
- **app.py** handles HTTP routes, JSON state serialization, and integrates bot autoplays.

## 3. Board Representation (`board.py`)
- The board is an 8×8 grid (`self.grid`), where each cell is `None` (empty), `'B'` (black), or `'W'` (white).
- **Initialization**: Centers at (3,3), (3,4), (4,3), (4,4) are populated in the standard Reversi starting configuration.
- **Cloning**: A custom `clone()` method returns a deep copy of the grid for simulation (used by Alpha-Beta search).
- **Move Application**: `apply_move(color, r, c)` flips opponent stones based on precomputed flip lists from `checks.get_flips()`.
- **Score Counting**: `get_score()` traverses the grid to count stones per color.

## 4. Rule Verification and Move Generation (`checks.py`)
1. **Color Utilities**
   - `opponent(color)`: Returns the opposite color `'W'` ↔ `'B'`.
2. **Flip Computation**
   - `get_flips(board, color, r, c)`: Scans in eight directions (±1 offsets) to collect contiguous opponent stones bordered by a friendly stone; returns a list of coordinates to flip.
   - `would_flip(...)`: Boolean test for at least one possible flip.
3. **Valid-Move Generation**
   - `get_valid_moves(board, color)`: Iterates empty cells and filters by `would_flip`; returns a list of `(r, c)`.
   - `has_valid_move(board, color)`: Quick boolean check for any valid move.

## 5. Game Engine (`game.py`)
`ReversiGame` class encapsulates full game state:
- **Attributes**
  - `id`: Unique game identifier.
  - `players`: Dict mapping `'B'` and `'W'` to `Player` instances (human or bot).
  - `board`: Instance of `Board`.
  - `current_player`: Active color (`'B'` or `'W'`).
  - `ended`, `ended_by`: Graceful termination flags.
- **Core Methods**
  - `clone()`: Shallow-copy the game container and deep-copy the board for search.
  - `get_valid_moves(color)`, `has_valid_move(color)`: Delegate to `checks.py`.
  - `apply_move(color, r, c)`: Delegate to `Board.apply_move` and switch turn.
  - `is_game_over()`: True if no valid moves for both players or `ended` flag set.
  - `get_score()`: Delegate to `Board.get_score`.
  - `end(by)`: Mark game as gracefully ended by human player.

## 6. Player and Bot Interfaces (`bots/`)
### 6.1 Base Classes (`bots/base.py`)
- `Player`: Abstract base defining `is_human()` & `move()`.
- `Human`: Marker class for human players (no auto-move).
- `Bot`: Abstract subclass for AI players.

### 6.2 Random Bot (`bots/random_bot.py`)
- Selects a move uniformly at random from `game.get_valid_moves(color)`.
- Returns `None` to skip when no valid moves.

### 6.3 Alpha-Beta Bot (`bots/alpha_beta_bot.py`)
Implements minimax search with Alpha-Beta pruning:
1. **Evaluation Function**
   - `evaluate(g) = score[color] − score[opponent(color)]`.
2. **Recursive Search (`ab_search`)**
   - **Base Case**: Depth zero or game over → return evaluation.
   - **No-Move Case**: Clone state, switch player, recurse with decremented depth.
   - **Maximizing Player**: Iterate child moves, update `alpha`, prune when `alpha ≥ beta`.
   - **Minimizing Opponent**: Iterate child moves, update `beta`, prune when `beta ≤ alpha`.
3. **Move Selection**
   - Top-level call returns best move according to search to a configurable `max_depth` (default 3).

## 7. Web Frontend and API (`app.py`)
- **Routes**
  - `GET /` → Index page.
  - `POST /create` → Create new game (PvP, PvB, BvB), returns game links or redirects.
  - `GET /game/<game_id>` → Render game UI for a human color.
  - `GET /game_state/<game_id>` → JSON payload of board, turn, valid moves, scores, and result.
  - `POST /move/<game_id>` → Submit a human move; returns updated state.
  - `POST /end/<game_id>` → Gracefully end game by human.

- **Bot Integration**
  - After each human move (and on fetch), `process_bots()` auto-plays all pending bot moves until a human’s turn or game over.

- **Frontend**
  - HTML/JavaScript handles rendering board, highlighting valid moves, and issuing AJAX calls.

## 8. Usage
1. Install requirements: `pip install -r requirements.txt`.
2. Run server: `python app.py --host 0.0.0.0 --port 5000`.
3. Open browser at `http://localhost:5000`.

## 9. Future Work
- Add advanced evaluation heuristics (corner occupancy, stability, mobility).
- Improve UI/UX and animations.
- Support persistence and multiplayer over network.
- Expose a packaged Python API for standalone engine use.