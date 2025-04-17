from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
import uuid

# Game logic and player interfaces
from game import ReversiGame, opponent
from bots.base import Human
from bots.random_bot import RandomBot
from bots.alpha_beta_bot import AlphaBetaBot

app = Flask(__name__)

# In-memory storage of games
games = {}

def process_bots(game):
    # Automatically play bot moves until it's human's turn or game over
    while not game.is_game_over() and not game.players[game.current_player].is_human():
        color = game.current_player
        bot = game.players[color]
        move = bot.move(game, color)
        if move is not None:
            game.apply_move(color, move[0], move[1])
        else:
            # No valid move: skip turn
            game.current_player = opponent(color)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    mode = request.form.get('mode')
    if mode not in ('pvp', 'pvb_random', 'pvb_ab', 'bvb'):
        abort(400)
    game_id = uuid.uuid4().hex
    # Initialize player instances
    if mode == 'pvp':
        players = {'B': Human(), 'W': Human()}
    elif mode == 'pvb_random':
        players = {'B': Human(), 'W': RandomBot()}
    elif mode == 'pvb_ab':
        players = {'B': Human(), 'W': AlphaBetaBot()}
    else:  # bot vs bot
        players = {'B': RandomBot(), 'W': AlphaBetaBot()}
    game = ReversiGame(game_id, players)
    games[game_id] = game
    if mode == 'pvp':
        # Show links for both players
        return render_template('pvp_links.html', game_id=game_id)
    # For other modes, redirect to game page (user as black if human)
    return redirect(url_for('game', game_id=game_id, color='B', _external=False))

@app.route('/game/<game_id>')
def game(game_id):
    game = games.get(game_id)
    if not game:
        abort(404)
    # Determine if viewer is a human player; only allow if color matches a human
    raw = request.args.get('color')
    color = None
    if raw in ('B', 'W') and game.players.get(raw) and game.players[raw].is_human():
        color = raw
    return render_template('game.html', game_id=game_id, color=color)

def build_state(game):
    # Process bot moves before returning state
    process_bots(game)
    board = [[cell for cell in row] for row in game.board]
    current = game.current_player
    # Valid moves only for human on their turn
    valid = []
    if game.players.get(current) and game.players[current].is_human():
        valid = game.get_valid_moves(current)
    scores = game.get_score()
    over = game.is_game_over()
    winner = None
    if over:
        if scores['B'] > scores['W']:
            winner = 'B'
        elif scores['W'] > scores['B']:
            winner = 'W'
    return {
        'board': board,
        'current_player': current,
        'valid_moves': valid,
        'score': scores,
        'game_over': over,
        'winner': winner,
        'ended_by': game.ended_by
    }

@app.route('/game_state/<game_id>')
def game_state(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Invalid game id'}), 404
    state = build_state(game)
    return jsonify(state)

@app.route('/move/<game_id>', methods=['POST'])
def move(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Invalid game id'}), 404
    data = request.get_json(force=True)
    r = data.get('r')
    c = data.get('c')
    color = data.get('color')
    player = game.players.get(color)
    if color != game.current_player or not player or not player.is_human():
        return jsonify({'error': 'Not your turn'}), 400
    try:
        r = int(r)
        c = int(c)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid coordinates'}), 400
    moves = game.get_valid_moves(color)
    if (r, c) not in moves:
        return jsonify({'error': 'Invalid move'}), 400
    game.apply_move(color, r, c)
    state = build_state(game)
    return jsonify(state)

@app.route('/end/<game_id>', methods=['POST'])
def end_game(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({'error': 'Invalid game id'}), 404
    data = request.get_json(force=True)
    by = data.get('by')
    # Only a human player can end the game
    if by not in ('B', 'W') or not game.players.get(by).is_human():
        return jsonify({'error': 'Invalid end request'}), 400
    game.end(by)
    state = build_state(game)
    return jsonify(state)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Reversi Flask server')
    parser.add_argument('--host', default='0.0.0.0',
                        help='Host interface to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000,
                        help='Port to listen on (default: 5000)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable Flask debug mode')
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)