# Alpha-Beta Pruning: A Detailed Algorithmic Tutorial

## Table of Contents
1. Introduction to Game Tree Search
2. The Minimax Algorithm
3. Alpha-Beta Pruning Concept
4. Formal Pseudocode
5. Theoretical Analysis
6. Advanced Enhancements
7. Current Implementation in this Codebase
8. References and Further Reading

---

## 1. Introduction to Game Tree Search
In two-player, zero-sum, perfect-information games (e.g., Reversi, Chess), agents must select moves to maximize their eventual outcome against an adversary. Game-tree search explores all possible move sequences:

- **States**: Configurations of the game.
- **Moves**: Legal actions transforming one state to another.
- **Terminal states**: End-of-game positions with known utilities.
- **Utility function** \(U(s)\): Numeric value from the perspective of the maximizing player.

The search problem: Given current state \(s_0\), compute
\[
\max_{a_0} \min_{a_1} \max_{a_2} \dots U(s_n)
\]
subject to alternation of moves between players.

## 2. The Minimax Algorithm
Minimax computes the optimal utility assuming both players play optimally.

### 2.1. Recursive Definition
Let \(V(s)\) denote the value of state \(s\) for the player to move. Then:
\[
V(s) =
\begin{cases}
U(s), & \text{if } s \text{ is terminal}, \\
\max_{a \in A(s)} V(\text{result}(s,a)), & \text{if player is maximizer}, \\
\min_{a \in A(s)} V(\text{result}(s,a)), & \text{if player is minimizer}.
\end{cases}
\]

### 2.2. Negamax Formulation
For zero-sum games, one can simplify using a single function:
\[
V(s) =
\begin{cases}
U(s), & \text{terminal}, \\
\max_{a \in A(s)} \bigl[-V(\text{result}(s,a))\bigr], & \text{otherwise}.
\end{cases}
\]

## 3. Alpha-Beta Pruning Concept
Alpha-Beta pruning reduces the number of nodes evaluated in the minimax tree without affecting the final minimax value.

- **\(\alpha\)**: Best (highest) value found so far along the path to the root for the maximizer.
- **\(\beta\)**: Best (lowest) value found so far along the path to the root for the minimizer.

At any node, if \(\alpha \ge \beta\), further exploration of its siblings cannot influence the final decision and can be pruned.

## 4. Formal Pseudocode
Below is a standard negamax implementation with alpha-beta pruning. Let `depth` be the remaining search depth.

```plaintext
function NEGAMAX-AB(node, depth, α, β, color):
    if depth = 0 or node is terminal:
        return color * Evaluate(node)
    bestValue ← -∞
    for each move in OrderMoves(node):
        child ← ApplyMove(node, move)
        val ← -NEGAMAX-AB(child, depth - 1, -β, -α, -color)
        bestValue ← max(bestValue, val)
        α ← max(α, val)
        if α ≥ β:
            break  // β-cutoff
    return bestValue

// Initial invocation:
rootValue ← NEGAMAX-AB(rootNode, maxDepth, -∞, +∞, +1)
```

### 4.1. Notation and Explanation
- **`Evaluate(node)`**: Heuristic evaluation from the root player’s perspective. 
- **`color`** ∈ {+1, −1}: Indicates whose perspective to evaluate.
- **`OrderMoves`**: Ideally sorts moves to maximize pruning (e.g., captures first).
- **Cutoffs**: When α ≥ β, remaining siblings of the current move cannot improve the minimax outcome.

## 5. Theoretical Analysis
- **Time Complexity**:
  - Worst-case: \(O(b^d)\), where \(b\) is branching factor and \(d\) is depth.
  - With perfect move ordering: \(O(b^{d/2})\) (effective depth-doubling).
- **Space Complexity**: \(O(d)\) for recursion stack (depth of search).

### 5.1. Impact of Move Ordering
- Good ordering (best moves first) dramatically increases pruning.
- Techniques include:
  1. **Killer Heuristic**: Retain moves causing cutoffs.
  2. **History Heuristic**: Score moves by past success in cutoffs.

## 6. Advanced Enhancements
1. **Iterative Deepening**: Repeated deepening from depth=1 to maxDepth, allows move-ordering data collection and time allocation.
2. **Transposition Tables**: Store previously evaluated positions (hash → value) to avoid re-search.
3. **Quiescence Search**: Extend search at “noisy” nodes (captures) to avoid horizon effect.
4. **Null Move Pruning**: Assume opponent passes for a quick bound on evaluation.
5. **Aspiration Windows**: Search with narrow (α,β) windows around expected values.
6. **Parallel Search**: Distribute branches across threads or processes.

## 7. Current Implementation in this Codebase
The `AlphaBetaBot` in `bots/alpha_beta_bot.py` implements a straightforward negamax alpha-beta search:

```python
def move(self, game, color):
    def evaluate(g):
        score = g.get_score()
        return score[color] - score[opponent(color)]

    def ab_search(g, depth, maximize_color, current_color, α, β):
        if depth == 0 or g.is_game_over():
            return evaluate(g), None
        moves = g.get_valid_moves(current_color)
        if not moves:
            # Pass turn
            g2 = g.clone()
            g2.current_player = opponent(current_color)
            return ab_search(g2, depth - 1, maximize_color, opponent(current_color), α, β)[0], None
        if current_color == maximize_color:
            value = -math.inf
            best_move = None
            for m in moves:
                g2 = g.clone(); g2.apply_move(current_color, *m)
                score, _ = ab_search(g2, depth - 1, maximize_color, opponent(current_color), α, β)
                if score > value:
                    value, best_move = score, m
                α = max(α, value)
                if α >= β:
                    break
            return value, best_move
        else:
            value = math.inf
            best_move = None
            for m in moves:
                g2 = g.clone(); g2.apply_move(current_color, *m)
                score, _ = ab_search(g2, depth - 1, maximize_color, opponent(current_color), α, β)
                if score < value:
                    value, best_move = score, m
                β = min(β, value)
                if β <= α:
                    break
            return value, best_move

    _, move = ab_search(game.clone(), self.max_depth, color, color, -math.inf, math.inf)
    return move
```

**Key characteristics**:
- Uses **piece-count difference** as the evaluation function.
- **Fixed depth** without iterative deepening.
- **No move ordering** heuristic; examines moves in arbitrary order.
- Handles **pass turns** by cloning and switching player.
- No **transposition tables**, **quiescence search**, or other optimizations.

## 8. References and Further Reading
- Pearl, J. *Heuristics: Intelligent Search Strategies*, 1984.
- Korf, R. E. *Depth-First Iterative-Deepening*, AI Journal, 1985.
- Various lecture notes on search algorithms.

---
*This document provides a rigorous foundation for alpha-beta search and explains its current implementation in the Reversi application.*